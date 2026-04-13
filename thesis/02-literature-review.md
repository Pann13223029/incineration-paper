<!--
  SUPERSEDED: This Markdown file is an earlier authoring draft.
  The authoritative version of every chapter now lives in thesis/thesis.tex,
  which has been through multiple rounds of panel review, factual correction, and discussion-section additions
  since this Markdown was last touched. Do NOT regenerate thesis.tex from
  these MD files without first back-porting all corrections.
-->

# Chapter 2: Literature Review

## 2.1 Overview

This chapter situates the thesis within four bodies of literature. Section 2.2 reviews the institutional and technical development of Japan's waste-to-energy sector. Section 2.3 introduces the industrial ecology concepts of material metabolism and infrastructure lock-in that frame the analysis. Section 2.4 surveys the empirical literature on energy recovery efficiency determinants in WtE systems globally and in Japan. Section 2.5 identifies the gap — the absence of fleet-level heterogeneity analysis using multi-year panel data — that this study addresses.

## 2.2 Japan's Waste-to-Energy System: Institutional Development and Technical Evolution

### 2.2.1 The Historical Foundation

Japan's reliance on waste incineration is not accidental. The country combines high population density, mountainous terrain that limits landfill siting, and a cultural and regulatory emphasis on hygiene and waste containment that made open dumping politically unacceptable from a relatively early period of industrialization [@Tanikawa2015]. The Waste Disposal and Public Cleansing Law of 1970 established national frameworks for municipal waste management and accelerated the shift toward controlled thermal treatment [@TabataTsai2016]. By the 1980s, Japan had constructed incinerators at a pace that left no comparable national fleet anywhere in the world.

The financial architecture of this expansion is important to understand because it shapes the lock-in dynamics analyzed in later chapters. Municipal incinerators in Japan are overwhelmingly publicly owned and operated, or operated under long-term contracts by private firms on behalf of municipalities. Construction is heavily subsidized by national government grants, typically covering 25–50% of capital costs [@TabataTsai2016]. Operating costs are borne by local governments, which creates a strong fiscal incentive to fully utilize installed capacity — a dynamic that, as this thesis demonstrates, has important implications for efficiency. The combination of high capital subsidy and municipal operational responsibility creates an institutional structure in which facilities, once built, are rarely closed early.

### 2.2.2 Technical Architecture: From Thermal Treatment to Energy Recovery

The dominant combustion technology in Japan's fleet is the stoker furnace (also called a moving-grate furnace), in which waste is fed onto a mechanically driven grate that moves material through progressive combustion zones [@Niessen2010]. Stoker furnaces are favored for their ability to handle heterogeneous waste streams without preprocessing, their operational reliability, and their long operational track record. Alternatives, including fluidized bed combustors (which suspend waste particles in an upward air current for more uniform combustion) and gasification systems, represent a small fraction of the Japanese fleet.

Energy recovery from combustion involves routing exhaust gases through a waste heat boiler to produce steam, which drives a turbine-generator set. The efficiency of this conversion depends on several factors: the steam temperature and pressure achievable, which are functions of furnace design and the metallurgical limits imposed by corrosive combustion gases; the turbine efficiency; and the extent to which parasitic electrical loads within the facility reduce net output. Larger facilities can justify higher-pressure boiler systems and more sophisticated turbine configurations, creating the scale economies that the regression analysis in this thesis detects [@vanBeukering1999]. Older facilities, designed to earlier engineering standards, cannot be straightforwardly upgraded to achieve modern performance levels because the boiler and turbine systems are integral to the structural design of the building.

### 2.2.3 Policy Context: Energy and Climate Drivers

Two policy developments frame the period analyzed in this thesis. First, the 2002 Law Concerning the Promotion of the Use of Non-Fossil Energy Sources and Effective Use of Fossil Energy Materials encouraged municipalities to expand power generation at incineration facilities, and the subsequent Renewable Portfolio Standard and its successor Feed-in Tariff (FiT) system made waste-derived electricity a revenue source that could offset operating costs [@MOEJ2022]. The FiT introduced in 2012, following the Fukushima disaster, included waste-to-energy at rates that varied by facility type and scale.

