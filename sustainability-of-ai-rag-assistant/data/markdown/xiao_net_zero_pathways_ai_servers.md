# Environmental impact and net-zero pathways for sustainable artificial intelligence servers in the USA

Authors: Tianqi Xiao, Francesco Fuso Nerini, H. Damon Matthews, Massimo Tavoni, Fengqi You
Publication Year: 2025 (received 3 January 2025; accepted 7 October 2025; published online 10 November 2025)
Source: Nature Sustainability, Volume 8, December 2025, pp. 1541-1553 (Analysis article). DOI: https://doi.org/10.1038/s41893-025-01681-y
Keywords: AI servers; generative AI; energy-water-climate nexus; water footprint; carbon emissions; net-zero pathways; power usage effectiveness (PUE); water usage effectiveness (WUE); grid decarbonization; spatial distribution of data centres; advanced liquid cooling; server utilization optimization; United States; 2030 (keywords derived from content; the extracted text does not list keywords)

## Executive Summary

Xiao, Fuso Nerini, Matthews, Tavoni and You analyse the combined energy-water-climate impact of operational AI servers in the United States from 2024 to 2030 and ask whether the AI server industry can reach net-zero carbon and net-zero water by 2030, the target date of major AI data-centre operators. They build an open-source, bottleneck-based model. It starts from the manufacturing capacity of the CoWoS (chip-on-wafer-on-substrate) packaging process, which is the bottleneck for top-tier AI servers. It then converts capacity into server power with a utilization-based electricity model and allocates servers to US states using the locations of existing and planned data centres of Google, Meta, Microsoft, AWS, xAI and Tesla. State-level PUE and WUE come from a hybrid statistical and thermodynamic model. Grid carbon and water factors come from the NREL ReEDS model. Five server-deployment scenarios (low demand, low power, mid-case, high application, high demand) are combined with best, base and worst practices for industry efficiency, server location and grid development.

Main results: AI servers in the US could generate an annual water footprint of 731 to 1,125 million m3 and additional annual carbon emissions of 24 to 44 Mt CO2-equivalent between 2024 and 2030, depending on the scale of expansion. Annual energy consumption ranges from 147.3 TWh (lowest) to 244.9 TWh (highest), with 174.1 TWh in the mid-case. Indirect (Scope 2) water makes up 71% of the water footprint and direct (Scope 1) water makes up 29%. Industry efficiency practices (lower PUE and WUE, advanced liquid cooling, server utilization optimization) can cut energy, water and carbon by about 12%, 32% and 11%. Location matters most: best and worst server distributions change carbon emissions by -49% and +90% and the water footprint by -52% and +354%. Grid decarbonization (low versus high renewable cost scenarios) changes carbon by about -15% to +20%. Combined best practices reduce residual carbon emissions and water footprints by up to 73% and 86%, but leave about 11 Mt of residual carbon in 2030 (equivalent to about 28 GW of wind or 43 GW of solar). Worst practices leave 71 Mt of carbon and over 5,224 million m3 of water per year in 2030 under the low-demand scenario.

The authors conclude that the industry is unlikely to meet its 2030 net-zero aspirations without substantial reliance on highly uncertain carbon offsets and water restoration. The best case is itself hard to achieve, because it requires ideal siting and near-physical-limit efficiency. Concentrating servers in Texas, Montana, Nebraska and South Dakota (the paper calls them Midwestern states) is the most favourable option considering water scarcity, renewable potential and unit water and carbon intensities. It faces grid, transmission and connectivity constraints. Sensitivity analysis shows up to about 40% variation in energy from key parameters, and the conclusions stay robust unless uncertainties greatly exceed the modelled ranges. The authors recommend public-private partnerships, transparent third-party-verified offsets, real-time monitoring, AI-specific energy, water and carbon benchmarks, and accelerated clean-energy deployment.

## Abstract

