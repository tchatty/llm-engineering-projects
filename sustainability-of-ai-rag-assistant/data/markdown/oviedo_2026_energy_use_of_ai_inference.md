# Energy use of AI inference, efficiency pathways, and test-time scaling

Authors: Felipe Oviedo, Fiodar Kazhamiaka, Esha Choukse, Allen Kim, Amy Luers, Melanie Nakagawa, Ricardo Bianchini, Juan M. Lavista Ferres (all Microsoft employees; correspondence: felipe.oviedo@microsoft.com)
Publication Year: 2026 (published online April 22, 2026; issue dated August 19, 2026)
Source: Joule 10, 102430 (Cell Press / Elsevier), open access, CC BY-NC-ND. https://doi.org/10.1016/j.joule.2026.102430. Code: https://github.com/microsoft/aienergy_simulation (Zenodo DOI 10.5281/zenodo.19584023)
Keywords: AI inference energy, energy per query, Wh/query, large language models, test-time scaling, reasoning models, agentic workflows, line-of-sight efficiency, Monte Carlo simulation, H100, PUE, data-center energy demand, rebound effect (keywords derived from content; not stated in the extracted text)

## Executive Summary

Oviedo et al. (2026, Joule) estimate the energy use of large language model (LLM) inference under realistic, large-scale production assumptions, because public per-query estimates differ by more than an order of magnitude and many rest on non-production settings (no batching, no serving engine, small-scale tests). The authors introduce a bottom-up Monte Carlo framework that estimates energy per query from token throughput (TPS), node power, power usage effectiveness (PUE) and token lengths, using NVIDIA H100 8-GPU nodes (10 GPUs for DeepSeek-R1) at FP8 precision with TensorRT-LLM-style continuous batching.

Key results:
- For frontier-scale models (>200B parameters: DeepSeek-R1 671B, Llama 3.1 405B, Llama 3.1 Nemotron Ultra 253B), the median energy for a standard query (300 median output tokens, 500 input tokens) is 0.31 Wh (interquartile range [IQR] 0.16-0.60). This agrees with production-scale measurements and disclosures (e.g., 0.34 Wh for an average ChatGPT query per Sam Altman; 0.24 Wh for a typical Gemini Apps query per Elsworth et al.; ML.ENERGY and Caravaca et al. measurements) and shows that estimates and measurements based on non-production conditions (AI Energy Score, IEA, de Vries) overstate energy by 4-20x.
- Test-time scaling (reasoning/agentic) queries with a median of 5,000 output tokens (15x longer than typical) raise median energy 13x to 3.91 Wh (IQR 2.15-7.05); energy scales roughly linearly with output tokens.
- Line-of-sight efficiency improvements (energy-efficiency interventions already deployed or near production) in three categories - model (1.5-10x), serving platform and workload management (1.5-5x), hardware and data center (1.5-2.5x) - could together cut per-query energy 8-20x (conservative stack about 1.5 x 2 x 2.5-3; optimistic 2 x 2.5 x 4 = 20x). In the traditional regime these reduce the median from 0.31 Wh to as low as 0.08 Wh (model improvements), and a 5,000-token reasoning query could be served at 1-1.5 Wh.
- At data-center scale, serving 1 billion queries/day takes about 0.73 GWh/day (0.7 GWh); with a very conservative 1.5-3x improvement this falls to 0.33 GWh. If 10% of queries are long test-time-scaling queries, demand more than doubles to about 1.7 GWh/day, but with efficiency interventions it is about 0.8 GWh/day. Even 10 billion queries/day (web-search scale) would be about 1.2 TWh/year, about 5.5% of the energy use of large hyperscalers and about 1% of current US data-center electricity.
- The authors draw an analogy to past over-forecasts of internet and data-center energy that ignored efficiency gains.

Limitations include single-node modelling at high utilization, idealized token-length distributions, limited treatment of prefill for long contexts, a TPS plateau assumption for very long generations (likely underestimating energy), and exclusion of image/video diffusion models. The authors caution that efficiency gains do not guarantee lower absolute energy because of the rebound effect (Jevons paradox). Their two conclusions: (1) non-production energy estimates overstate per-query energy by 4-20x, so alarmist claims from narrow benchmarks should be avoided and ranges reflecting workload diversity, utilization and scale should be reported; (2) more and longer inference raises energy use, but efficiency gains (small/distilled models, inference-optimized architectures, intelligent routing, serving and hardware improvements) can plausibly yield 8-20x reductions and limit the increase.

## Highlights and Brief Summary (graphical abstract / "In brief")

