# Robustness Checks

All models: Pooled OLS, cluster-robust SEs, DV = log(MWh/t) unless noted.

| Specification | N | R² | facility_age | capacity_100t | cap_utilization |
|:---|---:|---:|---:|---:|---:|
| Baseline (full sample) | 5604 | 0.294 | -0.0284*** | 0.0795*** | 0.6375*** |
| Pre-Fukushima (2005-2010) | 1383 | 0.428 | -0.0427*** | 0.0814*** | 0.5639*** |
| Post-Fukushima (2014-2024) | 3942 | 0.407 | -0.0324*** | 0.0950*** | 0.7073*** |
| Capacity: Small | 1985 | 0.234 | -0.0317*** | 0.3155*** | 0.8300*** |
| Capacity: Medium | 1823 | 0.358 | -0.0326*** | -0.0177 | 0.5164** |
| Capacity: Large | 1796 | 0.351 | -0.0241*** | 0.0426*** | 0.6721*** |
| Raw DV (MWh/t) | 5604 | 0.337 | -0.0072*** | 0.0209*** | 0.1670*** |
| Without heating value | 5673 | 0.294 | -0.0283*** | 0.0787*** | 0.6463*** |