The rapidly increasing demand for generative artificial intelligence (AI) models requires extensive server installation, with sustainability implications in terms of the compound energy-water-climate impacts. The deployment of AI servers across the United States could generate an annual water footprint ranging from 731 to 1,125 million m3 and additional annual carbon emissions from 24 to 44 Mt CO2-equivalent between 2024 and 2030, depending on the scale of expansion. Other factors, such as industry efficiency initiatives, grid decarbonization rates and the spatial distribution of server locations within the United States, drive deep uncertainties in the estimated water and carbon footprints. The AI server industry is unlikely to meet its net-zero aspirations by 2030 without substantial reliance on highly uncertain carbon offset and water restoration mechanisms. Although best practices may reduce emissions and water footprints by up to 73% and 86%, respectively, their effectiveness is constrained by current energy infrastructure limitations. These findings underscore the urgency of accelerating the energy transition and point to the need for AI companies to harness the clean energy potential of Midwestern states. Coordinating efforts of private actors and regulatory interventions would ensure the competitive and sustainable development of the AI sector.

## Introduction

### Background: AI server growth and energy-water-climate concerns

The accelerating deployment of AI servers is fuelled by growing demand for generative AI applications, ignited by milestones such as the release of ChatGPT in 2022. Projections signal even greater impact, exemplified by Nvidia's recent Blackwell platform, which analysts herald as a new Moore's Law era. Pronouncements from influential AI industry figures on both demand and supply sides are seen as transformative shifts for the entire data-centre industry. Whereas AI has been employed in various fields to advance sustainability, the remarkable energy requirements of AI itself raise concerns about energy provisioning, water scarcity and climate change stemming from the energy-water-climate nexus of AI data centres. The holistic energy-water-climate implications of AI computing are largely unknown, constrained by untransparent industry reports and limited data.

### Climate and water scopes for AI servers

The climate impact of AI servers stems primarily from their operations (Scopes 1 and 2) and supply-chain activities (Scope 3), including manufacturing and end-of-life treatment. Scope 2 emissions from indirect energy purchases are expected to constitute a substantial portion and indicate a high dependency on the increase of AI server energy consumption. According to the International Energy Agency, 0.6% of global total carbon emissions comes from data centres and data transmission networks due to their electricity consumption. Industry energy consumption could double by 2026, motivated by AI and other sectors, threatening decarbonization targets under the Paris Agreement, which include a 53% reduction in data-centre emissions by 2030 and net-zero goals for the AI sector. Growing AI server energy consumption also implies an increasing water footprint through Scope 1 (direct cooling) and Scope 2 (indirect procurement) water use. Centralized installation in water-stressed regions may perturb local water balance and threaten supply for millions.

### Limits of earlier methods and contributions of this study

Previous research developed bottom-up and top-down methods to assess energy-water-carbon outcomes of servers, but these approaches face challenges with the rise of AI servers. Top-down approaches based on activity indices, such as data traffic and computing instances, fail to accurately represent AI-driven workloads. Detailed bottom-up approaches suffer from limited data availability and lack of industry insight. Assumptions valid for traditional colocation centres often fail for AI data centres, which differ in installation and operation. Recent studies have explored computing task-based analyses to better quantify AI-related energy and resource consumption, but lack systematic policy guidance. Two notable contributions are the 2024 data-centre report by Lawrence Berkeley National Laboratory and the 2025 Energy and AI Report by the International Energy Agency, which present scenarios estimating US and global data-centre energy use under highly uncertain AI growth. Their use of confidential commercial data may limit reproducibility, but they offer important benchmarks.

This study extends that foundation by (1) developing an open-source, bottleneck-based modelling approach with comprehensive uncertainty analysis; (2) systematically assessing energy, water and carbon impacts, incorporating dynamic interactions with local energy systems; and (3) proposing actionable mitigation strategies for potential net-zero trajectories across different AI server deployment scenarios.

### Research questions and scope

The study analyses the combined energy-water-climate impact of operational AI servers in the United States between 2024 and 2030, balancing importance and future uncertainties. Two questions are addressed.

