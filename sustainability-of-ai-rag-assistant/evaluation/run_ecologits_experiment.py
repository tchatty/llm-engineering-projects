"""EcoLogits remote-inference experiment (OpenAI only). COMMANDS COST MONEY.

compat: one short standalone request. rag: controlled RAG requests sharing one retrieved context.
Writes a sanitized manifest.json and a local-only native_impacts.json under
evaluation/impact_results/ecologits/<experiment_id>/. Prompts, questions, context and
responses are never stored. Provider requests require --confirm-paid.
"""

import argparse
import hashlib
import json
import platform
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = EVAL_DIR.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))
sys.path.insert(0, str(EVAL_DIR))

from measure_local_compute import corpus_fingerprint, git_info  # noqa: E402

DEFAULT_RESULTS_DIR = EVAL_DIR / "impact_results" / "ecologits"
PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"
# Standard-tier USD per 1M tokens, from developers.openai.com/api/docs/pricing (fetched 2026-11-15)
PRICING_USD_PER_M = {"gpt-4o-mini": {"input": 0.15, "cached_input": 0.075, "output": 0.60}}
CRITERIA = ["energy", "gwp", "adpe", "pe", "wcf"]
PHASES = ["usage", "embodied"]
DEFAULT_CONDITIONS = [100, 100, 100, 250, 500]
COMPAT_PROMPT = "In one sentence, what is a data center?"
# Fixed public, non-sensitive research question (never written to results).
RAG_QUESTION = "What factors determine the environmental impact of running large language model inference?"


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", choices=["compat", "rag"])
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-tokens", type=int, nargs="+", default=None,
                   help="compat: one value (default 50). rag: one per request (default 100 100 100 250 500)")
    p.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    p.add_argument("--confirm-paid", action="store_true", help="Required to send paid OpenAI requests")
    return p.parse_args(argv)


# ---- impact extraction (pure; works on model_dump() dicts) ----

def extract_value(node):
    """Preserve scalar vs range, unit and optional mean. Returns None if absent."""
    if not isinstance(node, dict):
        return None
    v = node.get("value")
    out = {"unit": node.get("unit"), "scalar": None, "min": None, "max": None, "mean": None}
    if isinstance(v, dict) and ("min" in v or "max" in v):
        out.update(min=v.get("min"), max=v.get("max"), mean=v.get("mean"))
    elif isinstance(v, (int, float)) and not isinstance(v, bool):
        out["scalar"] = v
    else:
        return None
    return out


def extract_impacts(impacts):
    """impacts: model_dump() dict or None. Missing values stay None (never zero)."""
    if impacts is None:
        return None
    usage, embodied = impacts.get("usage") or {}, impacts.get("embodied") or {}
    criteria = {c: {"total": extract_value(impacts.get(c)), "usage": extract_value(usage.get(c)),
                    "embodied": extract_value(embodied.get(c))} for c in CRITERIA}
    return {"criteria": criteria,
            "phases_present": [p for p, d in [("usage", usage), ("embodied", embodied)] if d],
            "warnings": [{"code": w.get("code"), "message": w.get("message")} for w in impacts.get("warnings") or []],
            "errors": [{"code": e.get("code"), "message": e.get("message")} for e in impacts.get("errors") or []]}


def estimate_cost(model, input_tokens, cached, output_tokens):
    price = PRICING_USD_PER_M.get(model)
    if price is None or input_tokens is None or output_tokens is None:
        return None
    cached = cached or 0
    return ((input_tokens - cached) * price["input"] + cached * price["cached_input"]
            + output_tokens * price["output"]) / 1e6


def build_record(condition, max_tokens, model, repetition, response, latency, error=None):
    """Sanitized request record. response may be None (failed). No text content is read."""
    rec = {"condition": condition, "repetition": repetition, "requested_max_tokens": max_tokens,
           "provider": PROVIDER, "model_requested": model, "model_returned": None, "status": "failed",
           "impact_status": None, "finish_reason": None, "reached_output_limit": None,
           "latency_seconds": latency, "input_tokens": None, "cached_input_tokens": None,
           "output_tokens": None, "estimated_cost_usd": None, "impacts": None, "error": error}
    native = None
    if response is not None:
        usage = response.usage
        details = getattr(usage, "prompt_tokens_details", None)
        rec.update(model_returned=response.model, finish_reason=response.choices[0].finish_reason,
                   input_tokens=usage.prompt_tokens, output_tokens=usage.completion_tokens,
                   cached_input_tokens=getattr(details, "cached_tokens", None))
        rec["reached_output_limit"] = rec["finish_reason"] == "length"
        rec["estimated_cost_usd"] = estimate_cost(model, rec["input_tokens"], rec["cached_input_tokens"],
                                                  rec["output_tokens"])
        raw = getattr(response, "impacts", None)
        if raw is None:
            rec.update(status="unsupported", impact_status="unsupported")
        else:
            native = raw.model_dump() if hasattr(raw, "model_dump") else raw
            rec["impacts"] = extract_impacts(native)
            rec["impact_status"] = "partial" if rec["impacts"]["errors"] else "complete"
            rec["status"] = "success"
    return rec, native


