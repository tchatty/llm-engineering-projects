# Power Hungry Processing: Watts Driving the Cost of AI Deployment?

Authors: Alexandra Sasha Luccioni (Hugging Face), Yacine Jernite (Hugging Face), Emma Strubell (Carnegie Mellon University, Allen Institute for AI)
Publication Year: 2024 (ACM FAccT '24, June 3-6, 2024, Rio de Janeiro, Brazil; Corrected Version of Record V.1.1, published November 6, 2024)
Source: ACM Conference on Fairness, Accountability, and Transparency (FAccT '24), https://doi.org/10.1145/3630106.3658542
Keywords: AI inference energy, carbon emissions, generative AI, multi-purpose models, task-specific models, deployment cost, LLM, energy efficiency, Code Carbon, training vs inference, BLOOMz, Flan-T5, image generation, transparency

## Executive Summary

Luccioni, Jernite and Strubell present what they describe as the first systematic comparison of the ongoing inference (deployment) cost of different categories of machine learning systems, covering both task-specific models (fine-tuned for a single task) and multi-purpose ("general-purpose") generative models. Most prior work on the environmental impact of ML focused on training, yet inference happens far more often (billions of times a day for popular products) and is estimated to be 80-90% of ML cloud computing demand according to AWS, about 60% of ML energy use at Google (2022), and about one-third of Meta's ML carbon footprint (2021).

The authors measured the energy and carbon needed for 1,000 inferences using Code Carbon on an AWS node with NVIDIA A100 GPUs (us-west-2, carbon intensity 297.6 g CO2eq/kWh). They studied 88 models (80 task-specific, 8 multi-purpose: Flan-T5 base/large/xl/xxl and BLOOMz-560M/1B/3B/7B) across 10 tasks and 30 datasets spanning text and images. The whole study consumed 754.66 kWh and emitted 178.97 kg CO2eq.

Key findings: (1) Generative tasks (text generation, summarization, image captioning, image generation) are far more energy- and carbon-intensive than discriminative ones (classification, extractive QA, masked language modeling). Mean energy per 1,000 inferences ranged from 0.002 kWh (text classification) to 2.9 kWh (image generation), a factor of over 1,450; the least efficient image generation model used 11.49 kWh, equal to 522 smartphone charges. (2) Image-based tasks are more energy-intensive than text-based ones; image generation uses over 60 times more energy than text generation on average. (3) Task structure explains more of the variation in emissions than model size. The most carbon-intensive image model (stable-diffusion-xl-base-1.0) emits 1,594 g CO2eq per 1,000 inferences, roughly 4.1 miles driven by a gasoline car. (4) Multi-purpose generative models are orders of magnitude more expensive than task-specific models for discriminative tasks (for example 0.3 g vs 10 g for SciQ extractive QA per 1,000 inferences), and the gap narrows for summarization (4-10 g task-specific vs 20-30 g multi-purpose), mostly due to model size. (5) Decoder-only models (BLOOMz) emit more than sequence-to-sequence models (Flan-T5) of similar size, especially for long outputs. (6) Using BLOOMz as a case study, inference energy reaches parity with training plus fine-tuning energy after roughly 204 million (BLOOMz-560M) to 592 million (BLOOMz-7B) inferences, a number that can be reached within weeks or months for widely used services.

The authors conclude that the trend toward deploying multi-purpose generative systems for well-defined tasks (such as web search) is not supported by convincing evidence of necessity given its energy and emissions costs, urge that utility be weighed against environmental cost, and call for transparency from model developers about architecture, parameters, training and deployment impacts. Limitations: results are a set of initial data points, not representative of all deployment contexts, hardware, precision or optimization choices.

## Abstract

Recent years have seen a surge in the popularity of commercial AI products based on generative, multi-purpose AI systems promising a unified approach to building machine learning (ML) models into technology. However, this ambition of "generality" comes at a steep cost to the environment, given the amount of energy these systems require and the amount of carbon that they emit. In this work, the authors propose the first systematic comparison of the ongoing inference cost of various categories of ML systems, covering both task-specific (i.e. finetuned models that carry out a single task) and "general-purpose" models (i.e. those trained for multiple tasks). They measure deployment cost as the amount of energy and carbon required to perform 1,000 inferences on a representative benchmark dataset using these models. They find that multi-purpose, generative architectures are orders of magnitude more expensive than task-specific systems for a variety of tasks, even when controlling for the number of model parameters. They conclude with a discussion around the current trend of deploying multi-purpose generative ML systems, and caution that their utility should be more intentionally weighed against increased costs in terms of energy and emissions. All the data from the study can be accessed via an interactive demo for further exploration and analysis.

CCS concepts: Computing methodologies (Machine learning; Neural networks); Hardware (Impact on the environment; Power estimation and optimization).

**Figure 1 (caption):** The tasks examined in the study and the average quantity of carbon emissions they produced (in g of CO2eq) for 1,000 queries. The y axis is in logarithmic scale.

## 1 Introduction

### Context: environmental impact of ICT and data centres
Understanding the environmental impacts of different industries is an important first step towards developing effective strategies to mitigate those impacts. For newer industries such as information and communication technologies (ICT), of which AI and ML are considered a part, more work is needed to understand the extent of their environmental impacts and the factors that influence it. Between 2017 and 2021, the electricity used by Meta, Amazon, Microsoft, and Google, the main providers of commercially-available cloud compute, more than doubled. According to the most recent figures available, global data centre electricity consumption has grown by 20-40% annually in recent years, reaching 1-1.3% of global electricity demand and contributing 1% of energy-related greenhouse gas emissions in 2022. However, the contribution of the AI sector specifically towards these figures is unclear.

### Training versus inference
Recent work documenting the environmental impacts of ML has focused largely on quantifying the operational energy and carbon required for the training phase of the ML model life cycle, due to the relative ease of measuring per-model energy use for that phase and the impressive quantity of energy required for a single training run. Yet other phases of the life cycle, such as inference, stand to impact the environment just as much, or more, than training due to the computational resources required to deploy modern models at scale. While inference on a single example requires much less computation than training the same model, inference happens far more frequently, as many as billions of times a day for a model powering a popular user-facing product such as Google Translate. (Footnote: Google reported translating more than 100 billion words per day in 2016; assuming an average query length of 100 words yields an estimate of 1 billion queries to the model per day.) In-depth work quantifying the costs of model inference and deployment is limited, and its environmental impacts, in terms of energy and carbon as well as water and mining of rare earth minerals, have yet to be estimated.

Reported shares of inference in ML compute and emissions:
- AWS, the largest global cloud provider: inference is estimated to make up 80 to 90% of total ML cloud computing demand.
- Meta (2021 publication): approximately one-third of its internal end-to-end ML carbon footprint attributed to model inference, with the remainder from data management, storage, and training.
- Google (2022 study): 60% of its ML energy use attributed to inference, compared to 40% for training.

Looking at inference rather than training leads to drastically different conclusions when considering the multi-purpose ("general-purpose") aspect specifically. Training a single model for multiple tasks can be more energy-efficient when considering training costs only, but these gains can easily be lost and even reversed over the course of the model's lifetime, given how much inference is carried out when these models are deployed in user-facing applications like chat and web search.

### Scope and contribution of this study
The authors measure the energy required to deploy various ML models and architectures, including large language models (LLMs); to their knowledge, the study is the first to focus solely on the inference phase of the ML model life cycle. They study 88 models across 10 tasks and 30 datasets, spanning natural language and computer vision, analyzing the impact of end task, modality, model size, architecture, and learning paradigm (task-specific or multi-task/multi-purpose) on energy efficiency. They identify orders-of-magnitude differences in the energy required per inference across models, modalities and tasks, and highlight a trade-off between the benefit of multi-purpose systems, their energy cost, and ensuing carbon emissions. The aim is to help practitioners understand accuracy-efficiency trade-offs across tasks and models, and to enable better estimates, projections and policy decisions at the sector level.

## 2 Previous Work

### Estimating energy and emissions of ML
Estimating the energy and emissions of ML models remains relatively under-explored, though it has gathered traction since Strubell et al.'s 2019 article quantifying energy and carbon emissions of then-large NLP models. Most studies since then have focused on the training phase, including Patterson et al. (2021, 2022), who compared models and analyzed factors influencing emissions. Studies of specific architectures, e.g. BLOOM and Nour, carried out in-depth analyses of the different steps in the models' life cycle and their relative contribution to carbon emissions. Given increasing deployment of ML in the cloud, several studies have looked at cloud-specific ways to reduce emissions, such as delayed scheduling, workload elasticity, and choosing the least carbon-intensive electricity available (Chien et al., Dodge et al., Hanafy et al.).

### Lack of standardized methodology and embodied emissions
There is currently no standardized methodology for quantifying and comparing the energy consumption and carbon emissions of ML models. Tools such as Code Carbon, MLCO2 and LLMCarbon adopt different approaches and output different results, making it difficult to systematically compare carbon footprints. Existing tools and studies have largely focused on dynamic power consumption (the electricity necessary for powering hardware) and resulting emissions. There have been proposals to also account for embodied emissions (emissions attributable to manufacturing computing equipment), impeded by lack of transparency from designers of hardware such as GPUs; recent estimates show that the embodied carbon footprint of an LLM trained and deployed on Meta's compute cluster constitutes up to 50% of its carbon footprint.

### Inference studies
While most work has focused on training because it is more tractable (usually carried out over a set period on a specific compute instance), model inference has started to become the subject of scholarship. Luccioni et al.'s study of BLOOM was the first to look at the specific energy costs of deploying an LLM and found that, over time, this can represent a significant portion of a model's overall carbon footprint. The current study pursues this line of work, testing a variety of architectures on different tasks and datasets to understand the degree of variance and how seemingly small user choices can result in large differences in a model's environmental impact.

## 3 Methodology

The study focuses on the inference (deployment) stage of the model life cycle.

### 3.1 Task and dataset selection
Ten ML tasks were chosen from 5 modalities:
- Text-to-category: text classification, token classification, extractive question answering
- Text-to-text: masked language modeling, text generation, summarization
- Image-to-category: image classification, object detection
- Image-to-text: image captioning
- Text-to-image: image generation

These tasks are common in both NLP and computer vision and include several multimodal tasks (image captioning and image generation). For each task, the three most downloaded datasets from the Hugging Face Hub were chosen.

**Table 1: Tasks and datasets used in the study**

| Task | Datasets |
|---|---|
| image classification | CIFAR 10, CIFAR 100, ImageNet 1K |
| image captioning | Visual Genome, RedCaps, COCO |
| image generation | DiffusionDB, ImageReward, SD Prompts |
| masked language modeling | BookCorpus, C4, OSCAR |
| object detection | Visual Genome, CPPE-5, COCO |
| question answering | SQuAD, SQuAD v2, SciQ |
| summarization | SAMSum, CNN-Daily Mail, XSum |
| text classification | IMDB, Rotten Tomatoes, SST 2 |
| text generation | WikiText, BookCorpus, OSCAR |
| token classification | ReCoRD, WikiANN, CoNLL 2003 |

### 3.2 Models
To represent a broad diversity of deployment use cases, 88 models were sampled: some trained or fine-tuned for the selected tasks, others designed as zero-shot or multi-task models, allowing comparisons across architectures on a given task and across tasks for the same architecture.

**Task-specific models.** For each task, the 8 most popular models on the Hugging Face Hub (by downloads) were selected (80 models in total; full identifiers in Table 6, reproduced in Appendix A). Some models were discarded, e.g. if trained on another language or fine-tuned for a task incompatible with the selected datasets. For each model, 1,000 inferences were run for each of the 3 datasets for its task, using the Transformers library. Each set of inferences was run 10 times to ensure statistical significance. Inferences were run sequentially, without batching, to reflect the variability of model deployment in situ, which can make batching of inputs difficult.

**Multi-purpose models.** 8 multi-purpose models, trained to perform well in various application settings, were also selected: 4 sequence-to-sequence models from the Flan-T5 family (base, large, xl, xxl) and 4 decoder-only models from the BLOOMz family (BLOOMz-560M, BLOOMz-1B, BLOOMz-3B, BLOOMz-7B). They were tested on a subset of tasks: question answering, text classification and summarization, chosen because models were available that could carry them out with a unified architecture (not possible for all tasks, especially multimodal ones). The 8 models were prompted in a zero-shot setting constant across models, e.g. "Summarize the following text: [text]. Summary:", on the same 1,000 samples as the fine-tuned models, repeating each experiment ten times.

### 3.3 Hardware, measurement and carbon intensity
- All experiments ran on a node of 8 NVIDIA A100-SXM4-80GB GPUs hosted on Amazon Web Services.
- The Code Carbon package measured both energy consumed and carbon emitted during inference. Although experiments ran on a single GPU, the idle power usage of the other 7 GPUs is also reflected in the reported numbers.
- All experiments ran in one compute region (AWS us-west-2, Oregon), with an average carbon intensity of 297.6 grams of CO2eq per kWh, so energy and carbon are correlated; the paper plots one or the other depending on the point discussed.
- Energy consumed on A100 GPUs will remain similar in other regions, but carbon emissions vary with the regional energy source, hence reporting both energy and carbon separately for comparisons across regions and hardware.
- Carbon intensity is measured in CO2eq (not CO2) because the different greenhouse gases produced during electricity generation are reduced to a common denominator, carbon dioxide.
- Code and Code Carbon logs (with a breakdown by hardware component: GPU, CPU and RAM) are provided in the authors' GitHub repository.
- Total for all experimentation and evaluation: 754.66 kWh of energy and 178.97 kg CO2eq emitted.

## 4 Results

Section 4.1 analyzes energy and carbon per task for task-specific models; Section 4.2 examines multi-purpose (zero-shot) models, variation by size and architecture and the difference from task-specific models; Section 4.3 compares training and inference costs and computes parity.

### 4.1 Task-specific model analysis

#### Energy per task (Table 2)
Classification tasks for both images and text are at the low end (between 0.002 and 0.007 kWh for 1,000 inferences). Generative tasks such as text generation and summarization use on average over 10 times more energy for the same number of inferences (around 0.05 kWh per 1,000). Multimodal tasks such as image captioning and image generation are at the highest end (0.06-2.9 kWh per 1,000 inferences). Text-based tasks are in general more energy-efficient than image-based ones: image classification requires less energy (median 0.0068 kWh per 1,000 inferences) than image generation (1.35 kWh), and text generation (0.042 kWh) requires more than text classification (0.0023 kWh).

**Table 2: Mean and standard deviation of inference energy (kWh) per 1,000 queries, by task**

| Task | Mean (kWh) | Std (kWh) |
|---|---|---|
| text classification | 0.002 | 0.001 |
| extractive QA | 0.003 | 0.001 |
| masked language modeling | 0.003 | 0.001 |
| token classification | 0.004 | 0.002 |
| image classification | 0.007 | 0.001 |
| object detection | 0.038 | 0.02 |
| text generation | 0.047 | 0.03 |
| summarization | 0.049 | 0.01 |
| image captioning | 0.063 | 0.02 |
| image generation | 2.907 | 3.31 |

#### Smartphone charge comparison
Charging the average smartphone requires 0.022 kWh (EPA figure; before January 2024 the EPA estimated 0.012 kWh, used in an earlier version of the study). The most efficient text generation model uses as much energy as 9% of a full smartphone charge for 1,000 inferences, whereas the least efficient image generation model uses 11.49 kWh, as much as 522 smartphone charges, or around half a charge per image generation. There is also large variation between image generation models, depending on the size of the image generated.

#### Variation between tasks
Energy ranges from the least energy-intensive task, text classification (mean 0.002 kWh per 1,000 inferences), to the most energy-intensive, image generation (mean 2.9 kWh): the models examined vary by a factor of over 1450 in energy required for the same number of inferences. This is coherent with the decision space of each model type: from a binary classification task such as sentiment analysis (output 0 or 1) to an entire vocabulary for text generation and summarization models. Output length also matters: on average, text generation uses 15 times more energy than masked language modeling, because masked language modeling generates a single token, whereas in the setup the text generation task generates 10 new tokens per input, with input length growing as each sequence is fed back into the model. For image-based tasks, the level of abstraction is lower and the decision space larger, since models generate raw pixels rather than tokens: image classification uses over 3 times more energy than text classification (0.007 vs. 0.002 kWh) and image generation uses on average over 60 times more energy than text generation (0.047 vs. 2.9 kWh).

#### Model size versus task structure (Figure 2)
Figure 2 plots, for the 5 modalities, model emissions (g CO2eq per 1,000 inferences, log scale) against parameters (log scale). There is a relationship between model size and emissions during inference, with differing progressions per modality, but task structure accounts for more of the variation than model size does. Text-to-image is by far the most carbon- and energy-intensive: smaller image generation models such as segmind/tiny-sd (around 500M parameters) produce orders of magnitude more carbon than text-to-category models (100 g vs. 0.6 g CO2eq per 1,000 inferences). Within text-to-text tasks there are two sets of models: masked language modeling follows a lower trend, with emissions akin to text-to-category models, while text generation and summarization produce similar amounts of carbon to image captioning models with a similar number of parameters.

#### Carbon comparisons
The most carbon-intensive image generation model (stable-diffusion-xl-base-1.0) generates 1,594 g CO2eq per 1,000 inferences, roughly equivalent to 4.1 miles driven by an average gasoline-powered passenger vehicle. The least carbon-intensive text generation model (distilbert-base-uncased, as named in the paper) generates as much carbon as 0.0006 miles driven by a similar vehicle, i.e. 6,833 times less. This adds up quickly when image generation models such as DALL-E and MidJourney are deployed in user-facing applications used by millions of users.

#### Takeaway
Even for models trained for a single task, there is large variation within each task and an even larger one between tasks from different modalities. Tasks mapping image and text inputs to categorical outputs are less energy- and carbon-intensive than those that generate text or images. Such variation, sometimes several orders of magnitude, is important for policies seeking to mitigate environmental impacts of AI.

### 4.2 The environmental cost of multi-purpose systems

Multi-task models of two types were examined: decoder-only (BLOOMz family) and sequence-to-sequence (Flan-T5 family), comparing energy intensity and carbon emissions across parameter counts and tasks. A subset of 3 tasks (text classification, extractive question answering, summarization) was used, given their diversity and broad applicability, comparing the 8 zero-shot models on the same 3 datasets per task as in Table 1.

#### 4.2.1 Emissions of task-specific and multi-task architectures
Figure 3 plots mean per-query emissions per model for each dataset (log y axis; dot size proportional to model size; task-specific discriminative models in blue, multi-purpose sequence-to-sequence in yellow, decoder-only generative in green).

**Discriminative tasks (sentiment analysis on SST 2, Rotten Tomatoes, IMDB; question answering on SciQ, SQuAD, SQuAD v2):** task-specific discriminative models emit clearly less than both multi-purpose sequence-to-sequence and decoder-only generative models, by several orders of magnitude on the log scale. The most efficient task-specific models emit 0.3 g CO2eq per 1,000 inferences for extractive QA on a dataset like SciQ, while multi-purpose models emit 10 g for the same task. This follows from model structure: a task-specific model trained on binary text classification applies a softmax over a two-category vector, while a multi-purpose model generates "positive" or "negative", which requires more energy because the prediction is based on the model's entire vocabulary.

**Generative task (summarization on SAMSum, XSum, CNN-Daily Mail):** task-specific and multi-purpose models are closer: task-specific sequence-to-sequence models generate 4-10 g CO2eq per 1,000 inferences while multi-purpose models emit 20-30 g. The difference appears to come mostly from model size: all task-specific summarization models were at most 600 million parameters, compared to larger multi-purpose architectures up to 11 billion parameters.

#### Performance evaluation (comparability)
Task-specific models were evaluated with the Hugging Face evaluate library and zero-shot models with the LM Evaluation Harness. Comparing task-specific and multi-purpose models with the same metrics is fundamentally hard: task-specific models have a much more constrained decision space (e.g. two classes for binary text classification), whereas multi-purpose models have a large output vocabulary and depend on the prompt schema and prompting strategy. Using two standardized packages and a stable prompting approach across zero-shot models standardizes evaluation as far as possible.

Figure 4 (text classification): model size (x, log), accuracy (y), dot size = emissions (log). Among task-specific encoder models, accuracy varies widely: several smaller models of similar size and comparably small emissions have widely varying accuracy. Multi-purpose models vary less in accuracy and have higher average accuracy overall. Both sequence-to-sequence and decoder-only multi-purpose models produce comparable emissions, several orders of magnitude more than task-specific models. Mid-size multi-purpose models (around 3B parameters) may have slightly better accuracy than larger and smaller ones, but given the caveats in multi-purpose LLM evaluation this difference may not be significant. Full results for the other 2 tasks are in Appendix B (Table 7, Figures 7 and 8).

#### 4.2.2 Differences within multi-purpose architectures
Within each family (decoder-only and sequence-to-sequence), size and emissions are correlated: smaller models emit less carbon and use less energy (Table 3). However, sequence-to-sequence models are more efficient than decoder-only models of the same size: Flan-T5-XL and BLOOMz-3B are both around 3B parameters, but Flan-T5-XL generates on average 2 grams less CO2eq per 1,000 inferences. Flan-T5-XXL, the biggest multi-purpose model tested (11 billion parameters), has lower emissions (11.48 g on average) than the smaller BLOOMz-7B.

**Table 3: Zero-shot models, average emissions and energy per 1,000 inferences**

| Architecture | Model | Parameters | Emissions (g CO2eq) | Energy (kWh) |
|---|---|---|---|---|
| seq2seq | Flan-T5-base | 222M | 3.67 | 0.026 |
| seq2seq | Flan-T5-large | 750M | 7.68 | 0.055 |
| seq2seq | Flan-T5-xl | 2.8B | 8.08 | 0.058 |
| seq2seq | Flan-T5-xxl | 11B | 11.48 | 0.083 |
| decoder-only | BLOOMz-560M | 559M | 7.5 | 0.054 |
| decoder-only | BLOOMz-1B | 1.7B | 8.66 | 0.062 |
| decoder-only | BLOOMz-3B | 3B | 10.17 | 0.073 |
| decoder-only | BLOOMz-7B | 7B | 14.46 | 0.104 |

Per task (Figure 5): text classification is less carbon-intensive than question answering, and summarization is the most intensive of the three, the same pattern as for task-specific models. The spread between tasks is smaller for sequence-to-sequence models (dots in Figure 5) than for decoder-only models (crosses), where differences between tasks are more significant.

#### Output length and architecture
For summarization, decoder models generate more emissions than sequence-to-sequence models of similar size, while for question answering and text classification the two architectures have similar emissions. The authors explain this by the attention mechanism: sequence-to-sequence models only attend to the last layer of the input when producing answers, while decoder-only architectures attend to all layers for the full sequence, creating a stronger dependency of the number of operations on output length, hence more emissions for tasks with longer outputs.

Table 4 and Figure 6 verify this: tasks with longer outputs result in more emissions, especially for decoder-only models. Figure 6 (summarization; symbol = architecture, symbol size = model size, color = input length) shows a clear correlation between output length and emissions, with a higher slope for decoder-only (BLOOMz) than sequence-to-sequence (Flan-T5) models. There is no "one-size-fits-all" pattern for multi-purpose models either: they vary in emissions and energy by model size and output length, so careful consideration is needed when choosing models for tasks and scenarios.

**Table 4: Average input and output length (number of tokens) for the 8 zero-shot models and 9 datasets** (darker cell in the original = more carbon)

| Dataset | Avg input | BLOOMz 560M out | BLOOMz 1B out | BLOOMz 3B out | BLOOMz 7B out | Flan-T5 base out | Flan-T5 large out | Flan-T5 xl out | Flan-T5 xxl out |
|---|---|---|---|---|---|---|---|---|---|
| IMDB | 58.73 | 1.64 | 2.61 | 1.72 | 1.53 | 1.00 | 1.00 | 1.00 | 1.00 |
| Rotten Tomatoes | 30.08 | 1.00 | 0.99 | 1.03 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| SST 2 | 28.35 | 0.98 | 0.99 | 1.01 | 1.02 | 1.00 | 1.00 | 1.00 | 1.00 |
| SciQ | 113.12 | 1.28 | 1.25 | 1.10 | 1.10 | 2.03 | 5.41 | 3.12 | 2.42 |
| SQuAD | 134.00 | 1.93 | 1.96 | 2.02 | 1.95 | 2.01 | 2.15 | 2.16 | 2.13 |
| SQuAD 2 | 115.85 | 2.33 | 2.54 | 2.58 | 2.41 | 2.28 | 2.74 | 2.71 | 2.58 |
| CNN | 54.00 | 12.05 | 11.91 | 11.73 | 10.34 | 8.52 | 11.34 | 11.34 | 10.68 |
| SamSUM | 47.82 | 9.54 | 9.41 | 9.75 | 9.85 | 10.56 | 11.05 | 10.18 | 10.57 |
| XSum | 53.85 | 11.53 | 12.22 | 11.94 | 11.92 | 12.95 | 13.62 | 13.49 | 13.09 |

### 4.3 Comparing model training and inference costs

#### Motivation and data availability
An important trade-off for practitioners and policy-makers is when model inference costs reach parity with training (and fine-tuning) costs, i.e. when deployment uses as much energy as initial training. This is hard to determine because it requires total energy cost of all life-cycle steps, which is rarely available. Neither the BLOOMz nor the Flan-T5 papers report total training energy or carbon. However, BLOOMz models are fine-tuned versions of the original BLOOM models, so the authors used the logs from the BLOOM carbon footprint paper (Luccioni et al.) for training energy, and added fine-tuning energy estimated from the BLOOMz paper's training logs (carbon footprint of fine-tuning could not be inferred). Footnote: the fine-tuning energy consumption can be based on the Thermal Design Power (TDP) of the GPUs used; while it assumes 100% GPU utilization, it is the most accurate estimate possible without energy tracking during training.

#### Results (Table 5)
Energy per inference (per single query, in kWh) varies from 5.4 x 10^-5 for the smallest model, BLOOMz-560M, to 1.0 x 10^-4 kWh for the biggest, BLOOMz-7B. This is coherent with the figure reported for BLOOM-176B, which required on average 0.004 kWh per query, 40 times more than BLOOMz-7B while being roughly 25 times bigger (although that figure included API deployment of the model, which is not the case in this study).

**Table 5: BLOOMz training, fine-tuning and inference energy, and cost parity**

| Model | Training energy (kWh) | Finetuning energy (kWh) | Inference energy (kWh) | Cost parity (# inferences) |
|---|---|---|---|---|
| BLOOMz-7B | 51,686 | 7,571 | 1.0 x 10^-4 | 592,570,000 |
| BLOOMz-3B | 25,634 | 3,242 | 7.3 x 10^-5 | 395,602,740 |
| BLOOMz-1B | 17,052 | 1,081 | 6.2 x 10^-5 | 292,467,741 |
| BLOOMz-560M | 10,505 | 543 | 5.4 x 10^-5 | 204,592,592 |

(Cost parity = number of inferences needed for cumulative inference energy to equal the training energy; training energy from Luccioni et al. BLOOM paper, finetuning from the BLOOMz paper, inference from this study.)

Parity varies with model size: from around 200 million inferences for BLOOMz-560M to over 590 million for BLOOMz-7B. This may seem like a lot for a single instance but adds up quickly with multiple instances deployed in parallel. For instance, at its peak ChatGPT was estimated to have upward of 10 million users per day, and the ChatGPT login page received 1.7B visits in October 2023 (SimilarWeb). Even assuming a single query per user, which is rarely the case, the energy costs of deploying it would surpass its training costs after a few weeks or months of deployment.

BLOOMz models are not deployed in real time like ChatGPT, but have been downloaded hundreds of thousands of times from the Hugging Face Hub (as of November 2023: BLOOMz-7B 606,096; BLOOMz-3B 357,368; BLOOMz-1B 61,757; BLOOMz-560m 498,601 downloads), and have been fine-tuned for downstream tasks such as chat and deployed in Hugging Face Spaces. This analysis covers a relatively small sample of models, but such analyses are vital for estimating relative energy of different stages of the ML cycle, understanding trade-offs between training and inference emissions, and characterizing lifetime emissions of ML models; they require more transparency from model creators on both up-front (training) and downstream (inference) costs.

## 5 Discussion

Limited studies exist on LLM inference energy and emissions, largely due to its distributed nature (compared to the time- and location-constrained nature of training), which makes comparisons across models and tasks difficult. The authors kept as many parameters stable as possible: code, hardware, datasets, batch size and Python library. They provide all code and an interactive tool.

### Main takeaways
1. **Generative tasks are more energy- and carbon-intensive compared to discriminative tasks.** The most intensive tasks (Figure 1) are those generating new content: text generation, summarization, image captioning, and image generation.
2. **Tasks involving images are more energy- and carbon-intensive compared to those involving text alone.** Tasks predicting categories (text-to-category, image-to-category) are less energy-intensive than those generating images (text-to-image), with text tasks in between (Figure 2).
3. **Decoder-only models are slightly more energy- and carbon-intensive than sequence-to-sequence models** of a similar size applied to the same tasks (Table 3, Figures 3 and 6): more computation is required for decoder-only models, particularly for tasks with longer outputs. This is worth verifying for other architectures, tasks and datasets.
4. **Training remains orders of magnitude more energy- and carbon-intensive than inference** (per single inference). Initial numbers for BLOOMz of different sizes show the parity between training/finetuning and inference grows with model size. While the ratio is hundreds of millions of inferences per training, given the ubiquity of deployment, parity can be reached quickly for popular models.
5. **Using multi-purpose models for discriminative tasks is more energy-intensive compared to task-specific models for the same tasks.** Especially for text classification (IMDB, SST 2, Rotten Tomatoes) and question answering (SciQ, SQuAD v1 and v2), where the gap is particularly large, and less so for summarization (CNN-Daily Mail, SamSUM, XSum). As Table 4 shows, the gap between multi-purpose and task-specific models is amplified as output length grows.

### The paradigm shift to multi-purpose models
The authors find the last point the most compelling takeaway, given the paradigm shift from smaller models fine-tuned for specific tasks toward models carrying out many tasks at once and deployed to respond to a barrage of user queries in real time. This shift has occurred in ML research since GPT-3 (few- and zero-shot learning) and in consumer settings, with LLMs such as GPT-4 and PaLM deployed in web search, email and navigation, where smaller task-specific models such as BERT were previously used. The impact of this transition is hard to quantify given companies' lack of transparency about parameters, architecture and carbon emissions, but a comparison is possible from this study:
- A BERT-based model fine-tuned for extractive QA (bert-large-uncased-whole-word-masking-finetuned-squad), a task akin to extractive web search, emits on average 0.70 g CO2eq per 1,000 queries, less than 3 times that of the multi-purpose models (2.36 g for Flan-T5 base and 2.34 g for BLOOMz-560M).
- For text classification the difference is much more drastic: bert-base-multilingual-uncased-sentiment emits just 0.32 g CO2eq per 1,000 queries, compared to 2.66 g for Flan-T5-XL and 4.67 g for BLOOMz-7B.
- For scale, the first PaLM model (2022) has 540 billion parameters and GPT-3 has 175 billion parameters; the exact parameter numbers of GPT-4 and PaLM 2 have not been publicly shared.

While the benefit of generative zero-shot models (ability to carry out multiple tasks) is acknowledged, the authors see no convincing evidence for the necessity of deploying them in contexts where tasks are well-defined, for instance web search and navigation, given their energy requirements.

### Intent, limitations and future work
The study aims to set the stage for understanding the energy and emissions of the often overlooked final step of the ML life cycle, deployment. The training/finetuning/inference comparison in Section 4.3 is, to their knowledge, the first of its kind, and offers data points for researchers, practitioners and policy-makers estimating and regulating the environmental impacts of AI and ICT. The authors recognize that the study is not representative of all deployment contexts and constraints; it establishes initial data points. Avenues for future research include factors influencing inference efficiency: choice of architecture, techniques such as distillation, number of parameters, choice of hardware, and numerical (floating point) precision of model parameters. The growing lack of transparency in model architecture and training details makes this research, and work on fairness and accountability, increasingly difficult; the authors hope researchers and practitioners will be transparent about the nature and impacts of their models.

## Ethical Considerations Statement
The main ethical concern is the sheer energy and carbon of the study itself, given each of the 88 models was run on 3 datasets 10 times for statistical significance. In total, 754.66 kWh of energy was used and 178.97 kg CO2eq emitted. To reduce impact, all upfront experimentation was done on smaller portions of the datasets to reduce wasted resources.

## Researcher Positionality Statement
The authors have backgrounds in theoretical and applied machine learning and work in institutions based in North America. Their way of planning and running experiments is not necessarily reflective of other institutions in other regions, or the constraints faced by researchers with more limited access to compute.

## Adverse Impacts Statement
The work can be perceived as a critique of ML deployment in general, which could be used as an argument to stop ML research and development, or to target specific companies or organizations. The authors' intention is to shed light on the environmental impacts of ML so that model developers and researchers can make more informed choices as a function of their environmental footprint or energy usage.

## Appendix A: Full List of Task-Specific Models Tested (Table 6)
The 80 fine-tuned models tested across the ten tasks (8 per task):

- **Image classification:** microsoft/resnet-50, microsoft/beit-base-patch16-224, google/vit-base-patch16-384, facebook/convnextv2-tiny-22k-384, microsoft/resnet-18, google/mobilenet_v1_0.75_192, facebook/convnextv2-tiny-1k-224, google/vit-base-patch16-224
- **Image captioning:** nlpconnect/vit-gpt2-image-captioning, Salesforce/blip-image-captioning-large, Salesforce/blip-image-captioning-base, microsoft/git-large-coco, Salesforce/blip2-flan-t5-xl, Salesforce/blip2-opt-2.7b, ydshieh/vit-gpt2-coco-en, microsoft/git-base
- **Image generation:** runwayml/stable-diffusion-v1-5, stabilityai/stable-diffusion-2-1, stabilityai/stable-diffusion-xl-base-1.0, CompVis/stable-diffusion-v1-4, prompthero/openjourney, dreamlike-art/dreamlike-photoreal-2.0, nota-ai/bk-sdm-tiny, segmind/tiny-sd
- **Masked language modeling:** bert-base-uncased, xlm-roberta-base, distilbert-base-uncased, roberta-base, albert-base-v2, bert-base-cased, microsoft/deberta-base, bert-base-multilingual-cased
- **Object detection:** facebook/detr-resnet-50, hustvl/yolos-tiny, jozhang97/deta-swin-large, facebook/detr-resnet-101, hustvl/yolos-small, SenseTime/deformable-detr, polejowska/detr-r50-cd45rb-8ah-6l, polejowska/detr-r50-cd45rb-1ah-6l
- **Question answering:** distilbert-base-uncased-distilled-squad, distilbert-base-cased-distilled-squad, deepset/roberta-base-squad2, bert-large-uncased-whole-word-masking-finetuned-squad, timpal0l/mdeberta-v3-base-squad2, deepset/tinyroberta-squad2, deepset/electra-base-squad2, deepset/bert-large-uncased-whole-word-masking-squad2
- **Summarization:** sshleifer/distilbart-xsum-12-6, sshleifer/distilbart-cnn-12-6, pszemraj/led-large-book-summary, google/pegasus-xsum, google/pegasus-large, google/pegasus-multi_news, facebook/bart-large-cnn, ainize/bart-base-cnn
- **Text classification:** distilbert-base-uncased-finetuned-sst-2-english, nlptown/bert-base-multilingual-uncased-sentiment, twitter-roberta-base-sentiment-latest, cardiffnlp/twitter-xlm-roberta-base-sentiment, lvwerra/distilbert-imdb, siebert/sentiment-roberta-large-english, finiteautomata/bertweet-base-sentiment-analysis, sbcBI/sentiment_analysis_model
- **Text generation:** gpt2, bigscience/bloom-560m, distilgpt2, facebook/opt-6.7b, EleutherAI/gpt-neo-125m, gpt2-medium, facebook/opt-1.3b, gpt2-xl
- **Token classification:** QCRI/bert-base-multilingual-cased-pos-english, dslim/bert-base-NER, dslim/bert-large-NER, Jean-Baptiste/roberta-large-ner-english, oliverguhr/fullstop-punctuation-multilang-large, Babelscape/wikineural-multilingual-ner, ml6team/keyphrase-extraction-distilbert-inspec, obi/deid_roberta_i2b2

## Appendix B: Model Evaluation (Table 7)
Full performance metrics for the 32 models (24 fine-tuned, 8 multi-purpose) evaluated. Metrics: accuracy for SST 2, IMDB, Rotten Tomatoes and SciQ; F1 for SQuAD and SQuAD v2 (has-answer); ROUGE for SAMSum, XSum and CNN.

**Multi-purpose models** (column order follows the original header; alignment reconstructed from the extracted table)

| Model | SST 2 | IMDB | Rotten Tomatoes | SciQ | SQuAD | SQuAD v2 | SamSUM | XSum | CNN |
|---|---|---|---|---|---|---|---|---|---|
| bloomz-560m | 0.92 | 0.94 | 0.85 | 0.92 | 0.43 | 0.21 | 0.23 | 0.15 | 0.10 |
| bloomz-1b7 | 0.94 | 0.97 | 0.93 | 0.96 | 0.50 | 0.25 | 0.26 | 0.16 | 0.18 |
| bloomz-3b | 0.95 | 0.98 | 0.95 | 0.97 | 0.53 | 0.26 | 0.28 | 0.17 | 0.21 |
| bloomz-7b1 | 0.94 | 0.98 | 0.95 | 0.97 | 0.54 | 0.27 | 0.32 | 0.21 | 0.09 |
| flan-t5-xxl | 0.96 | 0.97 | 0.92 | 0.72 | 0.98 | 0.49 | 0.30 | 0.37 | 0.23 |
| flan-t5-xl | 0.96 | 0.97 | 0.93 | 0.66 | 0.97 | 0.49 | 0.49 | 0.38 | 0.24 |
| flan-t5-large | 0.94 | 0.96 | 0.92 | 0.53 | 0.97 | 0.50 | 0.45 | 0.30 | 0.24 |
| flan-t5-base | 0.93 | 0.95 | 0.88 | 0.61 | 0.95 | 0.48 | 0.46 | 0.32 | 0.23 |

**Task-specific question answering models (SciQ / SQuAD / SQuAD v2)**

| Model | SciQ | SQuAD | SQuAD v2 |
|---|---|---|---|
| distilbert-base-uncased-distilled-squad | 0.44 | 0.87 | 0.86 |
| distilbert-base-cased-distilled-squad | 0.46 | 0.87 | 0.87 |
| deepset/roberta-base-squad2 | 0.48 | 0.93 | 0.83 |
| bert-large-uncased-whole-word-masking-finetuned-squad | 0.48 | 0.93 | 0.84 |
| timpal0l/mdeberta-v3-base-squad2 | 0.46 | 0.91 | 0.90 |
| deepset/tinyroberta-squad2 | 0.45 | 0.98 | 0.91 |
| deepset/electra-base-squad2 | 0.48 | 0.89 | 0.82 |
| deepset/bert-large-uncased-whole-word-masking-squad2 | 0.46 | 0.92 | 0.92 |

**Task-specific summarization models (SamSUM / XSum / CNN ROUGE)**

| Model | SamSUM | XSum | CNN |
|---|---|---|---|
| sshleifer/distilbart-xsum-12-6 | 0.20 | 0.45 | 0.23 |
| sshleifer/distilbart-cnn-12-6 | 0.29 | 0.21 | 0.44 |
| pszemraj/led-large-book-summary | 0.33 | 0.16 | 0.33 |
| pegasus-xsum | 0.22 | 0.22 | 0.22 |
| pegasus-large | 0.27 | 0.17 | 0.34 |
| pegasus-multi_news | 0.12 | 0.16 | 0.29 |
| facebook/bart-large-cnn | 0.32 | 0.21 | 0.44 |
| ainize/bart-base-cnn | 0.27 | 0.16 | 0.26 |

**Task-specific text classification models (SST 2 / IMDB / Rotten Tomatoes accuracy)**

| Model | SST 2 | IMDB | Rotten Tomatoes |
|---|---|---|---|
| distilbert-base-uncased-finetuned-sst-2-english | 0.99 | 0.88 | 0.90 |
| nlptown/bert-base-multilingual-uncased-sentiment | 0.75 | 0.85 | 0.73 |
| twitter-roberta-base-sentiment-latest | 0.82 | 0.80 | 0.77 |
| cardiffnlp/twitter-xlm-roberta-base-sentiment | 0.79 | 0.71 | 0.74 |
| lvwerra/distilbert-imdb | 0.88 | 0.93 | 0.82 |
| siebert/sentiment-roberta-large-english | 0.92 | 0.92 | 0.92 |
| finiteautomata/bertweet-base-sentiment-analysis | 0.82 | 0.72 | 0.77 |
| sbcBI/sentiment_analysis_model | 0.81 | 0.75 | 0.76 |

**Figures 7 and 8 (captions):** Model size (number of parameters, x axis, log scale) versus summarization accuracy (Figure 7) and question answering accuracy (Figure 8), with dot size indicating the quantity of emissions.

