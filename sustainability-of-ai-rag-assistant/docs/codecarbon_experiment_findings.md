# CodeCarbon Local Compute Experiment Findings

## Document status

**Preliminary findings for methodology review.**

This document summarizes the first controlled CodeCarbon experiment for the Sustainability of AI application. It records the observed results, explains what those results do and do not support, and recommends the next validation step. It does not establish a production per-query impact factor or integrate CodeCarbon into the application.

The governing system boundaries, terminology, result classifications, and exclusions are defined in `docs/impact_accounting_scope.md`.

## 1. Executive summary

The experiment was successful as an initial feasibility study. CodeCarbon ran on the target Windows hardware, produced complete native outputs for every valid workload repetition, and captured component-level CPU, GPU, and RAM estimates.

### Preliminary decision

CodeCarbon is **provisionally suitable for controlled, machine-specific comparisons** of:

- cold-start corpus-resource construction; and
- sufficiently long batches of semantic-retrieval operations.

CodeCarbon is **not yet suitable** for:

- direct per-query disclosure in the Streamlit interface;
- application-lifetime aggregation of retrieval impacts; or
- an exact claim about the impact avoided by shared caching.

The main unresolved issue is attribution. The first experiment used machine-level tracking while the computer was running more than 420 processes and had approximately 20–35% CPU utilization before runs. The measured values therefore describe machine consumption during each workload window, not energy attributable exclusively to the Sustainability of AI process.

### Next decision gate

Run a focused follow-up using a longer retrieval workload under both `machine` and `process` tracking modes. If process-mode results are stable and the workload spans several 15-second sampling intervals, a hardware-specific batch-derived per-query range may become suitable for qualified user disclosure.

## 2. Objectives

The experiment evaluated whether CodeCarbon produces sufficiently granular, repeatable, and interpretable results for local computation associated with:

1. cold-start construction of shared corpus resources; and
2. semantic retrieval used by Evidence Explorer and the retrieval stage of Research Assistant.

The intended decision uses are:

- internal application-design comparisons;
- user-facing environmental-impact disclosures; and
- application-lifetime impact aggregation.

## 3. Experimental configuration

The experiment was implemented on branch `experiment/codecarbon-local-compute` without changing production application behavior.

| Configuration item | Value |
|---|---|
| CodeCarbon version | `3.3.2` |
| Embedding model | `all-MiniLM-L6-v2` |
| Embedding dimensions | `384` |
| Retrieval-eligible chunks | `253` |
| Retrieval Top-K | `5` |
| Tracking mode | `machine` |
| Sampling interval | `15 seconds` |
| Cloud upload | Disabled |
| Power source | AC power |

### Measurement basis

Hardware detection indicated:

- CPU energy tracking through the Windows Energy Meter Interface;
- GPU energy tracking through PyNVML on an NVIDIA T1200 Laptop GPU; and
- RAM energy represented through CodeCarbon's modeled RAM-power method.

The experiment is therefore classified as **partially measured** because it combines hardware telemetry with a modeled RAM component.

### Workloads

The experiment completed:

- one successful hardware-detection workflow after one corrected CLI invocation;
- three 60-second smoke-test repetitions;
- three cold-start corpus-resource repetitions;
- three batches of 100 retrieval operations; and
- three batches of 1,000 retrieval operations.

The 1,000-operation fallback was required because every 100-operation workload completed in less than the 15-second sampling interval.

The retrieval experiment reused the production `retrieve_relevant_chunks()` implementation and the reviewed retrieval-question set. Corpus resources were initialized before retrieval tracking, so retrieval results exclude cold-start corpus construction.

## 4. Results

### 4.1 Summary statistics

