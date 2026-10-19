# Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model

Authors: Alexandra Sasha Luccioni, Sylvain Viguier, Anne-Laure Ligozat
Publication Year: 2022 (arXiv:2211.02001v1 [cs.LG], 3 Nov 2022; the filename says 2021, but the arXiv stamp in the text gives November 2022)
Source: arXiv preprint arXiv:2211.02001 (cs.LG)
Keywords: carbon footprint, BLOOM, large language models, life cycle assessment, embodied emissions, dynamic power consumption, idle power consumption, inference, deployment, CO2eq, carbon intensity, PUE, BigScience, Jean Zay, CodeCarbon

## Executive Summary

This paper quantifies the carbon footprint of BLOOM, a 176-billion parameter open multilingual language model trained as part of the BigScience workshop (May 2021 to May 2022) on the Jean Zay cluster in France. It describes itself as the first attempt to estimate the broader carbon footprint of an LLM, including the manufacturing of computing equipment and deployment through an API. The goal is not an exact number but the relative contribution of each stage. The authors follow a Life Cycle Assessment (LCA) approach as far as available information allows, and express all results in CO2 equivalents (CO2eq).

BLOOM's final training took 118 days, 5 hours, 41 minutes and 1,082,990 GPU hours on Nvidia A100 80GB GPUs, using 433,196 kWh on a grid with a carbon intensity of 57 gCO2eq/kWh. Dynamic power consumption alone emitted about 24.7 tonnes of CO2eq. Embodied emissions of servers (7.57 t) and GPUs (3.64 t) add 11.2 tonnes. Idle consumption of the cluster (the nodes, network, storage and cooling that run alongside training) adds 256,646 kWh and 14.6 tonnes. The total is about 50.5 tonnes of CO2eq, split 22.2% embodied, 48.9% dynamic and 28.9% idle. This matches product footprint estimates in which embodied emissions are 20-30% of life cycle emissions.

For deployment, the authors ran CodeCarbon for about 18 days on a Google Cloud Platform instance with 16 Nvidia A100 40GB GPUs serving BLOOM through a real-time API. It received 558 requests per hour on average (230,768 in total). Mean power was 1,664 W (range 1,252-2,735 W), the instance consumed 914 kWh, and about 0.28 kWh per 10 minutes was used even with almost no requests. In the us-central1 region (394 gCO2eq/kWh), this is about 19 kg CO2eq per day, or 340 kg over the tracked period.

Comparisons: BLOOM's dynamic emissions (about 25 t) are less than half those of OPT-175B (70 t) and about 20 times lower than GPT-3 (502 t). The authors attribute this largely to the low-carbon French grid. BLOOM used somewhat more energy than OPT (433 MWh vs 324 MWh). All BigScience experiments added up to 3.46 million GPU hours, 1,163,032 kWh and about 66.29 tonnes CO2eq of dynamic emissions. Intermediate models alone emitted more than the final model. With embodied and idle emissions the workshop total is 123.82 tonnes, excluding the emissions from deploying the shared models.

The authors call for more precise embodied-emission data from hardware makers, more studies of inference and deployment, more transparent and disaggregated carbon reporting (energy, carbon intensity, PUE, R&D, evaluation), and attention to indirect and system-level impacts of ML.

## Abstract

Progress in machine learning (ML) comes with a cost to the environment, given that training ML models requires significant computational resources, energy and materials. The article aims to quantify the carbon footprint of BLOOM, a 176-billion parameter language model, across its life cycle. BLOOM's final training emitted approximately 24.7 tonnes of CO2eq if only the dynamic power consumption is considered, and 50.5 tonnes if all processes are accounted for, ranging from equipment manufacturing to energy-based operational consumption. The paper also studies the energy requirements and carbon emissions of deploying BLOOM for inference via an API endpoint receiving user queries in real time. It concludes with a discussion of the difficulty of precisely estimating the carbon footprint of ML models and of future research directions that can improve carbon emissions reporting.

## 1 Introduction

