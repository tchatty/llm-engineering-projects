# The Climate and Sustainability Implications of Generative AI

Authors: Noman Bashir, Priya Donti, James Cuff, Sydney Sroka, Marija Ilic, Vivienne Sze, Christina Delimitrou, Elsa Olivetti (MIT)
Publication Year: 2024 (published Mar 27, 2024, as part of "An MIT Exploration of Generative AI: From Novel Chemicals to Opera"; stated on the title page; filename attributes it to Olivetti et al.)
Source: MIT Exploration of Generative AI (MIT Climate and Sustainability Consortium), https://mit-genai.pubpub.org/pub/8ulgrckc; license CC-BY-NC 4.0
Keywords: generative AI, Gen-AI, sustainability, climate, datacenter electricity demand, embodied and operational emissions, life cycle assessment (LCA), benefit-cost evaluation framework, Jevons paradox, rebound effects, regulation, stakeholder engagement (keywords derived from content)

## Executive Summary

This MIT position paper argues that the rapid, largely unfettered growth of generative AI (Gen-AI) is driven by four contemporaneous factors: perceived benefits, consolidation of AI capability in a few large firms, limited regulatory oversight, and efficiency improvements in hardware, algorithms and datacenters. The authors contend that this trajectory neglects negative environmental effects: rising computing and electricity demand, larger carbon footprints, shifting electricity demand patterns, and accelerated depletion of natural resources. Datacenter capacity under construction in North America rose from 2,688 MW (end of 2022) to 5,341 MW (end of 2023). Global datacenter electricity consumption rose from 194 TWh (2010) to 204 TWh (2018), a 6% rise despite a 6x capacity increase thanks to efficiency gains, but then reached 460 TWh in 2022 and is projected by the IEA to reach 620-1,050 TWh in 2026 (base case just over 800 TWh).

The paper's central claim is that efficiency improvements alone (hardware energy efficiency, algorithmic refinement, carbon-aware spatiotemporal workload shifting) are insufficient and can even exacerbate the problem through rebound effects and the Jevons paradox, because they encourage further growth. Responsible development instead requires sustainability considerations beyond efficiency and benefit-cost evaluation frameworks that encourage or require Gen-AI to support social and environmental sustainability goals alongside economic opportunity.

The authors outline elements of such a comparative benefit-cost framework, aligned with life cycle assessment (LCA) but going beyond it: (1) scope and boundaries (goal, unit of analysis/functional unit, conceptual, geographic and temporal boundaries, consequential analysis and "relational footprinting"); (2) baselines and scenarios (business-as-usual baselines per application, benchmarks, scenario variables, thresholds based on planetary and social carrying capacity, lessons from voluntary carbon markets: additional, verifiable, immediate, durable); and (3) data and inventory (FAIR data principles, Scope 1/2/3 accounting, separating training, tuning and inference in the use phase). Costs are classed as computing-related (first-order, cradle-to-grave: embodied and operational), immediate application-related, and system-level (rebound, lock-in, consumption acceleration, misinformation). Two illustrative applications are sketched: scientific discovery (chemicals/materials) and search (a hypothetical "SearchAId" GPT-based search versus a CPU-based Google search).

The paper then describes the roles of stakeholders (leadership teams, policymakers and legal experts, AI practitioners and engineers, energy and supply chain sectors, economists, social scientists, civil society) in building this capability. It concludes that Gen-AI is emerging as a distinct sector warranting dedicated monitoring, that policies should rest on scientific evidence rather than solely economic ambition, and advocates "slow urgency" instead of a Klondike-gold-rush pace, aligning technological progress with environmental sustainability and social well-being. The authors acknowledge that a complete framework is beyond the paper's scope and that comprehensive benefit-cost analysis is complex and requires coordination across diverse stakeholders.

## Abstract

The rapid expansion of generative artificial intelligence (Gen-AI) is propelled by its perceived benefits, significant advancements in computing efficiency, corporate consolidation of artificial intelligence innovation and capability, and limited regulatory oversight. As with many large-scale technology-induced shifts, the current trajectory of Gen-AI, characterized by relentless demand, neglects consideration of negative effects alongside expected benefits. This incomplete cost calculation promotes unchecked growth and a risk of unjustified techno-optimism with potential environmental consequences, including expanding demand for computing power, larger carbon footprints, shifts in patterns of electricity demand, and an accelerated depletion of natural resources. This prompts an evaluation of our currently unsustainable approach toward Gen-AI's development, underlining the importance of assessing technological advancement alongside the resulting social and environmental impacts.