1. What are the magnitude and spatiotemporal distributions of energy consumption, water footprint and climate impact from AI server deployment? This is addressed using temporal projection models and regional frameworks, assuming deployment mirrors current large-scale AI data-centre patterns.
2. What are the prospects for near-term net-zero pathways? This is evaluated by analysing best- and worst-case scenarios of key drivers: industry efficiency improvements, server location distribution and grid decarbonization.

The United States is selected as the research region because of its dominant position in the global AI market. The period 2024-2030 reflects a trade-off between importance and uncertainty. The first step is projecting the accumulated AI server capacity in the United States from the forecast of AI chip manufacturing capacity, AI server specifications and the AI server adoption pattern. AI data centres are assumed to align with current large-scale data-centre allocation ratios of AI companies. PUE and WUE values are derived by a hybrid statistical and thermodynamics-based model, with applied values calculated as the average of best and worst practices. Projected grid factors are calculated with the Regional Energy Deployment System (ReEDS) model, using projected data-centre load data and regulations such as the Inflation Reduction Act.

## Results

### AI servers' environmental impact in the United States (base projections)

Figure 1a shows projected cumulative AI server installations in the United States from 2024 to 2030 under five scenarios: low demand, low power, mid-case, high application and high demand. The mid-case is the base scenario; low demand and high demand set projection bounds. Low power assumes server efficiency gains, and high application accounts for increased adoption driven by efficiency. Annual shipment capacity is 17.6 GW (lowest), 21.9 GW (mid-case) and 33.7 GW (highest).

Figure 1b shows the state-level allocation of AI servers with PUE, projected grid carbon intensity (carbon emissions per unit of electricity), WUE and projected grid water intensity (water footprint per unit of electricity) for each state. Southern states such as Florida exhibit higher PUE and WUE than northern states such as Washington, reflecting climate impacts. Grid factors are highly sensitive to location, so the local grid is important for AI servers' environmental impacts.

Key base results (Fig. 1c-g):
- AI server energy predominates over infrastructure energy (server energy is 0.89 and infrastructure energy 0.11 of the total).
- Indirect water footprint contributes 71% of the total and direct use 29%.
- Annual energy consumption of AI servers, 2024 to 2030: lowest scenario 147.3 TWh, mid-case 174.1 TWh, highest 244.9 TWh.
- Annual water footprint: lowest 730.8 million m3, mid-case 860.1 million m3, highest 1,124.5 million m3.
- Annual carbon emissions: lowest 24.0 Mt, mid-case 26.8 Mt, highest 44.1 Mt.

Even the lowest scenarios outline a considerable increase in the energy, water and carbon footprints of AI servers. The highest scenario yields the highest environmental impact, largely surpassing previous forecasts for the entire US data-centre market (shown as red dashed reference lines in Fig. 1e-g), underscoring the environmental risks of unchecked AI server expansion.

### Higher energy and water usage efficiencies

Over the past decade, efficiency gains in the data-centre industry have stabilized environmental costs despite a doubling of computing instances. This section examines the potential for further improvements through system optimization and technology adoption.

PUE and WUE (Fig. 2a-d). The best-practice scenario suggests over 7% PUE reduction and over 85% WUE reduction, despite the high efficiency of AI data centres compared with industry averages (PUE 1.58, WUE 1.8). The worst-practice scenario underscores the risk of neglecting efficiency efforts. PUE reduction yields over 7% reductions in total energy consumption and carbon emissions. WUE reduction efforts result in over a 29% reduction in the total water footprint. PUE and WUE efforts can align with each other, as observed in WUE improvement results. (In Fig. 2d, best and worst WUE practices change direct water by about -85.7% and +87.9% and total water by about -29.6% and +30.0%, as plotted.)

Advanced liquid cooling (ALC) and server utilization optimization (SUO) (Fig. 2e):
- Best ALC adoption can reduce about 1.7% of energy consumption, 2.4% of water footprint and 1.6% of carbon emissions of AI servers by 2030.
- SUO best case, representing total adoption by 2030, results in a 5.5% reduction in all footprint values.
- SUO worst case, representing frozen adoption, leads to a 7.3% increase by 2030.

