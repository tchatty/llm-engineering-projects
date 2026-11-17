"""Offline tests (mocked providers, no network, no real quota) for provider policy and the OpenAI fallback flow."""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

EVAL = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL.parent / "src"))
sys.path.insert(0, str(EVAL))

import tempfile  # noqa: E402

import httpx  # noqa: E402
from sustainability_rag import config, fallback, provider_health as ph, rag_pipeline as rp  # noqa: E402

CHUNK = {"source_id": "S1", "source": "s.md", "section": "### A", "text": "t", "type": "content"}
Q = "public question"
MSGS = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]


def isolate_health(test):
    """Point provider-health state at a temp file so tests never touch or count toward real state."""
    tmp = tempfile.TemporaryDirectory()
    test.addCleanup(tmp.cleanup)
    patcher = mock.patch.object(ph, "STATE_PATH", Path(tmp.name) / "state.json")
    patcher.start()
    test.addCleanup(patcher.stop)
    return Path(tmp.name) / "state.json"


class HttpError(Exception):
    def __init__(self, code):
        super().__init__("detail that must never be stored")
        self.code = code


def fake_pipeline(calls, fail=("gemini",)):
    def answer(question, chunks, emb, provider=config.DEFAULT_PROVIDER):
        calls.append(provider)
        if provider in fail:
            raise rp.GenerationUnavailable(provider)
        return {"answer": "ok", "provider": provider, "source_map": {}}
    return answer


class DefaultsTests(unittest.TestCase):
    def test_defaults_and_cap(self):
        self.assertEqual((config.DEFAULT_PROVIDER, config.MODELS["gemini"]), ("gemini", "gemini-3.5-flash-lite"))
        self.assertEqual((config.FALLBACK_PROVIDER, config.MODELS["openai"]), ("openai", "gpt-4o-mini"))
        self.assertEqual(config.MAX_OUTPUT_TOKENS, 500)

    def _run(self, provider=None):
        with mock.patch.object(rp, "retrieve_relevant_chunks", return_value=[(CHUNK, 0.9)]), \
             mock.patch.object(rp, "build_context", return_value="ctx"), \
             mock.patch.object(rp, "generate_text", return_value="a") as gen:
            kw = {} if provider is None else {"provider": provider}
            out = rp.answer_question(Q, [CHUNK], None, **kw)
        return gen, out

    def test_gemini_default_and_explicit_openai(self):
        gen, _ = self._run()
        self.assertEqual(gen.call_args[0][0], "gemini")
        gen, out = self._run("openai")
        self.assertEqual((gen.call_args[0][0], out["provider"]), ("openai", "openai"))


class GenerationTests(unittest.TestCase):
    def test_missing_credential_fails_safely_without_openai(self):
        with mock.patch.dict(os.environ, {}), mock.patch.object(rp, "_generate_chat") as chat:
            os.environ.pop("GEMINI_API_KEY", None)
            with self.assertRaises(rp.GenerationUnavailable) as cm:
                rp.generate_text("gemini", MSGS)
            chat.assert_not_called()  # no automatic fallback
        self.assertNotIn("GEMINI_API_KEY", str(cm.exception))

    def test_quota_and_503_hide_internals_and_do_not_fall_back(self):
        for err in (RuntimeError("429 RESOURCE_EXHAUSTED quota secret-detail"), RuntimeError("503 UNAVAILABLE")):
            with mock.patch.object(rp, "_generate_gemini", side_effect=err), \
                 mock.patch.object(rp, "_generate_chat") as chat:
                with self.assertRaises(rp.GenerationUnavailable) as cm:
                    rp.generate_text("gemini", MSGS)
                chat.assert_not_called()
            self.assertNotIn("quota", str(cm.exception))
            self.assertIsNone(cm.exception.__cause__)

    def test_empty_response_unknown_provider_and_rate_limit_hook(self):
        with mock.patch.object(rp, "_generate_gemini", return_value="  "):
            with self.assertRaises(rp.GenerationUnavailable):
                rp.generate_text("gemini", MSGS)
        with self.assertRaises(ValueError):
            rp.generate_text("nope", MSGS)
        with mock.patch.object(rp, "check_rate_limit", side_effect=rp.GenerationUnavailable("x")), \
             mock.patch.object(rp, "_generate_gemini") as g:
            with self.assertRaises(rp.GenerationUnavailable):
                rp.generate_text("gemini", MSGS)
            g.assert_not_called()


