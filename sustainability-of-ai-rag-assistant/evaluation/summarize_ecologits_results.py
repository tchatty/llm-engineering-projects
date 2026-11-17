"""Descriptive statistics over EcoLogits experiment manifests (no interpretation).

Bounds are summarized separately; no midpoints are computed. Missing values are
excluded and counted, never treated as zero. Units are recorded per metric.
"""

import argparse
import csv
import json
from pathlib import Path

from summarize_codecarbon_results import describe

DEFAULT_RESULTS_DIR = Path(__file__).resolve().parent / "impact_results" / "ecologits"
SCALARS = ["latency_seconds", "input_tokens", "cached_input_tokens", "output_tokens", "estimated_cost_usd"]
IMPACTS = ["energy", "gwp", "wcf", "pe", "adpe"]


def impact_metrics(rec):
    out = {}
    crit = (rec.get("impacts") or {}).get("criteria") or {}
    for c in IMPACTS:
        v = (crit.get(c) or {}).get("total")
        out[f"{c}_lower"] = None if v is None else (v["min"] if v["min"] is not None else v["scalar"])
        out[f"{c}_upper"] = None if v is None else (v["max"] if v["max"] is not None else v["scalar"])
    return out


def units(rec):
    crit = (rec.get("impacts") or {}).get("criteria") or {}
    return {c: ((crit.get(c) or {}).get("total") or {}).get("unit") for c in IMPACTS}


def collect(results_dir):
    groups = {}
    for path in sorted(results_dir.glob("*/manifest.json")):
        m = json.loads(path.read_text(encoding="utf-8"))
        for rec in m.get("requests", []):
            g = groups.setdefault(rec["condition"], {"valid": 0, "failed": 0, "unsupported": 0, "records": [],
                                                     "units": {}, "models": set(), "limit_hits": 0,
                                                     "warning_codes": set(), "error_codes": set(), "experiments": set()})
            key = {"success": "valid", "unsupported": "unsupported"}.get(rec["status"], "failed")
            g[key] += 1
            g["models"].add(rec.get("model_returned"))
            g["experiments"].add(m["experiment_id"])
            if rec["status"] != "success":
                continue
            g["records"].append(rec)
            g["limit_hits"] += bool(rec.get("reached_output_limit"))
            g["units"].update({k: v for k, v in units(rec).items() if v})
            imp = rec["impacts"]
            g["warning_codes"].update(w["code"] for w in imp["warnings"])
            g["error_codes"].update(e["code"] for e in imp["errors"])
    return groups


def summarize(results_dir):
    out = {}
    for cond, g in collect(results_dir).items():
        metrics = {k: [] for k in SCALARS}
        missing = {k: 0 for k in SCALARS}
        impact_names = [f"{c}_{b}" for c in IMPACTS for b in ("lower", "upper")]
        metrics.update({k: [] for k in impact_names})
        missing.update({k: 0 for k in impact_names})
        for rec in g["records"]:
            vals = {**{k: rec.get(k) for k in SCALARS}, **impact_metrics(rec)}
            for k, v in vals.items():
                if v is None:
                    missing[k] += 1
                else:
                    metrics[k].append(v)
        out[cond] = {"valid_requests": g["valid"], "failed_requests": g["failed"],
                     "unsupported_requests": g["unsupported"], "requests_reaching_output_limit": g["limit_hits"],
                     "models_returned": sorted(m for m in g["models"] if m), "units": g["units"],
                     "warning_codes": sorted(g["warning_codes"]), "error_codes": sorted(g["error_codes"]),
                     "missing_counts": missing, "statistics": {k: describe(v) for k, v in metrics.items()}}
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    args = p.parse_args(argv)
    summary = summarize(args.results_dir)
    (args.results_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with open(args.results_dir / "summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["condition", "valid", "failed", "unsupported", "metric", "missing", "n", "min", "max",
                    "median", "mean", "stdev", "cv"])
        for cond, s in summary.items():
            for metric, st in s["statistics"].items():
                w.writerow([cond, s["valid_requests"], s["failed_requests"], s["unsupported_requests"], metric,
                            s["missing_counts"][metric], *[st[k] for k in ["n", "min", "max", "median", "mean", "stdev", "cv"]]])
    print(f"summary written for {len(summary)} conditions: {args.results_dir / 'summary.csv'}")


if __name__ == "__main__":
    main()