Combined industry efforts (Fig. 2f-h, mid-case scenario). Following worst, base and best industry practices of all considered efforts, energy consumption changes by +13.1% (worst) and -11.6% (best), water footprint by +36.2% and -32.2%, and carbon emissions by +12.4% and -11.2%. The maximum reductions of energy, water and carbon from existing potential are about 12%, 32% and 11%, respectively, underscoring the considerable impact of industry efforts.

How best, base and worst practices are defined. Base PUE and WUE are calculated by averaging the best and worst practices because cooling specifications are unknown. Worst and best values come from solving optimization problems with constrained operational parameters. Best PUE is achieved mainly by extending the free-cooling period through input-air set-point adjustment and enhancing facility energy efficiency. WUE is improved by reducing windage and concentration water loss, adopting air-side economizers and enabling more free cooling. The model follows Lei and Masanet's previous work, with parameters in section 3 of the Supplementary Information. ALC adoption is evaluated through increased immersion cooling in AI data centres; SUO improvements focus on raising the active server ratio. Advances in AI hardware, as seen in Nvidia's future chip structures Blackwell and Rubin, could reduce footprints by improving energy efficiency, but these gains may be offset by the rebound effect. Hardware evolution and market uncertainties are discussed in the scenario definitions (Supplementary Information section 1).

### Influences of AI server spatial distribution

The location of data centres critically shapes their environmental impact. The study projects how spatial distribution affects consequences of rapid US expansion. Figure 3a,b presents the top 25%, 50% and 75% locations with the lowest projected water footprint and carbon emissions per unit of server energy; Fig. 3c the locations with combined lowest water and carbon factors. Allocation strategies are applied at the grid balancing-area level, with ReEDS computing the grid factors of each balancing area under different scenarios.

Findings:
- Texas has the most balancing areas within the top 25%, 50% and 75% water and carbon factors (Fig. 3d). Other western and southern states, including Montana, Louisiana, Idaho and New Mexico, take a large portion of areas under the combined strategies because of widely leveraged local renewables.
- West Coast states (California, Oregon, Washington) and New England states are suitable for carbon reduction but lead to higher water footprints. The primary driver is hydropower, which consumes large volumes of water through evaporation (Supplementary Fig. 6). With more hydropower in the grid, the Scope 2 water usage of AI servers could dramatically increase.
- Figure 3e-g shows changes in energy, water and carbon under the 25%, 50% and 75% spatial distribution scenarios, with the base scenario applied to isolate spatial effects. Installing AI servers in top water-oriented locations greatly reduces both water and carbon footprints. Carbon-oriented strategies lead to higher water footprints because of hydropower on the West Coast and in New England. Water and carbon footprints can be reduced concurrently under a combined allocation strategy.

Water scarcity and renewable potential by state (Fig. 3h,i):
- Top ten states with severe water scarcity: California, Nevada, Arizona, Utah, Washington, New Mexico, Colorado, Wyoming, Oregon and Montana, concentrated primarily in the western United States.
- Large hydropower adoption increases unit energy-water footprint in states such as Arizona, California, Nevada, New Mexico and Utah, exacerbating water scarcity.
- Top ten states with abundant renewable energy potential: Texas, New Mexico, Kansas, Arizona, California, Colorado, Nevada, Nebraska, Oklahoma and South Dakota.
- Combining water- and carbon-oriented strategies, Texas, Montana, Nebraska and South Dakota, which the paper describes as Midwestern states, emerge as optimal candidates for AI server installation, considering both water scarcity and future decarbonization.

### Influence of renewable energy penetration within the grid

This section analyses how future grid development affects AI server environmental impacts. Figure 4a,b shows modifications of grid carbon and water factors per state under a low renewable energy cost scenario (LRC, best practice) and a high renewable energy cost scenario (HRC, worst practice) compared with the base scenario. These are predefined ReEDS cases and represent the highest and lowest levels of renewable penetration, respectively.

