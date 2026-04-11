"""
06_robustness.py
=================
Robustness checks for the energy recovery efficiency regression.

Tests:
1. Pre/post Fukushima subsample (2005-2010 vs 2014-2024)
2. Capacity tercile subsample (small/medium/large)
3. Raw DV (MWh/t) instead of log
4. Dropping heating value (not significant in main models)
5. Hausman-style comparison: pooled OLS vs RE coefficients
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'processed')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')

EFF_FLOOR = 0.01
EFF_CEIL = 0.80


def load_clean():
    """Load and clean — same as 05."""
    path = os.path.join(PROCESSED_DIR, 'incineration_panel_enriched.csv')
    df = pd.read_csv(path)
    df = df[df['throughput_t_year'].notna() & (df['throughput_t_year'] > 0)]
    power = df[df['has_power_gen'] == True].copy()
    power = power[power['energy_efficiency_mwh_per_t'].notna()]
    power = power[
        (power['energy_efficiency_mwh_per_t'] >= EFF_FLOOR) &
        (power['energy_efficiency_mwh_per_t'] <= EFF_CEIL)
    ].copy()
    power['log_efficiency'] = np.log(power['energy_efficiency_mwh_per_t'])
    power['capacity_100t'] = power['capacity_t_day'] / 100
    power['heating_value_1000kj'] = power['heating_value_kj_kg'] / 1000
    return power


def run_ols(data, label, dv='log_efficiency', extra_drop=None):
    """Run pooled OLS with cluster-robust SEs. Return summary dict."""
    ivs = ['facility_age', 'capacity_100t', 'capacity_utilization',
           'heating_value_1000kj', 'grid_ef_kgco2_kwh']
    if extra_drop:
        ivs = [v for v in ivs if v not in extra_drop]

    reg_data = data[[dv] + ivs + ['facility_code']].dropna()
    if len(reg_data) < 50:
        print(f"  {label}: too few obs ({len(reg_data)}), skipping")
        return None

    y = reg_data[dv]
    X = sm.add_constant(reg_data[ivs])
    model = sm.OLS(y, X).fit(cov_type='cluster',
                              cov_kwds={'groups': reg_data['facility_code']})

    result = {
        'label': label,
        'n': int(model.nobs),
        'r2': model.rsquared,
    }
    for var in ivs:
        result[f'{var}_coef'] = model.params.get(var, np.nan)
        result[f'{var}_p'] = model.pvalues.get(var, np.nan)

    sig = lambda p: '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    print(f"\n  {label} (N={result['n']}, R²={result['r2']:.3f}):")
    for var in ivs:
        c = result[f'{var}_coef']
        p = result[f'{var}_p']
        print(f"    {var:<25} {c:>8.4f} {sig(p):>4}")

    return result


def main():
    power = load_clean()
    print(f"Clean sample: {len(power):,} obs\n")

    results = []

    # --- Baseline (reproduce Model 1) ---
    print("=" * 60)
    print("BASELINE: Full sample, log(efficiency)")
    print("=" * 60)
    r = run_ols(power, 'Baseline (full sample)')
    if r: results.append(r)

    # --- Test 1: Pre/Post Fukushima ---
    print("\n" + "=" * 60)
    print("TEST 1: Pre/Post Fukushima")
    print("=" * 60)
    pre = power[power['fiscal_year'] <= 2010]
    post = power[power['fiscal_year'] >= 2014]
    r = run_ols(pre, 'Pre-Fukushima (2005-2010)')
    if r: results.append(r)
    r = run_ols(post, 'Post-Fukushima (2014-2024)')
    if r: results.append(r)

    # --- Test 2: Capacity terciles ---
    print("\n" + "=" * 60)
    print("TEST 2: Capacity Terciles")
    print("=" * 60)
    terciles = pd.qcut(power['capacity_t_day'], 3, labels=['Small', 'Medium', 'Large'])
    for tier in ['Small', 'Medium', 'Large']:
        subset = power[terciles == tier]
        r = run_ols(subset, f'Capacity: {tier}')
        if r: results.append(r)

    # --- Test 3: Raw DV ---
    print("\n" + "=" * 60)
    print("TEST 3: Raw DV (MWh/t, not log)")
    print("=" * 60)
    r = run_ols(power, 'Raw DV (MWh/t)', dv='energy_efficiency_mwh_per_t')
    if r: results.append(r)

    # --- Test 4: Drop heating value ---
    print("\n" + "=" * 60)
    print("TEST 4: Drop heating value (not significant)")
    print("=" * 60)
    r = run_ols(power, 'Without heating value', extra_drop=['heating_value_1000kj'])
    if r: results.append(r)

    # --- Save comparison table ---
    print("\n" + "=" * 60)
    print("ROBUSTNESS SUMMARY")
    print("=" * 60)

    df_results = pd.DataFrame(results)
    core_vars = ['facility_age', 'capacity_100t', 'capacity_utilization']

    print(f"\n{'Specification':<30} {'N':>6} {'R²':>6}", end='')
    for var in core_vars:
        print(f" {var[:10]:>12}", end='')
    print()
    print("-" * 80)

    for _, row in df_results.iterrows():
        print(f"{row['label']:<30} {row['n']:>6} {row['r2']:>6.3f}", end='')
        for var in core_vars:
            c = row.get(f'{var}_coef', np.nan)
            p = row.get(f'{var}_p', np.nan)
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            if pd.notna(c):
                print(f" {c:>9.4f}{sig:<3}", end='')
            else:
                print(f" {'—':>12}", end='')
        print()

    # Stability assessment
    print("\n  STABILITY ASSESSMENT:")
    age_coefs = [r[f'facility_age_coef'] for r in results
                 if r and pd.notna(r.get('facility_age_coef'))]
    cap_coefs = [r[f'capacity_100t_coef'] for r in results
                 if r and pd.notna(r.get('capacity_100t_coef'))]
    util_coefs = [r[f'capacity_utilization_coef'] for r in results
                  if r and pd.notna(r.get('capacity_utilization_coef'))]

    for name, coefs in [('facility_age', age_coefs),
                        ('capacity_100t', cap_coefs),
                        ('capacity_utilization', util_coefs)]:
        if coefs:
            all_same_sign = all(c < 0 for c in coefs) or all(c > 0 for c in coefs)
            print(f"    {name}: {'STABLE (same sign)' if all_same_sign else 'UNSTABLE (sign changes)'} "
                  f"[range: {min(coefs):.4f} to {max(coefs):.4f}]")

    # Save
    path = os.path.join(OUTPUT_DIR, 'robustness_results.md')
    with open(path, 'w') as f:
        f.write("# Robustness Checks\n\n")
        f.write("All models: Pooled OLS, cluster-robust SEs, DV = log(MWh/t) unless noted.\n\n")
        f.write(f"| Specification | N | R² | facility_age | capacity_100t | cap_utilization |\n")
        f.write(f"|:---|---:|---:|---:|---:|---:|\n")
        for _, row in df_results.iterrows():
            f.write(f"| {row['label']} | {row['n']} | {row['r2']:.3f} |")
            for var in core_vars:
                c = row.get(f'{var}_coef', np.nan)
                p = row.get(f'{var}_p', np.nan)
                sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
                if pd.notna(c):
                    f.write(f" {c:.4f}{sig} |")
                else:
                    f.write(" — |")
            f.write("\n")

    print(f"\n  Saved: {path}")


if __name__ == '__main__':
    main()
