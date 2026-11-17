# EcoLogits Gemini Free-Tier Experiment Findings

## Status: COMPLETE. Operational Reliability Under Evaluation

Gemini 3.5 Flash-Lite passed compatibility, impact-structure, retrieval, and lightweight response-quality gates and is now the default Research Assistant provider.

OpenAI remains an explicit, nonautomatic fallback. Intermittent Gemini availability failures were observed, including HTTP 503 responses. Production reliability has not yet been established.

Structure follows `docs/ecologits_experiment_findings.md`. Boundaries: `docs/impact_accounting_scope.md`.
Results are sanitized and local under `evaluation/impact_results/ecologits/gemini/` (git-ignored).

## Configuration

| Item | Value |
| :-- | :-- |
| Branch / starting commit | `experiment/ecologits-gemini-free-tier` / `d6ef567` |
| EcoLogits / google-genai | 0.11.3 / 1.49.0 (no dependency changes; the `google_genai` tracer ships with 0.11.3) |
| Pre-API validation | syntax check, 15 focused tests, Hit@5 = 8/10: all passed |
| Credential | `GEMINI_API_KEY` present in the process after the app's normal `.env` load (presence only) |

## Model selection

Initially selected: `gemini-2.5-flash-lite` (404 on generateContent); retried with `gemini-3.5-flash-lite` at the human's direction (a costlier Flash-Lite model). Both are registered in EcoLogits, appears in the free `models.list` and `models.get` calls with `generateContent`, and is listed "Free of charge" on the first-party pricing page (aistudio.google.com/docs/pricing, fetched 2026-11-17). Neither name has a `-preview` suffix. The page does not state stability explicitly.

| Candidate | In EcoLogits | Listed for project | Free tier (pricing page) | Note |
| :-- | :-- | :-- | :-- | :-- |
| gemini-2.5-flash-lite | Yes | Yes | Yes | Cheapest (USD 0.10/0.40 per 1M paid rates); 404 on generateContent |
| gemini-3.1-flash-lite | Yes | Yes | Yes | Costlier (0.25/1.50); not tested |
| gemini-3.5-flash-lite | Yes | Yes | Yes | Costlier (0.30/2.50); compatibility request succeeded |
| gemini-3.1-flash-lite-preview | Yes | Yes | n/a | Preview; avoided |
| gemma-4 models | Yes | Yes | not checked | Not tested |

Free-tier content may be used by Google to improve its products (pricing page).

## Compatibility result

### gemini-2.5-flash-lite (failed)
Provider `google_genai`, error type `ClientError`, HTTP 404. The harness did not store the provider message, so a sanitized message is unavailable; the cause is **undetermined**. `models.get` confirmed the model is exposed, so it is not simply absent. No further 2.5 attempts were made. Record: `.../gemini/compat_20261117T175321Z_016fec/`.

### gemini-3.5-flash-lite (retry, exactly one request)
Checks: registered in EcoLogits 0.11.3 (yes); exposed to the project with `generateContent` (yes, free `models.get`); free-tier eligible ("Free of charge" on the first-party pricing page fetched 2026-11-17; no per-model free-tier field exists in the model metadata). Request: public prompt, cap 25 output tokens, temperature 0, non-streaming, no tools or grounding, no thinking config set.

Outcome: **success**, model returned `gemini-3.5-flash-lite` (no substitution), 11 input / 21 output tokens, 0.77 s, finish reason `MAX_TOKENS` although 21 < 25 (hidden thinking tokens were not reported: `thoughts_token_count` was absent; unexplained). Impacts: complete; phases usage and embodied; all five criteria returned as ranges (no mean, no midpoints): energy 1.86e-06 to 1.13e-05 kWh, GWP 8.39e-07 to 4.86e-06 kgCO2eq, water 7.5e-06 to 4.6e-05 L, primary energy 1.96e-05 to 1.16e-04 MJ, ADPe 7.1e-12 to 2.9e-11 kgSbeq. Energy and water have no embodied value (absent, not zero). Warnings: `model-arch-not-released`, `model-arch-multimodal`. Errors: none. Record: `.../gemini/compat_20261117T180045Z_7a244f/`. Single request; not a repeatability result.