- Frontier-scale inference uses 0.31 Wh/query, 4-20x below public estimates.
- Reasoning queries (5,000 output tokens) raise energy use 13x vs. standard queries.
- Model, serving, and hardware gains could reduce per-query energy by 8-20x.
- In brief: the study estimates the energy use of LLM inference under realistic deployment conditions; optimized systems consume sub-watt-hour energy per query, 4-20x lower than widely cited estimates, while long reasoning queries substantially increase energy demand and efficiency improvements could reduce per-query energy use by 8-20x.

## Context and Scale

As AI becomes widely used and new workflows scale token demand, how much energy LLMs consume matters for grid planning, AI development and energy policy. Rapid expansion of AI data-center capacity increases the importance of accurate estimates. Public estimates often overlook how efficiently large-scale inference systems operate and how rapidly efficiency improvements are reducing per-query energy. Under realistic assumptions, optimized frontier-scale inference consumes sub-watt-hour energy per query (median 0.31 Wh, IQR 0.16-0.60), aligning with multiple independent measurements and estimates under production conditions. High-profile public estimates and measurements based on non-production assumptions overstate energy use by 4-20x. Long reasoning and agentic queries are estimated to increase energy consumption by more than an order of magnitude due to increased token generation and reduced serving concurrency. At data-center scale, billions of queries per day translate into substantial electricity demand, and even a modest share of long reasoning queries (for example 10% of daily requests) can more than double total energy consumption. Efficiency improvements in model design, serving systems and hardware could together reduce energy use by 8-20x. This echoes how data centers historically tempered energy demand through efficiency gains during the internet and cloud buildup.

## Summary (abstract)

As AI inference scales to billions of queries, estimates of per-query energy use are increasingly important for capacity planning, efficiency interventions and policy. Many public estimates assume non-production settings, leading to systematic overestimation. The authors introduce a bottom-up framework estimating inference energy from token throughput, node power and overhead under large-scale deployment assumptions. For frontier-scale models (>200B parameters) on H100 nodes, the median energy is 0.31 Wh/query (IQR 0.16-0.60), indicating widely cited estimates are overstated by 4-20x. In test-time scaling scenarios 15x longer than typical queries, the median energy rises 13x to 3.91 Wh (IQR 2.15-7.05). Across models, serving systems and hardware, the authors estimate 8-20x line-of-sight energy reductions. At data-center scale, serving 1 billion queries/day requires 0.7 GWh; if 10% are long queries, demand rises to 1.7 GWh/day; with efficiency interventions it falls to 0.8 GWh/day, mitigating the energy impact of test-time scaling.

## Introduction

### Why per-query energy matters
LLM inference is one of the fastest-growing sources of computing demand, with energy use already approaching that of web search and other mature digital services. Stakeholders want reliable, granular figures (e.g., energy per textual query) as a firm basis for energy projections, for comparing serving approaches, and for relating efficiency considerations to engineering and product trade-offs. Public reports of "energy per query" differ by more than an order of magnitude.

### Two drivers of the discrepancy
1. Measurement boundaries vary: some account only for GPU draw, others include CPUs or application overhead.
2. Many benchmarks fail to capture realistic production conditions such as batching, concurrency and steady-state serving. Model-based estimates are also highly sensitive to assumptions about hardware specifications, parameter counts and token lengths. Direct measurements, although more precise, are often tied to non-production models or small-batch tests, which tend to overestimate energy use relative to large, high-concurrency deployments that handle most AI inference workloads.

### Per-query figures cannot be interpreted in isolation
Energy in inference also depends on how demand scales when billions of queries are served and how interventions at the model, serving software and hardware layers can moderate growth. Recent model-provider disclosures offer a more realistic baseline by measuring large-scale systems but are limited by confidentiality, typically reporting only a single "representative" or "average query", which masks how energy use changes with query-length distributions and model and serving configurations. This matters because test-time scaling (reasoning models) and agentic workflows are increasingly routine, and their long outputs can drive a disproportionate share of aggregate energy demand. Averages without system context are misleading and do not guide where efficiency effort should focus.

### Contributions
A bottom-up estimation approach aligned with production-scale disclosures that adds: (1) a decomposition of the interacting determinants of energy per query - model, serving platform and hardware - to give insight into practical efficiency interventions; and (2) explicit modeling of token-length distributions, showing how long inference increases energy per query.

## Results

### Definition of a query
Throughout, a "query" is the most common definition: a single text prompt-completion event, consisting of a single input sequence and the LLM-generated output sequence produced in response, under steady-state serving conditions.

### Estimated energy per query for various models (Figure 1)
Using the Monte Carlo estimation described in Methods, Figure 1 summarizes energy per query for five dense and mixture-of-experts (MoE) models: DeepSeek-R1 671B, Llama 3.1 405B, Llama 3.1 Nemotron Ultra 253B, Mixtral 8x22B and Llama 3.1 70B.