Presently, efforts to boost computing sustainability largely focus on efficiency improvements, including enhancing hardware energy efficiency, refining artificial intelligence algorithms, and improving the carbon efficiency of executing computing workloads through spatiotemporal workload shifting. In the presence of relentless demand and prioritization of economic growth, this siloed focus on efficiency improvements results instead in increased adoption without fundamentally considering the vast sustainability implications of Gen-AI. The authors argue that responsible development of Gen-AI requires a focus on sustainability beyond only efficiency improvements and necessitates benefit-cost evaluation frameworks that encourage (or require) Gen-AI to develop in ways that support social and environmental sustainability goals alongside economic opportunity. However, a comprehensive value consideration is complex and requires detailed analysis, coordination, innovation, and adoption across diverse stakeholders. Engaging stakeholders, including technical and sociotechnical experts, corporate entities, policymakers, and civil society, in a benefit-cost analysis would foster development in directions that are most urgent and impactful while also reducing unsustainable practices.

## 1. Unfettered Growth and Its Drivers

### 1.0 Overview: Gen-AI growth and rising datacenter demand

Generative AI (Gen-AI) has become a ubiquitous, global phenomenon, with significant increases in the number and diversity of use cases (Chui et al. 2023). This specific, albeit disruptive, set of machine learning (ML) algorithms has captured the mind share of researchers, scientists and corporations, comparable to the Klondike gold rush at the dawn of the twentieth century. Many predict the end of the AI winter and the dawn of a new age of intelligence. However, the reality behind this excitement is more complex.

- The growth of Gen-AI is driving increased electricity demand, which runs counter to the massive efficiency gains needed to achieve net-zero greenhouse gas emissions by 2050 in energy-related sectors (alongside simply "greening the grid") (IEA 2021).
- Current capacity to build sustainably cannot keep pace with the datacenter construction necessary to support Gen-AI.
- Explosive growth exacerbates supply chain issues, affecting essential goods and services that rely on the tech industry and potentially creating macroeconomic impacts.

Quantitative data on datacenter demand:

| Metric | Value | Source cited |
|---|---|---|
| North American datacenter capacity under construction (power requirement), end of 2022 | 2,688 MW | Beets and Hartnett 2024 |
| North American datacenter capacity under construction, end of 2023 | 5,341 MW | Beets and Hartnett 2024 |
| Additional expected co-location capacity from existing demand | 12,000 MW (exceeds demand of over 70% of countries) | Uptime 2024; GlobalEconomy.com 2021 |
| Global datacenter energy demand, 2010 | 194 TWh | Masanet et al. 2020 (conservative estimates) |
| Global datacenter energy demand, 2018 | 204 TWh (a 6% growth despite a 6x increase in datacenter capacity, primarily due to massive energy efficiency gains) | Masanet et al. 2020 |
| Global datacenter electricity consumption, 2022 | 460 TWh | IEA 2024 |
| Projected global datacenter electricity consumption, 2026 | 620-1,050 TWh range; base case just over 800 TWh | IEA 2024 |

The 2026 range depends on efficiency improvements, cryptocurrency trends and artificial intelligence demand; the base case reflects demand that outpaces even the most optimistic forecasts of technological improvements. The authors note the current pace of energy consumption growth is potentially under-reflective of actual demand, given limits on AI chip availability, multi-year lead times for datacenter equipment (Uptime 2024), and power availability constraints (Beets and Hartnett 2024).

A contemporaneous alignment of several factors beyond Gen-AI's perceived benefits (consolidation of AI power, limited regulatory oversight, and efficiency improvements) may explain this unbounded growth. Dissecting these enablers identifies key stakeholders who shape Gen-AI's trajectory, which provides context for Section 3 (stakeholder responsibilities).

### 1.1 Perceived Benefits of Generative AI

Popular implementations of Generative Pre-trained Transformer (GPT) models allow rapid inference packaged in easy-to-use interfaces, capturing global attention. By inputting simple text prompts, a user is instantly presented with what appears to be a magical output; it may seem that endless knowledge, images and information can be generated at one's fingertips. Beyond leisure use, there is genuine optimism that Gen-AI will unlock large-scale efficiency gains, productivity enhancements and innovations (Knight 2023). The hype implies no sector will forgo Gen-AI's transformative benefits (Chui et al. 2023).

Despite this potential, there is growing realization that not every Gen-AI application will be inherently beneficial or realize anticipated advantages (Nature editorial 2024; Bender et al. 2021). Stakeholders from technology giants to startups invest heavily, but this investment is often predicated on optimism that may not align with practical outcomes. In the worst case:
- Gen-AI's perceived benefits can be used as an argument for limited regulation of its direct impacts, or for delayed adoption of alternative sustainable approaches across sectors, even when expected benefits could be minor relative to environmental impact (Dauvergne 2022; Ipsen et al. 2019).
- Gen-AI applications can be actively counterproductive to society, for instance by facilitating the spread of misinformation or delaying the retirement of fossil fuel-based power plants (Kaack et al. 2022).

This highlights the need for a balanced perspective acknowledging potential, limitations and risks.

### 1.2 Consolidation of AI Capabilities

Gen-AI algorithm quality today correlates with the size of the required computing systems, requiring more or more powerful computers for more sophisticated data sets and models. Because the correlation appears simple, a few for-profit organizations (AI giants) deploy more datacenters and computing infrastructure than ever before.

