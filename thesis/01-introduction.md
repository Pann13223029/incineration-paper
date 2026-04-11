# Chapter 1: Introduction

## 1.1 The Paradox of Japan's Incineration Infrastructure

Every day, Japan burns approximately 100,000 tonnes of municipal solid waste. This is not an anomaly or a failure of recycling policy — it is the deliberate architecture of the world's most incineration-dependent waste management system, built over decades in a country where landfill space is scarce, geography is mountainous, and population density is extreme <!-- VERIFY: citation needed -->. Japan's incinerators are not temporary solutions awaiting replacement by something cleaner. They are permanent infrastructure, embedded in local government budgets, staffed by long-term employees, and serving as the physical backbone of urban metabolism in hundreds of municipalities.

And yet Japan has committed to carbon neutrality by 2050. This commitment creates a tension that has received insufficient analytical attention: the country's waste sector, which contributes meaningfully to national greenhouse gas emissions, is anchored by a fleet of over 1,000 facilities with lifespans typically exceeding 30 years. The question is not whether Japan will eventually decarbonize its waste system. The question is which facilities can contribute to that transition — and which cannot — and what determines the difference.

This thesis addresses that question through the lens of energy recovery efficiency: the amount of electricity generated per tonne of waste processed. Among Japan's incinerators, this metric varies dramatically. Some modern facilities generate nearly 0.5 MWh per tonne, comparable to small-scale renewable energy installations in terms of carbon avoided. Others — the majority — generate nothing at all, burning waste with no attempt to recover its thermal energy. Between these extremes lies a heterogeneous fleet whose carbon implications depend critically on which segment grows, which stagnates, and which is retired.

## 1.2 Background: Japan's Waste-to-Energy System

Japan's commitment to incineration dates to the 1960s, when rapid urbanization combined with severe land constraints made landfilling politically and physically untenable in most of the country [@Matsuietal2015 <!-- VERIFY: citation needed -->]. The national government provided subsidies for municipal incinerators, and local authorities responded by building them at scale. By the early 2000s, Japan operated more than 1,300 general waste incineration facilities — more than any other nation — and the system had become deeply institutionalized <!-- VERIFY: citation needed -->.

The technical core of these facilities is a stoker grate furnace (a mechanically driven combustion bed that moves waste through the burn zone), supplemented in more modern installations by heat recovery boilers and steam turbines that convert thermal energy into electricity. This conversion — from waste combustion to electrical output — is what transforms an incinerator into a "waste-to-energy" (WtE) facility. Not all Japanese incinerators make this conversion. Many, particularly older ones, simply burn waste and release heat to the atmosphere.

The energy recovery story has changed over time. In 2005, only about 21.6% of Japan's operating incinerators generated any electricity. By 2024, that share had risen to 41.1% — a substantial increase, achieved partly through new construction and partly through retirement of non-generating facilities. Over the same period, total facility count fell from 1,318 to 1,014. The fleet is shrinking and modernizing simultaneously, but 59% of active facilities still produce no power — a striking persistence given two decades of energy policy evolution.

This trajectory intersects with two major structural shocks. The first is the 2011 Fukushima Daiichi nuclear disaster, which caused Japan to shut down virtually all of its nuclear generating capacity and scrambled national energy markets. In this context, distributed power sources — including waste-to-energy — gained renewed policy attention as Japan sought to replace lost baseload capacity with a diversified portfolio [@Hasegawa2012 <!-- VERIFY: citation needed -->]. The second is the Paris Agreement commitments of 2015 and Japan's subsequent Green Growth Strategy, which set the 2050 carbon neutrality target and prompted systematic review of emission sources across all sectors, including waste.

## 1.3 The Problem: Heterogeneity Without Accountability

Despite this policy backdrop, Japan's incineration fleet has not been systematically analyzed through a heterogeneity lens. Most existing research treats WtE facilities as a category — comparing Japan to other countries, modeling aggregate emission flows, or evaluating specific technologies in isolation. What has been missing is a facility-level account of *what distinguishes high-efficiency from low-efficiency facilities*, and whether these distinctions are stable over time or responsive to operational and policy variables.

This gap matters for two reasons. First, aggregate statistics obscure the distribution. A fleet average efficiency of 0.30 MWh/t could represent a uniformly mediocre system or a bimodal distribution of excellent and poor performers. These scenarios have entirely different policy implications: the former calls for universal technology upgrades, while the latter calls for selective retirement and consolidation. Second, if efficiency is determined at the design stage rather than operationally, then no amount of operational incentive — higher feed-in tariffs, carbon pricing, efficiency audits — can improve the performance of existing facilities. Policy must instead work through the investment and decommissioning cycle.