Figure 1 caption: P5-P95 (5th-95th percentile) energy per query for several LLMs in two regimes, after sampling 10,000 queries (Lout, Pnode and PUE configurations). (A) Standard query, with 300 median output tokens (IQR 129-618). (B) Test-time scaling query, with 5,000 median output tokens (IQR 2,040-9,717). In both cases 500 input tokens are assumed and token throughput is estimated for realistic deployments on an H100 node. Bars represent median and IQR.

In the traditional regime (Figure 1A), the Monte Carlo estimates align with measured energy of production-optimized deployments (Table 1):
- Llama 3.1 405B: estimated median 0.39 Wh per query (IQR 0.19-0.68), consistent with the ML.ENERGY leaderboard (v3.0) median measured energy of 0.21 Wh and with the measurement by Caravaca et al.
- Mixtral 8x22B: estimated median 0.06 Wh/query (IQR 0.03-0.11), close to the ML.ENERGY measurement of 0.11 Wh (v2.0, normalized from BF16 to FP8 as 0.18 Wh / 1.7 = 0.11).
- Across all production-scale measurements compiled in Table 1, reported values fall within the estimated IQR with one exception: a single ML.ENERGY measurement for Llama 3.1 70B reporting 0.04 Wh/query, slightly below the IQR (estimate 0.09 Wh, IQR 0.05-0.17). An independent production measurement for the same model reports 0.05 Wh/query (Caravaca et al.), which falls within the estimated range.
- Most published measurements report GPU-only energy, whereas these estimates intentionally target full-node energy and include PUE, leading to modest and expected offsets when comparing absolute values.

### Table 1: Reported energy per query from prior studies compared with this study's estimates
Reported values are normalized to H100 and FP8 equivalents where possible. Normalization assumes a throughput gain of 1.7x for FP8 quantization vs. BF16/FP16 (the average gain reported by NVIDIA) and a Blackwell normalized throughput gain of 2.8x vs. H100 (NVIDIA MLPerf). The study's baseline for models >200B is 0.31 Wh (IQR 0.16-0.60). (The source table is garbled in extraction; rows below are reconstructed from the text and table layout.)

Traditional regime:

| Source | Type | Model / claim | Reported Wh/query (H100, FP8 equivalent) | Comparable estimate in this study | Comments |
|---|---|---|---|---|---|
| Altman | disclosure (unclear if measured or estimated) | average energy use of a ChatGPT query | 0.34 | >200B baseline 0.31 (IQR 0.16-0.60) | fleetwide measurement; no query length, hardware or model mix provided |
| Elsworth et al. | measurement | "typical Gemini Apps request" | 0.24 | >200B baseline 0.31 (IQR 0.16-0.60) | no query length, hardware or model mix provided |
| You (Epoch AI) | estimate | GPT-4o | 0.30 | >200B baseline 0.31 | heuristic FLOPs-based estimate for 500 output tokens |
| Jegham et al. | estimate | GPT-4o | 0.42 | >200B baseline 0.31 | API user-side throughput for 300 output tokens |
| de Vries | estimate | "average ChatGPT query" | 2.9 | >200B baseline 0.31 | outdated estimate; non-production conditions, no batching, no serving engine |
| ML.ENERGY Benchmark v2.0 | measurement | Mixtral 8x22B | 0.11 | Mixtral 8x22B 0.06 (IQR 0.03-0.11) | median energy per query using BF16 reported as 0.18 Wh; adjusted to FP8: 0.18/1.7 = 0.11; average output tokens 389 |
| ML.ENERGY Benchmark v3.0 | measurement | Llama 3.1 70B | 0.04 | Llama 3.1 70B 0.09 (IQR 0.05-0.17) | median energy per query for 4xH100 using BF16 reported as 0.04 Wh; assumed equivalent to 8xH100 using FP8; average output tokens 361; slightly below estimated IQR |
| Caravaca et al. | measurement | Llama 3.1 70B | 0.05 | Llama 3.1 70B 0.09 (IQR 0.05-0.17) | reported for FP16 as 0.08 Wh/query; approximated to FP8 as 0.08/1.7 = 0.05; 300 output tokens |
| ML.ENERGY Benchmark v3.0 | measurement | Llama 3.1 405B | 0.21 | Llama 3.1 405B 0.39 (IQR 0.19-0.68) | median energy per query using FP8 reported as 0.21 Wh; average output tokens 367 |
| Caravaca et al. | measurement | Llama 3.1 405B | 0.21 | Llama 3.1 405B 0.39 (IQR 0.19-0.68) | reported for FP16 as 0.35 Wh/query; approximated to FP8 as 0.35/1.7 = 0.21; 300 output tokens |
| AI Energy Score | measurement | Llama 3.1 70B | 1.01 | Llama 3.1 70B 0.09 (IQR 0.05-0.17) | adjusted for quantization as 1.72 Wh/1.7 = 1.01; non-production conditions, no batching, no serving engine; outside IQR |
| IEA | estimate | Mixtral 8x22B | 1.25 | Mixtral 8x22B 0.06 (IQR 0.03-0.11) | adjusted for quantization; non-production conditions, no batching, no serving engine; outside IQR |