- HRC scenario: about a 20% increase in carbon emissions (+19.8%) alongside a 2.0% increase in water footprint.
- LRC scenario: over 15% reduction in carbon emissions (-15.0%) with a 2.5% water footprint reduction.
- Carbon emissions of AI servers are heavily influenced by the grid decarbonization pattern, indicating both considerable reduction potential and risks.
- Georgia, Nevada, North Carolina and Tennessee show marked sensitivity to renewable cost scenarios (Fig. 4e).
- Pacific states (California, Oregon, Washington), which already have a low grid carbon factor, slow hydropower adoption under LRC, avoiding worsened water scarcity with additional AI servers. Wind and solar, which consume no water when generating, are adopted more under LRC, reducing carbon while easing water scarcity in these states.
- Grid decarbonization effects appear over time and in spatial variation among US states, which ties to the importance of ambitious green electricity policies in US states.

### Pathways to net-zero carbon and water goals

Figure 5a presents pathways from 2024 to 2030 to achieve net-zero carbon emissions and a net-zero water footprint of AI servers under the mid-case scenario; Fig. 5b presents residual emissions and water footprints across scenarios and practices. The 2030 target aligns with major AI data-centre operator goals (e.g. Microsoft, Meta, Google). The top and bottom 25% of locations form the best and worst spatial cases; best and worst grid practices are modelled with LRC and HRC. These form upper and lower bounds, although better solutions may be obtained through additional policies.

Quantitative results:
- Best and worst distribution patterns of AI server deployment lead to a 49% reduction and a 90% increase in carbon emissions, and a 52% reduction and a 354% increase in water footprints, respectively.
- Optimistic grid decarbonization gives a further 13% carbon reduction, while the worst case gives a 23% increase.
- Industry efficiency efforts are critical for water sustainability, offering over 32% reduction in water footprint under best practices.
- Combined best practices cut residual emissions and water footprints by 73% and 86%, indicating a feasible pathway to net zero.
- Under the mid-case, from a base of 186 Mt of carbon due to AI server installation (cumulative 2024-2030), best industry, spatial and grid scenarios each reduce over 21 Mt, 25 Mt and 92 Mt of carbon respectively.
- Best practices produce about 11 Mt residual carbon emissions by 2030, requiring 28 GW of wind or 43 GW of solar to fully offset. With over 13 GW of AI-company renewables already claimed, residual emissions could remain manageable with further expansion.
- Reaching the best case could be extremely challenging because of facility constraints in deploying AI servers at optimal locations and difficulty reaching ideal energy and water efficiency in AI data centres.
- Worst practices risk unachievable net-zero pathways: 71 Mt annual residual carbon emissions and over 5,224 million m3 annual residual water usage by 2030 under the low-demand scenario, which is nearly impossible to compensate in a short period.

Figure 5a cumulative contributions, mid-case, 2024-2030 (as plotted):

| Component | Carbon, best practice (Mt) | Carbon, worst practice (Mt) | Water, best practice (million m3) | Water, worst practice (million m3) |
|---|---|---|---|---|
| AI server growth | +187.5 | +187.5 | +6,020.4 | +6,020.4 |
| Industry efficiency | -21.2 | +23.7 | -1,935.2 | +2,179.3 |
| Grid development | -24.8 | +42.4 | -134.2 | +135.7 |
| Server location | -91.7 | +169.4 | -3,102.1 | +21,302.4 |
| Residual (grey area still to be reduced) | -49.9 | -423.0 | -848.9 | -29,637.8 |

### Sensitivity analysis

Figure 6 tests server lifetime, AI server manufacturing capacity, US allocation ratio, server idle and maximum power ratios, and training/inference distribution. Changes in these factors cause up to 40% variation in energy consumption, closely mirrored by water footprint and carbon emissions.