| Workload | Metric | n | Minimum | Maximum | Median | Mean | SD | CV |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Cold start | Duration (s) | 3 | 19.2 | 22.1 | 20.3 | 20.5 | 1.45 | 7.1% |
| Cold start | Energy (kWh) | 3 | 0.000240 | 0.000292 | 0.000259 | 0.000264 | 0.0000264 | 10.0% |
| Retrieval, 100 operations | Duration (s) | 3 | 4.30 | 5.30 | 4.86 | 4.82 | 0.502 | 10.4% |
| Retrieval, 100 operations | Energy (kWh) | 3 | 0.0000137 | 0.0000248 | 0.0000189 | 0.0000191 | 0.00000558 | 29.2% |
| Retrieval, 1,000 operations | Duration (s) | 3 | 15.0 | 20.3 | 16.9 | 17.4 | 2.69 | 15.5% |
| Retrieval, 1,000 operations | Energy (kWh) | 3 | 0.000136 | 0.000196 | 0.000158 | 0.000164 | 0.0000303 | 18.5% |
| Smoke test | Duration (s) | 3 | 63.2 | 63.2 | 63.2 | 63.2 | 0.031 | 0.05% |
| Smoke test | Energy (kWh) | 3 | 0.000693 | 0.000997 | 0.000751 | 0.000813 | 0.000161 | 19.8% |

Complete CPU, GPU, RAM, and greenhouse-gas statistics remain in the ignored local summary files.

### 4.2 Cold-start corpus construction

Cold-start construction averaged:

- **20.5 seconds**; and
- **0.000264 kWh**, equivalent to **264 mWh**.

Duration varied less than energy. This is expected because similar execution times do not guarantee similar machine-level energy consumption when background activity and hardware power states vary.

The observed repeatability is sufficient to treat cold-start construction as a promising target for machine-specific architecture comparisons. It is not sufficient to generalize the result to another computer, electricity region, corpus, or embedding model.

### 4.3 Retrieval batches

The 100-operation batches averaged:

- **4.82 seconds**; and
- **0.0000191 kWh**.

These runs were substantially shorter than one sampling interval and had the greatest energy variability. They should not be used to derive a per-query impact factor.

The 1,000-operation batches averaged:

- **17.4 seconds**; and
- **0.000164 kWh**.

The longer batch reduced energy variability from 29.2% to 18.5%, but it still covered only about one 15-second sampling interval. Two workload wall-clock runs were below 15 seconds even though CodeCarbon's tracker-reported durations were longer. A longer workload is required before evaluating convergence.

### 4.4 Provisional internal allocation

Dividing the 1,000-operation batch results by 1,000 gives a provisional diagnostic range of:

- **0.136–0.196 mWh per retrieval**; and
- a mean of approximately **0.164 mWh per retrieval**.

This is a **derived batch allocation**, not a direct measurement of an individual user query. It must not yet be displayed as a precise per-query impact because:

- machine tracking includes unrelated activity;
- the measured batch was short relative to the sampling interval;
- RAM power was modeled;
- energy variability remained material; and
- the value is specific to the tested hardware and application configuration.

## 5. Shared-resource optimization

The shared corpus-resource cache prevents Evidence Explorer and Research Assistant from independently loading, chunking, and embedding the same corpus within one Streamlit process.

This is a deterministic architecture benefit, but the experiment did not run a controlled cached-versus-uncached comparison. The defensible finding is:

> Shared caching avoids a duplicate corpus-construction operation. The experiment measured one cold-start operation but did not directly measure the environmental impact avoided by cache reuse.

The measured cold-start result must not be presented as the exact energy saved whenever a user moves between pages.

A separate paired experiment could compare:

1. two independent corpus-resource constructions; and
2. one corpus-resource construction followed by reuse.

A simpler deterministic verification should also confirm that `embed_chunks()` executes once per Streamlit process as users move from Evidence Explorer to Research Assistant.

## 6. Attribution and uncertainty

### 6.1 Machine-level tracking

The experiment used `tracking_mode="machine"`. Before runs, CPU utilization was approximately 20–35%, with about 425 active processes.

Machine mode answers:

> What did the tested computer consume while the workload ran?

It does not isolate:

> What energy was attributable only to the Sustainability of AI operation?

Background activity is representative of normal desktop use, so the results remain useful as an operational scenario. However, application impact reporting requires stronger attribution than machine mode currently provides.

### 6.2 Mixed measurement basis

CPU and GPU values came from available telemetry, while RAM was modeled. Results must therefore remain labeled **partially measured**. Component-level results should be retained so future methodology changes do not collapse measured and modeled contributions into an indistinguishable total.

### 6.3 Tracker and workload duration

The 60-second smoke workload produced a tracker duration of approximately 63.2 seconds. The difference may include tracker initialization, final sampling, metadata lookup, and output writing.

Future records should retain both:

- workload wall-clock duration; and
- CodeCarbon tracker duration.

The native energy value should remain associated with the native tracker boundary.