Test-time scaling regime:

| Source | Type | Model | Reported Wh/query | Comparable estimate in this study | Comments |
|---|---|---|---|---|---|
| ML.ENERGY Benchmark v3.0 | measurement | DeepSeek-V3 | 9.30 | DeepSeek-R1 10.6 (IQR 4.29-21.7) | median energy per query for B200 using FP8; adjusted to H100 as 3.32 Wh x 2.8 = 9.30 (based on NVIDIA); average output tokens 8,968 |
| ML.ENERGY Benchmark v3.0 | measurement | DeepSeek-R1 | 20.9 | DeepSeek-R1 10.6 (IQR 4.29-21.7) | median energy per query for B200 using FP8; adjusted to H100 as 7.45 Wh x 2.8 = 20.9; average output tokens 11,287 |
| IEA | estimate | DeepSeek-R1 | 2.25 | printed in the extracted table as "DeepSeek-R1, 0.63" (traditional regime) | adjusted for quantization; non-production conditions, no batching, no serving engine |

Table 1 note: reported values derived from production-scale measurements or estimates fall largely within the estimated IQR, while reports based on non-production settings fall outside it.

### Reports based on non-production settings overestimate by 4-20x
When in-production deployments are not considered, energy per query is substantially larger. AI Energy Score measured 1.01 Wh/query for Llama 3.1 70B (average of 1.72 Wh across 1,000 queries with FP16, 1.72/1.7 = 1.01 Wh at FP8). Under similar assumptions, the International Energy Agency (IEA) estimated 1.25 Wh/query for Mixtral 8x22B and 2.25 Wh/query for DeepSeek-R1. These later estimates did not consider basic in-production optimization techniques, including batching and inference acceleration, leading to 4-20x overestimation of energy per query. Benchmarking to these numbers or extrapolating them to large-scale inference is not representative of the energy use of major AI products.

### Test-time scaling query energy (Figure 1B)
Per-query energy scales approximately linearly with total output tokens. DeepSeek-R1 consumes 10.6 Wh (IQR 4.29-21.7), consistent with the median ML.ENERGY (v3.0) measurement of 20.9 Wh for an average query of 11,287 output tokens. For slightly shorter queries (8,968 average tokens) with the same backbone as R1 (DeepSeek-V3), the median ML.ENERGY measurement was 9.30 Wh. The energy cost of very long queries can be substantial, but models that maintain high throughput for long queries, such as Mixtral 8x22B, seem to have a scaling advantage at the same number of parameters.

### Baseline for models above 200B parameters
A "baseline" scenario was defined by sampling the estimated energy use of the three models above 200B parameters (DeepSeek-R1 671B, Llama 3.1 405B, Llama 3.1 Nemotron Ultra 253B). The threshold reflects the size of popular frontier-scale models, including open-weight DeepSeek-R1, Llama 3.1 405B and Qwen 3, and is also a reasonable range for proprietary models such as GPT-4o or Claude 3.5 Sonnet. The median energy per query in this baseline is 0.31 Wh (IQR 0.16-0.60) (Figure 2).

This is consistent with recent estimates for a typical chatbot query in a highly optimized deployment:
- 0.3 Wh for a typical GPT-4o query of 500 output tokens (heuristic FLOPs-based estimate for a 200B model, Epoch AI);
- 0.42 Wh for a GPT-4o query with 300 output tokens (based on user-side token throughput, Jegham et al.);
- 0.34 Wh for the "average energy use of a ChatGPT query" disclosed by Sam Altman;
- 0.24 Wh for "the typical Gemini Apps query" (Elsworth et al.).

This is not a standardized comparison, given the diversity of products, models, workloads and measurement approaches, but the range is substantially lower than previous widely reported estimates (de Vries; IEA).

### Comparison with web search
The range is also in the range of the commonly cited 0.3 Wh per web search from a 2009 Google disclosure. The authors emphasize that this search figure is dated and likely overestimates present-day web search energy; to their knowledge, no newer public web search disclosures exist. Web search and LLM inference are fundamentally different workloads, so the comparison is only a coarse historical reference point, not a direct benchmark.

### Why energy per query improved versus the previous generation
Factors: reduced size of new frontier models (shift from Kaplan to Chinchilla scaling laws, leading to smaller models trained with more data), hardware efficiency gains, and model and serving improvements.

### Test-time scaling regime baseline
With 5,000 median output tokens, sampling models over 200B parameters gives a median of 3.91 Wh/query (IQR 2.15-7.05), with over 10 Wh in a significant portion of queries. Even a small portion of test-time scaling queries or token-intensive agentic workflows can have a major impact on total inference energy; the authors see this as a key frontier for energy efficiency.

