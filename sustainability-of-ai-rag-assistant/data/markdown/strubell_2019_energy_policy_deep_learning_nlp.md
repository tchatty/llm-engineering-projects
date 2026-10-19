# Energy and Policy Considerations for Deep Learning in NLP

Authors: Emma Strubell, Ananya Ganesh, Andrew McCallum
Publication Year: 2019
Source: Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL 2019), pages 3645-3650, Florence, Italy, July 28 - August 2, 2019
Keywords: energy consumption, carbon footprint, CO2e emissions, training cost, deep learning, NLP, Transformer, BERT, ELMo, GPT-2, neural architecture search (NAS), hyperparameter tuning, PUE, cloud compute cost, equitable access to compute, efficient hardware and algorithms (keywords derived from content; not stated in the paper)

## Executive Summary

Strubell, Ganesh and McCallum (2019) quantify the financial and environmental costs of training large neural network models for natural language processing (NLP). Their motivation is that recent accuracy gains in NLP come from ever larger networks trained on abundant data, which require exceptionally large computational resources (GPUs, TPUs running for weeks or months) and therefore substantial energy. Research and development multiplies these costs by thousands of times because models must be retrained to experiment with architectures and hyperparameters.

Method: the authors train four popular off-the-shelf models (Transformer, ELMo, BERT, GPT-2) using default settings, sampling GPU power (NVIDIA System Management Interface) and CPU power (Intel RAPL) for up to 1 day, then combine reported training times and hardware from the original papers to estimate total energy. Power is the sum of CPU, DRAM and GPU draw multiplied by a Power Usage Effectiveness (PUE) of 1.58 (2018 global data center average): pt = 1.58 t (pc + pr + g pg) / 1000 kWh. CO2e (lbs) = 0.954 pt, using the U.S. EPA average emissions factor, which approximates the energy mix of Amazon AWS.

Key results: training Transformer base emits about 26 lbs CO2e, Transformer big 192 lbs, ELMo 262 lbs, and BERT base on 64 V100 GPUs 1438 lbs (roughly a trans-American flight; a NY-SF flight for one person is 1984 lbs). A neural architecture search (NAS) for the Transformer (So et al., 2019) required 274,120 hours on 8 P100 GPUs, about 656,347 kWh and 626,155 lbs CO2e (nearly five times the lifetime emissions of an average car, 126,000 lbs, including fuel), at a cloud cost of roughly $942,973-$3,201,722, to gain only 0.1 BLEU (29.7 for English-German). Cloud cost estimates: BERT base $3751-$12,571 on GPU; GPT-2 $12,902-$43,008 on TPUs.

A case study of developing Linguistically-Informed Self-Attention (LISA) shows R&D costs: 172 days, 123 hyperparameter grid searches, 4789 jobs, 9998 GPU-days (27 years), about 78,468 lbs CO2e, and $103k-$350k in cloud compute (electricity $9870), versus $52-$175 and 39 lbs CO2e for training a single final model. Tuning for a new dataset (about 24 jobs) costs $1238-$4205.

Recommendations: (1) report training time and sensitivity to hyperparameters, ideally with hardware-independent measures such as gigaflops to convergence; (2) provide academic researchers equitable access to compute, for example a government-funded shared academic compute cloud (an 8x GTX 1080 Ti server costs about $20,000; the case study hardware would cost about $145,000, about half the on-demand cloud cost); and (3) prioritize computationally efficient hardware and algorithms, including easy-to-use random or Bayesian hyperparameter search instead of brute-force grid search. The authors note energy mix varies by provider (Google 56% renewable, AWS 17%) and that TPU power is not publicly reported.

## Abstract