### 6.4 Multiple-instance warning

Six manifests included a message that multiple CodeCarbon instances were allowed. Runs were launched sequentially in separate processes, but the implementation should be reviewed for `allow_multiple_runs` or lock-file behavior before the next experiment. Concurrent machine-level trackers could double-count the same machine consumption.

### 6.5 Reproducibility

The experiment recorded a Git commit, but the working tree contained uncommitted experiment implementation changes. Future published experiments should run from a clean committed state so the exact script version is reproducible.

## 7. Suitability assessment

| Intended use | Decision | Basis |
|---|---|---|
| Internal cold-start comparisons | **Suitable with qualifications** | Workload boundary is clear and repeatability is promising; results remain machine-specific and partially measured. |
| Internal retrieval-batch comparisons | **Promising; validation required** | Longer batches reduced variability but still covered only about one sampling interval. |
| Shared-cache design justification | **Supported qualitatively** | Duplicate construction is avoided by design; environmental savings were not measured directly. |
| Per-query user disclosure | **Not yet suitable** | Current values are machine-level, batch-derived, and materially variable. |
| Lifetime retrieval aggregation | **Not yet suitable** | Application attribution, allocation rules, and compatibility boundaries remain unresolved. |
| Production frontend integration | **Premature** | Process-mode and longer-batch validation should precede display design. |

## 8. Recommended follow-up experiment

Run a focused retrieval validation using:

- 3,000 retrieval operations per repetition;
- three repetitions in `machine` mode;
- three repetitions in `process` mode;
- the existing 15-second sampling interval;
- the same hardware, corpus, embedding model, Top-K, and question set;
- a clean committed experiment branch; and
- recorded pre-run CPU utilization and active-process count.

This follow-up should answer:

1. Does the workload span several sampling intervals?
2. Does process mode improve application attribution?
3. Do batch-derived energy values converge across repetitions?
4. How different are process-mode and machine-mode results under the same workload?
5. Is a hardware-specific range defensible for qualified user disclosure?

Do not subtract an idle baseline automatically. If an idle control is used, treat it as context for background variability unless a defensible subtraction rule is established.

## 9. Data handling and analytics

Keep raw output ignored because native CodeCarbon records may contain hardware, operating-system, geographic, and local-path metadata.

Join application manifests to native CodeCarbon rows using:

```text
manifest.codecarbon_run_id = emissions.run_id
```

Do not join on the native CodeCarbon `experiment_id`, which is distinct from the application-generated experiment identifier.

A normalized local analytics table should preserve:

| Field group | Fields |
|---|---|
| Identity | Application experiment ID, CodeCarbon run ID, timestamp |
| Workload | Workload type, operation count, valid and failed operations |
| Configuration | Tracking mode, sampling interval, corpus fingerprint, embedding model, chunk count, Top-K |
| Duration | Workload wall time, tracker duration |
| Impact | Total energy, CPU energy, GPU energy, RAM energy, GHG emissions |
| Provenance | Measurement classification, CodeCarbon version, Git commit |

Do not build a production database until the CodeCarbon and EcoLogits output structures and aggregation rules have both been reviewed.

## 10. Streamlit reporting implications

Do not display the current mean as a definitive per-query value.

If the follow-up validates a stable process-attributed range, an initial disclosure could use language such as:

> **Local retrieval impact:** batch-derived estimate for the tested hardware and application version. See methodology for measurement basis and limitations.

The interface should separately represent:

- cold-start corpus initialization;
- per-question local retrieval;
- remote generative inference;
- cache hits and avoided live generation; and
- unsupported or excluded operations.

Measured, partially measured, modeled, and derived values must remain visibly distinct.

## 11. Responsible-practice implications

The experiment supports the following practices:

- Reuse unchanged corpus embeddings.
- Preserve Evidence Explorer as a non-generative pathway.
- Separate cold-start impacts from per-question impacts.
- Use workloads long enough for the estimator's sampling resolution.
- Distinguish system consumption from application-attributable consumption.
- Preserve component-level and methodology-version provenance.
- Avoid universal claims from machine-specific results.
- Keep local retrieval and remote inference as separate impact components.

## 12. Decision record

**Current decision:** retain CodeCarbon as the experimental local-compute estimator and proceed with one targeted validation study before production integration.

**Approved uses now:**

