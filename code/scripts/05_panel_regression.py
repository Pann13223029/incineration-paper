"""
05_panel_regression.py
======================
Panel regression: what predicts energy recovery efficiency among
Japan's power-generating incinerators?

METHODOLOGY PIVOT (from EDA findings):
- Within-facility efficiency SD ratio = 0.001
- Facility FE absorbs all signal (efficiency is design-determined)
- PRIMARY: Pooled OLS with cluster-robust SEs (clustered by facility)
- COMPARISON: Random Effects (RE) + Hausman test
- ROBUSTNESS: Year FE only (to absorb time trends)

DV: log(energy_efficiency_mwh_per_t) — winsorized to [0.01, 0.80]
IVs: facility_age, capacity_t_day, capacity_utilization,
     heating_value_kj_kg, grid_ef_kgco2_kwh

Sample: power-generating facilities only (has_power_gen == True)
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'processed')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Physical bounds for efficiency winsorization
EFF_FLOOR = 0.01  # MWh/t
EFF_CEIL = 0.80   # MWh/t


def load_and_clean():
    """Load enriched panel, apply cleaning rules from EDA."""
    path = os.path.join(PROCESSED_DIR, 'incineration_panel_enriched.csv')
    df = pd.read_csv(path)

    # Drop zero/missing throughput
    df = df[df['throughput_t_year'].notna() & (df['throughput_t_year'] > 0)].copy()

    # Power-gen subsample only
    power = df[df['has_power_gen'] == True].copy()

    # Require non-missing efficiency
    power = power[power['energy_efficiency_mwh_per_t'].notna()].copy()

    # Winsorize efficiency to physical bounds
    n_before = len(power)
    power = power[
        (power['energy_efficiency_mwh_per_t'] >= EFF_FLOOR) &
        (power['energy_efficiency_mwh_per_t'] <= EFF_CEIL)
    ].copy()
    n_dropped = n_before - len(power)

    # Log-transform DV
    power['log_efficiency'] = np.log(power['energy_efficiency_mwh_per_t'])

    # Create age bins for descriptive analysis
    power['age_group'] = pd.cut(
        power['facility_age'],
        bins=[0, 10, 20, 30, 100],
        labels=['0-10 yrs', '10-20 yrs', '20-30 yrs', '30+ yrs'],
        right=False
    )

    # Standardize capacity for interpretability
    power['capacity_100t'] = power['capacity_t_day'] / 100
    power['heating_value_1000kj'] = power['heating_value_kj_kg'] / 1000

    print(f"Clean power-gen sample: {len(power):,} obs")
    print(f"  Dropped {n_dropped} outliers outside [{EFF_FLOOR}, {EFF_CEIL}] MWh/t")
    print(f"  Facilities: {power['facility_code'].nunique()}")
    print(f"  Years: {power['fiscal_year'].min()}-{power['fiscal_year'].max()}")

    return power


def descriptive_stats(power):
    """Table 1: Summary statistics."""
    print("\n" + "=" * 60)
    print("TABLE 1: Summary Statistics (Power-Gen Subsample)")
    print("=" * 60)

    desc_vars = {
        'energy_efficiency_mwh_per_t': 'Efficiency (MWh/t)',
        'log_efficiency': 'log(Efficiency)',
        'facility_age': 'Facility Age (years)',
        'capacity_t_day': 'Capacity (t/day)',
        'capacity_utilization': 'Capacity Utilization',
        'heating_value_kj_kg': 'Heating Value (kJ/kg)',
        'power_capacity_kw': 'Power Capacity (kW)',
        'grid_ef_kgco2_kwh': 'Grid EF (kg-CO2/kWh)',
        'avoided_co2_t': 'Avoided CO2 (t/year)',
    }

    rows = []
    for var, label in desc_vars.items():
        if var in power.columns:
            s = power[var].dropna()
            rows.append({
                'Variable': label,
                'N': len(s),
                'Mean': f'{s.mean():.3f}',
                'Median': f'{s.median():.3f}',
                'SD': f'{s.std():.3f}',
                'Min': f'{s.min():.3f}',
                'Max': f'{s.max():.3f}',
            })

    desc_df = pd.DataFrame(rows)
    print(desc_df.to_string(index=False))

    # Save
    path = os.path.join(OUTPUT_DIR, 'table1_summary_stats.md')
    with open(path, 'w') as f:
        f.write("# Table 1: Summary Statistics (Power-Generating Facilities)\n\n")
        f.write(desc_df.to_markdown(index=False))
    print(f"\n  Saved: {path}")

    return desc_df


def efficiency_by_age_group(power):
    """Table 2: Efficiency by age group."""
    print("\n" + "=" * 60)
    print("TABLE 2: Efficiency by Facility Age Group")
    print("=" * 60)

    grouped = power.groupby('age_group', observed=True).agg(
        n_obs=('energy_efficiency_mwh_per_t', 'count'),
        mean_eff=('energy_efficiency_mwh_per_t', 'mean'),
        median_eff=('energy_efficiency_mwh_per_t', 'median'),
        mean_capacity=('capacity_t_day', 'mean'),
        mean_avoided=('avoided_co2_t', 'mean'),
        pct_of_total_avoided=('avoided_co2_t', lambda x: x.sum()),
    ).reset_index()

    total_avoided = power['avoided_co2_t'].sum()
    grouped['pct_of_total_avoided'] = (grouped['pct_of_total_avoided'] / total_avoided * 100).round(1)

    print(grouped.to_string(index=False))

    path = os.path.join(OUTPUT_DIR, 'table2_efficiency_by_age.md')
    with open(path, 'w') as f:
        f.write("# Table 2: Energy Recovery Efficiency by Facility Age Group\n\n")
        f.write(grouped.to_markdown(index=False))
    print(f"\n  Saved: {path}")


def run_pooled_ols(power):
    """Model 1: Pooled OLS with cluster-robust SEs."""
    print("\n" + "=" * 60)
    print("MODEL 1: Pooled OLS (cluster-robust SEs)")
    print("=" * 60)

    # Prepare regression data
    reg_vars = ['log_efficiency', 'facility_age', 'capacity_100t',
                'capacity_utilization', 'heating_value_1000kj', 'grid_ef_kgco2_kwh']
    reg_data = power[reg_vars + ['facility_code']].dropna()
    print(f"  Regression sample: {len(reg_data):,} obs")

    y = reg_data['log_efficiency']
    X = reg_data[['facility_age', 'capacity_100t', 'capacity_utilization',
                   'heating_value_1000kj', 'grid_ef_kgco2_kwh']]
    X = sm.add_constant(X)

    # Fit with cluster-robust SEs
    model = sm.OLS(y, X).fit(
        cov_type='cluster',
        cov_kwds={'groups': reg_data['facility_code']}
    )
    print(model.summary())

    return model


def run_ols_with_year_fe(power):
    """Model 2: OLS with year fixed effects."""
    print("\n" + "=" * 60)
    print("MODEL 2: OLS with Year Fixed Effects")
    print("=" * 60)

    reg_vars = ['log_efficiency', 'facility_age', 'capacity_100t',
                'capacity_utilization', 'heating_value_1000kj', 'grid_ef_kgco2_kwh',
                'fiscal_year', 'facility_code']
    reg_data = power[reg_vars].dropna()

    y = reg_data['log_efficiency']

    # Year dummies (drop first for identification)
    year_dummies = pd.get_dummies(reg_data['fiscal_year'], prefix='fy', drop_first=True, dtype=float)
    X = pd.concat([
        reg_data[['facility_age', 'capacity_100t', 'capacity_utilization',
                   'heating_value_1000kj', 'grid_ef_kgco2_kwh']],
        year_dummies
    ], axis=1)
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit(
        cov_type='cluster',
        cov_kwds={'groups': reg_data['facility_code']}
    )

    # Print only the main coefficients (not 19 year dummies)
    main_vars = ['const', 'facility_age', 'capacity_100t', 'capacity_utilization',
                 'heating_value_1000kj', 'grid_ef_kgco2_kwh']
    print(f"\n  R-squared: {model.rsquared:.4f}")
    print(f"  Adj R-squared: {model.rsquared_adj:.4f}")
    print(f"  N: {model.nobs:.0f}")
    print(f"\n  Main coefficients (year FE suppressed):")
    print(f"  {'Variable':<25} {'Coef':>10} {'SE':>10} {'t':>8} {'p':>8}")
    print("  " + "-" * 65)
    for var in main_vars:
        if var in model.params.index:
            coef = model.params[var]
            se = model.bse[var]
            t = model.tvalues[var]
            p = model.pvalues[var]
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            print(f"  {var:<25} {coef:>10.4f} {se:>10.4f} {t:>8.2f} {p:>8.4f} {sig}")

    return model


def run_random_effects(power):
    """Model 3: Random Effects (if linearmodels available)."""
    print("\n" + "=" * 60)
    print("MODEL 3: Random Effects")
    print("=" * 60)

    try:
        from linearmodels.panel import RandomEffects
    except ImportError:
        print("  linearmodels not installed. Skipping RE.")
        return None

    reg_vars = ['log_efficiency', 'facility_age', 'capacity_100t',
                'capacity_utilization', 'heating_value_1000kj', 'grid_ef_kgco2_kwh',
                'fiscal_year', 'facility_code']
    reg_data = power[reg_vars].dropna()

    # Set panel index
    reg_data = reg_data.set_index(['facility_code', 'fiscal_year'])

    y = reg_data['log_efficiency']
    X = reg_data[['facility_age', 'capacity_100t', 'capacity_utilization',
                   'heating_value_1000kj', 'grid_ef_kgco2_kwh']]
    X = sm.add_constant(X)

    model = RandomEffects(y, X).fit()
    print(model.summary)

    return model


def comparison_table(m1, m2, m3=None):
    """Save model comparison table."""
    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    path = os.path.join(OUTPUT_DIR, 'regression_results.md')
    with open(path, 'w') as f:
        f.write("# Regression Results: Determinants of Energy Recovery Efficiency\n\n")
        f.write("DV: log(MWh per tonne processed)\n\n")
        f.write("| Variable | Model 1 (Pooled OLS) | Model 2 (Year FE) |")
        if m3:
            f.write(" Model 3 (RE) |")
        f.write("\n")
        f.write("|:---------|:--------------------:|:-----------------:|")
        if m3:
            f.write(":------------:|")
        f.write("\n")

        main_vars = ['facility_age', 'capacity_100t', 'capacity_utilization',
                     'heating_value_1000kj', 'grid_ef_kgco2_kwh']

        for var in main_vars:
            f.write(f"| {var} |")
            for m in ([m1, m2] + ([m3] if m3 else [])):
                if m is not None and var in m.params.index:
                    coef = m.params[var]
                    p = m.pvalues[var]
                    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
                    f.write(f" {coef:.4f}{sig} |")
                else:
                    f.write(" — |")
            f.write("\n")

        f.write(f"| R-squared | {m1.rsquared:.4f} | {m2.rsquared:.4f} |")
        if m3:
            f.write(f" {m3.rsquared:.4f} |")
        f.write("\n")
        f.write(f"| N | {m1.nobs:.0f} | {m2.nobs:.0f} |")
        if m3:
            f.write(f" {m3.nobs} |")
        f.write("\n")

    print(f"  Saved: {path}")


def main():
    power = load_and_clean()
    descriptive_stats(power)
    efficiency_by_age_group(power)
    m1 = run_pooled_ols(power)
    m2 = run_ols_with_year_fe(power)
    m3 = run_random_effects(power)
    comparison_table(m1, m2, m3)

    print("\n" + "=" * 60)
    print("REGRESSION COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
