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


def read_native(rep_dir, filename):
    path = rep_dir / filename
    if not path.exists():
        return None
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows[-1] if rows else None


def group_key(manifest):
    ops = manifest.get("requested_operations")
    return manifest["experiment_type"] + (f"_{ops}" if ops else "")


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
        row = read_native(path.parent, manifest.get("native_output_filename", "emissions.csv"))
        if row is None:
            g["failed"] += 1
            continue
        g["valid"] += 1
        for name, column in METRICS.items():
            value = to_float(row.get(column))
            if value is None:
                g["missing"][name] += 1
            else:
                g["values"][name].append(value)
    return groups


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
    print(f"summary written for {len(summary)} workloads: {args.results_dir / 'summary.csv'}")


if __name__ == "__main__":
    main()