Climate change is one of our generation's biggest challenges, impacting ecosystems and livelihoods across the world; estimating and reducing carbon emissions is an important part of mitigating its impacts. According to recent estimates, the global CO2 emissions of the information and communications technology (ICT) sector account for around 2% of global CO2 emissions, but this figure is hard to estimate precisely given the distributed nature of global computing infrastructure. The infrastructure used for training and deploying ML models contributes to this number, but the exact extent of the contribution is unclear. It is important to start systematically tracking the carbon footprint of ML models and algorithms and the main sources of emissions.

Large language models (LLMs) are among the biggest ML models, spanning up to hundreds of billions of parameters, requiring millions of GPU hours to train, and emitting carbon in the process. As these models grow in size (the trend in recent years), it is crucial to track the scope and evolution of their carbon footprint. The study describes the first attempt to estimate the broader carbon footprint of an LLM, including the emissions produced by manufacturing the computing equipment used for its training, as well as by model deployment via an API. The goal is not to hone in on an exact number for the emissions, but to estimate the relative contribution of each step of the deployment process to overall emissions. The paper concludes with a discussion about the carbon emissions of different LLMs and of the BigScience workshop overall, and proposes directions for future work to quantify and report these emissions.

## 2 Related Work

### Empirical Studies on ML CO2 Emissions
Most existing work has estimated CO2 emissions incurred during model training. Starting with the seminal work of Strubell et al., who looked at the carbon footprint of training a Transformer model, more recent studies have looked at other model architectures and their emissions (e.g. Patterson et al.). Other studies have analysed trends in the energy requirements and CO2 emissions of ML models in general. Some studies (Thompson et al.) predict growth in the carbon emissions of ML models, while others (Patterson et al., "The carbon footprint of machine learning training will plateau, then shrink") predict that emissions will shrink in coming years; further work is needed to get estimates from a broader variety of models and use cases.

### Tools for Estimating Carbon Impact
Several tools estimate the CO2 emissions of training ML models. Some run in parallel to training code and track energy consumption and CO2 emissions (e.g. CodeCarbon, Carbontracker), while others are used post-training to produce a higher-level estimate (e.g. the ML CO2 Impact calculator by Lacoste et al.). However, these tools are seldom used for reporting CO2 emissions in ML publications, and a recent study found that they vary significantly in the estimates they produce (Bannour et al.).

### Additional Factors
Complementary work covers other contributions to the carbon footprint of ML: in-person versus virtual conference attendance, manufacturing of computing hardware (Gupta et al., "Chasing carbon"), the life cycle analysis of the entire ML development and deployment cycle (Ligozat et al.), and certification of ML systems according to their social and environmental impacts (SECURE). Increasingly, scholars consider the environmental impacts of ML beyond training CO2 emissions, including equipment manufacturing and deployment (Wu et al.; Kaack et al.). However, there is still a need for a common approach to estimating and comparing the carbon emissions of ML models that spans the different parts of the model life cycle.

## 3 Background and Methodology

### 3.1 The BLOOM Model
The BigScience Large Open-science Open-access Multilingual Language Model (BLOOM) is a 176 billion parameter language model. It was trained on 1.6 terabytes of data in 46 natural languages and 13 programming languages as part of the BigScience workshop, a year-long initiative that lasted from May 2021 to May 2022 and brought together over a thousand researchers from around the world. The workshop was granted access to the computing resources of the Institut du developpement et des ressources en informatique scientifique (IDRIS) of the Centre national de la recherche scientifique (CNRS) in France, so training was carried out on the Jean Zay computer cluster of IDRIS.

**Table 1: Key statistics about BLOOM model training**

| Statistic | Value |
|---|---|
| Total training time | 118 days, 5 hours, 41 min |
| Total number of GPU hours | 1,082,990 hours |
| Total energy used | 433,196 kWh |
| GPU models used | Nvidia A100 80GB |
| Carbon intensity of the energy grid | 57 gCO2eq/kWh |

Many other efforts were needed beyond the final training: data sourcing, collection and processing, tokenization, architecture engineering and evaluation. In the months preceding the final BLOOM training, several smaller-scale experiments evaluated different model sizes and architectures, which helped converge on the final BLOOM architecture. Section 4 reports the emissions of the final 176B parameter BLOOM model, whereas the emissions of intermediate model training and evaluation within the BigScience project are presented in Section 5.2.