class FallbackFlowTests(unittest.TestCase):
    def setup_flow(self, fail=("gemini",)):
        isolate_health(self)
        calls = []
        patcher = mock.patch.object(fallback, "answer_question", fake_pipeline(calls, fail))
        patcher.start()
        self.addCleanup(patcher.stop)
        return calls, {}

    def test_gemini_failure_opens_dialog_without_openai(self):
        calls, state = self.setup_flow()
        self.assertIsNone(fallback.run_primary(state, Q, [], None))
        pending = fallback.take_pending(state)
        self.assertEqual((calls, pending["question"]), (["gemini"], Q))
        self.assertNotIn("pending_fallback", state)  # dismissal leaves no pending state
        self.assertIsNone(fallback.take_pending(state))  # a rerun cannot reopen the dialog

    def test_rerun_and_cancel_make_no_openai_call(self):
        calls, state = self.setup_flow()
        fallback.run_primary(state, Q, [], None)
        fallback.cancel(state)
        fallback.run_primary(state, Q, [], None)  # rerun
        self.assertEqual(calls, ["gemini"])
        self.assertNotIn("pending_fallback", state)
        fallback.retry_primary(state)
        fallback.run_primary(state, Q, [], None)
        self.assertEqual(calls, ["gemini", "gemini"])  # explicit retry uses Gemini, never OpenAI

    def test_exactly_one_openai_call_after_confirmation_and_duplicates_blocked(self):
        calls, state = self.setup_flow()
        fallback.run_primary(state, Q, [], None)
        pending = fallback.take_pending(state)
        self.assertEqual(fallback.confirm_openai(state, pending, [], None)["provider"], "openai")
        self.assertIsNone(fallback.confirm_openai(state, pending, [], None))  # rerun / double click
        self.assertEqual(fallback.run_primary(state, Q, [], None)["provider"], "openai")  # served from session
        self.assertEqual(calls.count("openai"), 1)
        self.assertNotIn("pending_fallback", state)

    def test_openai_failure_is_safe_and_not_retried(self):
        calls, state = self.setup_flow(fail=("gemini", "openai"))
        fallback.run_primary(state, Q, [], None)
        pending = fallback.take_pending(state)
        self.assertIsNone(fallback.confirm_openai(state, pending, [], None))
        self.assertTrue(state["fallback_failed"])
        self.assertIsNone(fallback.confirm_openai(state, pending, [], None))
        self.assertIsNone(fallback.run_primary(state, Q, [], None))
        self.assertEqual(calls.count("openai"), 1)
        self.assertNotIn("pending_fallback", state)

    def test_state_serialization_is_secret_free(self):
        _, state = self.setup_flow()
        fallback.run_primary(state, Q, [], None)
        text = json.dumps(state)
        for needle in ("API_KEY", "Traceback", "RESOURCE_EXHAUSTED"):
            self.assertNotIn(needle, text)
        self.assertEqual(set(state["pending_fallback"]), {"id", "question"})


