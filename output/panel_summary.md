# Incineration Facility Panel Dataset Summary

- **Observations:** 23,599
- **Years:** FY2005 to FY2024 (20 years)
- **Unique facilities:** 2,949
- **Prefectures:** 47
- **Columns:** 24

## Facilities per year

| FY | Facilities | % with power gen |
|:---|:----------:|:----------------:|
| 2005 | 1,318 | 21.6% |
| 2006 | 1,301 | 22.7% |
| 2007 | 1,307 | 22.7% |
| 2008 | 1,307 | 23.1% |
| 2009 | 1,310 | 23.8% |
| 2010 | 1,245 | 24.5% |
| 2011 | 1,251 | 24.9% |
| 2012 | 1,222 | 26.0% |
| 2013 | 1,199 | 26.9% |
| 2014 | 1,207 | 27.9% |
| 2015 | 1,192 | 29.4% |
| 2016 | 1,154 | 31.5% |
| 2017 | 1,139 | 32.8% |
| 2018 | 1,128 | 33.9% |
| 2019 | 1,093 | 35.1% |
| 2020 | 1,087 | 35.5% |
| 2021 | 1,060 | 37.3% |
| 2022 | 1,038 | 38.9% |
| 2023 | 1,027 | 39.8% |
| 2024 | 1,014 | 41.1% |

## Key variable coverage

| Variable | Coverage | Notes |
|:---------|:--------:|:------|
| throughput_t_year | 98.3% | Annual waste processed |
| capacity_t_day | 99.8% | Design capacity |
| year_started | 99.8% | Year operations began |
| facility_age | 99.8% | Derived: fiscal_year - year_started |
| heating_value_kj_kg | 96.2% | Energy content of waste |
| power_capacity_kw | 35.4% | Only for power-gen facilities |
| power_generated_mwh | 34.6% | Only for power-gen facilities |
| power_sold_mwh | 7.9% | FY2018+ only |
| energy_efficiency_mwh_per_t | 33.2% | Derived: MWh / throughput |

## Power-generating subsample

| Metric | Value |
|:-------|:------|
| Observations | 6,950 |
| Years | FY2005 to FY2024 |
| power_generated_mwh coverage | 98.1% |
| energy_efficiency_mwh_per_t coverage | 96.0% |
| power_efficiency_pct coverage | 98.7% |