### 3.2 Methodology
There is no universally accepted approach for assessing the environmental impacts of ML models, so the authors adopt the widely used Life Cycle Assessment (LCA) methodology, which aims to cover all stages of the life cycle of a product or process. They lack the information for a "cradle-to-grave" assessment of BLOOM (all processes from raw material extraction to disposal), so they focus on the steps for which they have sufficient information, from manufacturing the equipment used for training to model deployment (Figure 1; the stages studied are highlighted in green in the figure).

Kaack et al. proposed a framework for categorizing ML's effects on greenhouse gas (GHG) emissions with 3 categories: (A) computing-related impacts, (B) immediate impacts of deploying ML and (C) system-level impacts on other domains. This framework is not yet widely adopted in the field, but the authors find it useful given the specificity of the ML life cycle. The study focuses on category (A) and briefly discusses deployment and system-level impacts in Section 5.3.

**Carbon dioxide equivalents (CO2eq).** Because LCA accounts for all possible GHG sources (methane, carbon dioxide, nitrous oxide, etc.), the gases are converted to a single unit so they can be added. The standard measure is carbon dioxide equivalents (CO2eq), calculated by comparing the global-warming potential (GWP) of different greenhouse gases to that of CO2. For instance, methane has a 100-year GWP 25 times that of CO2, so it equals 25 CO2eq. All BLOOM emissions are given in this unit.

## 4 Results: Carbon Emissions of the BLOOM Model

The study brings together the elements contributing to the carbon footprint of training BLOOM and compares the relative contribution of each to BLOOM's total emissions. It focuses on model training but also covers emissions from manufacturing the computing equipment, energy-based operational emissions, and the carbon footprint of model deployment and inference. Code and data are available in the authors' GitHub repository.

### 4.1 Embodied Emissions
Embodied emissions are those associated with the materials and processes involved in producing a product, such as the computing equipment needed to train and deploy ML models. They arise only in manufacturing, but the total is usually spread over the equipment's period of use by dividing total embodied emissions by time of use.

BLOOM was trained on HPE Apollo 6500 Gen10 Plus servers containing Nvidia A100 GPUs. The closest comparable equipment with LCA information is HPE's ProLiant DL345 Gen10 Plus server, similar to the Apollo 6500, with a production footprint of approximately 2500 kg of CO2eq. This excludes the embodied emissions of the GPUs, which must be calculated separately. Nvidia does not disclose the carbon footprint of its GPUs; recent estimates put the lower bound at approximately 150 kg of CO2eq, which is the number used.

Assuming a replacement rate of 6 years and 85% average usage (figures provided by IDRIS), this translates to approximately 0.056 kg CO2eq per hour of server time and 0.003 kg CO2eq per hour of GPU time. BLOOM training lasted a total of 1.08 million hours using, on average, 384 GPUs across 48 computing nodes. Embodied emissions associated with BLOOM training are therefore approximately 7.57 tonnes for the servers and 3.64 tonnes for the GPUs, a total of 11.2 tonnes of CO2eq. This does not include the embodied emissions of the rest of the computing infrastructure (network switches, cooling equipment and other devices powering the network), which are difficult to quantify without information on their distribution and usage.

### 4.2 Dynamic Power Consumption
Most existing research on ML carbon footprint has focused on the CO2 emissions from generating the electricity that powers model training, typically called dynamic consumption. It is calculated by multiplying the number of GPU hours by the thermal design power (TDP) of the GPUs and the carbon intensity of the energy grid. TDP is an upper bound of GPU power consumption but is often used as a proxy when real-time GPU power consumption cannot be accessed. A grid's carbon intensity depends on its electricity source; coal-powered grids emit more carbon per kWh than grids powered by hydroelectricity or solar. Although many compute providers carry out post hoc carbon offsetting or heat recycling, the authors do not take this into account, since they focus on direct emissions linked to dynamic power consumption. (Footnote: a percentage of the heat produced by the Jean Zay cluster is recuperated to supply the heat and cold exchange network of the Paris-Saclay urban campus.)

BLOOM training required a total of 1.08 million GPU hours on a hardware partition of Nvidia A100 SXM4 GPUs with 80GB of memory, which have a TDP of 400W. Real-time power consumption was not tracked, but GPU utilization was empirically observed to be very high, nearing 100%. CPU power usage is not considered: CPUs consume approximately 40 times less energy than GPUs and are less used during training. This gives an electrical consumption of 433,195 kWh during training; multiplied by the grid's carbon intensity of approximately 57 gCO2eq/kWh, this gives 24.69 tonnes of CO2eq emitted from dynamic energy consumption.

