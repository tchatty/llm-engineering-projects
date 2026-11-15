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
