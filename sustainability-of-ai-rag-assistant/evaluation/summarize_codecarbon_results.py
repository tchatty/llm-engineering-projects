"""Descriptive statistics over CodeCarbon experiment results (no interpretation).

Reads manifest.json and the native emissions.csv in each repetition directory.
Native units: duration s, energy kWh, emissions kg CO2eq. Missing values are
excluded from statistics and counted, never treated as zero.
"""

import argparse
import csv
import json
import statistics
from pathlib import Path

DEFAULT_RESULTS_DIR = Path(__file__).resolve().parent / "impact_results" / "codecarbon"
METRICS = {
    "duration": "duration",
    "total_energy": "energy_consumed",
    "cpu_energy": "cpu_energy",
    "gpu_energy": "gpu_energy",
    "ram_energy": "ram_energy",
    "emissions": "emissions",
}


def describe(values):
    if not values:
        return {k: None for k in ["n", "min", "max", "median", "mean", "stdev", "cv"]}
    mean = statistics.fmean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else None
    cv = stdev / mean if stdev is not None and mean != 0 else None
    return {"n": len(values), "min": min(values), "max": max(values),
            "median": statistics.median(values), "mean": mean, "stdev": stdev, "cv": cv}


def to_float(text):
    try:
        return float(text) if text not in (None, "") else None
    except ValueError:
        return None


def read_native(rep_dir, filename, run_id=None):
    """Return the native row joined by manifest.codecarbon_run_id = emissions.run_id."""
    path = rep_dir / filename
    if not path.exists():
        return None
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if run_id:
        rows = [r for r in rows if r.get("run_id") == run_id]
    return rows[-1] if rows else None


def group_key(manifest):
    ops = manifest.get("requested_operations")
    mode = (manifest.get("tracking_configuration") or {}).get("tracking_mode")
    return manifest["experiment_type"] + (f"_{ops}" if ops else "") + (f"_{mode}" if mode else "")


def collect(results_dir):
    groups = {}
    for path in sorted(results_dir.glob("*/*/manifest.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest["experiment_type"] == "detect":
            continue
        g = groups.setdefault(group_key(manifest), {"valid": 0, "failed": 0, "values": {m: [] for m in METRICS},
                                                    "missing": {m: 0 for m in METRICS}})
        if manifest["execution_status"] != "success":
            g["failed"] += 1
            continue
        row = read_native(path.parent, manifest.get("native_output_filename", "emissions.csv"),
                          manifest.get("codecarbon_run_id"))
        if row is None:
            g["failed"] += 1
            continue
        g["valid"] += 1
        g.setdefault("reps", []).append((manifest, row))
        for name, column in METRICS.items():
            value = to_float(row.get(column))
            if value is None:
                g["missing"][name] += 1
            else:
                g["values"][name].append(value)
    return groups


PER_RETRIEVAL_LABEL = "DERIVED BATCH ALLOCATION — NOT DIRECTLY MEASURED"
REP_METRICS = {"tracker_duration": "duration", "total_energy": "energy_consumed", "cpu_energy": "cpu_energy",
               "gpu_energy": "gpu_energy", "ram_energy": "ram_energy", "emissions": "emissions"}


def attribution_report(results_dir):
    """Per-repetition records, per-mode statistics, derived per-retrieval values, mode comparison."""
    groups = collect(results_dir)
    reps, modes = [], {}
    for key, g in groups.items():
        if not key.startswith("retrieval_"):
            continue
        mode = key.rsplit("_", 1)[1]
        vals = {"workload_duration": [], **{m: [] for m in REP_METRICS}}
        per = {m: [] for m in REP_METRICS if m != "tracker_duration"}
        for manifest, row in g["reps"]:
            done = manifest.get("completed_operations")
            env = manifest.get("environment_snapshot") or {}
            rec = {"mode": mode, "requested": manifest.get("requested_operations"), "completed": done,
                   "failed": manifest.get("failed_operations"), "pre_cpu_percent": env.get("cpu_percent_1s_sample"),
                   "pre_process_count": env.get("process_count"), "workload_seconds": manifest.get("wall_clock_seconds"),
                   "codecarbon_run_id": manifest.get("codecarbon_run_id"), "git_commit": (manifest.get("git") or {}).get("commit"),
                   "git_dirty": (manifest.get("git") or {}).get("dirty"), "warnings": manifest.get("warnings"),
                   "missing": [m for m, c in REP_METRICS.items() if to_float(row.get(c)) is None]}
            if rec["workload_seconds"] is not None:
                vals["workload_duration"].append(rec["workload_seconds"])
            for m, c in REP_METRICS.items():
                v = to_float(row.get(c))
                rec[m] = v
                if v is not None:
                    vals[m].append(v)
                    if m in per and done:
                        per[m].append(v / done)
            reps.append(rec)
        modes[mode] = {"valid": g["valid"], "failed": g["failed"], "missing_counts": g["missing"],
                       "statistics": {m: describe(v) for m, v in vals.items()},
                       "per_retrieval_label": PER_RETRIEVAL_LABEL,
                       "per_retrieval": {m: describe(v) for m, v in per.items()}}
    comparison = {}
    if {"machine", "process"} <= modes.keys():
        for m in modes["machine"]["statistics"]:
            a, b = modes["machine"]["statistics"][m], modes["process"]["statistics"][m]
            if a["mean"] is None or b["mean"] is None:
                comparison[m] = None
                continue
            comparison[m] = {"mean_difference_process_minus_machine": b["mean"] - a["mean"],
                             "mean_ratio_process_over_machine": b["mean"] / a["mean"] if a["mean"] else None,
                             "ranges_overlap": a["min"] <= b["max"] and b["min"] <= a["max"],
                             "cv_difference_process_minus_machine": None if a["cv"] is None or b["cv"] is None else b["cv"] - a["cv"],
                             "n_machine": a["n"], "n_process": b["n"]}
    return {"repetitions": reps, "modes": modes, "comparison": comparison}


def summarize(results_dir):
    return {
        key: {"valid_repetitions": g["valid"], "failed_repetitions": g["failed"],
              "missing_counts": g["missing"],
              "statistics": {m: describe(v) for m, v in g["values"].items()}}
        for key, g in collect(results_dir).items()
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    p.add_argument("--attribution", action="store_true", help="Also write attribution_analysis.json")
    args = p.parse_args(argv)
    summary = summarize(args.results_dir)
    (args.results_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with open(args.results_dir / "summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["workload", "valid", "failed", "metric", "missing", "n", "min", "max", "median", "mean", "stdev", "cv"])
        for key, s in summary.items():
            for metric, st in s["statistics"].items():
                w.writerow([key, s["valid_repetitions"], s["failed_repetitions"], metric,
                            s["missing_counts"][metric], *[st[k] for k in ["n", "min", "max", "median", "mean", "stdev", "cv"]]])
    if args.attribution:
        report = attribution_report(args.results_dir)
        (args.results_dir / "attribution_analysis.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"summary written for {len(summary)} workloads: {args.results_dir / 'summary.csv'}")


if __name__ == "__main__":
    main()