### 4.3 Idle Power Consumption
The ML community has focused on the energy of specialized hardware such as GPUs, but the broader infrastructure that maintains and connects this hardware also needs large amounts of energy; this is called idle consumption. The energy needed depends on the efficiency of the computing cluster and the configuration of devices. It can be partly reflected by the PUE (Power Usage Effectiveness) of the data centers, the approach used by Patterson et al. for estimating emissions of ML models such as T5 and GPT-3. However, PUE represents energy used for cooling and other overhead but does not account for the totality of energy consumed by data center infrastructure.

To estimate idle consumption, the authors compared the total energy consumption of idle devices on Jean Zay (network, GPUs, storage, cooling/heating and computation nodes) to the total consumption of the same devices while running the training code. Table 2 shows the results for the A100 partition used for BLOOM.

**Table 2: Breakdown of power consumption of the A100 partition of the Jean Zay cluster**

| Computing mode | Power consumption | Percentage of total |
|---|---|---|
| Infrastructure consumption | 27 kWh | 13.5% |
| Idle consumption | 64 kWh | 32% |
| Dynamic consumption | 109 kWh | 54.5% |
| Total consumption | 200 kWh | 100% |

(Row-value alignment was garbled in extraction; the values follow the text: infrastructure 27 kWh, idle 64 kWh, training average over 109 kWh.) Infrastructure mode measures power consumed by networking systems, datacenter maintenance and cooling systems (servers turned off). Idle measures power consumed by servers turned on but unused. Dynamic measures power consumed by servers actively training BLOOM.

In Infrastructure mode (compute nodes off, but network, storage and cooling on), consumption was 27 kWh; in Idle mode (network, storage and compute nodes on, no processes running), 64 kWh. During BLOOM training, consumption averaged over 109 kWh. Only around 54% of power consumption can be attributed to running the code (the dynamic consumption of Section 4.2), while the remaining 46% keeps the computing nodes on. Multiplied by total training time, this adds 256,646 kWh of idle power consumption on top of the dynamic power used for training BLOOM, and 14.6 tonnes of CO2eq to the carbon footprint of model training.

The authors argue that although this is a large overhead, accounting for embodied and idle emissions better reflects the true emissions of training than considering only GPU dynamic consumption, since it includes the network overhead and larger computing infrastructure without which training cannot take place.

**Table 3: Breakdown of CO2 emissions from different sources of the BLOOM model life cycle**

| Process | CO2 emissions (CO2eq) | Percentage of total emissions |
|---|---|---|
| Embodied emissions | 11.2 tonnes | 22.2% |
| Dynamic consumption | 24.69 tonnes | 48.9% |
| Idle consumption | 14.6 tonnes | 28.9% |
| Total | 50.5 tonnes | 100.00% |

These figures are similar to product carbon footprint estimates for computing equipment (such as the HPE servers in Section 4.1), which estimate that embodied emissions account for approximately 20-30% of life cycle emissions, whereas use (dynamic plus idle consumption) is 70-80% of the total footprint. These estimates are limited to BLOOM training; the next section analyses deployment.

### 4.4 Deployment and Inference
To estimate the emissions of deploying BLOOM, the authors ran the CodeCarbon tool on a Google Cloud Platform (GCP) instance with 16 Nvidia A100 40GB GPUs, where BLOOM was deployed via an inference API, and tracked energy usage for approximately 18 days. The model received an average of 558 requests per hour, handled in real time (without any batching), for 230,768 requests in total. This is not representative of all deployment use cases, but is an example of real-time deployment in applications such as chatbots responding to a constant, varying flux of user queries. It is a useful data point for ML inference emissions, which have not been the focus of much research.

**Power draw (Figure 2).** Figure 2 plots the fluctuation of mean power used by the 16 Nvidia A100 GPUs running the BLOOM API, with mean power consumption of 1664 W. Over the 18 days, the power consumed by the compute instance fluctuated between 1252 W and 2735 W; divided by 16 GPUs, this is 78-171 W per GPU, significantly less than the TDP of this GPU type (400 W). The GPUs are not used at maximum capacity, which is coherent with API deployment: because inference requests are unpredictable, memory optimization techniques such as batching and padding (the norm during training) are not possible, and GPUs remain idle between user requests.