class ProviderHealthTests(unittest.TestCase):
    def setUp(self):
        self.path = isolate_health(self)
        self.calls = []
        self.outcomes = []  # next Gemini outcome per call: "ok", or the failure category to raise

    def answer(self, question, chunks, emb, provider=config.DEFAULT_PROVIDER):
        self.calls.append(provider)
        outcome = self.outcomes.pop(0) if provider == "gemini" else "ok"
        if outcome != "ok":
            raise rp.GenerationUnavailable(provider, outcome)
        return {"answer": "ok", "provider": provider, "source_map": {}}

    def ask(self, state, now, question=Q):
        with mock.patch.object(fallback, "answer_question", self.answer):
            return fallback.run_primary(state, question, [], None, now=now)

    def test_classification(self):
        for code in (408, 429, 500, 502, 503, 504):
            self.assertEqual(ph.classify_failure(HttpError(code)), "retryable")
        for code in (400, 401, 403, 404):
            self.assertEqual(ph.classify_failure(HttpError(code)), "nonretryable")
        self.assertEqual(ph.classify_failure(httpx.ReadTimeout("x")), "retryable")
        with mock.patch.object(rp, "_generate_gemini", side_effect=HttpError(503)):
            with self.assertRaises(rp.GenerationUnavailable) as cm:
                rp.generate_text("gemini", MSGS)
        self.assertEqual(cm.exception.category, "retryable")
        with mock.patch.dict(os.environ, {}):  # missing credential: never reached Gemini, not eligible
            os.environ.pop("GEMINI_API_KEY", None)
            with self.assertRaises(rp.GenerationUnavailable) as cm:
                rp.generate_text("gemini", MSGS)
        self.assertIsNone(cm.exception.category)

    def test_one_failure_keeps_closed_two_within_five_minutes_open(self):
        self.outcomes = ["retryable", "retryable"]
        self.ask({}, 1000)
        self.assertEqual(ph.load().circuit_state, "closed")
        self.ask({}, 1200)
        h = ph.load()
        self.assertEqual((h.circuit_state, h.circuit_opened_at, h.retryable_failures), ("open", 1200, 2))

    def test_failures_more_than_five_minutes_apart_do_not_open(self):
        self.outcomes = ["retryable", "retryable"]
        self.ask({}, 1000)
        self.ask({}, 1400)
        self.assertEqual(ph.load().circuit_state, "closed")

    def test_open_circuit_skips_gemini_uses_dialog_path_and_openai_only_on_confirmation(self):
        self.outcomes = ["retryable", "retryable"]
        self.ask({}, 1000)
        self.ask({}, 1100)
        state = {}
        self.assertIsNone(self.ask(state, 1200))  # open: Gemini skipped
        self.assertEqual(self.calls, ["gemini", "gemini"])
        pending = fallback.take_pending(state)
        self.assertIsNotNone(pending)
        fallback.cancel(state)
        self.assertEqual(self.calls, ["gemini", "gemini"])  # open, dismiss, cancel: no OpenAI
        with mock.patch.object(fallback, "answer_question", self.answer):
            fallback.confirm_openai(state, pending, [], None)
            fallback.confirm_openai(state, pending, [], None)
        self.assertEqual(self.calls.count("openai"), 1)
        self.assertEqual(ph.load().eligible_attempts, 2)  # skipped and OpenAI requests not counted

    def test_half_open_probe_success_closes_and_failure_reopens(self):
        self.outcomes = ["retryable", "retryable", "ok"]
        self.ask({}, 1000)
        self.ask({}, 1100)
        self.assertIsNone(self.ask({}, 1100 + 599, "q2"))  # still cooling down
        self.assertEqual(len(self.outcomes), 1)
        self.assertEqual(self.ask({}, 1100 + 600, "q3")["provider"], "gemini")  # probe
        h = ph.load()
        self.assertEqual((h.circuit_state, h.consecutive_retryable_failures), ("closed", 0))
        self.outcomes = ["retryable", "retryable", "retryable"]
        self.ask({}, 3000, "a")
        self.ask({}, 3100, "b")
        self.ask({}, 3100 + 600, "c")  # failed probe
        h = ph.load()
        self.assertEqual((h.circuit_state, h.circuit_opened_at), ("open", 3700))
        self.assertIsNone(self.ask({}, 3700 + 599, "d"))

    def test_nonretryable_half_open_failure_reopens_without_retry_or_openai(self):
        self.outcomes = ["retryable", "retryable", "nonretryable"]
        self.ask({}, 1000)
        self.ask({}, 1100)
        state = {}
        self.assertIsNone(self.ask(state, 1700))  # probe fails with a nonretryable error
        h = ph.load()
        self.assertEqual((h.circuit_state, h.circuit_opened_at, h.nonretryable_failures), ("open", 1700, 1))
        self.assertEqual(self.calls, ["gemini"] * 3)  # one probe, no automatic retry
        self.assertIsNone(self.ask(state, 1701, "other"))  # cooling down again
        self.assertEqual(self.calls, ["gemini"] * 3)
        self.assertNotIn("openai", self.calls)
        self.outcomes = [None]  # missing credential on the next probe: not counted, stays open
        self.ask({}, 1700 + 600, "again")
        h = ph.load()
        self.assertEqual((h.circuit_state, h.eligible_attempts), ("open", 3))

    def test_cached_and_not_eligible_requests_are_excluded(self):
        state = {}
        self.outcomes = ["ok"]
        self.ask(state, 1000)
        self.ask(state, 1001)  # cached for the same question
        self.assertEqual(ph.load().eligible_attempts, 1)
        self.outcomes = [None]  # missing credential / blocked: never reached Gemini
        self.ask({}, 1002, "other")
        self.assertEqual(ph.load().eligible_attempts, 1)

    def test_reliability_thresholds_and_no_side_effects(self):
        r = ph.evaluate_provider_reliability
        self.assertEqual((r(49, 49)["evaluation_ready"], r(49, 49)["recommended_default"]), (False, "gemini"))
        self.assertEqual((r(50, 45)["evaluation_ready"], r(50, 45)["recommended_default"]), (True, "gemini"))
        self.assertEqual((r(50, 44)["recommended_default"], r(50, 44)["success_rate"]), ("openai", 0.88))
        self.assertEqual(set(r(50, 45)), {"attempts", "successes", "success_rate", "evaluation_ready",
                                          "recommended_default", "reason"})
        calls = []
        with mock.patch.object(fallback, "answer_question", lambda *a, **k: calls.append(1)):
            r(50, 44)
        self.assertEqual((calls, config.DEFAULT_PROVIDER), ([], "gemini"))

    def test_missing_malformed_and_sanitized_state(self):
        self.assertEqual(ph.load(), ph.ProviderHealth())
        for bad in ("{not json", '{"eligible_attempts": "x"}', '{"circuit_state": "weird"}', "[]"):
            self.path.write_text(bad, encoding="utf-8")
            self.assertEqual(ph.load(), ph.ProviderHealth())
        self.outcomes = ["retryable"]
        self.ask({}, 1000, "SECRET QUESTION TEXT")
        text = self.path.read_text(encoding="utf-8")
        for needle in ("SECRET", "QUESTION", "detail that", "API_KEY"):
            self.assertNotIn(needle, text)
        self.assertEqual(set(json.loads(text)), set(ph.ProviderHealth.__dataclass_fields__))
        self.assertFalse(self.path.with_name("state.json.tmp").exists())


class PageStructureTests(unittest.TestCase):
    def test_page_wiring_and_evidence_explorer_independent(self):
        pages = EVAL.parent / "pages"
        page = (pages / "research_assistant.py").read_text(encoding="utf-8")
        for needle in ('@st.dialog("Live synthesis is temporarily unavailable")', "Open Evidence Explorer",
                       "Generate once with OpenAI", "Cancel", "Free-tier content may be used"):
            self.assertIn(needle, page)
        self.assertEqual(page.count("        fallback_dialog(pending)"), 1)  # the call, not the def
        self.assertNotIn("answer_question", page)  # provider logic stays out of the page
        explorer = (pages / "evidence_explorer.py").read_text(encoding="utf-8")
        for name in ("answer_question", "generate_text", "rag_pipeline", "fallback"):
            self.assertNotIn(name, explorer)  # evidence-only path never reaches generation


if __name__ == "__main__":
    unittest.main()