| Parameter | Low / applied / high values |
|---|---|
| Server lifetime (years) | 3 / 4 / 5 |
| CoWoS manufacturing capacity (%) | 40 / 54.3 / 70 |
| US allocation ratio (%) | 30 / 53 / 70 |
| Server idle power (%) | 0 / 23 / 40 |
| Server maximum power (%) | 70 / 88 / 100 |
| Training ratio (%) | 10 / 30 / 50 |

Reported energy-consumption sensitivities in Fig. 6 range from about -43.4% to +32.1% (values plotted include -16.0/+10.4, -23.2/+25.5, -43.4, -25.3/+18.7, +32.1, -15.3/+10.2 and -10.7/+10.7; the assignment of each value to a parameter is not recoverable from the extracted text). Water footprint and carbon emissions show nearly identical sensitivities (for example carbon: -22.1/+24.2, -43.4, -25.5/+18.9, +32.1, -10.8/+10.8).

Unmodelled uncertainties can largely be reflected by changing these factors. For example, innovations such as DeepSeek can lower power requirements for AI tasks, which may trigger a rebound effect with more AI applications. That could imply larger CoWoS manufacturing capacity, longer server lifetime and a smaller training/job ratio due to more inference. The key conclusions remain robust unless future uncertainties greatly exceed the modelled ranges, and the model can be revised with new data.

## Discussion

### Optimal siting: Texas, Montana, Nebraska and South Dakota

Investment in AI servers is accelerating, as in the $500 billion Stargate project. To mitigate environmental risk, the authors identify that concentrating AI server deployment in Texas, Montana, Nebraska and South Dakota (which they call Midwestern states) is optimal, given abundant renewables, low water scarcity and favourable projected unit water and carbon intensities. These states have substantial untapped wind and solar resources, enabling green power portfolios and reducing competition with other sectors. Lower water stress also eases public concerns and reduces the need for costly water-saving measures.

Implementation challenges:
- Texas may need to support an additional 74-178 TWh of AI server demand, possibly exceeding its current total renewable generation of 139 TWh. This would require substantial new renewable capacity and transmission infrastructure, already constrained by congestion.
- Montana, Nebraska and South Dakota host minimal data-centre capacity, so their internet infrastructure may support only residential or standard industrial uses. This raises connectivity and security concerns; broadband and security upgrades would add emissions and capital cost.

### Public health, local development and policy

Expansion in the suggested regions may be obstructed by public health concerns and local sustainable-development impacts. Operations and construction could generate air and water pollution through fossil fuel use, substantial water consumption and large-scale construction and transportation. The authors recommend public-private partnerships between AI companies and local governments. These could ease government budget pressures, create local jobs and mitigate health concerns by funding green power upgrades and monitoring systems (such as tracking PM2.5 levels). Governments could use tax exemptions on related facilities, with transparent accountability to prevent privatized gains at public cost. Local economic growth is evidenced in Virginia. Energy market adaptations are needed as AI-driven hyperscale loads challenge utilities' duty to serve. Requirements to connect large data centres could lead to collocation with generation, but such choices should not crowd out renewable investments to decarbonize the economy. Broader political and economic factors lie beyond the study's scope.

### Reliance on offsets and the need for transparency

The challenges of optimal spatial distribution add substantial uncertainty to the projected 73% and 86% carbon and water reductions under best practices, and are unlikely to be offset by further efficiency or decarbonization beyond what is considered. The best-case industry efficiency scenario approaches the physical limits of AI data centres, and US Energy Information Administration projections offer limited support for additional grid decarbonization beyond the best case. Without additional interventions, AI data centres are likely to generate substantial environmental impacts. AI companies are therefore expected to continue investing in offset mechanisms (power purchase agreements, carbon removal and water restoration), reaching an unprecedented level of reliance on them to meet net-zero aspirations by 2030. This raises concerns about securing long-term contracts and providing convincing reduction credits, given the capacity needed. The authors argue AI companies should shift to a more transparent approach, cooperating closely with third-party verification groups, service providers and governmental agencies, as a model for other electrified sectors.

