"""Synthetic, offline tests for EcoLogits extraction, sanitization and summarizing (no provider calls)."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import run_ecologits_experiment as r
import summarize_ecologits_results as s

RANGE = lambda lo, hi, unit: {"value": {"min": lo, "max": hi}, "unit": unit}  # noqa: E731
IMPACTS = {
    "energy": RANGE(1.0, 2.0, "kWh"), "gwp": RANGE(3.0, 4.0, "kgCO2eq"), "adpe": RANGE(5.0, 6.0, "kgSbeq"),
    "pe": {"value": {"min": 7.0, "max": 8.0, "mean": 7.5}, "unit": "MJ"}, "wcf": {"value": 9.0, "unit": "L"},
    "usage": {"energy": RANGE(1.0, 2.0, "kWh"), "gwp": RANGE(2.0, 3.0, "kgCO2eq")},
    "embodied": {"gwp": RANGE(1.0, 1.5, "kgCO2eq")},
    "warnings": [{"code": "model-arch-not-released", "message": "m"}], "errors": None,
}


class _Impacts:
    def model_dump(self):
        return IMPACTS


def fake_response(impacts=True, finish="stop", model="gpt-4o-mini-2024-07-18"):
    resp = SimpleNamespace(
        model=model, choices=[SimpleNamespace(finish_reason=finish, message=SimpleNamespace(content="SECRET TEXT"))],
        usage=SimpleNamespace(prompt_tokens=1000, completion_tokens=100,
                              prompt_tokens_details=SimpleNamespace(cached_tokens=0)))
    if impacts:
        resp.impacts = _Impacts()
    return resp


class ExtractionTests(unittest.TestCase):
    def test_range_scalar_mean_preserved(self):
        e = r.extract_impacts(IMPACTS)["criteria"]
        self.assertEqual((e["energy"]["total"]["min"], e["energy"]["total"]["max"]), (1.0, 2.0))
        self.assertIsNone(e["energy"]["total"]["mean"])
        self.assertEqual(e["pe"]["total"]["mean"], 7.5)
        self.assertEqual(e["wcf"]["total"]["scalar"], 9.0)
        self.assertIsNone(e["wcf"]["total"]["min"])
        self.assertEqual(e["energy"]["total"]["unit"], "kWh")

    def test_phases_and_missing_not_zero(self):
        e = r.extract_impacts(IMPACTS)
        self.assertEqual(e["phases_present"], ["usage", "embodied"])
        self.assertIsNone(e["criteria"]["energy"]["embodied"])
        self.assertIsNone(e["criteria"]["adpe"]["usage"])
        self.assertEqual(e["criteria"]["gwp"]["embodied"]["max"], 1.5)

    def test_warnings_and_errors_preserved(self):
        d = dict(IMPACTS, errors=[{"code": "model-not-registered", "message": "x"}])
        e = r.extract_impacts(d)
        self.assertEqual(e["warnings"][0]["code"], "model-arch-not-released")
        self.assertEqual(e["errors"][0]["code"], "model-not-registered")


class RecordTests(unittest.TestCase):
    def test_success_and_sanitization(self):
        rec, native = r.build_record("rag_100", 100, "gpt-4o-mini", 1, fake_response(), 1.5)
        self.assertEqual((rec["status"], rec["impact_status"]), ("success", "complete"))
        self.assertNotIn("SECRET TEXT", json.dumps(rec))
        self.assertIs(native, IMPACTS)
        self.assertAlmostEqual(rec["estimated_cost_usd"], (1000 * 0.15 + 100 * 0.60) / 1e6)

    def test_unsupported_and_failed(self):
        rec, native = r.build_record("c", 50, "m", 1, fake_response(impacts=False), 1.0)
        self.assertEqual((rec["status"], rec["impacts"], native), ("unsupported", None, None))
        rec, _ = r.build_record("c", 50, "m", 1, None, 1.0, error="AuthenticationError")
        self.assertEqual((rec["status"], rec["input_tokens"]), ("failed", None))

    def test_limit_flag_and_cli(self):
        rec, _ = r.build_record("c", 50, "gpt-4o-mini", 1, fake_response(finish="length"), 1.0)
        self.assertTrue(rec["reached_output_limit"])
        self.assertFalse(r.parse_args(["compat"]).confirm_paid)
        self.assertEqual(r.main(["compat"]), 2)  # refuses without --confirm-paid


def fake_gemini(impacts=True, finish="STOP", model="gemini-2.5-flash-lite"):
    resp = SimpleNamespace(
        model_version=model, candidates=[SimpleNamespace(finish_reason=SimpleNamespace(name=finish))],
        usage_metadata=SimpleNamespace(prompt_token_count=900, candidates_token_count=80,
                                       cached_content_token_count=None, thoughts_token_count=None), text="SECRET TEXT")
    if impacts:
        resp.impacts = _Impacts()
    return resp


class GeminiRecordTests(unittest.TestCase):
    def test_gemini_record_sanitized_and_missing_not_zero(self):
        rec, native = r.build_record("rag_100", 100, "gemini-2.5-flash-lite", 1, fake_gemini(), 1.0,
                                     provider="google_genai")
        self.assertEqual((rec["provider"], rec["status"], rec["input_tokens"], rec["output_tokens"]),
                         ("google_genai", "success", 900, 80))
        self.assertIsNone(rec["cached_input_tokens"])
        self.assertIsNone(rec["estimated_cost_usd"])
        self.assertNotIn("SECRET TEXT", json.dumps(rec))
        self.assertIs(native, IMPACTS)

    def test_gemini_limit_unsupported_and_cli(self):
        rec, _ = r.build_record("c", 50, "m", 1, fake_gemini(finish="MAX_TOKENS"), 1.0, provider="google_genai")
        self.assertTrue(rec["reached_output_limit"])
        rec, _ = r.build_record("c", 50, "m", 1, fake_gemini(impacts=False), 1.0, provider="google_genai")
        self.assertEqual(rec["status"], "unsupported")
        a = r.parse_args(["compat", "--provider", "google_genai"])
        self.assertEqual((a.model, a.results_dir.name), ("gemini-2.5-flash-lite", "gemini"))
        self.assertEqual(r.main(["compat", "--provider", "google_genai"]), 2)  # refuses without confirmation


class SummaryTests(unittest.TestCase):
    def test_bounds_separate_and_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            recs = [r.build_record("rag_100", 100, "gpt-4o-mini", i, fake_response(), 1.0 + i)[0] for i in range(2)]
            recs.append(r.build_record("rag_100", 100, "gpt-4o-mini", 3, fake_response(impacts=False), 1.0)[0])
            recs.append(r.build_record("rag_100", 100, "gpt-4o-mini", 4, None, 1.0, error="E")[0])
            d = root / "x"
            d.mkdir()
            (d / "manifest.json").write_text(json.dumps({"experiment_id": "x", "requests": recs}))
            out = s.summarize(root)["rag_100"]
            self.assertEqual((out["valid_requests"], out["unsupported_requests"], out["failed_requests"]), (2, 1, 1))
            self.assertEqual(out["statistics"]["energy_lower"]["mean"], 1.0)
            self.assertEqual(out["statistics"]["energy_upper"]["mean"], 2.0)
            self.assertEqual(out["units"]["wcf"], "L")
            self.assertEqual(out["statistics"]["wcf_lower"]["n"], 2)  # scalar fills both bounds only if scalar
            self.assertEqual(out["missing_counts"]["cached_input_tokens"], 0)


if __name__ == "__main__":
    unittest.main()