Recent progress in hardware and methodology for training neural networks has ushered in a new generation of large networks trained on abundant data. These models have obtained notable gains in accuracy across many NLP tasks. However, these accuracy improvements depend on the availability of exceptionally large computational resources that necessitate similarly substantial energy consumption. As a result these models are costly to train and develop, both financially, due to the cost of hardware and electricity or cloud compute time, and environmentally, due to the carbon footprint required to fuel modern tensor processing hardware. In this paper the authors bring this issue to the attention of NLP researchers by quantifying the approximate financial and environmental costs of training a variety of recently successful neural network models for NLP. Based on these findings, they propose actionable recommendations to reduce costs and improve equity in NLP research and practice.

## 1 Introduction

### Motivation: accuracy gains depend on compute and energy
Advances in techniques and hardware for training deep neural networks have recently enabled impressive accuracy improvements across many fundamental NLP tasks (Bahdanau et al., 2015; Luong et al., 2015; Dozat and Manning, 2017; Vaswani et al., 2017), with the most computationally-hungry models obtaining the highest scores (Peters et al., 2018; Devlin et al., 2019; Radford et al., 2019; So et al., 2019). Training a state-of-the-art model now requires substantial computational resources which demand considerable energy, along with the associated financial and environmental costs. Research and development of new models multiplies these costs by thousands of times by requiring retraining to experiment with model architectures and hyperparameters.

### Financial access concerns
A decade ago most NLP models could be trained and developed on a commodity laptop or server. Many now require multiple instances of specialized hardware such as GPUs or TPUs, therefore limiting access to these highly accurate models on the basis of finances.

### Environmental concerns
Even when these expensive computational resources are available, model training also incurs a substantial cost to the environment due to the energy required to power this hardware for weeks or months at a time. Though some of this energy may come from renewable or carbon credit-offset resources, the high energy demands of these models are still a concern because: (1) energy is not currently derived from carbon-neutral sources in many locations, and (2) when renewable energy is available, it is still limited to the equipment we have to produce and store it, and energy spent training a neural network might better be allocated to heating a family's home. It is estimated that we must cut carbon emissions by half over the next decade to deter escalating rates of natural disaster. Based on the estimated CO2 emissions in Table 1, model training and development likely make up a substantial portion of the greenhouse gas emissions attributed to many NLP researchers.

### Table 1: Estimated CO2 emissions from training common NLP models, compared to familiar consumption

| Consumption | CO2e (lbs) |
|---|---|
| Air travel, 1 person, NY to SF (NYSF) | 1984 |
| Human life, avg, 1 year | 11,023 |
| American life, avg, 1 year | 36,156 |
| Car, avg incl. fuel, 1 lifetime | 126,000 |
| Training one model (GPU): NLP pipeline (parsing, SRL) | 39 |
| NLP pipeline (parsing, SRL) w/ tuning & experiments | 78,468 |
| Training one model (GPU): Transformer (big) | 192 |
| Transformer (big) w/ neural arch. search | 626,155 |

Sources for the familiar-consumption figures (footnote 1): air travel and per-capita consumption, and car lifetime, from public sources cited by the authors.

### Contributions and approach
To heighten the awareness of the NLP community and promote mindful practice and policy, the authors characterize the dollar cost and carbon emissions that result from training the neural networks at the core of many state-of-the-art NLP models. They estimate the kilowatts of energy required to train a variety of popular off-the-shelf NLP models, which can be converted to approximate carbon emissions and electricity costs. To estimate the even greater resources required to transfer an existing model to a new task or develop new models, they perform a case study of the full computational resources required for the development and tuning of a recent state-of-the-art NLP pipeline (Strubell et al., 2018).

Recommendations, in brief: (1) time to retrain and sensitivity to hyperparameters should be reported for NLP machine learning models; (2) academic researchers need equitable access to computational resources; and (3) researchers should prioritize developing efficient models and hardware.

## 2 Methods

### Overview
To quantify the computational and environmental cost of training deep neural network models for NLP, the authors analyze the energy required to train a variety of popular off-the-shelf NLP models, as well as a case study of the complete sum of resources required to develop LISA (Strubell et al., 2018), a state-of-the-art NLP model from EMNLP 2018, including all tuning and experimentation.