The industrial ecology literature has developed concepts precisely for this kind of problem. Infrastructure lock-in describes the phenomenon whereby early investment decisions constrain future options through physical durability, sunk costs, and co-evolutionary institutional arrangements [@Unruh2000]. Carbon lock-in is the specific case where fossil fuel-intensive infrastructure persists beyond its economic or environmental optimum because the system of production, regulation, and social expectation surrounding it resists change [@GruebbandWilson2018 <!-- VERIFY: citation needed -->]. Applied to waste incineration, lock-in predicts that low-efficiency facilities will continue operating not because they are optimal but because the institutional and physical architecture of local waste management makes replacing them costly and politically difficult.

Whether Japan's fleet is experiencing carbon lock-in, circular transition, or some heterogeneous combination of both — this is the empirical question this thesis addresses.

## 1.4 Research Question and Objectives

The primary research question guiding this thesis is:

**What facility characteristics predict energy recovery efficiency among Japan's power-generating incinerators, and how has this changed as the fleet modernizes?**

To answer this, the thesis pursues four specific objectives:

1. **Describe fleet evolution** — document how the composition, scale, and power-generation penetration of Japan's incineration fleet has changed between FY2005 and FY2024.

2. **Identify efficiency determinants** — estimate the effects of facility age, design capacity, capacity utilization, waste heating value, and regional grid emission factors on energy recovery efficiency, using panel regression with cluster-robust inference.

3. **Assess within-facility dynamics** — determine whether efficiency changes meaningfully within facilities over time, or whether it is effectively fixed at installation.

4. **Derive policy implications** — translate the empirical findings into recommendations consistent with Japan's net-zero trajectory and the industrial ecology framework of material metabolism and infrastructure transition.

## 1.5 Significance of the Study

This study makes three contributions. Analytically, it provides the first systematic multi-year panel regression of efficiency determinants across Japan's full incineration fleet, using facility-level data from the Ministry of the Environment's General Waste Treatment Survey. Most prior empirical work on WtE efficiency has relied on cross-sectional comparisons or technology-level analyses; this panel approach allows decomposition of between-facility and within-facility variation in ways that directly inform policy.

Theoretically, the study applies infrastructure lock-in theory — developed primarily in the context of energy systems — to the waste sector, contributing to industrial ecology's understanding of how material metabolism infrastructure evolves and resists change. The finding that efficiency is design-determined, with a within-facility variation ratio of just 0.001, provides unusually clean empirical support for the lock-in hypothesis in this domain.

Policy-practically, the results arrive at a moment when Japan is actively restructuring its waste management system. The government's 2023 revisions to the Basic Policy on Establishing a Sound Material-Cycle Society call for further consolidation of the incineration fleet and increased energy recovery <!-- VERIFY: citation needed -->. This thesis provides an evidence base for evaluating those policies: specifically, the finding that scale and youth are the two most reliable efficiency predictors suggests that consolidation — replacing multiple small old facilities with fewer large modern ones — is the intervention most likely to yield efficiency gains.

## 1.6 Thesis Structure

The remainder of this thesis is organized as follows. Chapter 2 reviews the relevant literature, covering the institutional context of Japan's WtE sector, the industrial ecology concepts of lock-in and material metabolism, the empirical literature on energy recovery efficiency determinants, and the gap this study addresses. Chapter 3 describes the data, variable construction, panel design, and estimation strategy, including the rationale for choosing random effects over facility fixed effects. Chapter 4 presents the results: descriptive fleet trends, regression estimates across eight model specifications, and robustness checks. Chapter 5 discusses what the results mean for theory and policy, including the Fukushima effect, the role of scale and age, and the limits of operational optimization. Chapter 6 concludes with a summary of contributions, policy recommendations, and directions for future research.

A note on framing: throughout this thesis, "energy recovery efficiency" refers specifically to the ratio of electricity generated to waste processed (MWh per tonne), among facilities that generate any electricity at all. Facilities with no power generation capability are analyzed as part of the fleet composition story in the descriptive sections but are excluded from the regression analysis, where the dependent variable requires a positive value. This distinction — between the 41% of facilities that generate power and the 59% that do not — is itself one of the central empirical findings of the study.