Second, the 2015 Paris Agreement and Japan's Nationally Determined Contribution (NDC) commitments set increasingly stringent targets for economy-wide emissions reductions. Waste management contributes to Japan's greenhouse gas inventory through methane emissions from landfills, process CO₂ from combustion of biogenic and fossil fractions of waste, and the avoided emissions credited when waste-derived electricity displaces grid power [@MOEJ2024]. The net climate impact of incineration depends critically on the efficiency of energy recovery — precisely the variable this thesis examines.

The 2050 carbon neutrality target, formalized in Japan's Green Growth Strategy (2020) and subsequent policy documents, has intensified scrutiny of the waste sector. The government's approach has been to encourage consolidation — fewer, larger, more efficient facilities — rather than to mandate specific technology upgrades. This strategy is implicitly validated by the findings of this thesis, though the pace of consolidation observed in the data suggests it is proceeding more slowly than net-zero targets may require.

### 2.2.4 Fleet Modernization and Consolidation

The empirical literature on Japan's fleet trajectory is largely descriptive. Studies by the Ministry of the Environment's research institutes have documented the decline in facility count and the increase in power-generating share, but without multivariate analysis of what distinguishes modernizing from stagnating portions of the fleet [@MOEJ2022]. Aggregate statistics show that total incineration capacity has remained relatively stable even as facility count has fallen — consistent with a consolidation trend in which small old facilities are replaced by fewer large new ones.

International comparisons are instructive. Northern European countries, particularly Sweden, Denmark, and Germany, operate WtE fleets with substantially higher average energy recovery efficiencies than Japan, attributable to a combination of larger average facility size, district heating integration that allows recovery of both electricity and heat, and more recent construction vintage [@Münster2010]. Japan's lack of district heating networks — a consequence of its different urban form and climate patterns in major population centers — means that only electrical efficiency is typically considered, understating the potential thermal recovery value but also limiting the realistic efficiency ceiling.

## 2.3 Industrial Ecology: Material Metabolism and Infrastructure Lock-In

### 2.3.1 Material Metabolism as Analytical Framework

Industrial ecology approaches waste management as a question of material flows through social-technical systems — the "metabolism" of industrial society, by analogy with biological metabolism [@Ayres1994]. In this framing, incineration facilities are nodes in a material flow network: they receive organic and inorganic waste, transform it through combustion, and export energy, bottom ash, and air emissions. The efficiency of this transformation — how much useful energy is extracted per unit of material processed — is a direct measure of the metabolic productivity of the node.

The material metabolism perspective draws attention to system-level properties that facility-level analysis might miss. A single high-efficiency facility embedded in a network of low-efficiency facilities may have limited system-level impact if waste routing decisions are driven by proximity rather than efficiency. Conversely, consolidation of waste flows toward high-efficiency nodes is a system-level intervention that requires institutional coordination beyond the technical capacity of individual facilities. This perspective shapes the policy discussion in Chapter 5, where the fleet-level implications of the regression findings are developed.

### 2.3.2 Infrastructure Lock-In: Mechanisms and Applications

Lock-in, in the industrial ecology literature, refers to the persistence of suboptimal technological trajectories due to the co-evolutionary entrenchment of physical infrastructure, institutions, and social practices [@Unruh2000]. The concept has roots in evolutionary economics — Arthur's (1989) analysis of path dependence in technology adoption — but has been developed in the sustainability transitions literature to explain why sociotechnical systems resist change even when superior alternatives are available [@Geels2004].

Carbon lock-in is the specific case where energy and material systems dependent on fossil carbon persist beyond their economic or environmental optimum. Unruh [-@Unruh2000] identifies three interacting mechanisms: technological lock-in (existing infrastructure embodies past design choices and is costly to abandon), institutional lock-in (regulatory frameworks, subsidy structures, and market rules co-evolve with dominant technologies), and cognitive lock-in (professional expertise, organizational routines, and public expectations are adapted to existing technology). All three mechanisms are visible in Japan's incineration sector: physical facilities with 30-year lifespans embody 1980s and 1990s engineering; municipal waste management governance is organized around existing facility locations; and the expertise of the waste management workforce is calibrated to stoker furnace operation.

The lock-in hypothesis has a specific empirical prediction for this study: if efficiency is primarily determined by design decisions made at construction, then the within-facility variance in efficiency over time should be low — much lower than the between-facility variance driven by differences in construction vintage and design capacity. This prediction is tested directly in the panel regression analysis. The result — a within-to-total variation ratio of approximately 0.11 (stable across pre- and post-Fukushima subsamples) — provides clear support for the lock-in mechanism: roughly 89% of efficiency variation is between facilities, not within them over time.

