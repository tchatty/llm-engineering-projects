### Retrieval Evaluation: Questions and Excerpts

1. **How do we understand AI’s net effect on incumbent energy systems?**   
     
   S1, Section: Net-Climate Impacts of AI  
     
   Excerpt:  
   At a systemic level, this raises the question of whether AI’s net effect reinforces or displaces incumbent energy systems. We characterize displacement as the following: eroding fossil supply economics, reducing total fossil consumption, and reducing economic activity within fossil-embedded systems; reinforcement is the inverse. The answer has significant implications for energy transition pathways, given that AI is enhancing productivity within an energy-economic system still anchored in fossil fuels. Answering this systemic question is complicated by two compounding mechanisms  
   through which AI’s applications generate indirect, system-wide emissions effects. First, productivity gains from digital optimization frequently generate rebound effects, defined as efficiency improvements that stimulate additional consumption16. Second, AI’s impacts extend beyond these familiar dynamics to lesser-studied induction effects, in which new technological options reshape production economics by altering capital, labor, and resource productivity17. Together, rebound and induction effects suggest that AI’s most consequential climate impacts may arise through indirect, economy-wide channels.  
     
     
2. **What are the limitations of existing approaches to quantify the net impacts of AI?**  
     
   S1, Section: Net-Climate Impacts of AI  
     
   Although these indirect, system-wide impacts of its applications may substantially exceed AI’s comparatively well-studied direct operational footprint from computational infrastructure14,18–20, they remain largely unquantified21,22. This gap is visible in three limitations of existing methodological approaches. First, industry and solution-oriented assessments predominantly emphasize the potential of emissions-reducing applications, often leaving emissions-increasing uses outside the defined analytical boundary23,24. Second, prevailing quantitative frameworks are not designed to capture economy-wide, cross-sector dynamics. Partial-equilibrium approaches risk underrepresenting economy-wide feedbacks25; avoided-emissions methodologies omit system-level rebound and induction effects within their stated boundaries26; and even net carbon impact approaches that identify AI-enabled fossil expansion as a higher-order mechanism acknowledge that rigorous quantification remains beyond their present scope27. Third, the climate modeling architectures most commonly used for long-term projections, including Integrated AssessmentModels (IAMs), are less suited to resolving the near-term, cross-sector supply dynamics through  
   which AI reshapes competing energy pathways28. An extended discussion of these gaps is provided in SI Note S2.2.  
     
     
3. **Do net global emissions from AI adoption increase or decrease?**  
     
   S1, Section: Net global emissions increase under parallel adoption  
     
   Under parallel adoption assumptions—a neutral benchmark representing all pathways at the same adoption tier (a methodologically conservative simplification; see “Methods”)—AI-driven productivity increased net global annual CO2 emissions by 0.47–1.8 Gt, equivalent to 1.2–4.8% of total global energy-related CO2 emissions in 20245\. Isolating individual pathways revealed that fossil fuel productivity gains were the primary contributor to the net increase, while renewables optimization offset only part of that effect, as illustrated in Fig. 2\.  
     
   Enabled emissions (0.6–2.4 Gt CO2 annually) exceed the IEA’s 2025  
   datacenter emissions estimates (0.18 Gt CO2 annually)14 by 3.3–13.3×, and  
   its projected 2035 datacenter emissions (0.3–0.5 Gt CO2 annually) by 1.2–8×  
   (Fig. 2). This contextualizes magnitude only; it is not an aggregation across  
   analytical frameworks. Modeled net second-order effects under parallel  
   adoption exceed the IEA’s 2025 datacenter estimates across all modeled  
   scenarios and their projected 2035 estimates across most (see SI Note S2.3).  
     
   S7, Section: Introduction  
     
   Several dynamic trends are driving AI emissions in opposing directions. Algorithmic efficiency for a given level of performance has roughly halved every eight months (Ho, et al., 2024), and inference-side optimizations (e.g., batching, KV and prompt caching, speculative decoding, quantized inference) and optimized software and hardware co-design can dramatically reduce per-query energy. At the same time, AI use is shifting toward higher per-task compute intensity with reasoning models generating extended inference; multi-modal systems handling text, image, audio, and video; and agentic systems executing multi-step workflows autonomously, which means that a single request triggers many model calls.  
     
     