- In Q3 2023, Microsoft and Meta each bought three times more NVIDIA graphics processing units (GPUs) than Amazon and Google, which acquired 50,000 units each (Norem 2023).
- Larger investment is perceived to bring higher quality and return on investment.
- AI giants consolidate power through strategic partnerships (Ward and Lung 2023), such as Microsoft with OpenAI and Amazon with Anthropic. This leads to global growth in model training and increased use of consumer-facing web-based inference engines.
- Capital, equipment, resources and energy are effectively viewed as fuel for Gen-AI algorithms, driving an insatiable need for more inputs, predominantly procured by these AI powerhouses.

Computational power also allows handling large, diverse datasets crucial for competitive edge (Clarke 2023; Kak and West 2023), e.g., Google's use of web data for BERT (Devlin et al. 2018) and OpenAI's varied text sources for GPT models (OpenAI 2023). This data control, coupled with its proprietary nature, is central to model development and a major focus of industry AI policy. Concentration of computing power and data also lets these giants attract top AI talent: at the end of 2022, Amazon, Microsoft and Meta employed more than 33,000 AI personnel, with almost 8,000 in core AI research scientist roles (glass.ai 2023), fostering a self-sustained innovation ecosystem.

Trade-off noted by the authors: consolidation could enable efficiency improvements and centralize reporting or auditing; but it makes it challenging to devise effective incentives and to increase the social sustainability of the technology, and has negative implications for the equity of technological trajectories and outcomes.

### 1.3 Limited Regulatory Oversight

Gen-AI growth has outpaced global regulatory efforts, leading to varied and insufficient oversight of socioeconomic and environmental impact (Jelinek, Wallach, and Kerimi 2021; Scherer 2015; West 2023).

- Many countries are passing regulatory measures, including the European Union (EU), South Korea, Brazil, Singapore and the United States (Kremer et al. 2023).
- The EU AI Act aims to address risks to health, safety, the environment and fundamental rights. It calls for robust and transparent accounting of emissions for AI systems but, like many other jurisdictions and sectors, has no explicit call to limit emissions.
- The Greenhouse Gas (GHG) Protocol, an essential international framework for managing emissions, fails to adequately address the technology sector's unique challenges (Becker et al. 2022; Mytton 2020), leading to substantial underreporting of GHG emissions by technology companies (Klaassen and Stoll 2021). Other social and environmental impacts, such as water usage, receive even less regulatory attention (Coeckelbergh 2021; Kak and West 2023).
- Fully characterizing the social and environmental impacts of Gen-AI is complex and hinders targeted regulation. Recent US initiatives, such as Executive Order 14030 (2021) on climate-related financial risk and the CHIPS Act (H.R.4346, 2021), highlight these issues but lack comprehensive guidelines for Gen-AI's broader impacts. The CHIPS Act, focused on semiconductor manufacturing, only indirectly addresses the tech industry's environmental responsibilities.
- Even where legislation exists, implementation may differ across regions, challenging regulators and risk management professionals given Gen-AI's rapid evolution (Cihon, Maas, and Kemp 2020; Kremer et al. 2023).

This scarcity of actionable regulation limits effective oversight, inadvertently enabling rapid adoption without sufficient environmental and social accountability. Adequate and targeted regulations require a comprehensive and comparative evaluation capability weighing Gen-AI's potential societal benefits against the costs of its unfettered growth.

### 1.4 Efficiency Improvements

Rapid performance growth of general-purpose GPUs, sophisticated low-latency and high-bandwidth communications, and specialized hardware (e.g., TPUs, Jouppi et al. 2017) have collectively enabled execution of large multibillion-parameter models in significantly reduced time.

- The transformer architecture (Vaswani et al. 2017) lets AI models scale to billions of parameters with a sublinear increase in associated computational costs.
- Mixture-of-Experts models optimized computational efficiency and allowed scaling to trillions of parameters with manageable computational requirements (Du et al. 2021; Shazeer et al. 2017).
- Efficient architectures combined with distributed training techniques such as pipeline parallelism facilitated giant Gen-AI models.
- ML training improvements include Adam optimization, dropout, batch normalization, transfer learning and fine-tuning.
- Hyperscale datacenter growth, capabilities and efficiency improvements, such as parallel processing, allowed significant increases in the implementation of large Gen-AI models, triggering further unbounded growth.

#### Efficiency gains have not reduced overall energy consumption (rebound effect and Jevons paradox)

These efficiency gains have not reduced Gen-AI's overall energy consumption because of rebound effects and the Jevons paradox (Hintemann 2018a; Masanet et al. 2020a). Furthermore, with tools such as ChatGPT and Bard expanding and 33% of the global population still offline (ITU 2023), demand and energy use are far from saturation. Academic and industrial research has focused on enhancing energy efficiency and carbon efficiency of computational technologies (e.g., carbon-aware datacenters and scheduling, workload elasticity). However, whereas efficiency gains remain critical, a narrow focus on them does not solve the problem; it can exacerbate it by encouraging further unbounded growth (Birhane et al. 2022; Giampietro and Mayumi 2018; Wright et al. 2023).

