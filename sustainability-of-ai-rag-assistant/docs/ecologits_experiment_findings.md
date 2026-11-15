# EcoLogits Remote Inference Experiment Findings

## Document status

**Preliminary findings for methodology review.** Governing boundaries and terminology: `docs/impact_accounting_scope.md`. Protocol: `docs/ecologits_experiment_protocol.md`. No production code or Streamlit integration was changed. Results are sanitized (no questions, prompts, context, responses, keys, or raw impact objects) and live locally under `evaluation/impact_results/ecologits/` (git-ignored).

## 1. Objective and configuration

Assess whether EcoLogits can estimate impacts of the Research Assistant's remote generation call (compatibility, completeness, suitability).

| Item | Value |
| :-- | :-- |
| EcoLogits / OpenAI SDK | 0.11.3 / 2.7.1 |
| Starting Git commit | `ce1e07f` (working tree dirty during runs: new files and dependency changes) |
| Provider / request path | OpenAI chat completions via the existing `rag_pipeline.client`; non-streaming; temperature 0 |
| Corpus / retrieval | Current corpus (fingerprint in manifest), Top-K 5, 5 chunks retrieved once, 7,614 context characters, identical for all RAG requests |
| Prompt / retrieval versions | Neither is versioned in code; system-prompt and question hashes are recorded instead |
| Conditions | 1 compatibility request (cap 50); 3 RAG requests at cap 100; 1 at 250; 1 at 500 |

## 2. Model selection

**Experimental model: `gpt-4o-mini` (returned as `gpt-4o-mini-2024-07-18`). Production model: `gpt-4.1-mini` (`config.py`). These differ; no result here applies to `gpt-4.1-mini` or any other model.**

| Candidate | In EcoLogits | Accessible to account | Price in/cached/out per 1M (USD) | Outcome |
| :-- | :-- | :-- | :-- | :-- |
| gpt-5-nano | Yes | Yes | 0.05 / 0.005 / 0.40 | Not used: reasoning model; documented to reject `max_tokens` and non-default temperature, so incompatible with the application's request path (not tested, to avoid discovery spend) |
| gpt-4.1-nano | Yes | No (absent from account model list) | not checked | Not usable |
| gpt-4o-mini | Yes | Yes | 0.15 / 0.075 / 0.60 | **Selected** |
| gpt-5.4-nano | Yes | Yes | 0.20 / 0.02 / 1.25 | Reasoning family; costlier |
| gpt-4.1-mini (production) | Yes | Yes | 0.40 / 0.10 / 1.60 | Costlier than selected |

Pricing source: OpenAI pricing page (`developers.openai.com/api/docs/pricing`, standard tier, fetched 2026-11-15). The page listed only a moderation model as free; no free text-generation API access was verified. **Lowest-cost status: pricing was verified, but "lowest-cost compatible" rests on an assumption that gpt-5-nano is incompatible (documented, not tested).** Access was checked with the free model-list call.

## 3. Results

### Compatibility (Observed)
All six requests succeeded. EcoLogits initialized, the normal response remained available, an impact object was present on every response, token usage and latency were readable, and no model substitution occurred. Valid / failed / unsupported: 6 / 0 / 0. One compatibility attempt was used.

### Tokens, latency, estimated provider cost (Observed)

| Condition | n | Input tokens | Cached input | Output tokens | Latency s (mean) | Hit cap |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| compat (cap 50) | 1 | 17 | 0 | 35 | 2.26 | 0 |
| rag_100 | 3 | 1,749 each | 0, 1,664, 1,664 | 100 each | 2.48 (2.07–2.96) | 3 of 3 |
| rag_250 | 1 | 1,749 | 1,664 | 250 | 3.63 | 1 of 1 |
| rag_500 | 1 | 1,749 | 1,664 | 382 | 4.64 | 0 (finished naturally) |

Totals: 8,762 input (6,656 cached), 967 output tokens. Estimated provider cost about USD 0.0014 (computed from the pricing above; not a billed amount). The first RAG request had no cached input; the rest did.

