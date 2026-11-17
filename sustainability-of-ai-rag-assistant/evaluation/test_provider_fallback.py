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

from sustainability_rag import config, fallback, rag_pipeline as rp  # noqa: E402

CHUNK = {"source_id": "S1", "source": "s.md", "section": "### A", "text": "t", "type": "content"}
Q = "public question"
MSGS = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]


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