The current approach of growing the Gen-AI sector to satisfy every imaginable application considers neither what benefits have actually been realized in practice nor the extensive societal costs. The authors call for sustainable development of Gen-AI and propose a comparative benefit-cost evaluation framework as a potential approach toward responsible development.

## 2. Need for Comparative Evaluation Capability

### 2.0 Context and definition of costs

Recent legislative and regulatory efforts sharpen the focus on Gen-AI sustainability:
- The newly adopted US Securities and Exchange Commission (SEC) rules compel public companies to disclose material climate-related risks and their Scope 1 and Scope 2 emissions (SEC 2024).
- A bill proposed by Senator Ed Markey (Artificial Intelligence Environmental Impacts Act of 2024) pushes for closer examination of AI's environmental footprint.

These measures align with the authors' proposed evaluation framework, which aims to encompass a spectrum of costs (including sustainability) and benefits of Gen-AI across stakeholders and sectors. Stakeholders must assemble to provide guidance weighing societal benefits against societal costs. The guidance should offer a comprehensive, comparative evaluation capability including costs and perceived benefits across multiple stakeholders (individual, organizational or regional), sectors and contexts. Gen-AI costs extend beyond sustainability (labor, privacy, copyright infringement: Luccioni 2023), but this paper focuses primarily on sustainability-related costs. The authors use the term "cost" specifically to delineate negative impacts from benefits or positive impacts.

### 2.0.1 Three levels of costs: computing-related, application-related and system-level

**First-order (computing-related) costs.** These are direct computing-related impacts (Kaack et al. 2022) from cradle to grave: materials used for everything from individual semiconductors to datacenter infrastructure, manufacturing processes and distribution, energy to power computing devices, and waste management at end of product life. These result in energy, water and materials use as well as emissions to land, air and water, which can lead to depletion of natural resources and damage to human health and ecosystems. Accounting is typically done through life cycle assessment (LCA) (Finkbeiner et al. 2006; ISO 14040/14044), which includes steps to: define a study goal and scope, account for the life cycle inventory at each step, assess impact along a defined set of metrics, and interpret results. LCA provides basic guidelines but leaves much open to the practitioner. Stakeholders in a sector then define specific rules for a product or service, termed "product category rules" (Ingwersen and Subramanian 2014).

**Embodied vs. operational phases.** Although study differences make summary statements challenging, there is contemporary consensus that the highest computing-related costs are in the manufacturing (or embodied) phase and the use (or operational) phase, including datacenter cooling and infrastructure (Itten et al. 2020; Clement, Jacquemotte, and Hilty 2020).
- Embodied impacts are driven by fabrication of integrated circuits, including high-performance processors and high-density memory semiconductor devices.
- Water consumption is correlated with electricity consumption throughout the life cycle and device manufacture.
- Whether cost is higher for embodied versus operational phases depends on whether computations occur on a datacenter or an edge device.
- Computing sector GHG emissions will likely shift toward embodied emissions dominance for both consumer devices and datacenters as hardware becomes more efficient, software and algorithms are optimized, and cleaner energy powers datacenters (Das and Mao 2020; Belkhir and Elmeligi 2018).
- For this reason, measuring impact across multiple environmental metrics, not only carbon and energy, will become critical (e.g., the EU Product Environmental Footprint guidelines recommend nineteen impact categories).

**Application-related and system-level (consequential or indirect) costs.** Sustainability costs also include unintended consequences from use of models for an immediate application or broadly at a system or structural level (LCA practitioners call these consequential or indirect costs). Kaack et al. 2022 suggest costs result from: extending (or locking in) impact-intensive technologies, sectors and energy sources; accelerating consumption through consumer behavior; and miseducation through faster spread of climate-negative information. System-level impacts induced by Gen-AI include those relevant to any innovation: rebound, rematerialization, learning and scale effects, technology evolution, or cultural shifts. Costs dominate the computing-related impacts, whereas immediate applications and system-level impacts can result in benefits (Rolnick et al. 2022) and/or costs depending on the application.

A framework to assess intended benefits and costs must balance quantitative data with qualitative assessments. The authors suggest three framework elements: defining scope and boundaries, developing baselines and scenarios, and building a data inventory for accounting, with examples of existing frameworks that could be leveraged, adopted or adapted. Articulating a complete framework is beyond the paper's scope; it provides starting points for collaborative investigation by the Gen-AI and industrial ecology communities and broader stakeholders.

### 2.1 Scope and Boundaries

Estimating benefit and cost should align with LCA methodology (but leverage methods beyond LCA), beginning by articulating the analysis goal and scope: the intended audience and desired metrics, a unit of analysis (to enable comparison), and the conceptual, geographic and temporal boundaries.

#### Unit of analysis (functional unit and reference flow)