### 2.3.3 Circular Economy and Circular Transition

Alongside the lock-in literature sits the growing body of work on circular economy and circular transition — the reorganization of material flows to eliminate waste and maintain the value of materials and energy in use [@EllenMacArthurFoundation2013]. In the waste management context, circular economy thinking prioritizes material recovery (recycling, reuse) over energy recovery (incineration with power generation), which in turn is preferred over simple disposal (landfilling or combustion without energy recovery).

This hierarchy creates an apparent tension with WtE: by converting materials to energy, incineration forecloses material recovery options. However, the industrial ecology literature increasingly treats WtE not as an alternative to circular economy but as an element of an integrated system that handles residual waste streams that cannot be economically recycled [@Astrup2015]. In this view, the question is not whether to incinerate but how efficiently to recover energy from the incineration that will inevitably occur. The "circular transition" concept, as used in this thesis, refers specifically to the shift from non-energy-recovering incineration toward high-efficiency WtE — a transition that is clearly underway in Japan but far from complete.

### 2.3.4 Stranded Assets and Infrastructure Transition

A third conceptual thread from the industrial ecology and sustainability transitions literature concerns stranded assets — infrastructure that loses value before the end of its physical or economic life because of shifts in the regulatory, technological, or market environment [@Caldecott2016]. In the context of this thesis, the stranded asset risk applies to two types of facilities: old low-efficiency power-generating incinerators that are unlikely to improve their performance before retirement, and non-power-generating facilities that may face political pressure to add generation capacity they are too old or too small to accommodate economically.

The stranded asset concept connects to the net-zero policy discussion because it highlights the cost dimension of transition. A municipality that built a new incinerator in 2000 faces a very different calculus from one that built in 1985: the former facility may have 15 years of remaining service life and be young enough to justify retrofitting or efficiency improvements; the latter may be approaching end of life in any case. The regression finding that age is the single most consistent predictor of efficiency — with effects ranging from −0.028 to −0.043 per year — means that the stranded asset risk is spatially distributed across Japan according to the vintage of local infrastructure, creating a heterogeneous transition challenge.

## 2.4 Determinants of Energy Recovery Efficiency: The Empirical Literature

### 2.4.1 Scale Effects

The relationship between facility scale and energy recovery efficiency is among the most consistently documented findings in the WtE literature. Larger facilities can support higher-pressure boiler systems, more sophisticated turbine configurations, better instrumentation and control, and more specialized technical staff, all of which contribute to higher electricity output per tonne of waste [@Genon2008]. Scale economies in boiler design are particularly significant: at small scale, heat losses relative to output are large, and the pressure ratings achievable are limited by the cost of pressure vessel fabrication. At large scale, fixed costs are amortized over more output and engineering can be optimized.

This relationship has been documented empirically in European contexts, where WtE facilities range from small municipal installations to very large urban facilities exceeding 1,000 tonnes per day of capacity. Studies of the Danish and German fleets find positive and statistically significant relationships between facility capacity and electrical efficiency [@Münster2010]. The current study extends this finding to Japan's fleet, where the scale range is similarly large — from facilities below 50 t/day to installations exceeding 500 t/day — and where the policy relevance of the scale relationship is directly tied to the consolidation agenda.

### 2.4.2 Facility Age and Vintage Effects

Age effects in WtE efficiency have been analyzed less systematically than scale effects, partly because most empirical studies use cross-sectional data that conflate age with design vintage. A facility built in 1985 operates with 1985 engineering standards regardless of how many years have passed; its low efficiency reflects design constraints, not degradation. This distinction between age-as-proxy-for-vintage and age-as-wear-and-tear is important but often blurred in the literature.

Some studies have examined facility degradation — the decline in performance of boiler systems and turbines as they age — finding modest efficiency losses that are partially offset by maintenance and component replacement [@Astrup2015]. However, the more robust finding across multiple contexts is that the vintage effect (newer facilities are built to more efficient designs) dominates the degradation effect. This is consistent with the lock-in hypothesis: design determines efficiency, and design improves with each generation of new construction.

The Japanese context adds a specific dimension: the rapid expansion of the fleet in the 1980s and 1990s means that a large cohort of facilities share a similar vintage and will reach end of life within a relatively compressed time window. This creates both a challenge (managing a wave of simultaneous retirements) and an opportunity (replacing them with modern, efficient facilities on a planned schedule).

