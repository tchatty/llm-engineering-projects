"""Run one CodeCarbon repetition (one Python process) for a local-compute experiment.

Experiments: detect, smoke, coldstart, retrieval. Native CodeCarbon output and a
sanitized manifest are written under evaluation/impact_results/codecarbon/.
"""

import argparse
import hashlib
import json
import logging
import platform
import subprocess
import sys
import time
import uuid
import warnings
from datetime import datetime, timezone
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = EVAL_DIR.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))
sys.path.insert(0, str(EVAL_DIR))

DEFAULT_RESULTS_DIR = EVAL_DIR / "impact_results" / "codecarbon"
EXPERIMENTS = ["detect", "smoke", "coldstart", "retrieval"]
NATIVE_FILENAME = "emissions.csv"


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", choices=EXPERIMENTS)
    p.add_argument("--repetition", type=int, default=1, help="Repetition number label")
    p.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    p.add_argument("--measure-power-secs", type=int, default=15, help="CodeCarbon sampling interval")
    p.add_argument("--tracking-mode", choices=["machine", "process"], default="machine")
    p.add_argument("--smoke-seconds", type=int, default=60)
    p.add_argument("--operations", type=int, default=100, help="Measured retrieval operations")
    p.add_argument("--warmup", type=int, default=10, help="Unmeasured retrieval warm-up searches")
    p.add_argument("--expected-chunks", type=int, default=None)
    p.add_argument("--expected-dim", type=int, default=384)
    return p.parse_args(argv)


def git_info():
    def run(*cmd):
        return subprocess.run(["git", *cmd], capture_output=True, text=True, cwd=PROJECT_DIR).stdout.strip()
    return {"commit": run("rev-parse", "HEAD") or None, "dirty": bool(run("status", "--porcelain"))}


def package_versions():
    from importlib.metadata import PackageNotFoundError, version
    out = {}
    for name in ["codecarbon", "sentence-transformers", "torch", "numpy", "streamlit"]:
        try:
            out[name] = version(name)
        except PackageNotFoundError:
            out[name] = None
    return out


def environment_snapshot():
    """Visible conditions only; does not establish that the machine was idle."""
    import psutil
    snap = {
        "cpu_percent_1s_sample": psutil.cpu_percent(interval=1),
        "process_count": len(psutil.pids()),
        "logical_cpus": psutil.cpu_count(),
    }
    battery = psutil.sensors_battery()
    snap["on_ac_power"] = None if battery is None else battery.power_plugged
    return snap


def corpus_fingerprint():
    from sustainability_rag.config import DATA_DIR, SOURCE_METADATA_PATH
    h = hashlib.sha256()
    for path in [SOURCE_METADATA_PATH, *sorted(Path(DATA_DIR).glob("*.md"))]:
        h.update(path.name.encode())
        h.update(path.read_bytes())
    return h.hexdigest()


class WarningCollector(logging.Handler):
    def __init__(self):
        super().__init__(level=logging.WARNING)
        self.messages = []

    def emit(self, record):
        msg = record.getMessage()
        if msg not in self.messages:
            self.messages.append(msg[:300])


def smoke_workload(seconds):
    import numpy as np
    rng = np.random.default_rng(0)
    a = rng.random((400, 400))
    end = time.perf_counter() + seconds
    iterations = 0
    while time.perf_counter() < end:
        a = a @ a
        a /= np.linalg.norm(a)
        iterations += 1
    return {"iterations": iterations}


def coldstart_workload(args):
    from sustainability_rag.resources import initialize_corpus_resources
    resources = initialize_corpus_resources()
    return {
        "chunk_count": len(resources["content_chunks"]),
        "embedding_shape": list(resources["embeddings"].shape),
        "source_count": len(resources["source_metadata"]),
    }


def load_questions():
    import evaluate_retrieval as er
    from sustainability_rag.documents import build_source_registry, load_source_metadata
    records = json.loads(er.QUESTIONS_PATH.read_text(encoding="utf-8"))
    er.validate_records(records, set(build_source_registry(load_source_metadata()).values()))
    return [r["question"] for r in records], er.TOP_K


def retrieval_setup():
    from sustainability_rag.resources import initialize_corpus_resources
    from sustainability_rag.retrieval import retrieve_relevant_chunks
    questions, top_k = load_questions()
    resources = initialize_corpus_resources()
    chunks, embeddings = resources["content_chunks"], resources["embeddings"]

    def search(i):
        retrieve_relevant_chunks(questions[i % len(questions)], chunks, embeddings, top_k=top_k)

    return search, {"chunk_count": len(chunks), "embedding_shape": list(embeddings.shape), "top_k": top_k}


def retrieval_measured(search, operations):
    completed = failed = 0
    for i in range(operations):
        try:
            search(i)
            completed += 1
        except Exception:
            failed += 1
    return {"completed": completed, "failed": failed}


def validate_corpus(details, args, source_count_check=True):
    from sustainability_rag.documents import load_source_metadata
    problems = []
    if details["embedding_shape"][1] != args.expected_dim:
        problems.append(f"embedding dim {details['embedding_shape'][1]} != {args.expected_dim}")
    if details["embedding_shape"][0] != details["chunk_count"]:
        problems.append("embedding rows != chunk count")
    if args.expected_chunks is not None and details["chunk_count"] != args.expected_chunks:
        problems.append(f"chunk count {details['chunk_count']} != {args.expected_chunks}")
    if source_count_check and "source_count" in details:
        if details["source_count"] != len(load_source_metadata()):
            problems.append("source count mismatch")
    return problems