### Measurement procedure
- The models described in section 2.1 are trained using the default settings provided, while sampling GPU and CPU power consumption during training.
- Each model was trained for a maximum of 1 day.
- All models were trained on a single NVIDIA Titan X GPU, except ELMo, which was trained on 3 NVIDIA GTX 1080 Ti GPUs.
- During training, the NVIDIA System Management Interface (nvidia-smi) is repeatedly queried to sample GPU power consumption; the average over all samples is reported.
- CPU power consumption is sampled using Intel's Running Average Power Limit (RAPL) interface.
- Total training time to completion is estimated using training times and hardware reported in the original papers.

### Energy and power formula (Equation 1)
Definitions: pc = average power draw (watts) from all CPU sockets during training; pr = average power draw from all DRAM (main memory) sockets; pg = average power draw of a GPU during training; g = number of GPUs used to train; t = training time in hours.

Total power consumption is estimated as combined GPU, CPU and DRAM consumption, multiplied by Power Usage Effectiveness (PUE), which accounts for the additional energy required to support the compute infrastructure (mainly cooling). The authors use a PUE coefficient of 1.58, the 2018 global average for data centers (Ascierto, 2018). The total power pt (in kWh) required during training is:

pt = 1.58 t (pc + pr + g pg) / 1000    (Equation 1)

### Carbon conversion (Equation 2)
The U.S. Environmental Protection Agency (EPA) provides average CO2 produced (in pounds per kilowatt-hour) for power consumed in the U.S. (EPA, 2018), used to convert power to estimated CO2 emissions:

CO2e = 0.954 pt    (Equation 2)

This conversion takes into account the relative proportions of different energy sources (primarily natural gas, coal, nuclear and renewable) consumed to produce energy in the United States. The U.S. breakdown of energy is comparable to that of the most popular cloud compute service, Amazon Web Services, so the authors believe this conversion provides a reasonable estimate of CO2 emissions per kilowatt hour of compute energy used.

### Table 2: Percent energy sourced from renewable, natural gas, coal and nuclear

Energy sources of the top 3 cloud compute providers (Cook et al., 2017), compared to the United States, China and Germany (U.S. Dept. of Energy; China Electricity Council; Burger, 2019).

| Consumer | Renewable | Gas | Coal | Nuclear |
|---|---|---|---|---|
| China | 22% | 3% | 65% | 4% |
| Germany | 40% | 7% | 38% | 13% |
| United States | 17% | 35% | 27% | 19% |
| Amazon-AWS | 17% | 24% | 30% | 26% |
| Google | 56% | 14% | 15% | 10% |
| Microsoft | 32% | 23% | 31% | 10% |

Renewable includes e.g. hydro, solar, wind.

### 2.1 Models
The authors analyze four models. All models have code freely available online, which they used out-of-the-box.