An essential criterion for comparability is the unit of analysis, based on the desired performance (termed "functional unit" in LCA) and the amount of a product or service required to meet that performance (termed "reference flow" in LCA; e.g., a volume of paper bag for carrying groceries) (Andrae and Andersen 2010). There are several ways to develop functional units; recent work recommends a practiced approach for screening multiple options (Furberg, Arvidsson, and Molander 2022). Within Gen-AI, a unit of analysis could be a query result. The functional unit is translated to a reference flow, such as floating-point operations per unit of power to deliver that result, informed by hardware type, task type, model used and dataset characteristics (including product power draw and system infrastructure and inefficiencies) (Debus et al. 2023).

#### Boundaries: temporal, geographic and conceptual

Defining boundaries completely and consistently is essential for comparative evaluation but tremendously complex, especially for Gen-AI given interdependent supply chains and cascading application implications.
- Temporal boundaries: should be short in duration and revisited frequently, given the pace of Gen-AI development and adoption.
- Geographic boundaries: can be guided by spatial delineation where data are currently collected, then broadened or made more granular depending on study goal.
- Conceptual boundaries: the most challenging (computing-related and application-related, including immediate application and system level; Kaack et al. 2022). Boundaries that account for application-related impact (benefit and cost) are informed by "what has changed" from introducing a product, technology or service. The LCA community calls this consequential analysis, which accounts for what has been "displaced" (Weidema 2003). It defines the main affected marginal player in both short and long term; determining this marginal impact (the displaced or competing product) is the most important aspect. The conceptual boundary includes material and energy flows directly or indirectly affected by the change. Marginal effects are critical in cases of constrained resources (steep supply curves, where each additional new supply is much more expensive than the previous), where timing and scale matter (e.g., electricity use for which a new plant will be built or turned on), and when growth trajectories are high.

The challenge of limited data availability, the spatial nature of datacenter energy consumption and diversity in study scope argue for emphasizing narrow approaches to consistent boundary definition over global assessments. One recent idea is "relational footprinting" (Pasek, Vaughan, and Starosielski 2023), with boundaries aligned to discrete (and perhaps more measurable) geographic, spatial, technical and social units. This relationship-based approach resonates with the need to bring affected communities into the conversation about system-level costs of Gen-AI (Debnath et al. 2023).

### 2.2 Baselines and Scenarios

#### Baselines

The largest methodological need for effective benefit-cost determination for Gen-AI is to develop specific baselines for comparison. For each Gen-AI application, practitioner and user communities should specify what business as usual was before the new algorithmic capability. Since Gen-AI is a subset of ML capabilities, one must differentiate capabilities enabled by data-driven approaches generally (quality enhancement or productivity increases) from those resulting from Gen-AI specifically. A baseline demonstrates Gen-AI application benefits and costs over business as usual, whereas a scenario provides comparisons across multiple Gen-AI approaches (Norris et al. 2021). This seemingly intractable task should be initiated through collectively articulated baselines and scenarios by application, geography and time period that evolve with study needs and capture broad cost implications.

#### Benchmarks

The ML community is well-versed in benchmarks for comparing model performance. Gen-AI use cases are far from the data and task delineation of formal ML benchmarking, but the community must move toward this specificity to understand benefit-cost implications. Initial precedents are emerging in sustainability-relevant domains such as transportation (Vinitsky et al. 2018), scientific discovery (Fung et al. 2021) and soil carbon (Wijewardane et al. 2016). Guidance can come from processes that develop climate change scenarios, such as Shared Socioeconomic Pathways (Riahi et al. 2017) or sector-specific road-mapping.

#### Scenarios and thresholds

Once baselines are established by application, scenarios account for what would have happened without the actor being an agent of change (Norris et al. 2021). Scenarios are typically defined by variables that change from one point in time to the next, coupled with a narrative justifying the change (Faure et al. 2017).
- Variables should be defined relative to study scope and boundaries, and articulate whether a variable change is explicit to a Gen-AI benefit or cost.
- Scenarios should be dynamic as innovations and mitigation efforts continue (Borjesson Rivera et al. 2014).
- Scenarios should be framed alongside geographically relevant GHG emissions reduction strategies, to understand whether benefits persist beyond proposed emissions reductions, and should consider multiple forms of potential costs related to extending emissions-intensive sectors or spreading misinformation.
- Baselines could define thresholds for an application (metrics indicating where Gen-AI has a clear benefit for a sector), leveraging notions of planetary and social carrying capacity (Steffen et al. 2015). Crossing these thresholds increases the risk of large-scale abrupt or irreversible changes.
- Scenarios define a set of explanatory variables that define key variants for a Gen-AI application (e.g., hardware, model type, task).

#### Limits of extrapolating from case studies; lessons from carbon markets