4. **What are the embodied emissions associated with computing equipment required to train and deploy ML models?**  
     
   S2, Section: Results: Carbon Emissions of the BLOOM Model, Embodied Emissions

   The embodied emissions are those emissions associated with the materials and processes involved in producing a given product, such as the computing equipment needed to train and deploy ML models. While the production of these emissions is exclusively limited to the manufacturing process, this total amount is usually spread over the time during which equipment is used by dividing the total embodied emissions by the time of use. The BLOOM model was trained on HPE Apollo 6500 Gen10 Plus servers containing Nvidia A100 GPUs. The closest comparable computing equipment that provides LCA information is HPE’s ProLiant DL345 Gen10 Plus server, which is similar to the Apollo 6500 and has a production footprint of approximately 2500 kg of CO2eq \[13\]. This does not include the embodied emissions of the GPUs which are used in the server, whose embodied emissions must be calculated separately. While Nvidia does not currently disclose the carbon footprint of its GPUs, recent estimates put the lower bound of this amount at approximately 150 kg of CO2eq \[9\], which is the number we will use for our embodied emissions estimates.  
   Assuming a replacement rate of 6 years and 85% average usage (which are the figures provided to us by IDRIS), the figures above translate to an embodied carbon footprint of approximately 0.056 kg of CO2eq for each hour of server time and 0.003 kg of CO2eq for each hour of GPU time. Given that BLOOM training lasted a total of 1.08 million  
   hours using, on average, 384 GPUs across 48 computing nodes, we can estimate that the embodied emissions associated to BLOOM training represent approximately 7.57 tonnes for the servers and 3.64 tonnes for the GPUs, adding a total of 11.2 tonnes of CO2eq to its carbon footprint. This does not include the embodied emissions of the rest of the computing infrastructure (e.g. the network switches, cooling equipment and other devices that power the network), which are difficult to quantify given that we do not have the necessary information regarding their distribution and usage.  
     
   S4, Section: Need for Comparative Evaluation Capability  
     
   More specifically, embodied impacts are driven by the fabrication of integrated circuits including high-performance processors and high-density memory semiconductor devices. Water consumption is correlated with electricity consumption throughout the life cycle and device manufacture. Whether cost is higher for embodied versus operational phases is determined by whether computations are occurring on a datacenter or an  
   edge device. Computing sector GHG emissions will likely shift more toward embodied emissions dominance for both consumer devices and datacenters as computing hardware becomes increasingly efficient, software and algorithms are optimized, and cleaner energy is used to power datacenter operations (Das and Mao 2020; Belkhir and Elmeligi 2018). For this reason, measuring impact not only for carbon and energy, but also across multiple environmental metrics will become critical (for example, the EU Product Environmental Footprint guidelines recommend nineteen impact categories).

   

5. **How are the emissions produced by electricity powering model training quantified?**  
     
   S2, Section: Dynamic Power Consumption  
     
   This is calculated by multiplying the number of GPU hours used by the thermal design power (TDP) of those GPUs and the carbon intensity of the energy grid used to power the hardware. TDP remains an upper bound of GPU power consumption, but it is often used as a proxy given when access to real-time GPU power consumption is impossible. A grid’s carbon intensity depends on the electricity source that powers it – for instance, coal-powered grids result in more carbon emissions per kWh of electricity compared to grids powered by hydroelectricity or solar power. Also, while many compute providers carry out post hoc carbon offsetting or heat recycling, we do not take this into account in our estimation, given that we are focusing on the direct carbon emissions linked to dynamic power consumption  
     
     