- **Transformer.** The Transformer (T2T) model (Vaswani et al., 2017) is an encoder-decoder architecture primarily recognized for efficient and accurate machine translation. The encoder and decoder each consist of 6 stacked layers of multi-head self-attention. Vaswani et al. report that the Transformer base model (T2Tbase; 65M parameters) was trained on 8 NVIDIA P100 GPUs for 12 hours, and the Transformer big model (T2Tbig; 213M parameters) was trained for 3.5 days (84 hours; 300k steps). This model is also the basis for recent work on neural architecture search (NAS) for machine translation and language modeling (So et al., 2019), and the NLP pipeline studied in section 4.2 (Strubell et al., 2018). So et al. (2019) report that their full architecture search ran for a total of 979M training steps, and that their base model requires 10 hours to train for 300k steps on one TPUv2 core. This equates to 32,623 hours of TPU or 274,120 hours on 8 P100 GPUs.
- **ELMo.** The ELMo model (Peters et al., 2018) is based on stacked LSTMs and provides rich word representations in context by pre-training on a large amount of data using a language modeling objective. Replacing context-independent pre-trained word embeddings with ELMo has been shown to increase performance on downstream tasks such as named entity recognition, semantic role labeling, and coreference. Peters et al. report that ELMo was trained on 3 NVIDIA GTX 1080 GPUs for 2 weeks (336 hours).
- **BERT.** The BERT model (Devlin et al., 2019) provides a Transformer-based architecture for building contextual representations similar to ELMo, but trained with a different language modeling objective. BERT substantially improves accuracy on tasks requiring sentence-level representations such as question answering and natural language inference. Devlin et al. report that the BERT base model (BERTbase; 110M parameters) was trained on 16 TPU chips for 4 days (96 hours). NVIDIA reports that they can train a BERT model in 3.3 days (79.2 hours) using 4 DGX-2H servers, totaling 64 Tesla V100 GPUs (Forster et al., 2019).
- **GPT-2.** The latest edition of OpenAI's GPT general-purpose token encoder, also based on Transformer-style self-attention and trained with a language modeling objective (Radford et al., 2019). By training a very large model on massive data, Radford et al. show high zero-shot performance on question answering and language modeling benchmarks. The large model described in Radford et al. (2019) has 1542M parameters and is reported to require 1 week (168 hours) of training on 32 TPUv3 chips (information obtained via the authors on Reddit).

## 3 Related Work

There is some precedent for work characterizing the computational requirements of training and inference in modern neural network architectures in the computer vision community. Li et al. (2016) present a detailed study of the energy use required for training and inference in popular convolutional models for image classification in computer vision, including fine-grained analysis comparing different neural network layer types. Canziani et al. (2016) assess image classification model accuracy as a function of model size and gigaflops required during inference. They also measure average power draw required during inference on GPUs as a function of batch size. Neither work analyzes the recurrent and self-attention models that have become commonplace in NLP, nor do they extrapolate power to estimates of carbon and dollar cost of training.

Analysis of hyperparameter tuning has been performed in the context of improved algorithms for hyperparameter search (Bergstra et al., 2011; Bergstra and Bengio, 2012; Snoek et al., 2012). To the authors' knowledge there exists to date no analysis of the computation required for R&D and hyperparameter tuning of neural network models in NLP.

## 4 Experimental Results

### 4.1 Cost of training

Table 3 lists CO2 emissions and estimated cost of training the models described in section 2.1.

#### Table 3: Estimated cost of training a model in terms of CO2 emissions (lbs) and cloud compute cost (USD)

| Model | Hardware | Power (W) | Hours | kWh x PUE | CO2e (lbs) | Cloud compute cost |
|---|---|---|---|---|---|---|
| T2Tbase | P100 x8 | 1415.78 | 12 | 27 | 26 | $41-$140 |
| T2Tbig | P100 x8 | 1515.43 | 84 | 201 | 192 | $289-$981 |
| ELMo | P100 x3 | 517.66 | 336 | 275 | 262 | $433-$1472 |
| BERTbase | V100 x64 | 12,041.51 | 79 | 1507 | 1438 | $3751-$12,571 |
| BERTbase | TPUv2 x16 | -- | 96 | -- | -- | $2074-$6912 |
| NAS | P100 x8 | 1515.43 | 274,120 | 656,347 | 626,155 | $942,973-$3,201,722 |
| NAS | TPUv2 x1 | -- | 32,623 | -- | -- | $44,055-$146,848 |
| GPT-2 | TPUv3 x32 | -- | 168 | -- | -- | $12,902-$43,008 |