### Efficiency innovations, rebound effects and recommendations

Emerging high-efficiency technologies in hardware and software, exemplified by DeepSeek, may transform AI server supply and demand. Across the study's five scenarios, they may cause deviations of up to 393 million m3 in water footprints and 20 Mt CO2-equivalent in emissions between minimum and maximum impact cases. Efficiency gains may reduce cost per computing task but risk a rebound effect in which lower costs increase total application volume, as reflected by the high-application scenario. Recommendations:
- Government agencies and industry should establish real-time monitoring systems for timely alerts and proactive measures.
- Continue improving energy and water efficiency through system optimization and strategies such as SUO and ALC.
- The data-centre industry should establish AI-specific benchmarks for energy, water and carbon performance.

## Methods

### Framework and goals

The methodology has two goals: (1) estimate energy-water-climate impacts of AI servers in the United States from 2024 to 2030, and (2) identify best and worst practices of each influencing factor to scheme net-zero pathways for 2030 water and climate targets. Unlike many climate pathway studies that extend to 2050, this study focuses on 2024-2030 because of great uncertainty in the future of AI applications and hardware. Scenario-based projections first give capacity-increasing patterns of AI servers. Technology dynamics such as SUO and ALC adoption are defined with best, base and worst scenarios, and similar methods capture grid decarbonization and spatial distribution. More detail is in sections 1-4 of the Supplementary Information.

### Data description