To date, benefit assessment in the information and communication technology (ICT) industry has focused on extrapolation from individual case study baselines, such as telework or smart metering (Ligozat et al. 2022; Rasoldier et al. 2022). Extrapolating from case studies is problematic because overly optimistic extrapolation factors are often used and negative effects (including induced demand or rebound) are incompletely accounted for (Roussilhe, Ligozat, and Quinton 2023). Those authors suggest that, for Gen-AI, improvements would limit extrapolation, provide transparency in assumptions, and perform case studies with more random sampling.

Lessons could also be drawn from carbon market validation frameworks (Knox-Hayes 2016), acknowledging the limitation of assigning monetary value to many system-level implications. Standards for verification and validation in voluntary carbon markets (MacKenzie 2009) provide a precedent for valuing interventions. To demonstrate carbon reduction, projects must be:
- **additional**: reduce emissions that would not otherwise be cut;
- **verifiable**;
- **immediate**: emissions happen today, so projects occurring imminently are more valuable;
- **durable** (permanent): CO2 emissions stay in the atmosphere for a century or more, requiring offset of an equivalent amount for at least that long.

### 2.3 Data and Inventory

The goal and scoping exercise identifies the materials and processes to consider, defining the inflows and outflows to quantify. The inventory step is an accounting exercise including primary data collection by life cycle stage or process step but relying on background datasets assembled by varied practitioners with varying regional, temporal and technology relevance. Given Gen-AI's unprecedented pace, supporting data must align with findable, accessible, interoperable and reusable (FAIR) data principles (Wilkinson et al. 2016), and impact methods must be transparent and available. This enables users to estimate impact on a level playing field and drives traceable, auditable reporting. Industry associations and government agencies have a significant role in improving data collection.