- controlled cold-start comparisons;
- controlled retrieval-batch comparisons with disclosed limitations; and
- architecture decisions about avoiding unnecessary local computation.

**Deferred uses:**

- per-query Streamlit disclosure;
- lifetime local-compute aggregation; and
- combined local-plus-remote impact totals.

**Next review trigger:** completion of the 3,000-operation machine/process comparison and deterministic shared-cache verification.

## Follow-up Attribution and Convergence Validation

Generated results are ignored by Git under `evaluation/impact_results/codecarbon/attribution_validation/` (per-repetition manifests and native `emissions.csv`; `summary.csv`, `summary.json`, `attribution_analysis.json`). Manifests were joined to native rows with `manifest.codecarbon_run_id = emissions.run_id`. Energy is in kWh, emissions in kg CO2eq.

### Follow-up configuration (Observed)

- 3,000 measured retrievals per repetition; 3 repetitions each for `tracking_mode=machine` and `process`, run alternately.
- `measure_power_secs=15`; 10 unmeasured warm-up retrievals before each batch; Top-K 5; existing corpus, embedding model, and reviewed questions.
- Validation before measurement: syntax checks and 6 unit tests passed; Hit@5 = 8/10 (unchanged); chunk count 253 and embedding dimensions 384 (enforced by the harness in every run).
- Code changes: summarizer joins on `run_id`, splits groups by tracking mode, and adds `--attribution` analysis; one cache test added. No production module changed.

### Cache-check result (Observed)

Pass. First `initialize_corpus_resources()` call: `embed_chunks` call count 1. Second call in the same process: count still 1, and the same cached object was returned. Avoided energy was not calculated.

### Machine-mode results (Observed; n=3, 0 failed, 0 missing)

| Metric | Min | Max | Median | Mean | SD | CV |
|---|---:|---:|---:|---:|---:|---:|
| Workload duration (s) | 30.5 | 54.9 | 33.2 | 39.5 | 13.4 | 33.8% |
| Tracker duration (s) | 33.7 | 58.1 | 36.3 | 42.7 | 13.4 | 31.3% |
| Total energy (kWh) | 4.63e-4 | 6.31e-4 | 5.24e-4 | 5.39e-4 | 8.50e-5 | 15.8% |
| CPU energy (kWh) | 2.62e-4 | 3.08e-4 | 2.72e-4 | 2.81e-4 | 2.42e-5 | 8.6% |
| GPU energy (kWh) | 3.06e-5 | 5.31e-5 | 3.13e-5 | 3.83e-5 | 1.28e-5 | 33.3% |
| RAM energy (kWh) | 1.70e-4 | 3.05e-4 | 1.84e-4 | 2.20e-4 | 7.43e-5 | 33.8% |
| Emissions (kg) | 9.86e-5 | 1.35e-4 | 1.12e-4 | 1.15e-4 | 1.81e-5 | 15.8% |

### Process-mode results (Observed; n=3, 0 failed, 0 missing)

| Metric | Min | Max | Median | Mean | SD | CV |
|---|---:|---:|---:|---:|---:|---:|
| Workload duration (s) | 36.4 | 83.8 | 45.4 | 55.2 | 25.2 | 45.6% |
| Tracker duration (s) | 39.7 | 87.0 | 48.6 | 58.4 | 25.1 | 43.0% |
| Total energy (kWh) | 3.18e-4 | 7.31e-4 | 4.35e-4 | 4.95e-4 | 2.13e-4 | 43.0% |
| CPU energy (kWh) | 1.82e-4 | 4.18e-4 | 2.65e-4 | 2.88e-4 | 1.20e-4 | 41.5% |
| GPU energy (kWh) | 3.49e-5 | 8.07e-5 | 4.44e-5 | 5.33e-5 | 2.41e-5 | 45.3% |
| RAM energy (kWh) | 1.01e-4 | 2.32e-4 | 1.26e-4 | 1.53e-4 | 6.97e-5 | 45.6% |
| Emissions (kg) | 6.78e-5 | 1.56e-4 | 9.28e-5 | 1.05e-4 | 4.54e-5 | 43.0% |

Pre-run conditions: CPU 21.8–43.7%, 391–408 processes (machine: 25.5–43.7%, 391–408; process: 21.8–33.3%, 391–403).

### Derived per-retrieval ranges