## Line-of-sight reductions in energy use

### Definition and approach
Line-of-sight improvements are energy-efficiency interventions already deployed or close to production in some serving configurations and credibly expected to be adopted in large-scale inference deployments within the next hardware or model generation. For each category a multiplier (eta, P5-P95 range) is estimated from literature to capture uncertainty (conservative-to-optimistic bounds from reported results, treated as non-additive within each category).

Figure 2 caption: Estimates of baseline and line-of-sight optimized scenarios for LLMs with over 200B parameters, after sampling 10,000 queries (Lout, Pnode and PUE configurations). (A, B) P5-P95 energy per query in two regimes: (A) traditional query, 300 median output tokens (IQR 129-618); (B) test-time scaling query, 5,000 median output tokens (IQR 2,040-9,717). 500 input tokens, realistic H100 node deployments. Each category of improvement is considered independent and non-additive compared with the others. Bars represent median and IQR.

### Category 1: Model (eta = [P5: 1.5, P95: 10])
Algorithm and architecture improvements have been the largest drivers of energy efficiency for inference. Estimated line-of-sight improvement: 1.5-10x for next-generation deployments.

- Model distillation: energy reductions of 5-10x (Elsworth et al.). Distillation yields more FLOP-efficient models and allows larger batch sizes on the same hardware. It has proven useful for reasoning models: smaller models with longer inference can outperform larger non-reasoning models, e.g., a 7B to 70B reasoning model distilled from DeepSeek-R1 showed comparable performance to models three to five times larger, and carefully distilled Qwen 3 reasoning models outperformed larger models. In certain areas, small language models (SLMs) can reduce energy by one to two orders of magnitude for token-intensive tasks such as math, coding or specific agentic workflows, compared with models above 100 billion parameters. Traditional natural language processing techniques can reduce energy by orders of magnitude compared with LLMs in tasks such as text classification.
- Model quantization: already substantial in production; FP8 on H100 delivers 1.4-2.4x TPS over FP16. Emerging low-bit quantization supported in newer hardware can plausibly increase inference TPS by 1.5-3x if model performance holds steady. Technical challenges for running heavily quantized models with large batches must still be addressed.
- Mixture-of-experts (MoE): reduces inference compute compared with equivalent dense models. Optimization approaches include optimized expert parallelism (DeepSpeed-MoE), dynamic gating and load balancing (Tutel), and expert offloading/caching (MoE-Lightning), reporting 1.3-8x inference speedups depending on baseline and workload. Attention operations and architectures have also been optimized (FlashAttention, Multi-Head Latent Attention) for efficient inference and long sequence generation.
- Efficient reasoning models: Llama-Nemotron demonstrated 1.9-4x TPS compared with DeepSeek-R1 using neural architecture search, selective attention removal and feedforward network optimization. Hybrid attention models using linear or sliding attention variations have achieved gains for test-time scaling, e.g., MiniMax-M1 consumes 4x fewer FLOPs generating 100,000 tokens compared with DeepSeek-R1. Adaptive computing and controllable reasoning-length generation can dynamically reduce generated tokens by up to 40% while maintaining good accuracy.

### Category 2: Serving platform and workload management (eta = [1.5, 5])
Optimizing deployments to service-level objectives (SLOs) significantly affects the energy and carbon footprint of inference. Large-scale AI systems also allow efficiency gains through workflow management, e.g., routing models according to query complexity. Estimated improvement: 1.5-5x.

- Adaptive serving based on SLOs demonstrated over 50% reduction in energy consumption (DynamoLLM). Disaggregated serving separates the prefill and decoding stages and optimizes each with different resources, caching or accelerators, giving 1.4-2.3x TPS improvement. Better resource utilization in the decoding stage due to disaggregation is especially impactful in long generation and agentic workflows, with TPS gains of 1.4-4x in distributed settings, especially when combined with dynamic GPU allocation, smart routing and low-latency communication.
- Key-value (KV) cache management and quantization are critical: techniques such as LServe, KVQuant and LMCache enable long context management and long sequence generation with over 2-15x throughput and inference speedup. Speculative decoding has demonstrated 2-3x TPS speedups.
- Automated or user-triggered model routing can greatly affect token throughput and memory and token utilization, and has become popular in next-generation models such as GPT-5. It is particularly useful for reasoning models: models that allow explicit switching of reasoning capabilities can reduce per-query energy by 5x or more because of reduced query length. Smart routing can maintain response performance while reducing per-query energy and cost, e.g., routing with continual learning maintained 97% response quality with 2-4x cost reduction. Dynamic filtering of low-quality reasoning traces, as in DeepConf, demonstrated up to 99.9% accuracy with 5x query-length reduction.