Standards for quantifying organizational emissions have been developed through the Global Reporting Initiative and Carbon Disclosure Project since the 2000s, covering carbon emissions, water footprint and other metrics (Matisoff, Noonan, and O'Brien 2013). Impact is tracked as direct impact (Scope 1), purchased electricity (Scope 2), and associated upstream and downstream impacts (Scope 3). Despite cited challenges with these initiatives, there are relevant details to leverage. More recently, the Science Based Targets initiative outlined sector-specific guidelines for how quickly companies must reduce GHG emissions, emphasizing power and industrial sectors, with significant guidance on land use emissions (Science Based Targets 2019).

#### 2.3.1 Impact of Gen-AI: use-phase inventory

For Gen-AI, attention must focus on primary data collection and inventory specification for the use phase (operational impact). Operational impact is so extensive and dynamic that a benefit-cost analysis must separate elements within the use phase inventory:
- Model development and training (e.g., tuning model variants through hyperparameter search), accounted individually.
- Inference (lower energy cost per instance but most frequent occurrence).
- Difficulty of accounting for overall usage patterns cannot be overstated; it depends on knowledge of "model type and size, hardware and resource utilization, training requirements, and frequency" of each disaggregated step (Ligozat et al. 2022; Luccioni, Viguier, and Ligozat 2022).
- The burden of data generation and storage itself should be within analysis scope.
- Foundation models may be at least a factor of two more energy consumptive than more task-specific models, although standardizing comparisons is challenging (Bommasani et al. 2021).
- Increasing use of relevant priors might focus model development more efficiently but could increase multimodal algorithm needs; generative and multimodal tasks may consume ten times more energy per inference (Luccioni, Jernite, and Strubell 2023).
- Beyond the use phase, maintaining relevant hardware performance may increase upstream manufacturing burdens as devices become more specialized (slower manufacturing learning rates) or experience more dynamic use patterns (shorter device lifetimes) (Bell 2023). Attention should be paid to the impact of Gen-AI on hardware specialization, device lifetime and operating system integration.
- Application data would initially derive from specific case studies (e.g., quality of search result or prediction) but broaden to metrics including individuals and communities impacted and how search behavior changes over time.

### 2.4 Initial Framework Applications

Figure 1 (a preliminary example of the benefit-cost evaluation for the scientific discovery and search application) shows a high-level overview of the proposed framework. The paper offers two brief examples: scientific discovery (a sustainability-domain application) and search (a broader application). The figure itself is a diagram; its content is described in the text below.

#### 2.4.1 Example 1: Scientific discovery (chemicals, materials, processes)

Gen-AI can support discovery of chemicals, materials and processes (Bran et al. 2023; Bran and Schwaller 2023), e.g., chemicals for catalysis, more recyclable or biodegradable materials, materials for improved battery storage, or more durable metal alloys. Generative models and large language models have been used to predict stability or reactivity of chemical compounds, discover new materials, identify synthesis pathways, and structure information in text, tables or images (Jablonka et al. 2023). Elements that map onto the framework:
- Boundaries: the materials discovery process can be bounded by life cycle stages from design to synthesis to manufacture and use.
- Baselines/scenarios: the ways Gen-AI accelerates determination of process pathways, reaction yields, synthesis byproducts, device performance and manufacturing process can be incorporated into scenario and baseline development (Subramanian et al. 2024). Costs of increased consumption, emissions-intensive technology lock-in and model misuse should be part of the scenarios.
- Benchmarks: Gen-AI advances in materials discovery correspond to specific workflows for incorporating AI-enabled prediction into scientific inquiry, so benchmarks could eventually be established along each workflow step (MacLeod et al. 2022).
- Thresholds: the application space for a particular material can be used to place a threshold on global sustainability relevance.

#### 2.4.2 Example 2: Search ("SearchAId")

The example analyzes an "ultra, next-generation GPT model called SearchAId" used for search.
- Unit of analysis: the returned search query results from executing a single search.
- Baseline scenario: a user performs a standard Google search on CPU-based servers.
- Gen-AI scenario: the user prompts SearchAId, running on a GPU cluster.
- Compute-related costs cover three phases:
  1. Inference: quantify energy, carbon and water costs of executing a search query on the required computing resources.
  2. Development and training: environmental impacts and computing resources for training, tuning or indexing, with costs amortized over the model's or search engine's lifecycle.
  3. Supply chain and end-of-life: resources and emissions of manufacturing required hardware and building infrastructure such as buildings.
- Application-related impacts and benefits: two approaches: either fix the number of queries or prompts to compare response quality in both scenarios, or quantify the number of queries or prompts needed to achieve a specific information quality or response. The choice hinges on application needs and the tools available for evaluating search task quality.
- Baselines would incorporate time, quality and extent of the search-query result, assessed through expert input, measures of similarity, or benchmark tests of what steps users take after receiving results.
- Scenarios could look across Gen-AI model types, including ChatGPT 3.5, ChatGPT 4 and Bard search.
- System-level impacts include socioeconomic effects of Gen-AI applications across domains, such as job loss, competition for electricity, AI hardware acquisition and land use implications.

## 3. Stakeholder Engagement for Responsible Development of Gen-AI

Unfettered Gen-AI growth poses significant economic, social and environmental challenges. Advocating an outright halt to Gen-AI development is impractical (Future of Life Institute 2023). Even a comprehensive benefit-cost analysis is far from straightforward. Although a perfect framework may never emerge, the authors work iteratively toward impact evaluation criteria integrating many perspectives through active stakeholder engagement. The complex, interdependent nature of Gen-AI's sustainability implications requires a collaborative, multistakeholder approach; strategies shaped by many perspectives will be more robust to sector-specific pitfalls and challenges at sector interfaces. Sustainability-cognizant and coordinated implementation will foster adoption and move toward relational footprinting that is geographically grounded and accounts for regional differences. The following action items are identified for stakeholders.

### 3.1 The Role of Leadership Teams

Leadership teams (CEOs, executive teams, board members at organizations steering Gen-AI) shape its trajectory; their decisions touch ethical, social and environmental implications. A commitment to responsible AI practices is essential for embedding ethical considerations into Gen-AI initiatives. Through governance, leaders can spearhead industry standards and best practices prioritizing sustainability, equity and transparency, and engage policymakers, academia and civil society so Gen-AI evolves in line with societal values and global sustainability goals. This does not preclude the need for decisive governmental action and regulation.

### 3.2 The Role of Policy Makers and Legal Experts

Lack of access to industry data, bottom-up versus top-down assessments, system boundaries, geographic averaging, functional units and differential energy efficiency assumptions make precise estimation of Gen-AI costs complex or impossible. Even historical datacenter energy consumption estimates vary widely (Andrae 2019; Andrae and Edler 2015; Belkhir and Elmeligi 2018; Ferreboeuf 2019; Hintemann 2018b; Masanet et al. 2020b; Andrae 2020): estimates for 2018 range from about 200 TWh (Masanet et al. 2020b) to more than 900 TWh (Hintemann 2018b).

- Policies ensuring transparency across these factors would significantly aid cost estimation and a functional benefit-cost framework.
- Even if measurement is resolved, creating effective incentives for environmental and social sustainability alongside efficiency is challenging; poorly designed incentives can lead to unintended behaviors or exacerbate the problem (Hallegatte and Engle 2019).
- In a growth-driven economy, social issues such as data privacy and job automation are generally sidelined for economic benefits. The lack of holistic metrics skews understanding of Gen-AI's impact, so policy-driven approaches must include environmental and social metrics, set clear reporting standards, and foster transparent, accountable AI practices.
- Policymakers should work with legal experts, human rights activists and civil society on ethical issues. Legal experts can help practitioners comply with legislation and improve risk resiliency by anticipating future regulations.

### 3.3 The Role of AI Practitioners and Engineers

Those who develop and apply Gen-AI can describe tool capabilities and predict innovations to other stakeholders. Targeted outreach and collaboration can lower barriers in translating the language of technology into the language of policy (Krafft et al. 2020). A comprehensive impact assessment framework and standardized sustainability metrics require insight from computer scientists to account for technical considerations such as spatiotemporal variations in environmental costs of a distributed cloud environment. AI practitioners already contribute to discourse on ethical and sustainable AI regulation (Schiff et al. 2020), crucial given the outsized impact of leadership at AI innovation hubs.

AI practitioners and application domain architects can tip the benefit-cost trade-off by reducing costs or enhancing realized benefits:
- Continue pursuing algorithmic efficiency (transfer learning, fine-tuning, mixed-expert models).
- Compound algorithmic gains by improving hardware efficiency, especially in the operational life cycle stage, and by optimizing datacenters' resource and power usage effectiveness.
- Application and data structure developers can maximize benefits, e.g., by efficiently and rapidly processing data to ensure reliability and resilience of complex systems (Ilic 2016) and by coordinating Internet of Things (IoT) devices for demand response (Ilic and Jaddivada 2019).

### 3.4 The Role of Energy and Supply Chain Sectors

Addressing Gen-AI's impact involves managing supply chain accuracy and evaluating electric grid factors such as clean energy use, benefits of demand response programs and grid cleanliness. Proper baselines are necessary for comparison. Reviewing policies for impact on long-term, nonfinancial or secondary goals may solve multiple problems at once; for instance, expanding computing infrastructure can be done alongside strategically improving power infrastructure (Kirchhoff et al. 2016).

### 3.5 The Role of Economists

Continual capital growth is crucial for a healthy economy, yet rapid expansion of technologies such as "dot com" and "crypto" has historically led to boom-and-bust cycles. Economists should identify lessons from prior unsustained booms and analyze warning signs of rapid growth. Mechanisms to ameliorate negative labor market and supply chain consequences depend on whether AI growth causes a macroeconomic disruption, a series of sector-specific disturbances, or both (Furman and Seamans 2019), so economists must monitor AI's impact, identify key indicators of economic bubbles versus sustainable capital expansion, and study the consequences of unchecked Gen-AI deployment on the labor market (Chui et al. 2023). These studies will also illuminate how market speculation alone cannot sustain long-term economic health.

### 3.6 The Role of Social Scientists

Social scientists provide insight into societal benefits and costs. Quantitative and qualitative trade-off analyses of Gen-AI growth strategies would illuminate a broad spectrum of social impacts, from user experience and societal acceptance to ethical considerations, ensuring the evaluation framework is sensitive to the sociocultural milieu in which Gen-AI operates.

### 3.7 The Role of Civil Society

NGOs are well positioned to collect and synthesize diverse perspectives on AI (Schiff et al. 2020) and to link AI developers with communities first to experience economic and social consequences. Through third-party evaluations of benefits and costs, advocacy groups and think tanks can elevate priorities of stakeholders affected by technology developments but unable to shape them directly. Because much existing AI ethics and policy literature comes from wealthy countries, the field risks disproportionately catering to the needs and economies of wealthy countries rather than the challenges unique to the Global South (Schiff et al. 2020). As governments invest in AI and develop regulations (Ulnicane 2022), civil society can leverage existing organizational structures to convey reactions and recommendations.

## 4. Conclusion

A structured, comprehensive evaluation framework is essential for responsible Gen-AI growth, and the authors emphasize immediate implementation, while acknowledging the turbulence and inherent limitations of implementing an evolving framework.

- Gen-AI's rapid growth and substantial energy consumption suggest its emergence as a distinct sector warranting dedicated monitoring and analysis (de Vries 2023). Current understanding of the direct and indirect impacts of digitalization on energy use, carbon emissions and mitigation is limited (IPCC 2022), which influences understanding of Gen-AI's implications.
- The framework can adopt traditional sector-analysis methods: tracking economic indicators, regulatory changes, environmental impacts and technological developments (Parmesan, Morecroft, and Trisurat 2022). Collected data aids integrated assessment models and emissions projections, enabling more accurate description of Gen-AI's impact to inform policy and strategy.
- A crucial aspect is identifying and maximizing the benefit-cost ratio of Gen-AI initiatives. Policies should be rooted in scientific evidence and sustainable growth strategies rather than driven solely by economic ambition.
- Climate mitigation and adaptation research shows incremental changes are easier than transformational changes, due to actual or perceived cost and required individual or institutional behavior change (Kates, Travis, and Wilbanks 2012). The more Gen-AI grows using and encouraging responsible and sustainable practices up front, the less likely a costly, difficult transformational change will be needed to address an entrenched vulnerability later. The framework therefore seeks opportunities where incremental advancements yield substantial economic and environmental benefits.
- The framework also facilitates exploring eco-economic decoupling, balancing technological advancement with environmental sustainability.
- Drawing on Bayo Akomolafe's "slow urgency" (Akomolafe 2023), it suggests a more measured approach, cautioning against a frenetic pace akin to a Klondike gold rush, and promoting a deliberate approach that considers long-term environmental impacts and societal needs. It encourages stakeholders to reevaluate the notion of growth, advocating a model that aligns technological progress with environmental sustainability and social well-being, so Gen-AI contributes positively to society without exacerbating environmental challenges.