(Power column values were re-aligned from the PDF's garbled table layout and checked against kWh = 1.58 x hours x power / 1000.) Power and carbon footprint are omitted for TPUs due to lack of public information on power draw for this hardware. Note that the table lists ELMo hardware as P100 x3, while the text of section 2 says the authors' own measurement used 3 GTX 1080 Ti GPUs and Peters et al. report GTX 1080 GPUs.

Footnote 7 (cloud pricing assumptions): the GPU lower bound is computed using pre-emptible P100/V100 U.S. resources priced at $0.43-$0.74/hr; the upper bound uses on-demand U.S. resources priced at $1.46-$2.48/hr. Similarly, pre-emptible ($1.46/hr-$2.40/hr) and on-demand ($4.50/hr-$8/hr) pricing are used as lower and upper bounds for TPU v2/3; cheaper bulk contracts are available.

#### Findings
- TPUs are more cost-efficient than GPUs on workloads that make sense for that hardware (e.g. BERT): BERTbase costs $2074-$6912 on 16 TPUv2 chips versus $3751-$12,571 on 64 V100 GPUs.
- Models emit substantial carbon emissions; training BERT on GPU (1438 lbs CO2e) is roughly equivalent to a trans-American flight (1984 lbs for one person NY to SF).
- Neural architecture search: So et al. (2019) report that NAS achieves a new state-of-the-art BLEU score of 29.7 for English to German machine translation, an increase of just 0.1 BLEU, at the cost of at least $150k in on-demand compute time and non-trivial carbon emissions (626,155 lbs CO2e in Table 3, versus 126,000 lbs for the lifetime of an average car including fuel).

### 4.2 Cost of development: Case study

#### Scope
To quantify the computational requirements of R&D for a new model, the authors study the logs of all training required to develop Linguistically-Informed Self-Attention (LISA; Strubell et al., 2018), a multi-task model that performs part-of-speech tagging, labeled dependency parsing, predicate detection and semantic role labeling. It makes an interesting case study as a representative NLP pipeline and as a Best Long Paper at EMNLP.

#### Project statistics
- Model training spanned a period of 172 days (approx. 6 months).
- 123 small hyperparameter grid searches were performed, resulting in 4789 jobs in total.
- Job length ranged from a minimum of 3 minutes (indicating a crash) to a maximum of 9 days, with an average job length of 52 hours.
- All training was done on a combination of NVIDIA Titan X (72%) and M40 (28%) GPUs. Cloud cost is approximated using P100 pricing.
- The sum GPU time required for the project totaled 9998 days (27 years), averaging about 60 GPUs running constantly throughout the 6 month duration of the project.

#### Table 4: Estimated cost in terms of cloud compute and electricity for training (1) a single model (2) a single tune and (3) all models trained during R&D

| Models | Hours | Cloud cost (Google Cloud) | Electric cost |
|---|---|---|---|
| 1 (a single model) | 120 | $52-$175 | $5 |
| 24 (a single tune, for a new dataset) | 2880 | $1238-$4205 | $118 |
| 4789 (all models trained during R&D) | 239,942 | $103k-$350k | $9870 |

Electricity cost is based on the average U.S. cost of electricity of $0.12/kWh. The table gives upper and lower bounds of estimated cost in terms of Google Cloud compute and raw electricity required to develop and deploy this model.

#### Findings
While training a single model is relatively inexpensive, the cost of tuning a model for a new dataset (estimated here to require 24 jobs), or performing the full R&D required to develop this model, quickly becomes extremely expensive. In Table 1, the LISA NLP pipeline emits 39 lbs CO2e for one model trained on GPU versus 78,468 lbs CO2e with tuning and experiments.

## 5 Conclusions and Recommendations

### Recommendation 1: Authors should report training time and sensitivity to hyperparameters
The experiments suggest it would be beneficial to directly compare different models to perform a cost-benefit (accuracy) analysis. To address this, when proposing a model that is meant to be re-trained for downstream use, such as retraining on a new domain or fine-tuning on a new task, authors should report training time and computational resources required, as well as model sensitivity to hyperparameters. This will enable direct comparison across models, allowing subsequent consumers of these models to accurately assess whether the required computational resources are compatible with their setting. More explicit characterization of tuning time could also reveal inconsistencies in time spent tuning baseline models compared to proposed contributions. Realizing this will require: (1) a standard, hardware-independent measurement of training time, such as gigaflops required to convergence, and (2) a standard measurement of model sensitivity to data and hyperparameters, such as variance with respect to hyperparameters searched.

### Recommendation 2: Academic researchers need equitable access to computation resources
Recent advances in available compute come at a high price not attainable to all who desire access. Most of the models studied in this paper were developed outside academia; recent improvements in state-of-the-art accuracy are possible thanks to industry access to large-scale compute.

Limiting this style of research to industry labs hurts the NLP research community in many ways:
1. It stifles creativity. Researchers with good ideas but without access to large-scale compute will simply not be able to execute their ideas, instead constrained to focus on different problems.
2. It prohibits certain types of research on the basis of access to financial resources. This even more deeply promotes the already problematic "rich get richer" cycle of research funding, where groups that are already successful and thus well-funded tend to receive more funding due to their existing accomplishments.
3. The prohibitive start-up cost of building in-house resources forces resource-poor groups to rely on cloud compute services such as AWS, Google Cloud and Microsoft Azure.

While these services provide valuable, flexible, and often relatively environmentally friendly compute resources, it is more cost effective for academic researchers, who often work for non-profit educational institutions and whose research is funded by government entities, to pool resources to build shared compute centers at the level of funding agencies, such as the U.S. National Science Foundation. For example, an off-the-shelf GPU server containing 8 NVIDIA 1080 Ti GPUs and supporting hardware can be purchased for approximately $20,000 USD. At that cost, the hardware required to develop the model in the case study (approximately 58 GPUs for 172 days) would cost $145,000 USD plus electricity, about half the estimated cost to use on-demand cloud GPUs. Unlike money spent on cloud compute, however, that invested in centralized resources would continue to pay off as resources are shared across many projects. A government-funded academic compute cloud would provide equitable access to all researchers.

### Recommendation 3: Researchers should prioritize computationally efficient hardware and algorithms
The authors recommend a concerted effort by industry and academia to promote research of more computationally efficient algorithms, as well as hardware that requires less energy. An effort can also be made in terms of software. There is already a precedent for NLP software packages prioritizing efficient models. An additional avenue through which NLP and machine learning software developers could aid in reducing the energy associated with model tuning is by providing easy-to-use APIs implementing more efficient alternatives to brute-force grid search for hyperparameter tuning, e.g. random or Bayesian hyperparameter search techniques (Bergstra et al., 2011; Bergstra and Bengio, 2012; Snoek et al., 2012). While software packages implementing these techniques do exist (for example the Hyperopt Python library), they are rarely employed in practice for tuning NLP models. This is likely because their interoperability with popular deep learning frameworks such as PyTorch and TensorFlow is not optimized, i.e. there are not simple examples of how to tune TensorFlow Estimators using Bayesian search. Integrating these tools into the workflows with which NLP researchers and practitioners are already familiar could have notable impact on the cost of developing and tuning in NLP.

## Limitations and Assumptions (as stated in the paper)
- Energy for the off-the-shelf models was sampled from runs of at most 1 day on a single NVIDIA Titan X (3 GTX 1080 Ti for ELMo); total training time and hardware come from the original papers.
- PUE is fixed at 1.58 (2018 global data center average) and the CO2 factor is the U.S. EPA average (0.954 lbs per kWh), judged comparable to AWS's energy mix; providers such as Google (56% renewable) have much cleaner mixes, so actual emissions depend on location and provider.
- Power and carbon estimates are omitted for TPUs because TPU power draw is not publicly available.
- Cloud cost is a range between pre-emptible and on-demand pricing; cheaper bulk contracts exist. Case study cloud cost uses P100 pricing though GPUs used were Titan X and M40; electricity assumes $0.12/kWh.
- The scope is training and development, not inference.