### Category 3: Hardware and data center (eta = [1.5, 2.5])
Hardware and data-center advances remain a foundation of inference speedups.
- NVIDIA Blackwell delivers a substantial improvement in TPS per watt vs. H100/H200. In MLPerf Inference v5.0 running Llama 3.1 405B, a single Blackwell B200 achieved up to 2.8-3.4x higher TPS per GPU than H100. SemiAnalysis notes Blackwell improves TFLOPS per GPU-W by 47%-82% relative to H100 at the same quantization level.
- Custom AI inference chips (ASIC, FPGA) have TPS/W gains of around 5-20x, in part due to better performance in the memory-bound decoding stage, a critical capability for test-time scaling.
- Power management (oversubscription, voltage/frequency scaling, power capping) can allow up to 30% more servers in existing clusters and 20% peak power reduction.
- Data-center cooling optimization: cold-plate and immersion cooling can reduce energy demand by 15%-20% compared with air cooling.
- Taken together, without considering improved quantization or custom hardware, these data points support a TPS per GPU-W increase of 1.5-2.5x.

### Impact of the interventions (Figure 2)
The Monte Carlo simulation is re-run with a category-specific efficiency multiplier eta applied to Equation 1 while other categories stay at baseline, so savings are independent of each other.
- Traditional regime: hardware/data-center improvements and serving/workflow optimization reduce median energy per query from 0.31 Wh to 0.16 Wh and 0.11 Wh respectively (roughly 2x and 3x), while model improvements reduce it to a median of 0.08 Wh (4x), conditional on maintaining competitive model performance.
- Test-time scaling regime: relative reductions are similar and long-tail (P95) energy is reduced. Model and serving optimizations enable intensive test-time scaling - a reasoning query with a median of 5,000 output tokens can be served at 1-1.5 Wh, comparable to much smaller queries without optimization.
- Compounding: if adopted jointly across layers, gains compound multiplicatively. Conservative illustrative stack: about 1.5x from hardware/data-center advances, 2x from serving/workflow optimization, and 2.5-3x from model improvements gives an overall 8-9x reduction (e.g., 1.5 x 2 x 2.5 is about 8x). Representative optimistic stack: 2x hardware, 2.5x serving, 4x model gives 20x (2 x 2.5 x 4 = 20x). This combined range reflects realistic stacking across layers rather than the product of category endpoints, which would overstate gains due to overlap and deployment trade-offs; the magnitude is consistent with reductions reported in large-scale production systems (33x, Elsworth et al.).

## Energy use of a billion queries per day

### Scale and method
The 1 billion queries/day scale aligns with reported usage on leading conversational AI platforms, e.g., ChatGPT at 2.5 billion queries/day as of July 2025; dominant web search platforms handle around 10 billion queries/day. Energy for serving 1 billion queries in the baseline scenario was sampled and aggregated, using a scale factor gamma = 1.31 to account for non-uniform demand, networking and redundancy at rack and data-center level.

Figure 3 caption: Energy required for serving 1 billion queries/day. (A) Traditional regime with median output length 300 tokens (IQR 129-618); baseline (model >200B parameters) compared with a conservative improved scenario with efficiency gains eta = 1.5-3. (B) Traditional regime compared with a mixed scenario with 10% test-time scaling queries with median 5,000 output tokens (IQR 2,040-9,717). Although very long inference has a large effect on energy, the conservative improved scenario with efficiency gains of 1.5-3x moderates energy growth.

### Traditional queries
- Naive baseline: 0.73 GWh/day for 1 billion queries. A very conservative line-of-sight improvement (eta = [1.5, 3]) gives less than half: 0.33 GWh.
- References: a single 30 MW H100 data center operating at constant 80% utilization consumes under 0.6 GWh per day, comparable to the baseline. Using the stated per-search energy (0.3 Wh), 1 billion web searches consume approximately 0.3 GWh.
- Inference can be distributed across geographies and electrical grids, so this is a large but manageable load (in contrast to past claims by Elsworth et al., AI Energy Score and IEA). Even if AI inference scaled to 10 billion queries/day (on par with web search), energy use would be around 1.2 TWh/year, about 5.5% of the current energy use of large hyperscalers such as Microsoft or Google and 1% of current US data-center electricity consumption.
- The greatest strain on power grids from new AI workloads is not inference energy but training loads, the rapid rate of AI adoption and concentrated capacity buildup, which are harder to distribute and optimize (IEA).