Historical DGX (Nvidia's high-performance AI server line) parameters were sourced from official documentation, and future scenarios were projected from historical configurations and industry forecasts. CoWoS manufacturing capacity, the bottleneck for top-tier AI server production, was projected from the most updated industrial reports. Server electricity usage was assessed using experimental data on maximum power, idle power and utilization rate from existing AI server systems. PUE and WUE values by location were calculated using operational data from previous studies and industrial sources combined with average climate data for each state (Meteonorm). Allocation ratios of AI servers per state came from configurations of existing and planned AI data centres in reports of major US AI companies. Grid carbon and water factors came from the ReEDS model using default scenario data. All datasets are publicly available. A key uncertainty is the number of manufactured AI server units because supply-chain reports are opaque; the authors use best available industry reports rather than commercial sources such as IDC data, which are not open access and would limit validation.

### AI server power capacity projections

The energy consumption of AI servers is assumed to be driven predominantly by top-tier models designed for large-scale generative AI computing. Power capacity is estimated from the CoWoS process, controlled nearly exclusively by the Taiwan Semiconductor Manufacturing Company (TSMC). Other factors translating capacity into power capacity are the CoWoS size of AI chips (how many chips per wafer), the rated power of future AI servers, and adoption patterns (server type mix over time). Values derive mainly from Nvidia DGX systems, the dominant product in top-tier AI servers.

Equations (as described): annual shipments N_AI of top-tier AI servers are computed from the CoWoS capacity (C_CoWoS), the ratio of CoWoS capacity allocated to top-tier AI servers (R_AI), the units yield per CoWoS wafer of each chip type i (n_i), the adoption ratio of each chip type (R_i), and the number of GPUs per server (N_GPU, set to 8). Average rated power P_AI = sum over i of R_i x P_i, where P_i is the rated power of chip type i. R_AI is set to 40% for 2022, 40.7% for 2023, 48.5% for 2024 and 54.3% for 2025 from industry reports, and held constant at the 2025 value afterwards. Details are in Supplementary Information section 1, Supplementary Figs. 1-4 and Supplementary Table 1.

Scenarios:
- Mid-case: CoWoS capacity slightly increases after 2026, consistent with 2023 growth. Rated power has a linear relationship with anticipated die-size increase and adoption stays on the current trajectory.
- Low-demand: lower CoWoS capacity growth and lower server rated power than mid-case.
- Low-power: mid-case assumptions with lower server rated power, representing hardware and software efficiency gains.
- High-application: lower server rated power with high CoWoS capacity, capturing a potential rebound effect where efficiency gains drive increased AI workload deployment.
- High-demand: higher CoWoS capacity expansion, higher server rated power and higher adoption of new servers than mid-case.

### AI server electricity usage calculation

A utilization-based model initially derived for CPU-dominant servers is used: P_server = (P_max - P_idle) u + P_idle (Eq. 2), where total server power is linear in processor utilization u. The linear relationship is well validated for CPU machines; its application to GPUs is less established, but recent studies show a strong correlation between GPU utilization and overall server power for AI workloads, with GPUs the dominant energy contributors. Systematic GPU validation is still limited. Maximum and idle power derive from recent DGX experiments and are set at 88% and 23% of rated power (the Methods text lists the percentages in the order 23% and 88%, but the sensitivity table identifies idle power as 23% and maximum power as 88%).

GPU utilization is u = u_active x r_active (Eq. 3), where u_active is the average utilization of active GPUs and r_active is the ratio of active GPUs to total GPUs. Both are generally higher for training than for inference. Using AI traces (Philly, Helios, PAI and Acme), r_active is 50% for inference and 90% for training. u_active is 50% for inference and 80% for training. Processor utilization is therefore 25% for inference and 72% for training. Base estimates assume 30% of computing capacity for training and 70% for inference. Sensitivity analysis is in Fig. 6.

### Assessment of the environmental footprints of AI servers

State-level allocation is used. The authors compiled current and in-construction large-scale data centres of major purchasers of top-tier AI servers: Google, Meta, Microsoft, AWS, xAI and Tesla. Location, building area and construction year give each state's server capacity share by aggregating building area. No major change in spatial distribution is projected between 2024 and 2030 even with new data centres, so the current distribution is held constant (Supplementary Information section 2).

Energy per state follows from server electricity use and PUE. Water and carbon are analysed by scope:
- Scope 1: on-site water footprint from on-site WUE, and on-site carbon emissions (typically negligible for data centres).
- Scope 2: off-site water footprint and carbon emissions, dependent on the local grid supply portfolio.
- Scope 3: embodied water and carbon from facility manufacturing, outside this study's scope.

A regional PUE and WUE model (hybrid thermodynamics and statistics, per Lei and Masanet) uses state average climate data for 2024-2030. Because AI data-centre cooling settings are unknown, base values average worst and best cases (parameters in Supplementary Table 2). Scope 2 water and carbon use ReEDS grid factors, which can incorporate projected data-centre load interacting with the grid via services such as demand response. ReEDS validation against current high-resolution data is in Supplementary Figs. 7 and 8 (section 4). Optimization and analytical techniques determine best and worst practices for efficiency, spatial distribution and grid decarbonization. State water scarcity and remaining renewable potential come from the calculated footprints and previous literature.

### Uncertainties and limitations

Substantial uncertainties exist in projecting AI server evolution. Unmodelled areas are:
- Model and algorithm innovations: breakthroughs could fundamentally alter computing requirements.
- Supply-chain uncertainties: new bottlenecks beyond CoWoS may change expansion patterns.
- Hardware and facility evolutions: improvements in AI hardware and data-centre efficiency could substantially affect impacts.
- Out-of-scope factors: market forces and geopolitical influences.

For example, DeepSeek's release has been interpreted as reducing AI server energy demand but may trigger a rebound effect that raises overall energy, water and carbon footprints; no fresh data were available to simulate this. Sensitivity analysis covered manufacturing capacities, US allocation ratios, server lifetimes, idle and maximum power ratios and training/inference distributions. Key conclusions should stay robust unless future uncertainties notably exceed the ranges considered. Other limitations implied by the methods: Scope 3 emissions are excluded, spatial distribution is held fixed at the current allocation, and the linear GPU power model has limited experimental validation.

### Data and code availability

All data, material and code are available at https://github.com/PEESEgroup/US-AI-Server-Analysis.