6. **How is idle power consumption of the computing infrastructure used for training quantified?**  
     
   S2, Section: 4.2 Idle Power Consumption  
     
   In order to estimate the idle consumption of the computing infrastructure that we used for training BLOOM, we ran a series of experiments to compare the total energy consumption of idle devices on the Jean Zay computing cluster (e.g. network, GPUs, storage, cooling/heating and computation nodes) to the total consumption of the same devices while running the model training code. As we show in Table 2, we found that for the A100 partition of the cluster used for training the model, in Infrastructure mode (with the computing nodes turned off but the network, storage and cooling turned on), the power consumption was 27 kWh; in Idle mode (with network, storage and compute nodes on, but no processes running), the power consumption was 64 kWh. During BLOOM training, power consumption averaged at over 109 kWh. This indicates that only around 54% of the power consumption can be attributed to running the code (i.e. the dynamic power consumption described in Section 4.2), whereas the remaining 46% is used for keeping the computing nodes on. Multiplying this by the total training time, this adds a further 256,646 kWh of idle power consumption on top of the dynamic power used for training BLOOM, and 14.6 tonnes of CO2eq to the overall carbon footprint of model training.  
     
7. **What is Power Usage Effectiveness (PUE)?**  
     
   S2, Section: Idle Power Consumption  
     
   So far, the emphasis in the ML community has been on estimating the energy consumption and ensuing carbon emissions of the energy used to power specialized hardware such as GPUs. However, it is important to keep in mind that the broader infrastructure that maintains and connects this hardware also requires large amounts of energy to power it – this is referred to as idle consumption. The quantity of energy needed for this depends on the efficiency of the computing cluster that is being used and the configuration of the devices on the cluster. This can be reflected in part by factoring in the PUE (Power Usage Effectiveness) of the data centers used for training these models, which is the approach adopted by Patterson et al. for estimating the carbon emissions of ML models such as T5 and GPT-3 \[28\]. However, while PUE is a useful metric for representing the amount of energy used for cooling and other overhead, it does not account for the totality of energy consumed by the data center infrastructure \[6, 17\].  
     
8. **How do the impacts of inference compare to model training?**  
     
   S3, Section: Introduction  
     
   While inference on a single example requires much less computation than that required to train the same model, inference happens far more frequently than model training — as many as billions of times a day for a model powering a popular user-facing product such as Google Translate.1 Yet, in-depth work quantifying the costs of model inference and deployment is limited and their environmental impacts, in terms of energy and carbon as well as water and mining of rare earth minerals, have yet to be estimated. According to AWS, the largest global cloud provider, inference is estimated to make up  
   80 to 90% of total ML cloud computing demand \[2, 28\], whereas a 2021 publication by Meta attributed approximately one-third of their internal end-to-end ML carbon footprint to model inference, with the remainder produced by data management, storage, and  
   training \[57\]; similarly, a 2022 study from Google attributed 60% of its ML energy use to inference, compared to 40% for training \[40\].  
     
   Given the increasing ubiquity of AI model deployment, it is crucial to go beyond these high-level statistics to get a better idea of the energy requirements and carbon emissions of model inference for different models and tasks. In particular, looking at inference  
   rather than training leads to drastically different conclusions when considering the multi-purpose (or “general-purpose”) aspect specifically. Training a single model for multiple tasks can indeed be more energy-efficient when considering training costs only, but these gains can easily be lost and even reversed over the course of the model’s lifetime, given how much inference is carried out when these models are deployed in user-facing applications like chat and web search.  
     
   S3, Section: Comparing model training and inference costs  
     
   An important trade-off for many AI practitioners and policy-makers is determining when exactly model inference costs reach parity with model training (and fine-tuning) \- i.e. when does the deployment of models use as much energy as their initial training?  
     
   If we compare the amount of energy used per inference for each of the models with the total amount of energy used for both training and fine-tuning them, we can estimate how many inferences would be needed to be carried out with a given model in order for the  
   cost of inference to reach the cost of training. As can be seen in Table 5, this varies depending on model size: from around 200 million inferences for the smallest model, BLOOMz-560M, to over 590 million inferences for the biggest model, BLOOMz-7B. This may seem like a lot if a single instance of a model is deployed, but can add up quickly if there are multiple instances of models deployed in parallel. For instance, it has been estimated that, at its peak, ChatGPT had upward of 10 million users per day \[36\]; the most recent statistics indicate that the ChatGPT login page received 1.7B visits in October 2023\. Even assuming a single query per user, which is rarely the case, the energy costs of deploying it would surpass its training costs after a few weeks or months of deployment.  
     
   S7, Section: Areas of emerging consensus  
     
   Inference can dominate lifetime emissions for many models, especially as reasoning and agentic models become more prevalent. Agentic and reasoning workflows (e.g., multi-step model chains, tool use, self-reflection loops) can multiply per-task emissions by orders of magnitude relative to a single-turn query, while variation across input and output modalities (text, image, audio, and video) adds further spread in energy and carbon intensity.  
     