### Mixed scenario with 10% test-time scaling queries
- Modeled as 90% traditional and 10% long-inference queries. The 90/10 per-query split approximates the incidence of long inference queries in production; since test-time scaling queries are typically an order of magnitude longer than standard responses, such a mix yields token distributions where test-time scaling accounts for roughly half of total tokens served, consistent with public OpenRouter telemetry for 100 trillion tokens.
- Naive estimate (no improvements): 10% long queries can more than double the daily energy footprint of serving 1 billion queries (about 1.7 GWh/day).
- Optimized scenario with 10% test-time scaling queries: total 0.8 GWh for 1 billion queries, equivalent to the daily energy consumption to power roughly 0.4% of television watching in US households.
- Algorithmic advances may produce the largest efficiencies, but model routing and workflow management show impact even with limited reliance on more complex model optimization. Because cost per token is the dominant driver of AI adoption, efficiency gains in long inference should be expected and actively pursued.

### Historical perspective
Projections of digital infrastructure energy use have repeatedly overestimated demand by ignoring rapid efficiency gains amid multiplicative demand growth. A 1999 forecast warned the internet could consume 50% of the US grid by 2010, but data-center usage peaked around 2%. A 2015 projection estimated data centers would consume 8,000 TWh/year by 2030 (more than 25% of global electricity), whereas updated estimates suggest 600-800 TWh or about 2%. The authors opine that the current AI inference surge appears to repeat this pattern: absolute energy use will grow, but efficiency gains in hardware, software and deployment strategies at scale can moderate the long-term footprint.

## Discussion

### Summary of approach
The bottom-up methodology combines node-level power parameters, utilization factors, PUE distributions and empirically fitted token throughput under realistic serving conditions; estimates align with disclosures from optimized production environments and quantify how optimization techniques and token-length distributions shape overall energy.

### Limitations
1. Single-node inference with relatively high utilization, typical of large-scale production; does not fully capture inter-node orchestration overhead, ramp-up dynamics, correlation between token throughput and power utilization, or network latency.
2. Idealized token-length distribution for traditional and long inference, which may differ across enterprise and consumer deployments. Agentic workflows can be very heterogeneous, with energy dominated by tool calling or multiple parallel calls rather than a single long generation.
3. Limited modeling of prefill costs in long-context queries; in extreme scenarios (e.g., 100 thousand input tokens) prefill energy will be substantially higher. Relevant to agentic coding, multi-document summarization and retrieval workflows; in practice context management, tool use (e.g., grep for code search), disaggregated prefill and conversation/KV caching significantly reduce this effect.
4. The TPS model is an interpolation within the decoding-dominant regime, assuming a plateau of token throughput for very long generations, even though real systems often show decline; this likely underestimates energy in such cases.
5. Analysis covers autoregressive text generation only, not diffusion-based image or video generation, which have different serving constraints and higher energy utilization.

### Rebound effect
Efficiency gains do not guarantee lower absolute energy use. Lower energy per query, lower cost per token, or increases in model size can enable higher usage, longer generations and more token-intensive workflows. This "rebound effect" (Jevons paradox) can increase total inference energy even as systems become more efficient; system-level outcomes depend jointly on efficiency and demand dynamics and should be evaluated together in future studies. Many tasks do not require the most energy-intensive models, since performance often shows diminishing returns beyond a certain model size or amount of test-time compute, motivating right-sizing via routing and specialization.

### Two central conclusions
1. Non-production energy use per query is overestimated. Estimates or measurements based on small-scale or non-optimized deployments overestimate inference energy by 4-20x. Policymakers and stakeholders should avoid alarmist claims drawn from narrow benchmarks; disclosures and estimates should emphasize ranges reflecting workload and serving diversity, utilization and deployment scale. Comparisons must use a systems approach in the context of products, rather than comparing isolated models.
2. More and longer inference increases energy use, but efficiency gains can limit the increase. Rapid AI adoption, test-time scaling and agentic workflows substantially raise inference energy use, but the impact can be managed. The largest efficiency gains are expected from algorithmic advances - particularly small/distilled LLMs and inference-optimized architectures - and from intelligent model routing that prevents unnecessary use of large models. Hardware improvements and serving optimization also contribute meaningfully. Together these levers can plausibly yield 8-20x line-of-sight reductions. Realizing these per-query efficiencies promptly, along with managing demand and usage dynamics, will be critical to moderating the energy impact of AI inference as it scales.

## Methods

### Framework overview
The study focuses on at-scale deployments where nodes are saturated through batching, high concurrency and optimized serving. LLM inference has two stages: prefill, where the input sequence is processed once in parallel; and decoding, where output tokens are generated step by step. Because decoding cannot be parallelized across tokens, it often dominates energy use in most real-world workloads - a trend amplified in reasoning and agentic workflows or when multiple sequences are generated per request (best-of-n sampling). The estimation framework is a bottom-up Monte Carlo simulation for various open-source models.

### Equation 1
For a fixed GPU node, per-query energy E_query (Wh/query) is:

E_query = PUE x P_node x L_eff / (3.6 x TPS(L_in, L_out)) x (1/eta)   (Equation 1)