**Energy breakdown and idle draw (Figure 3).** In total the instance used for the BLOOM API consumed 914 kWh: 22.7% by the RAM (207.2 kWh), 2% by the CPU (18.5 kWh) and 75.3% by the GPU (688.38 kWh). Idle versus dynamic consumption cannot be disaggregated because the authors lacked access to the GCP platform as they had for Jean Zay, but energy can be compared with the number of requests. Figure 3 plots the requests received in a 10 minute interval against the instance's energy consumption in that interval: even when there are almost no incoming requests, about 0.28 kWh is consumed during the interval, which represents the energy consumption of the model when not responding to user requests. The authors highlight the high proportion of energy dedicated to maintaining an LLM like BLOOM in memory (approximately 75% of the instance's total energy) without it being used.

**Emissions.** The GCP instance runs in the us-central1 region, with a carbon intensity of 394 gCO2eq/kWh, giving approximately 19 kg of CO2eq emitted per day of API deployment, or 340 kg over the whole tracking period.

**Context.** Many configurations are possible for deploying ML models (hardware, inference batch size, region), so this use case is one among many, but it is a useful starting point. A 2019 article estimated that 80-90% of Nvidia's ML workload is inference processing, a figure cited by Patterson et al.; a recent Meta publication (Wu et al.) reported that inference accounted for approximately one-third of their end-to-end ML carbon footprint, the remainder owing to data management, storage and training. The authors hope these rough estimates shed light on this question.

## 5 Discussion and Future Work

The main contribution is to define and connect the different sources of carbon emissions involved in training and deploying BLOOM. The calculations remain estimates based on available information. This section compares BLOOM to similar LLMs, estimates the dynamic consumption of all BigScience processes, and discusses next steps.

### 5.1 Comparisons with Other LLMs
Several LLM papers reported the carbon footprint of training, including OPT-175B, GPT-3 and Gopher. Because accounting methodologies are not standardized, precise comparison is hard. Table 4 disentangles (1) energy consumption of training, (2) CO2eq emissions from dynamic consumption during training, and (3) CO2eq emissions from dynamic consumption including datacenter PUE (overhead). Some numbers in the original table were italicized, indicating values inferred from the model papers rather than stated explicitly.

**Table 4: Comparison of carbon emissions between BLOOM and similar LLMs**

| Model | Parameters | Datacenter PUE | Carbon intensity of grid | Power consumption | CO2eq emissions | CO2eq emissions x PUE |
|---|---|---|---|---|---|---|
| GPT-3 | 175B | 1.1 | 429 gCO2eq/kWh | 1,287 MWh | 502 tonnes | 552 tonnes |
| Gopher | 280B | 1.08 | 330 gCO2eq/kWh | 1,066 MWh | 352 tonnes | 380 tonnes |
| OPT | 175B | 1.09 | 231 gCO2eq/kWh | 324 MWh | 70 tonnes | 76.3 tonnes |
| BLOOM | 176B | 1.2 | 57 gCO2eq/kWh | 433 MWh | 25 tonnes | 30 tonnes |

