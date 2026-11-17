"""Session-state logic for the Research Assistant: Gemini first, OpenAI only after explicit confirmation.

`state` is st.session_state (or any dict). Only the pending question and a one-time id are kept.
"""

import uuid

from . import provider_health
from .config import FALLBACK_PROVIDER
from .rag_pipeline import GenerationUnavailable, answer_question

UNAVAILABLE_MESSAGE = "Live synthesis is currently unavailable. Evidence Explorer remains available."


def run_primary(state, question, content_chunks, embeddings, now=None):
    """Answer with the default provider. Returns the response, or None when unavailable (sets pending fallback)."""
    cached = state.get("answer")
    if cached and cached["question"] == question:
        return cached["response"]
    if state.get("failed_question") == question:
        return None  # do not re-call the provider on every rerun
    health = provider_health.load()
    if provider_health.may_attempt(health, now):
        try:
            response = answer_question(question, content_chunks, embeddings)
        except GenerationUnavailable as exc:
            provider_health.record_outcome(health, exc.category, now)  # None: never reached Gemini, not counted
            provider_health.save(health)
            response = None
        else:
            provider_health.record_outcome(health, "success", now)
            provider_health.save(health)
    else:  # circuit open: skip Gemini, never call OpenAI
        provider_health.save(health)
        response = None
    if response is None:
        state["failed_question"] = question
        state["pending_fallback"] = {"id": uuid.uuid4().hex, "question": question}
        return None
    state["answer"] = {"question": question, "response": response}
    return response


def take_pending(state):
    """Consume the pending request when the dialog opens, so dismissal leaves no pending state."""
    return state.pop("pending_fallback", None)


def cancel(state):
    state.pop("pending_fallback", None)


def retry_primary(state):
    state.pop("failed_question", None)
    state.pop("fallback_failed", None)


def confirm_openai(state, pending, content_chunks, embeddings):
    """Exactly one OpenAI request per pending id. Returns the response or None (failure never exposes details)."""
    if state.get("fallback_consumed") == pending["id"]:
        return None
    state["fallback_consumed"] = pending["id"]
    state.pop("pending_fallback", None)
    try:
        response = answer_question(pending["question"], content_chunks, embeddings, provider=FALLBACK_PROVIDER)
    except Exception:
        state["fallback_failed"] = True
        return None
    state["answer"] = {"question": pending["question"], "response": response}
    state.pop("fallback_failed", None)
    state.pop("failed_question", None)
    return response
