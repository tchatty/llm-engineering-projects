import csv
import json
import tempfile
import unittest
from pathlib import Path

import measure_local_compute as m
import summarize_codecarbon_results as s


class SummaryTests(unittest.TestCase):
    def test_describe(self):
        d = s.describe([1.0, 2.0, 3.0])
        self.assertEqual((d["n"], d["min"], d["max"], d["median"], d["mean"]), (3, 1.0, 3.0, 2.0, 2.0))
        self.assertAlmostEqual(d["cv"], 0.5)

    def test_empty_is_missing_not_zero(self):
        self.assertIsNone(s.describe([])["mean"])

    def test_missing_cell_not_zero(self):
        self.assertIsNone(s.to_float(""))

    def test_collect_counts_failed_and_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for i, (status, gpu) in enumerate([("success", ""), ("success", "0.5"), ("failed", "")]):
                d = root / "smoke" / f"r{i}"
                d.mkdir(parents=True)
                (d / "manifest.json").write_text(json.dumps(
                    {"experiment_type": "smoke", "execution_status": status, "native_output_filename": "emissions.csv"}))
                with open(d / "emissions.csv", "w", newline="") as fh:
                    w = csv.writer(fh)
                    w.writerow(["duration", "energy_consumed", "cpu_energy", "gpu_energy", "ram_energy", "emissions"])
                    w.writerow([60, 1, 1, gpu, 1, 1])
            out = s.summarize(root)["smoke"]
            self.assertEqual((out["valid_repetitions"], out["failed_repetitions"]), (2, 1))
            self.assertEqual(out["missing_counts"]["gpu_energy"], 1)
            self.assertEqual(out["statistics"]["gpu_energy"]["n"], 1)


class CliTests(unittest.TestCase):
    def test_defaults(self):
        a = m.parse_args(["retrieval"])
        self.assertEqual((a.operations, a.warmup, a.measure_power_secs, a.tracking_mode), (100, 10, 15, "machine"))


if __name__ == "__main__":
    unittest.main()