## RAG requests (`gemini-3.5-flash-lite`, 5 of 5 succeeded)

Experiment `rag_20261117T180648Z_4bd001`; Top-K 5, 5 chunks, 7,614 context characters, identical for all requests; 1,860 input tokens each; cached input and thinking tokens not reported (absent, not zero). Summary: `evaluation/impact_results/ecologits/gemini/summary.csv` / `summary.json` (these also count the failed 2.5 compat record).

| Condition | n | Output tokens | Latency s | Finish | Energy kWh (lower to upper) | GWP kgCO2eq (lower to upper) |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| rag_100 | 3 | 96 each | 0.99 / 1.10 / 0.78 | MAX_TOKENS x3 | 6.58e-06 to 6.81e-06 / 4.42e-05 to 4.51e-05 | 2.65e-06 to 2.80e-06 / 1.75e-05 to 1.81e-05 |
| rag_250 | 1 | 246 | 1.58 | MAX_TOKENS | 1.66e-05 / 1.12e-04 | 6.62e-06 / 4.41e-05 |
| rag_500 | 1 | 386 | 44.71 | STOP | 2.70e-05 / 1.80e-04 | 1.10e-05 / 7.16e-05 |

All criteria were ranges with usage and embodied phases (energy and water: no embodied value, recorded as absent). Warnings on every request: `model-arch-not-released`, `model-arch-multimodal`. Errors: none. Output counts of 96 and 246 under caps of 100 and 250 with `MAX_TOKENS` repeat the unexplained discrepancy seen in the compat request. The 44.71 s latency for rag_500 is an unexplained outlier (n = 1); its estimate rises with that latency and should be read with care. Input and output tokens were identical across the three 100-cap repeats; estimate bounds varied by under 4%.

Answer completeness and citation quality were **not assessed**: responses are deliberately not stored. The 100 and 250 caps truncated; only the 500 cap finished naturally. OpenAI comparison (gpt-4o-mini, same question): output 100/250/382 tokens, energy upper bounds 8.4e-06 / 2.0e-05 / 2.95e-05 kWh. Gemini's ranges are wider and its upper bounds roughly 4 to 6 times higher at similar output lengths; the models differ in estimation assumptions, so this is not a like-for-like efficiency comparison.

## Quality review (500-token cap, one request)

An earlier quality request failed with `ServerError` 503 on both harness attempts (`rag_20261117T182424Z_98ff4e`, no response). A later single request (`rag_20261117T185626Z_6a10e5`, no retry) succeeded: finish reason `STOP`, 413 output tokens (1,860 input), 9.29 s, impacts present. The question, retrieved passages and response are kept only in the git-ignored `quality_review_local.json` in that folder; none appear here.

| Check | Result | Brief evidence |
| :-- | :-- | :-- |
| 1. Directly and fully answers | Pass | Addresses the factors in the retrieved passages (task structure, model size, learning paradigm, user choices, algorithm and architecture improvements) |
| 2. Natural conclusion | Pass | `STOP`; 413 of 500 tokens |
| 3. Claims supported by passages | Pass, with caveats | Every claim traces to a retrieved passage. The orders-of-magnitude example blends text-to-image/text-to-category with text-generation/masked-language-modeling, which the passage does not quite say |
| 4. Cited IDs exist and support claims | Pass | Only S3 and S5 are cited; both were retrieved and match the attached claims |
| 5. Nothing invented | Pass | No extra sources, figures or conclusions found |

Quality caveat for the human reviewer: the answer omits the quantified ranges and conditions in the S5 passage (for example the 1.5 to 10x improvement estimate and "if model performance holds steady"), so uncertainty is only partly preserved. This is one question and one response by one reviewer (Claude); it is not a robust quality evaluation.

