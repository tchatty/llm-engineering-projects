"""Gemini provider health: a 50-attempt reliability count and a short-lived circuit breaker.

Development decision support only. Stores counters and timestamps, never request content, credentials,
exception messages or user identifiers. State lives in evaluation/provider_health_state.json (git-ignored,
created at runtime); ephemeral deployment filesystems may reset it. Timestamps are epoch seconds and every
function takes an explicit `now` so tests need no sleeping.
"""

import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parents[2] / "evaluation" / "provider_health_state.json"
RETRYABLE_HTTP = {408, 429, 500, 502, 503, 504}
FAILURE_WINDOW_SECONDS = 5 * 60
COOLDOWN_SECONDS = 10 * 60
FAILURES_TO_OPEN = 2
CLOSED, OPEN, HALF_OPEN = "closed", "open", "half_open"


@dataclass
class ProviderHealth:
    eligible_attempts: int = 0
    successful_attempts: int = 0
    retryable_failures: int = 0
    nonretryable_failures: int = 0
    consecutive_retryable_failures: int = 0
    recent_retryable_failure_times: list = field(default_factory=list)
    circuit_state: str = CLOSED
    circuit_opened_at: float | None = None
    last_failure_category: str | None = None


def classify_failure(exc):
    """'retryable' for HTTP 408/429/500/502/503/504 and network timeouts, else 'nonretryable'."""
    import httpx
    if isinstance(exc, (httpx.TimeoutException, TimeoutError)):
        return "retryable"
    code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    return "retryable" if code in RETRYABLE_HTTP else "nonretryable"


def load(path=None):
    """Missing or malformed state is treated as empty."""
    try:
        data = json.loads(Path(path or STATE_PATH).read_text(encoding="utf-8"))
        health = ProviderHealth(**{k: v for k, v in data.items() if k in ProviderHealth.__dataclass_fields__})
        ints = [health.eligible_attempts, health.successful_attempts, health.retryable_failures,
                health.nonretryable_failures, health.consecutive_retryable_failures]
        if (not all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in ints)
                or health.circuit_state not in (CLOSED, OPEN, HALF_OPEN)
                or not isinstance(health.recent_retryable_failure_times, list)
                or not all(isinstance(t, (int, float)) for t in health.recent_retryable_failure_times)):
            return ProviderHealth()
        return health
    except Exception:
        return ProviderHealth()


def save(health, path=None):
    """Write through a temporary file and atomically replace."""
    path = Path(path or STATE_PATH)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(asdict(health), indent=2), encoding="utf-8")
    os.replace(tmp, path)


def may_attempt(health, now=None):
    """True if Gemini may be tried. After the cooldown, the first call becomes the single half-open probe."""
    now = time.time() if now is None else now
    if health.circuit_state == CLOSED:
        return True
    if health.circuit_state == OPEN and now - health.circuit_opened_at >= COOLDOWN_SECONDS:
        health.circuit_state = HALF_OPEN
        return True
    return False


def record_outcome(health, outcome, now=None):
    """One final outcome per user request: 'success', 'retryable', 'nonretryable', or None (not eligible)."""
    now = time.time() if now is None else now
    probing = health.circuit_state == HALF_OPEN
    if outcome is None:
        if probing:  # probe never reached Gemini: stay open and probe again next time
            health.circuit_state = OPEN
        return health
    health.eligible_attempts += 1
    if outcome == "success":
        health.successful_attempts += 1
        health.consecutive_retryable_failures = 0
        health.recent_retryable_failure_times = []
        health.circuit_state, health.circuit_opened_at = CLOSED, None
    elif outcome == "retryable":
        health.retryable_failures += 1
        health.consecutive_retryable_failures += 1
        health.last_failure_category = "retryable"
        recent = [t for t in health.recent_retryable_failure_times if now - t < FAILURE_WINDOW_SECONDS]
        health.recent_retryable_failure_times = recent + [now]
        if probing or len(health.recent_retryable_failure_times) >= FAILURES_TO_OPEN:
            health.circuit_state, health.circuit_opened_at = OPEN, now
    else:
        health.nonretryable_failures += 1
        health.last_failure_category = "nonretryable"
        if probing:  # failed probe of any kind reopens the circuit; never retried automatically
            health.circuit_state, health.circuit_opened_at = OPEN, now
    return health


def evaluate_provider_reliability(eligible_attempts, successful_attempts, minimum_attempts=50,
                                  required_success_rate=0.90):
    """Human-review recommendation only. Never changes config or calls a provider."""
    rate = successful_attempts / eligible_attempts if eligible_attempts else None
    ready = eligible_attempts >= minimum_attempts
    if not ready:
        default, reason = "gemini", f"fewer than {minimum_attempts} eligible attempts; keep collecting"
    elif rate >= required_success_rate:
        default, reason = "gemini", "success rate meets the required threshold"
    else:
        default, reason = "openai", "success rate is below the required threshold"
    return {"attempts": eligible_attempts, "successes": successful_attempts, "success_rate": rate,
            "evaluation_ready": ready, "recommended_default": default, "reason": reason}


def developer_review(path=None):
    """Sanitized snapshot plus recommendation, for developer review (no UI)."""
    health = load(path)
    return {"health": asdict(health),
            "reliability": evaluate_provider_reliability(health.eligible_attempts, health.successful_attempts)}


if __name__ == "__main__":
    print(json.dumps(developer_review(), indent=2))