(The extracted equation layout is garbled; this form is reconstructed from the term definitions below.)

### Parameters
- P_node: steady-state power draw per GPU node during inference (kW). Models are assumed hosted on 8xH100 GPUs at FP8 precision, as in the NVIDIA DGX H100 architecture, or 10xH100 for DeepSeek-R1, with maximum power draw P_max of 10.2 or 12.5 kW (linearly scaled), respectively. For highly utilized nodes, average power utilization has been reported around 70% during inference. P_node is modeled as a log-normal distribution centered at 0.7 P_max with a P5-P95 range of 0.4 P_max - 0.9 P_max. The aggregated effect of idle nodes and overhead is explored separately.
- PUE: power usage effectiveness of the AI data center, a log-normal distribution with P5-P95 range 1.05-1.40, consistent with hyperscaler public reports.
- 3.6: constant converting kW to Wh.
- eta: efficiency factor, defined by a log-normal distribution, capturing potential energy-efficiency gains per query; eta = 1 for all baseline computations and estimated from literature for the various scenarios.
- L_in, L_out: input and output tokens. Discrete values are chosen for L_in and L_out is sampled from an exponential distribution. Two regimes: (1) traditional, common in conversational queries with no intensive test-time scaling, median L_out = 300 tokens (IQR 129-618); (2) test-time scaling, long queries common in reasoning models such as OpenAI o3 or DeepSeek-R1 or long agentic workflows, median L_out = 5,000 (IQR 2,040-9,717).
- L_eff: effective token length, scales the energy by the number of tokens in the query. Because output tokens dominate energy, L_eff is approximated as L_out and L_in is fixed at 500 in the main analysis. Note S3 explores additional L_in and L_eff configurations.
- Agentic workflows: a query is a single prompt-completion event, but multi-step and agentic workflows can be modeled as multiple queries per user request, with total energy approximated by total output tokens across the steps (additional orchestration, tool calling and long-context management overhead is out of scope).
- TPS: token throughput per second, which varies with model architecture, deployment configuration, concurrency and latency constraints. For steady-state deployment, existing benchmark data for H100 with NVIDIA's TensorRT-LLM, parallelism of 8 (10 for DeepSeek-R1) and continuous batching are used. As presented in Note S1, TPS for the five models (DeepSeek-R1 671B, Llama 3.1 405B, Llama 3.1 Nemotron Ultra 253B, Mixtral 8x22B, Llama 3.1 70B) was measured for multiple (L_in, L_out) configurations, approximating a fully saturated node with high concurrency. TPS(L_in, L_out) is a piecewise log-linear regression model trained on this curated data (Note S2), using benchmark data up to 4,000 output tokens. For longer outputs TPS is held at the plateau rather than modeling the gradual decline from growing KV and attention overhead - a simplification that likely underestimates energy for very long generation but provides a conservative baseline. Although TPS and P_node are correlated, TPS is treated as independent of P_node in the main analysis; a linear dependency explored in Note S4 gives similar results.

### Sampling and baseline
E_query is estimated by sampling 10,000 random configurations of L_out, P_node and PUE and computing the corresponding TPS for a given model. The baseline approximates a large LLM deployment with the most common production optimization techniques in modern serving frameworks, including dynamic batching, KV cache and other common optimizations in inference engines such as vLLM or TensorRT-LLM.

### Line-of-sight scenarios
Many hardware-, model- and serving-level optimizations are increasingly being adopted (e.g., prefill/generation disaggregation, improved quantization). For these, the most imminent improvements and expected gains in throughput or energy per token are compiled from literature. Equation 1 is modified with a multiplier eta that scales up token throughput (TPS) or scales energy per query (1/eta). For a fixed node, eta is a log-normal distribution with P5-P95 ranges estimated from literature to capture the uncertainty of each optimization's impact.

### Aggregating to total deployment energy
Energy for serving millions of queries in the baseline scenario is sampled and summed. Because the estimate is at node level, the total is scaled by gamma = 1.31, accounting for non-uniform demand during the day, node redundancy and networking (Note S5).

## Resource Availability and Declarations
- Lead contact: Felipe Oviedo. Materials availability: non-applicable.
- Data and code: analysis scripts on Zenodo and GitHub (microsoft/aienergy_simulation); all data used are in the public domain.
- Declaration of interests: all authors are Microsoft employees; all analyses are based on open-source models and publicly disclosed algorithms and performance metrics.
- Generative AI statement: the first author used ChatGPT for research and manuscript preparation; the authors reviewed and edited the content.
- Dates: received November 5, 2025; revised January 29, 2026; accepted March 25, 2026; published April 22, 2026. Supplemental Notes S1-S5 (TPS data, regression model, L_in/L_eff configurations, TPS-power dependency, scale factor) are online and not reproduced in the main text.