**DERIVED BATCH ALLOCATION — NOT DIRECTLY MEASURED** (batch value ÷ 3,000 completed retrievals; mWh).

| Component | Machine range (mean, CV) | Process range (mean, CV) |
|---|---|---|
| Total | 0.154–0.210 (0.180, 15.8%) | 0.106–0.244 (0.165, 43.0%) |
| CPU | 0.087–0.103 (0.094, 8.6%) | 0.061–0.139 (0.096, 41.5%) |
| GPU | 0.010–0.018 (0.013, 33.3%) | 0.012–0.027 (0.018, 45.3%) |
| RAM | 0.057–0.102 (0.073, 33.8%) | 0.034–0.077 (0.051, 45.6%) |
| Emissions (µg CO2eq) | 32.9–44.8 (38.3) | 22.6–52.0 (35.2) |

### Mode comparison (Derived)

- Total energy: process − machine = −4.4e-5 kWh; ratio of means 0.918; ranges overlap; CV difference +27.3 points.
- CPU ratio 1.03, GPU ratio 1.39, RAM ratio 0.70; all component ranges overlap.
- Workload duration ratio 1.40 (process slower on average); ranges overlap.
- Component coverage: CPU, GPU, RAM, total, and emissions present in 6/6 repetitions; missing-value counts 0 in both modes; no difference in coverage.

### Evidence for or against convergence (Observed/Derived)

- Against: identical work took 30.5–83.8 s across repetitions, and energy tracked duration. Machine CV for total energy was 15.8% (similar to the earlier 18.5% at 1,000 operations); process CV was 43.0%. With n=3 these CVs are imprecise.
- For: machine-mode CPU energy was comparatively stable (CV 8.6%). Total-energy ranges overlapped between modes.
- Workload length: shortest run 30.5 s (about 2 sampling intervals); the 3,000-operation batches spanned roughly 2–5.6 intervals. All exceeded 15 s.
- Interpretation: no convergence is demonstrated for process mode; machine mode is no more convergent than the 1,000-operation batches. Process-mode values being lower on average is not evidence of better attribution, since the ranges overlap and process mode was more variable.

### Warnings and deviations

- No CodeCarbon or Python warnings were captured in any manifest (including no multiple-instance message).
- Deviation: the working tree was not clean at measurement time because the summarizer and test edits were uncommitted. All six manifests record `dirty=true` against commit `99b2bfc`. `measure_local_compute.py` was unchanged, so the measured code path is the committed one. Nothing was committed, as instructed.
- Run order alternated by mode, so system drift is shared but not controlled. The unequal workload durations suggest uncontrolled background or power-state variation.
- RAM remains modeled, so all totals remain partially measured.

### Questions answered

1. Process tracking did not demonstrably improve attribution: energy was lower on average, but ranges overlapped and variability was larger.
2. Batch-derived values did not converge in process mode and only moderately in machine mode (n=3).
3. The 3,000-operation workload was long enough to span at least two sampling intervals in every run.
4. Component coverage did not differ between modes.
5. The shared cache prevented a second `embed_chunks()` call in the deterministic test.

### Unresolved questions

- What causes the 2.7× spread in duration for identical work?
- Does process mode capture only process CPU while GPU and RAM remain system-level? That was not checked here.
- Would more repetitions or controlled background load narrow the ranges?
- What range width is acceptable for disclosure? No threshold was applied.

### Updated suitability matrix

| Intended use | Status | Basis |
|---|---|---|
| Internal cold-start comparisons | Unchanged: suitable with qualifications | Not retested. |
| Internal retrieval-batch comparisons | Promising; machine mode more repeatable than process mode | CV 15.8% vs 43.0%, n=3. |
| Shared-cache design justification | Deterministically verified; energy avoided still not measured | Call count 1 → 1. |
| Per-query user disclosure | Not yet supported | Process-mode attribution unproven; wide ranges. |
| Lifetime retrieval aggregation | Not yet supported | Same. |
| Production frontend integration | Not assessed | No decision made. |

### Human decision required

1. Accept machine-mode batch ranges as an internal diagnostic only.
2. Run a larger or controlled follow-up (more repetitions, a quiesced machine, a clean committed tree).
3. Investigate what process mode attributes per component before any attribution claim.
4. Set an explicit variability criterion for disclosure.
5. Defer disclosure until one of the above is complete.