BLOOM training resulted in less than half the emissions of the closest comparable model, OPT (70 tonnes vs BLOOM's 25 tonnes), and 20 times less than GPT-3 (502 tonnes). This is explained largely by the carbon intensity of the energy source: Jean Zay's grid is 57 gCO2eq/kWh, versus 231 for OPT, 429 for GPT-3 and 330 for Gopher. In raw energy, BLOOM consumed slightly more than OPT (433 MWh vs 324 MWh) despite similar size and training setup. Other factors matter too, such as hardware type, number of tokens seen and model architecture, so exact comparison is difficult.

The accounting approach of Patterson et al. includes datacenter PUE, which is not always taken into account by other papers. Since PUEs of datacenters used for training are relatively efficient and similar (1.08-1.2), their contribution to overall footprint is relatively small. However, these numbers are a small part of the actual emissions and environmental impacts of training ML models, since they reflect neither embodied emissions nor emissions from inference and deployment.

### 5.2 Carbon Footprint of the BigScience Workshop
Training the 176B parameter BLOOM represents only part of the experiments run on Jean Zay as part of BigScience. All experiments by project members add up to 3.46 million GPU hours (2.2 million hours on V100 GPUs and 1.24 million hours on A100 GPUs), representing 1,163,032 kWh of electricity and approximately 66.29 tonnes of CO2eq via dynamic power consumption. Table 5 gives the breakdown.

**Table 5: Breakdown of dynamic energy consumption and CO2 emissions of different parts of the BigScience project**

| Process | Energy consumed (kWh) | CO2 emissions (tonnes CO2eq) | Percentage of total emissions |
|---|---|---|---|
| 176B BLOOM Model | 433,196 | 24.69 | 37.24% |
| 104B Model | 266,522 | 15.19 | 22.92% |
| 1B Model | 158,972 | 9.06 | 13.68% |
| 13B Model | 87,210 | 4.97 | 7.49% |
| Other Models | 64,257 | 3.66 | 5.53% |
| Miscellaneous Processes | 57,961 | 3.3 | 4.98% |
| 6B Model | 51,686 | 2.95 | 4.45% |
| Model Evaluation | 43,172 | 2.46 | 3.71% |
| Total | 1,163,088 | 66.29 | 100.00% |


Experimenting with intermediate models (such as the 104B, 13B and 1B models) adds up to a total of 35.8 tonnes of CO2eq, more than the training of the final model. This is slightly higher than the OPT authors' statement that their model's total carbon footprint is roughly 2 times higher due to experimentation, baselines and ablations. Training these models allowed the team to converge on the architecture and hyperparameters of final BLOOM, and many intermediate models were shared with the community (e.g. BLOOM 1B and BLOOM 3B). Model evaluation emitted 2.46 tonnes of CO2eq, and miscellaneous processes such as benchmarking, data processing and tokenization 3.3 tonnes. These are not part of model training itself, but the authors consider it important to estimate and report them.

Including embodied emissions of these processes (3.46 million GPU hours) adds 35.9 tonnes of CO2eq. Adding the embodied emissions and idle consumption of equipment (per the percentages in Section 4.3, this accounts for a further 73.32 tonnes of CO2eq) brings the total to 123.82 tonnes of CO2eq. The additional experiments also produced several LLMs that were shared and deployed, and these continue to generate emissions during deployment and usage, which the authors cannot account for and keep in mind as a further addition.

### 5.3 Future Work
Many questions remain unanswered for lack of data.

**Gathering more precise figures regarding embodied emissions.** The closest available figures were used for embodied emissions of the GPUs used for BLOOM; exact hardware figures were unavailable, so the numbers are estimates. More transparency is needed regarding the environmental impacts of manufacturing computing equipment, given the large quantities of chemicals and minerals required, the significant quantities of ultra-pure water and energy needed, and the complex, carbon-intensive supply chains and transportation involved in shipping them around the world.

**Running additional studies on model inference and deployment.** The Section 4.4 results barely scratch the surface of the complexity of deploying, scaling and maintaining ML models in practice and in real time. Bridging the gap between chip designers and users can help, as can more empirical studies testing different hardware setups and configurations and how they affect energy consumption and carbon emissions.

**Advocating for increased transparency and granularity in carbon reporting.** Some papers introducing ML models have begun reporting CO2 emissions, which the authors applaud, but disaggregating this single figure into energy consumption, carbon intensity and PUE is needed for meaningful comparisons between models. Tallying and reporting emissions attributable to research and development, as well as evaluation and benchmarking, helps contextualize the relative contribution of final model training.

**Considering the broader impacts of ML.** Environmental impacts of ICT are classified into 3 categories: computing-related impacts (hardware manufacturing and electricity consumption), indirect impacts of deploying the models, and system-level impacts on other domains (Kaack et al.). This article and the studies in Section 2 focus solely on direct impacts. It can be useful to consider indirect impacts on industries such as transportation, agriculture or urban planning, given increased reliance on ML in these sectors. The paper also does not discuss ML's impact on changing consumer behaviors, for instance more use of smart speakers or connected devices to do tasks previously done by hand. These impacts are harder to quantify but worth including in the broader environmental impacts of ML.