## Provider decision and implementation

The quality gate passed, so **Gemini (`gemini-3.5-flash-lite`) is now the default** in `config.py` (`DEFAULT_PROVIDER`, `MODELS`, `MAX_OUTPUT_TOKENS = 500`). OpenAI remains available as `FALLBACK_PROVIDER` with `gpt-4o-mini`, the cheapest OpenAI model validated with EcoLogits here; it is never called automatically. `gemini-3.5-flash-lite` costs more than the 2.5 model that returned a 404, and "default" means the first provider tried: if `GEMINI_API_KEY` is missing the request fails safely and triggers the dialog.

Fallback behavior: when Gemini cannot proceed (missing credential, quota, 503, empty response) the Research Assistant opens one `st.dialog` titled "Live synthesis is temporarily unavailable". It says Gemini is unavailable, that Evidence Explorer remains available, and that choosing OpenAI sends the grounded request to a separate external provider. Actions: Open Evidence Explorer, Generate once with OpenAI, Cancel. Opening, dismissing or cancelling makes no OpenAI call; one confirmed click makes exactly one call; a one-time id blocks duplicates across reruns; pending state is consumed when the dialog opens. Provider details are never shown. If OpenAI fails, a short message is shown, nothing is retried, and Evidence Explorer stays linked. A response already produced is kept in session state for that question (a session-only answer cache); no persistent cache exists. A rate-limiting hook (`check_rate_limit`) is a no-op extension point.

Privacy limitation: the Research Assistant shows a free-tier notice, but free-tier content may be used by Google to improve its products, and the app cannot detect sensitive content. EcoLogits is used only in the experiment harness; per-response impact display in the app was not added. Evidence Explorer was not changed.

### Operational reliability and circuit breaker

The experiment established Gemini compatibility but did not establish a service-level reliability guarantee. The application therefore treats Gemini as a best-effort default provider.

#### Retry classification

The application may make one short retry for errors considered transient:

- HTTP 408
- HTTP 429
- HTTP 500, 502, 503, or 504
- network timeouts

The application must not retry:

- HTTP 400
- HTTP 401
- HTTP 403
- HTTP 404
- missing credentials
- invalid model or malformed request errors

Retry behavior must account for retries already performed by the Google Gen AI SDK so that nested retry loops do not cause excessive delays or request volume.

#### Circuit states

The Gemini circuit breaker has three states:

- **Closed:** Gemini requests are allowed.
- **Open:** Gemini requests are skipped temporarily and the fallback dialog is
  shown immediately.
- **Half-open:** one Gemini probe request is allowed after the cooldown period.

#### Proposed initial policy

- Open the circuit after two retryable Gemini failures within five minutes.
- Keep the circuit open for ten minutes.
- After ten minutes, allow one half-open Gemini request.
- Close the circuit if the probe succeeds.
- Reopen it for another ten minutes if the probe fails.

The circuit breaker stores only operational state:

- consecutive retryable failures;
- time the circuit opened;
- last failure category;
- last probe time.

It must not store questions, prompts, retrieved passages, generated responses, credentials, or personal identifiers.

#### User experience while the circuit is open

When Gemini is unavailable:

1. Do not call Gemini repeatedly.
2. Keep Evidence Explorer and other non-generative functionality available.
3. Show the existing availability dialog.
4. Do not call OpenAI automatically.
5. Call OpenAI only after the user explicitly selects
   **Generate once with OpenAI**.

### Initial reliability evaluation

The first production-like reliability review will occur after 50 eligible
Gemini generation attempts.

#### Eligible attempts

Include:

- real Research Assistant requests for which Gemini was the selected provider;
- Gemini requests that succeeded;
- Gemini requests that failed because of timeout, HTTP 429, or HTTP 5xx;
- half-open circuit probe requests.

Exclude:

- cached responses that made no provider request;
- synthetic or mocked tests;
- experiment-harness requests;
- requests cancelled before submission;
- OpenAI fallback requests;
- failures caused by a missing local credential or invalid application
  configuration.

Configuration failures remain operational defects, but they are tracked
separately from provider-availability reliability.

#### Success definition

A Gemini attempt counts as successful when:

- the provider returns a nonempty response;
- the requested model is used;
- the response is returned to the application;
- no provider fallback is required.

A successful request may still have separate answer-quality or impact-estimation
issues. Those issues should not be hidden by the availability metric.

#### Metrics

After 50 eligible attempts, calculate:

Gemini success rate = successful Gemini requests / eligible Gemini attempts

#### Cost guardrail

Before changing the default to OpenAI, define:

- the validated fallback model;
- maximum output tokens;
- per-user or per-session generation limits;
- daily and monthly request caps;
- a project spending alert;
- behavior when the spending limit is reached.

If the budget limit is reached, live synthesis should become unavailable rather
than silently exceeding the approved cost. Evidence Explorer must remain
available.

## Acceptance gates

| # | Gate | Result |
| :-- | :-- | :-- |
| 1 | Model registered in EcoLogits and free-tier | Pass |
| 2 | All six experiment requests succeed | Pass (plus one failed 503 and one 404 on 2.5, recorded) |
| 3 | Impacts, ranges, phases, warnings, errors preserved | Pass |
| 4 | No secrets or request content stored in tracked files | Pass (content only in ignored local review file) |
| 5 | Repeated requests succeed | Pass (n = 3; the 500-cap request varied 9 to 45 s) |
| 6 | 500-token answer complete and grounded | Pass with caveats (see above) |
| 7 | Source IDs and citations correct | Pass |
| 8 | Hit@5 = 8/10 | Pass |
| 9 | Credential and quota failures handled safely | Pass (mocked tests) |
| 10 | OpenAI optional | Pass |
| 11 | All tests pass | Pass (26) |

## Limitations and human decisions

- This is no evidence about measured energy, exact impacts, lifecycle coverage or production readiness.
- Human decisions: accept `gemini-3.5-flash-lite` as the default despite higher list prices than 2.5, whether one reviewed answer is enough quality evidence, whether the free-tier data-use limitation is acceptable for the intended audience, whether to rerun the 44.7 s latency outlier, whether to add in-app impact display, and whether to investigate the 2.5 404 (not investigated).
- A manual Streamlit check of the dialog was not run; the dialog logic is covered by mocked tests of `fallback.py` plus a structural test of the page.

### Required operational tests

The circuit-breaker implementation should include deterministic tests for:

1. One retryable failure does not open the circuit.
2. Two retryable failures within five minutes open the circuit.
3. Nonretryable 400, 401, 403, and 404 errors do not trigger retries.
4. An open circuit skips Gemini and opens the availability dialog.
5. Opening or dismissing the dialog does not call OpenAI.
6. Explicit confirmation makes exactly one OpenAI call.
7. A half-open probe succeeds and closes the circuit.
8. A failed half-open probe reopens the circuit.
9. Cached responses do not count as Gemini attempts.
10. OpenAI fallback requests do not count in Gemini's success-rate denominator.
11. The 50-attempt evaluation produces a recommendation below 90%.
12. Crossing the threshold does not silently call or configure OpenAI.
13. No operational metric contains request text, credentials, or user content.


### Updated operational decision

Gemini 3.5 Flash-Lite remains the cost-minimizing, best-effort default during
an initial 50-attempt observation period.

The application will use:

- bounded handling of transient failures;
- a short-lived circuit breaker;
- an always-available Evidence Explorer pathway; and
- an explicit, nonautomatic OpenAI fallback.

After 50 eligible Gemini attempts:

- a success rate of at least 90% supports retaining Gemini as the default;
- a success rate below 90% triggers human review of an OpenAI-default change;
- no paid-provider default change occurs silently.

This decision balances provider cost, application reliability, user consent, and the project's objective of making AI impacts visible.