9. **What is the variability of energy consumption across different types of inference tasks?**  
     
   S3, Section: Task-specific model analysis  
     
   We can see that classification tasks for both images and text are on the lower end of the spectrum in terms of emissions (ranging between 0.002 and 0.007 kWh for 1,000 inferences), whereas generative tasks such as text generation and summarization use, on average, over 10 times more energy for the same number of inferences (around 0.05 kWh for 1,000 inferences), and multimodal tasks such as image captioning and image generation are on the highest end of the spectrum (0.06-2.9 kWh for 1,000 inferences). Text-based tasks are, all things considered, more energy-efficient than image-based tasks, with image classification requiring less energy (median of 0.0068 kWh for 1,000 inferences) than image generation (1.35 kWh) and, conversely, text generation (0.042 KwH) requiring more than text classification (0.0023 kWh).  
     
   We can also observe that there is a large variation in the amount of energy used, from the least energy-intensive task, text classification, with mean consumption of 0.002 KwH per 1,000 inferences, to the most energy-intensive one, image generation, whose mean consumption is 2.9kWh. This means that the different models examined in our study can vary by a factor of over 1450 in terms of the energy required to perform the same number of inferences.  
     
10. **What are the challenges to quantifying energy consumption during inference?**  
      
    S5, Section: Introduction  
      
    Public reports of ‘‘energy per query’’ differ by more than an order of magnitude. Two issues drive this discrepancy. First, measurement boundaries vary—some account only for GPU draw, and others include CPUs or application overhead. Second, many benchmarks fail to capture realistic production conditions such as batching, concurrency, and steady-state serving.5–7 Model-based estimates are also highly sensitive to assumptions about hardware specifications, parameter counts, and token lengths.8–10 Direct measurements, although more precise, are often tied to non-production models or small-batch tests.6 These settings tend to overestimate energy use relative to large, high-concurrency deployments, which handle most artificial intelligence (AI) inference workloads.  
      
    An added challenge to characterizing inference energy is that per-query figures cannot be interpreted in isolation. The energy used in inference also depends on how energy demand scales when billions of queries are served and how interventions at the model, serving software, and hardware layers can moderate that growth. Recent model provider disclosures offer a more realistic baseline2,11 by measuring large-scale systems but remain limited by confidentiality. Typically, these reports only include a single ‘‘representative’’ or ‘‘average query,’’ masking how energy use changes with query-length distributions and model and serving configurations. This limitation is significant; test-time scaling (reasoning models) and agentic workflows are increasingly routine, and their long outputs can drive a disproportionate share of aggregate energy demand. Without this system context, averages give a misleading picture of energy use in inference. Furthermore, such metrics fail to provide guidance on where future efficiency efforts should focus.  
      
      
      
      
      
     