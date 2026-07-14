# Major-Revision Literature Positioning

Search date: 14 July 2026

## Purpose

This note records the comparator search used to delimit the paper's novelty.
It is not a systematic review. The search was designed to find the closest
Japanese facility-level studies, recent high-profile national waste-to-energy
benchmarks, and methodological guidance relevant to reconstructed
administrative lineages.

## Search Logic

Searches combined terms for Japan, municipal solid waste incineration,
electricity or heat recovery, facility panels, longitudinal records, generator
performance, national databases, efficiency hierarchy, and record-linkage
validation. Publisher pages, journal repositories, government portals, and DOI
records were preferred over secondary summaries.

The search established four comparator classes:

1. Japanese facility-panel studies of heat or electricity production.
2. Detailed engineering studies of electricity generation per unit waste.
3. Recent national studies that rank heterogeneous incinerators or model
   optimization potential.
4. Record-linkage guidance for longitudinal administrative data without a
   stable identifier.

## Closest Comparators and Boundaries

| Comparator | What it establishes | What this paper adopts | What remains distinct here |
|:--|:--|:--|:--|
| Sasao (2018), DOI `10.31025/2611-4135/2018.13650` | Japanese incinerators can be analyzed as repeated facility observations; treatment capacity and continuous operation matter for reported heat and electricity. | A facility-level national perspective and explicit scale controls. | A twenty-year identity-reconstructed event history, first reported installed-capacity entry, denominator decomposition, and separation of installed generator design from annual use. |
| Shino (2019), DOI `10.3985/jjsmcwm.30.113` | Electricity per unit waste is observable, but thermal efficiency requires calorific-value and combustion information; the study uses 22 Tokyo facilities in FY2012-FY2017. | Careful treatment of gross output per tonne as an administrative indicator rather than net thermal efficiency. | National coverage, longitudinal entry risk sets, and a component decomposition that does not require claiming thermal efficiency. |
| Cui et al. (2026), DOI `10.1038/s41467-026-69897-w` | A national engineering database can expose an efficiency hierarchy and distinguish disposal-oriented from energy-recovery plants. It covers 975 Chinese plants and 2,151 incinerators with richer technical and operational measurements. | The premise that facilities are heterogeneous and should not be reduced to a fleet mean or count. | Japan's administrative transition history, identity reconstruction across code gaps, sparse first-entry modeling, and decomposition of apparent cohort performance into installed capacity and annual capacity factor. No Cui data, equations, optimization frontier, classification thresholds, or scenarios are reproduced. |
| Harron, Doidge, and Goldstein (2020), DOI `10.1080/03014460.2020.1742379` | Linkage error can bias longitudinal inference; quality should be assessed with validation data, linked-versus-unlinked comparisons, and sensitivity to linkage choices. | Blinded clerical-review packets and linkage-sensitive analysis frames. | A domain-specific reconstruction of Japanese incinerator administrative lineages and direct propagation of identity restrictions into the entry model. |

## Defensible Novelty Statement

The paper should not claim that it is the first Japanese facility panel, the
first study of electricity per tonne, or the first national incinerator
hierarchy. Those claims would be contradicted by Sasao, Shino, and Cui.

The defensible contribution is the integration of three margins that prior
comparators study separately or do not identify longitudinally:

1. **Coverage margin:** facility participation, waste throughput, and reported
   processing design capacity answer different fleet-coverage questions.
2. **Transition margin:** first reported entry into positive installed
   electrical capacity is estimated from witnessed at-risk histories rather
   than inferred from a cross-section.
3. **Component margin:** conditional electricity output is separated into
   installed generator capacity and annual capacity factor, preventing a newer
   cohort's larger generator from being misread as uniformly better operation.

The strongest result is not the intuitive statement that large facilities are
more likely to generate electricity. It is that this scale-selective transition
survives lower-degree-of-freedom Firth models, alternative continuity frames,
whole-lineage bootstrap uncertainty, and every event-level perturbation, while
the component model shows that the apparent cohort hierarchy lies primarily in
installed design rather than annual use. Together, these results show why
facility counts and undivided output ratios can diagnose the same fleet
differently.

## Claims the Evidence Does Not Support

- causal effects of scale, age, policy, or the 2011 earthquake and nuclear
  accident;
- verified retrofit, replacement, or commissioning dates;
- net electricity export, useful heat, thermal efficiency, avoided emissions,
  or lifecycle benefit;
- a complete engineering frontier comparable to Cui et al.;
- completed independent linkage validation until a second reviewer returns the
  blinded packet and disagreements are adjudicated.

## Verified Sources

- Sasao article page: <https://digital.detritusjournal.com/articles/how-does-municipal-solid-waste-policy-affect-heat-and-electricity-produced-by-incinerators/109>
- Shino article page: <https://www.jstage.jst.go.jp/article/jjsmcwm/30/0/30_113/_article/-char/en>
- Cui et al. article page: <https://www.nature.com/articles/s41467-026-69897-w>
- Harron et al. open version: <https://discovery.ucl.ac.uk/id/eprint/10099105/>
- e-Stat survey record: <https://www.e-stat.go.jp/en/statistics/00650101>
- e-Stat terms of use: <https://www.e-stat.go.jp/en/terms-of-use>

The e-Stat terms permit reuse with source citation and require an edited-content
notice when content is modified. Repository and manuscript data statements
must therefore cite e-Stat and clearly distinguish source workbooks from
researcher-created harmonized files.