### 2.4.3 Capacity Utilization

Capacity utilization — the ratio of actual throughput to design capacity — affects efficiency through thermodynamic and operational mechanisms. At low utilization, combustion systems operate outside their design range, making it difficult to maintain stable temperatures and steam parameters. Below certain throughput thresholds, facilities may switch from power-generating mode to simple heat disposal mode to maintain combustion stability. High utilization, conversely, allows facilities to operate at or near design conditions, maximizing steam generation and turbine output.

The empirical literature on utilization effects in WtE is sparse but generally consistent with a positive relationship [@Beylot2015]. The policy implication — that routing more waste to high-utilization facilities improves system-level efficiency — points toward regional consolidation as a policy lever. In Japan's highly fragmented waste management system, where municipal jurisdiction boundaries often limit inter-municipality waste transfers, this implication is institutionally challenging to implement even where the technical case is clear.

### 2.4.4 Waste Composition and Heating Value

The energy content of waste — typically measured as lower heating value (LHV) in MJ/kg — is a natural candidate for an efficiency determinant. Higher-energy waste should, all else equal, generate more steam per unit mass, and hence more electricity. However, the empirical literature on this relationship is surprisingly ambiguous [@Astrup2009].

Several mechanisms complicate the straightforward prediction. First, modern furnace control systems are designed to maintain stable combustion temperatures across a range of waste heating values, effectively buffering the direct relationship between waste energy content and boiler output. Second, high-heating-value waste may require additional cooling (through waste mixing or steam injection) to prevent equipment damage, reducing net efficiency gains. Third, the heating value data available in administrative datasets — typically estimated from waste composition surveys rather than direct measurement — may not accurately reflect actual combustion conditions.

This thesis finds that heating value is not a statistically significant predictor of efficiency in any of the eight model specifications, a result that aligns with the more skeptical strand of the literature and has important implications for data collection policy.

### 2.4.5 Regional and Grid Factors

Some studies include regional variables to capture differences in grid emission factors, energy prices, or climate conditions that might affect operational decisions. The theoretical case for a grid emission factor effect on *efficiency* (as opposed to *avoided emissions*) is not straightforward — a facility's efficiency in converting waste to electricity should not depend on what that electricity displaces in the grid. However, there may be indirect effects through incentive structures: in regions with high grid emission factors, the value of waste-derived electricity is higher, potentially incentivizing investment in efficiency upgrades or attracting more capital to new facility construction.

This thesis includes regional grid emission factors as a control variable and finds that the coefficient sign is unstable across model specifications — positive in some and negative in others — suggesting that this variable does not capture a stable efficiency determinant. This instability is itself informative: it suggests that regional energy market conditions are not a reliable lever for improving incineration efficiency, and that the primary determinants are physical (age, scale) rather than economic.

## 2.5 The Research Gap: Fleet-Level Heterogeneity Analysis

The literature surveyed above shares a common limitation: it treats WtE efficiency determinants as properties of technology types or average systems, rather than as characteristics that vary systematically across a heterogeneous fleet over time. Cross-sectional studies capture between-facility variation at a point in time but cannot assess whether the relationships are stable, how they change as the fleet modernizes, or what within-facility dynamics look like over time. Technology-level analyses abstract from the facility-level variation that is, empirically, the main source of efficiency differences in the Japanese fleet.

Three gaps are particularly important. First, no published study has applied panel regression methods to Japan's full incineration fleet using facility-level administrative data over a multi-decade period. The available data source — the Ministry of the Environment's General Waste Treatment Survey — covers all operating facilities annually and contains the variables needed for this analysis, but it has not been exploited for this purpose in the academic literature. Second, the question of within-facility efficiency dynamics — whether facilities improve their performance over their operational lives — has not been addressed empirically for Japan. This question is theoretically central to the lock-in debate: if within-facility improvement is negligible, then operational optimization policies are ineffective and retirement/replacement is the only viable path. Third, the fleet-level implications of heterogeneity — the distribution of avoided emissions across facility types, the concentration of efficiency gains in a small number of large modern plants — have not been quantified.

This thesis addresses all three gaps. It contributes a panel dataset of 23,599 facility-year observations, regression estimates robust to multiple model specifications, and a framework for translating fleet heterogeneity findings into net-zero policy recommendations grounded in industrial ecology theory.