# ---- execution ----

def send(client, model, messages, max_tokens):
    """One request; one retry only for clearly transient connection/timeout/5xx failures."""
    import openai
    transient = (openai.APIConnectionError, openai.APITimeoutError, openai.InternalServerError)
    for attempt in (1, 2):
        start = time.perf_counter()
        try:
            resp = client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens,
                                                  temperature=0)
            return resp, time.perf_counter() - start, None
        except transient as exc:
            if attempt == 2:
                return None, time.perf_counter() - start, f"{type(exc).__name__}"
        except Exception as exc:  # auth, billing, quota, bad request: no retry
            return None, time.perf_counter() - start, f"{type(exc).__name__}: {str(exc)[:120]}"


def package_versions():
    from importlib.metadata import PackageNotFoundError, version
    out = {}
    for name in ["ecologits", "openai"]:
        try:
            out[name] = version(name)
        except PackageNotFoundError:
            out[name] = None
    return out


def rag_messages(question, context):
    from sustainability_rag.rag_pipeline import SYSTEM_PROMPT
    # Identical message construction to rag_pipeline.answer_question
    return [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
        Question: {question}\n\n
        Research Context:\n{context}"""}]


def main(argv=None):
    args = parse_args(argv)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    experiment_id = f"{args.experiment}_{stamp}_{uuid.uuid4().hex[:6]}"
    manifest = {"experiment_id": experiment_id, "experiment_type": args.experiment, "timestamp_utc": stamp,
                "git": git_info(), "package_versions": package_versions(), "python_version": platform.python_version(),
                "provider": PROVIDER, "model": args.model, "temperature": 0, "streaming": False,
                "pricing_source": "developers.openai.com/api/docs/pricing (standard tier, fetched 2026-11-15)",
                "execution_status": "failed", "failure": None, "requests": []}
    if not args.confirm_paid:
        print("refusing: provider requests incur cost; pass --confirm-paid")
        return 2
    out_dir = args.results_dir / experiment_id
    out_dir.mkdir(parents=True, exist_ok=True)
    natives = []
    try:
        from ecologits import EcoLogits
        from ecologits.model_repository import models
        manifest["model_registered_in_ecologits"] = models.find_model(PROVIDER, args.model) is not None
        from sustainability_rag.rag_pipeline import client
        EcoLogits.init(providers=[PROVIDER])  # patches the OpenAI SDK used by rag_pipeline.client
        if args.experiment == "compat":
            caps = args.max_tokens or [50]
            jobs = [("compat", caps[0], 1, [{"role": "user", "content": COMPAT_PROMPT}])]
        else:
            from sustainability_rag.config import TOP_K
            from sustainability_rag.rag_pipeline import SYSTEM_PROMPT
            from sustainability_rag.resources import initialize_corpus_resources
            from sustainability_rag.retrieval import build_context, retrieve_relevant_chunks
            res = initialize_corpus_resources()
            results = retrieve_relevant_chunks(RAG_QUESTION, res["content_chunks"], res["embeddings"], top_k=TOP_K)
            context = build_context(results)
            messages = rag_messages(RAG_QUESTION, context)
            manifest.update(corpus_fingerprint_sha256=corpus_fingerprint(), top_k=TOP_K,
                            retrieved_chunk_count=len(results), context_characters=len(context),
                            system_prompt_sha256=hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
                            question_sha256=hashlib.sha256(RAG_QUESTION.encode()).hexdigest(),
                            prompt_version="unversioned (system prompt hash recorded)",
                            retrieval_version="unversioned (cosine top-k over all-MiniLM-L6-v2)")
            caps = args.max_tokens or DEFAULT_CONDITIONS
            seen = {}
            jobs = []
            for c in caps:
                seen[c] = seen.get(c, 0) + 1
                jobs.append((f"rag_{c}", c, seen[c], messages))
        for condition, cap, rep, msgs in jobs:
            resp, latency, err = send(client, args.model, msgs, cap)
            rec, native = build_record(condition, cap, args.model, rep, resp, latency, err)
            if rec["model_returned"] and not rec["model_returned"].startswith(args.model):
                rec.update(status="failed", error="model_substitution")
            manifest["requests"].append(rec)
            natives.append({"condition": condition, "repetition": rep, "impacts": native})
            print(f"{condition} rep{rep}: {rec['status']} in={rec['input_tokens']} out={rec['output_tokens']}"
                  f" lat={latency:.2f}s" + (f" error={rec['error']}" if rec["error"] else ""))
            if rec["status"] == "failed":
                manifest["failure"] = rec["error"]
                break
        statuses = {r["status"] for r in manifest["requests"]}
        manifest["execution_status"] = "success" if statuses == {"success"} else "failed"
    except Exception as exc:
        manifest["failure"] = f"{type(exc).__name__}: {str(exc)[:200]}"
    (out_dir / "native_impacts.json").write_text(json.dumps(natives, indent=2, default=str), encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"{args.experiment}: {manifest['execution_status']} -> {out_dir}")
    return 0 if manifest["execution_status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
