# Major-Revision Red-Team Review

Review date: 14 July 2026

## Decision

The revised paper has a credible and clearly bounded contribution for professor
and external review. Its novelty is the integrated diagnosis of three margins
in one identity-reconstructed national panel: fleet coverage, first reported
installed-capacity entry, and the separation of installed generator sizing from
annual electrical use. It does not need, and should not make, a claim of a new
estimator or the first Japanese facility panel.

No manuscript can make novelty literally unrefusable. The present version makes
the contribution difficult to dismiss without disputing a specific estimand,
data layer, or result. The remaining P0 dependency is independent human review
of the blinded linkage packet.

## Panel Attacks And Disposition

| Persona | Strongest attack | Revision response | Residual status |
|:--|:--|:--|:--|
| Waste Management editor | "Large and newer facilities generate more" sounds intuitive rather than publishable. | The paper now distinguishes facility-count, throughput, and design-capacity coverage; estimates witnessed first entry; and shows that cohort differences lie primarily in raw installed kW rather than uniformly higher capacity factor. | Addressed as an integrated measurement contribution. |
| Sparse-event econometrician | Thirty-five events cannot support the former 11-parameter primary model. | The primary Firth model is frozen at five parameters, uses 1,999 complete whole-lineage bootstraps, and retains the larger model only as sensitivity. | Addressed, subject to the irreducible precision limit. |
| Adversarial reviewer | One mislabeled event may create the scale result. | Every event is reclassified once and every event lineage is deleted once; all 70 attacks leave the 300-versus-100 t/day odds ratio between 6.12 and 7.30. | Addressed for single-event influence, not unmeasured confounding. |
| Record-linkage specialist | Reconstructed lineages may manufacture transitions. | Code gaps and the FY2019-FY2020 recode are explicit; uncertain links are exposed; same-episode and identity-certain frames are reported; a 558-pair blinded packet is generated. | Partly addressed. Independent clerical review and adjudication remain P0. |
| Incineration engineer | Gross MWh/t conflates installed sizing and operation. | Raw installed kW, electrical capacity factor, waste loading, and direct gross output are modeled separately; reported start year is not called generator vintage. | Addressed within available administrative fields; net output, useful heat, and thermodynamic efficiency remain outside scope. |
| Comparator and originality reviewer | The argument may duplicate Sasao, Shino, or Cui et al. | The paper states exactly what is adapted and what is different: no comparator data, code, frontier, thresholds, or scenarios are reused; the Japan transition, identity, and component estimands are project-specific. | Addressed if attribution and bounded novelty language remain visible. |
| Reproducibility reviewer | A polished narrative may conceal researcher degrees of freedom. | Raw-file hashes, stage manifests, a frozen model decision, complete bootstrap requirements, evidence synchronization, and executable claim checks are retained. | Addressed for the implemented pipeline; retrieval timestamps remain unavailable. |

## Contribution That Should Survive Peer Review

1. Facility participation is not a proxy for waste-volume coverage: the FY2024
   shares are 41.1% of records, 80.1% of throughput, and 70.5% of processing
   design capacity.
2. First reported installed-capacity entry is rare but strongly scale-selective:
   the primary 300-versus-100 t/day odds ratio is 6.72 with a 1,999-bootstrap
   interval of 4.31-12.46, and it survives all specified frame and event attacks.
3. Apparent start-year cohort hierarchy is primarily an installed-design
   pattern: older cohorts have much lower adjusted installed kW, but not
   uniformly lower annual electrical capacity factors.
4. Linking these margins changes interpretation. A fleet can have limited
   equipment participation, high waste coverage, scale-selective entry, and
   cohort differences in generator sizing at the same time.

## Claims That Must Remain Prohibited

- causal effects of processing scale, age, policy, or retrofit;
- verified physical commissioning, replacement, or closure events;
- net electricity, useful heat, thermal efficiency, or recoverable potential;
- a transferable engineering frontier comparable to Cui et al.;
- completed independent linkage validation before the blinded review is returned.

## Next Decision Gate

Ask an independent reviewer to classify the blinded linkage packet without the
answer key. Report agreement by pair stratum, adjudicate disagreements, and
rerun the entry models if any event lineage changes. If that review preserves
the event set and estimates, the paper moves from strong computationally audited
draft to externally checked research product. If it does not, the linkage layer
must be revised before stronger novelty language is considered.