def make_tracker(args, out_dir, collector):
    from codecarbon import EmissionsTracker
    logging.getLogger("codecarbon").addHandler(collector)
    settings = {
        "project_name": f"sustainability_rag_{args.experiment}",
        "measure_power_secs": args.measure_power_secs,
        "tracking_mode": args.tracking_mode,
        "output_dir": str(out_dir),
        "output_file": NATIVE_FILENAME,
        "save_to_file": True,
        "save_to_api": False,
        "save_to_logger": False,
        "save_to_prometheus": False,
        "save_to_logfire": False,
        "log_level": "warning",
    }
    return EmissionsTracker(**settings), settings


def run_detect(out_dir):
    with open(out_dir / "hardware_detect.txt", "w", encoding="utf-8") as fh:
        exe = Path(sys.executable).parent / ("codecarbon.exe" if sys.platform == "win32" else "codecarbon")
        proc = subprocess.run([str(exe), "detect"], stdout=fh,
                              stderr=subprocess.STDOUT, text=True)
    return proc.returncode == 0


def execute(args, out_dir, manifest):
    collector = WarningCollector()
    if args.experiment == "detect":
        ok = run_detect(out_dir)
        manifest["execution_status"] = "success" if ok else "failed"
        manifest["native_output_filename"] = "hardware_detect.txt"
        return
    manifest["environment_snapshot"] = environment_snapshot()
    manifest["corpus_fingerprint_sha256"] = corpus_fingerprint() if args.experiment != "smoke" else None
    search = None
    if args.experiment == "retrieval":  # setup is outside tracking
        search, setup = retrieval_setup()
        manifest.update(chunk_count=setup["chunk_count"], top_k=setup["top_k"])
        manifest["embedding_model"] = _model_name()
        problems = validate_corpus(setup, args, source_count_check=False)
        if problems:
            raise RuntimeError("validation: " + "; ".join(problems))
        for i in range(args.warmup):
            search(i)
    tracker, settings = make_tracker(args, out_dir, collector)
    manifest["tracking_configuration"] = settings
    manifest["requested_operations"] = args.operations if args.experiment == "retrieval" else None
    details, failure = {}, None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        tracker.start()
        t0 = time.perf_counter()
        try:
            if args.experiment == "smoke":
                details = smoke_workload(args.smoke_seconds)
            elif args.experiment == "coldstart":
                details = coldstart_workload(args)
            else:
                details = retrieval_measured(search, args.operations)
        except Exception as exc:  # recorded, never converted to zero
            failure = f"{type(exc).__name__}: {str(exc)[:200]}"
        finally:
            wall = time.perf_counter() - t0
            tracker.stop()
    manifest["wall_clock_seconds"] = wall
    manifest["codecarbon_run_id"] = getattr(getattr(tracker, "final_emissions_data", None), "run_id", None)
    manifest["native_output_filename"] = NATIVE_FILENAME
    manifest["warnings"] = collector.messages + sorted({str(w.message)[:300] for w in caught})
    status = "failed" if failure else "success"
    if args.experiment == "coldstart" and not failure:
        problems = validate_corpus(details, args)
        manifest.update(chunk_count=details["chunk_count"], embedding_model=_model_name())
        if problems:
            status, failure = "failed", "validation: " + "; ".join(problems)
    if args.experiment == "retrieval":
        manifest.update(completed_operations=details.get("completed"), failed_operations=details.get("failed"))
        manifest["shorter_than_sampling_interval"] = wall < args.measure_power_secs
        if not failure and details["failed"]:
            status = "failed"
    manifest["workload_details"] = details if args.experiment == "smoke" else None
    manifest["execution_status"] = status
    manifest["failure"] = failure


def _model_name():
    from sustainability_rag.config import EMBEDDING_MODEL_NAME
    return EMBEDDING_MODEL_NAME


def main(argv=None):
    args = parse_args(argv)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    experiment_id = f"{args.experiment}_rep{args.repetition}_{stamp}_{uuid.uuid4().hex[:6]}"
    out_dir = args.results_dir / args.experiment / experiment_id
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "experiment_id": experiment_id,
        "experiment_type": args.experiment,
        "repetition": args.repetition,
        "timestamp_utc": stamp,
        "git": git_info(),
        "package_versions": package_versions(),
        "python_version": platform.python_version(),
        "operating_system": platform.platform(),
        "execution_status": "failed",
        "failure": None,
        "warnings": [],
    }
    try:
        execute(args, out_dir, manifest)
    except Exception as exc:
        manifest["execution_status"] = "failed"
        manifest["failure"] = manifest.get("failure") or f"{type(exc).__name__}: {str(exc)[:200]}"
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    ops = ""
    if args.experiment == "retrieval":
        ops = f" ops={manifest.get('completed_operations')}/{args.operations} short={manifest.get('shorter_than_sampling_interval')}"
    print(f"{args.experiment} rep{args.repetition}: {manifest['execution_status']}"
          f" wall={manifest.get('wall_clock_seconds', 0):.1f}s{ops}"
          + (f" failure={manifest['failure']}" if manifest["failure"] else ""))
    return 0 if manifest["execution_status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