### Modeled estimates: criteria, phases, units
Criteria returned for every request: energy (kWh), GWP (kgCO2eq), water consumption (L), primary energy (MJ), ADPe (kgSbeq). All values were **ranges** (lower and upper); EcoLogits supplied no mean, and none was computed. Total and usage phases were present for all five criteria. Embodied phase was present for GWP, primary energy and ADPe only; energy and water have no embodied value (recorded as absent, not zero). In rag_100 request 2, embodied GWP had equal lower and upper bounds.

Warnings on all six requests: `model-arch-not-released`, `model-arch-multimodal` (both state lower precision). Errors: none.

### Repeatability (rag_100, n = 3; input and output tokens identical)

| Metric | Min | Max | CV |
| :-- | :-- | :-- | :-- |
| Latency (s) | 2.066 | 2.955 | 0.181 |
| Energy lower (kWh) | 7.023e-06 | 7.064e-06 | 0.0034 |
| Energy upper (kWh) | 8.389e-06 | 8.431e-06 | 0.0028 |
| GWP lower / upper (kgCO2eq) | 3.036e-06 / 3.561e-06 | 3.060e-06 / 3.585e-06 | 0.0046 / 0.0040 |

Full statistics (all criteria, bounds separate) are in `summary.json` / `summary.csv`. Observed: with fixed token counts, estimate CVs (below 0.015) were much smaller than the latency CV (0.181). Cached-input tokens differed (0 vs 1,664) while the energy bounds differed by under 1% (request 2's lower bound was slightly lower than requests 1 and 3); the cause was not investigated.

### Output-length observations (n = 1 each except 100)
Energy lower bound (kWh): 7.06e-06 (cap 100, request 1) → 1.64e-05 (cap 250) → 2.43e-05 (cap 500, 382 actual tokens). Upper: 8.43e-06 → 1.98e-05 → 2.95e-05. Estimates rose with output tokens and latency, as expected from the model. **Interpretation:** length policy changes the modeled estimate, but this experiment did not assess answer completeness or citations, so it supports no conclusion that the shortest output is preferable. **Human decision required:** completeness and citation review of each length.

## 4. Limitations

- **Modeled estimate, not measured provider energy.** Not an exact or complete lifecycle impact; ranges and warnings reflect undisclosed OpenAI architecture and multimodal assumptions.
- Single model, single question, single corpus state, one session, n = 1 for 250/500/compat; no variance claim for them.
- Model differs from production; results do not transfer.
- Default electricity-mix zone was used (not configured for the actual provider location).
- Impacts exclude local retrieval, context construction, and UI. They use a different boundary from CodeCarbon and **must not be added to CodeCarbon values** automatically.
- Prompt construction in the harness replicates the message layout in `answer_question` because `max_tokens` and model are hard-coded there; drift is possible.
- EcoLogits is initialized with SDK patching in the harness only; interaction with the app's provider abstraction under Streamlit was not tested.
- Cost is an estimate from public list prices.

## 5. Preliminary suitability (Interpretation, unreviewed)

| Use | Status |
| :-- | :-- |
| Internal model / response-length comparisons | Provisionally suitable for scenario comparison, with ranges and warnings shown and with the production model tested separately |
| Per-response disclosure | Not yet determined: values complete and stable here, but warnings indicate low precision and the production model is untested |
| Application-lifetime aggregation | Not yet determined: no versioned prompt/retrieval/corpus identity, no ledger by design, and embodied-phase gaps for energy and water need a handling rule |
| Streamlit integration | Not assessed: not tested in the app |

## 6. Next steps and human decisions

Evidence-supported next steps: test `gpt-4.1-mini` (the production model) as a separately labeled run; repeat the 250 and 500 conditions if variance matters; decide how to handle criteria with no embodied value.

**Human decision required:** accept or reject `gpt-4o-mini` as a stand-in; whether warnings of reduced precision permit disclosure; electricity-mix zone; answer-quality review across output lengths; the protocol §12 outcome.
