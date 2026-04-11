"""
04_eda_facility.py
===================
Panel-directed EDA: data integrity checks + two thesis figures.

Phase 1 — Data Integrity (gates everything downstream):
  1. Missingness audit (is 4% missing heating value non-random?)
  2. Bounds & outlier check (efficiency distribution, log-transform DV)
  3. Panel balance check (attrition test, within-facility SD)
  Hard rule: drop zero-throughput with positive power gen.

Phase 2 — Two Figures Only:
  Figure 1: Establishing shot (fleet count + mean efficiency time series)
  Figure 2: Heterogeneity shot (avoided CO2 vs facility age)

Phase 3 — Pre-regression decision paragraph.

No other figures. No exploration for exploration's sake.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'processed')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 10


def load_panel():
    """Load enriched panel."""
    path = os.path.join(PROCESSED_DIR, 'incineration_panel_enriched.csv')
    df = pd.read_csv(path)
    print(f"Loaded: {len(df):,} rows, {df['fiscal_year'].nunique()} years, "
          f"{df['facility_code'].nunique():,} facilities")
    return df


# ================================================================
# PHASE 1: DATA INTEGRITY
# ================================================================

def phase1_hard_rule(df):
    """Drop zero-throughput observations with positive power generation."""
    print("\n" + "=" * 60)
    print("PHASE 1.0: Hard Rule — Drop measurement errors")
    print("=" * 60)

    bad = (
        (df['throughput_t_year'].isna() | (df['throughput_t_year'] <= 0)) &
        (df['power_generated_mwh'].notna()) & (df['power_generated_mwh'] > 0)
    )
    n_bad = bad.sum()
    print(f"Zero/missing throughput + positive power gen: {n_bad} rows")

    if n_bad > 0:
        print(f"  Dropping {n_bad} rows.")
        df = df[~bad].copy()

    # Also drop rows with zero throughput (facility not operating that year)
    zero_throughput = df['throughput_t_year'].isna() | (df['throughput_t_year'] <= 0)
    n_zero = zero_throughput.sum()
    print(f"Total zero/missing throughput: {n_zero} rows → dropping")
    df = df[~zero_throughput].copy().reset_index(drop=True)

    print(f"Clean panel: {len(df):,} rows")
    return df


def phase1_missingness(df):
    """Check if missing heating_value is non-random."""
    print("\n" + "=" * 60)
    print("PHASE 1.1: Missingness Audit")
    print("=" * 60)

    missing = df['heating_value_kj_kg'].isna()
    n_miss = missing.sum()
    pct_miss = missing.mean() * 100
    print(f"Missing heating_value: {n_miss} ({pct_miss:.1f}%)")

    if n_miss == 0:
        print("No missing values — skip audit.")
        return

    # Compare missing vs non-missing on key variables
    compare_vars = ['facility_age', 'capacity_t_day', 'throughput_t_year',
                    'power_capacity_kw', 'has_power_gen']
    print("\n  Comparing missing vs non-missing heating_value:")
    print(f"  {'Variable':<25} {'Present (mean)':>15} {'Missing (mean)':>15} {'Difference':>12}")
    print("  " + "-" * 70)

    for var in compare_vars:
        if var not in df.columns:
            continue
        present_mean = df.loc[~missing, var].astype(float).mean()
        missing_mean = df.loc[missing, var].astype(float).mean()
        diff = missing_mean - present_mean
        print(f"  {var:<25} {present_mean:>15.1f} {missing_mean:>15.1f} {diff:>+12.1f}")

    print("\n  Verdict: Check if differences are substantively large.")


def phase1_bounds(df):
    """Check distribution of energy efficiency, flag outliers."""
    print("\n" + "=" * 60)
    print("PHASE 1.2: Bounds & Outlier Check")
    print("=" * 60)

    # Focus on power-gen subsample
    power = df[df['has_power_gen'] == True].copy()
    eff = power['energy_efficiency_mwh_per_t'].dropna()

    print(f"\nEnergy efficiency (MWh/t) among power-gen facilities:")
    print(f"  N: {len(eff):,}")
    print(f"  Mean: {eff.mean():.4f}")
    print(f"  Median: {eff.median():.4f}")
    print(f"  Skew ratio (mean/median): {eff.mean()/eff.median():.2f}x")
    print(f"  Std: {eff.std():.4f}")
    print(f"  Min: {eff.min():.6f}")
    print(f"  Max: {eff.max():.4f}")
    print(f"  P1: {eff.quantile(0.01):.4f}")
    print(f"  P99: {eff.quantile(0.99):.4f}")

    # Physical bounds check
    # Typical WtE efficiency: 0.05-0.80 MWh/t (50-800 kWh/t)
    # High-efficiency modern plants: up to ~0.75 MWh/t
    # Below 0.01 or above 0.80 is suspicious
    EFF_FLOOR = 0.01
    EFF_CEIL = 0.80
    low_outliers = (eff < EFF_FLOOR).sum()
    high_outliers = (eff > EFF_CEIL).sum()
    print(f"\n  Outliers (efficiency < {EFF_FLOOR} MWh/t): {low_outliers}")
    print(f"  Outliers (efficiency > {EFF_CEIL} MWh/t): {high_outliers}")
    print(f"  → Will winsorize to [{EFF_FLOOR}, {EFF_CEIL}] before regression")

    # Log-transform assessment
    log_eff = np.log(eff[eff > 0])
    print(f"\n  After log-transform:")
    print(f"    Skewness (raw): {eff.skew():.2f}")
    print(f"    Skewness (log): {log_eff.skew():.2f}")
    print(f"    → {'Log-transform recommended' if abs(log_eff.skew()) < abs(eff.skew()) else 'Log-transform not helpful'}")

    return eff


def phase1_panel_balance(df):
    """Check panel balance, attrition, and within-facility variation."""
    print("\n" + "=" * 60)
    print("PHASE 1.3: Panel Balance & Within-Facility Variation")
    print("=" * 60)

    power = df[df['has_power_gen'] == True].copy()

    # Panel balance
    obs_per_facility = power.groupby('facility_code').size()
    print(f"\nPower-gen subsample panel balance:")
    print(f"  Unique facilities: {len(obs_per_facility):,}")
    print(f"  Mean years per facility: {obs_per_facility.mean():.1f}")
    print(f"  Median years per facility: {obs_per_facility.median():.0f}")
    print(f"  Min: {obs_per_facility.min()}, Max: {obs_per_facility.max()}")
    print(f"  Facilities with 10+ years: {(obs_per_facility >= 10).sum()}")
    print(f"  Facilities with 15+ years: {(obs_per_facility >= 15).sum()}")
    print(f"  Facilities with all 20 years: {(obs_per_facility >= 20).sum()}")

    # Attrition test: do early-exit facilities differ from survivors?
    # Define: "survivor" = facility present in FY2024
    # "exiter" = facility NOT present in FY2024 but was present at some point
    latest_year = power['fiscal_year'].max()
    survivors = set(power[power['fiscal_year'] == latest_year]['facility_code'].unique())
    all_facs = set(power['facility_code'].unique())
    exiters = all_facs - survivors

    print(f"\n  Attrition test:")
    print(f"    Survivors (present in FY{latest_year}): {len(survivors)}")
    print(f"    Exiters (closed before FY{latest_year}): {len(exiters)}")

    if len(exiters) > 5:
        # Compare baseline characteristics (first observation per facility)
        first_obs = power.sort_values('fiscal_year').groupby('facility_code').first()
        first_obs['is_survivor'] = first_obs.index.isin(survivors)

        compare_vars = ['capacity_t_day', 'facility_age', 'energy_efficiency_mwh_per_t',
                        'power_capacity_kw']
        print(f"\n    Baseline comparison (first observation per facility):")
        print(f"    {'Variable':<30} {'Survivors':>12} {'Exiters':>12} {'p-value':>10}")
        print("    " + "-" * 66)

        for var in compare_vars:
            if var not in first_obs.columns:
                continue
            surv_vals = first_obs.loc[first_obs['is_survivor'], var].dropna()
            exit_vals = first_obs.loc[~first_obs['is_survivor'], var].dropna()
            if len(surv_vals) > 2 and len(exit_vals) > 2:
                t_stat, p_val = stats.ttest_ind(surv_vals, exit_vals, equal_var=False)
                print(f"    {var:<30} {surv_vals.mean():>12.2f} {exit_vals.mean():>12.2f} {p_val:>10.4f}")

    # Within-facility variation
    print(f"\n  Within-facility standard deviation of key variables:")
    within_sd = power.groupby('facility_code').agg({
        'energy_efficiency_mwh_per_t': 'std',
        'capacity_utilization': 'std',
        'throughput_t_year': 'std',
    }).dropna()

    for col in within_sd.columns:
        med_sd = within_sd[col].median()
        overall_sd = power[col].std()
        ratio = med_sd / overall_sd if overall_sd > 0 else 0
        print(f"    {col:<35} within-SD median: {med_sd:.4f}  "
              f"overall-SD: {overall_sd:.4f}  ratio: {ratio:.2f}")

    print(f"\n  → If within/overall ratio < 0.10, FE will struggle to identify effects.")


# ================================================================
# PHASE 2: TWO FIGURES ONLY
# ================================================================

def figure1_establishing_shot(df):
    """Dual-axis time series: fleet count + mean efficiency."""
    print("\n" + "=" * 60)
    print("PHASE 2.1: Figure 1 — Establishing Shot")
    print("=" * 60)

    power = df[df['has_power_gen'] == True].copy()

    yearly = power.groupby('fiscal_year').agg(
        n_facilities=('facility_code', 'nunique'),
        mean_efficiency=('energy_efficiency_mwh_per_t', 'mean'),
        median_efficiency=('energy_efficiency_mwh_per_t', 'median'),
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bars: facility count
    color_bar = '#90CAF9'
    ax1.bar(yearly['fiscal_year'], yearly['n_facilities'],
            color=color_bar, alpha=0.7, label='Power-gen facilities (count)')
    ax1.set_xlabel('Fiscal Year')
    ax1.set_ylabel('Number of Power-Generating Facilities', color='#1565C0')
    ax1.tick_params(axis='y', labelcolor='#1565C0')
    ax1.set_ylim(0, yearly['n_facilities'].max() * 1.3)

    # Fukushima annotation
    ax1.axvspan(2011, 2013, alpha=0.15, color='red', label='Post-Fukushima period')

    # Line: mean efficiency
    ax2 = ax1.twinx()
    color_line = '#C62828'
    ax2.plot(yearly['fiscal_year'], yearly['mean_efficiency'],
             color=color_line, linewidth=2.5, marker='o', markersize=5,
             label='Mean energy efficiency')
    ax2.plot(yearly['fiscal_year'], yearly['median_efficiency'],
             color='#E65100', linewidth=1.5, linestyle='--', marker='s', markersize=3,
             label='Median energy efficiency')
    ax2.set_ylabel('Energy Efficiency (MWh/tonne)', color=color_line)
    ax2.tick_params(axis='y', labelcolor=color_line)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

    plt.title('Japan\'s Waste-to-Energy Fleet: Growth and Efficiency (FY2005-2024)',
              fontsize=13, fontweight='bold')
    fig.tight_layout()

    path = os.path.join(OUTPUT_DIR, 'fig01_establishing_shot.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def figure2_heterogeneity_shot(df):
    """Scatter: avoided CO2 vs facility age, colored by active/closed."""
    print("\n" + "=" * 60)
    print("PHASE 2.2: Figure 2 — Heterogeneity Shot")
    print("=" * 60)

    # Use latest year for cross-sectional snapshot
    latest = df['fiscal_year'].max()
    power = df[(df['has_power_gen'] == True) & (df['fiscal_year'] == latest)].copy()

    # Also get facilities that existed in earlier years but are gone now
    all_power = df[df['has_power_gen'] == True].copy()
    latest_facilities = set(power['facility_code'].unique())
    all_facilities = set(all_power['facility_code'].unique())

    # For closed facilities, use their last observation
    closed_codes = all_facilities - latest_facilities
    closed = all_power[all_power['facility_code'].isin(closed_codes)].copy()
    closed_last = closed.sort_values('fiscal_year').groupby('facility_code').last().reset_index()

    power['status'] = 'Active (FY' + str(latest) + ')'
    closed_last['status'] = 'Closed'

    plot_data = pd.concat([power, closed_last], ignore_index=True)
    plot_data = plot_data.dropna(subset=['avoided_co2_t', 'facility_age'])

    fig, ax = plt.subplots(figsize=(12, 7))

    for status, color, alpha, size in [
        ('Closed', '#B0BEC5', 0.5, 20),
        ('Active (FY' + str(latest) + ')', '#2E7D32', 0.7, 35),
    ]:
        mask = plot_data['status'] == status
        ax.scatter(
            plot_data.loc[mask, 'facility_age'],
            plot_data.loc[mask, 'avoided_co2_t'],
            c=color, alpha=alpha, s=size, label=status, edgecolors='white', linewidth=0.3
        )

    # Annotate mean and median
    active_avoided = power['avoided_co2_t'].dropna()
    if len(active_avoided) > 0:
        ax.axhline(active_avoided.mean(), color='#C62828', linestyle='-', linewidth=1,
                    alpha=0.7, label=f'Mean: {active_avoided.mean():,.0f} t-CO2')
        ax.axhline(active_avoided.median(), color='#E65100', linestyle='--', linewidth=1,
                    alpha=0.7, label=f'Median: {active_avoided.median():,.0f} t-CO2')

    ax.set_xlabel('Facility Age (years)', fontsize=11)
    ax.set_ylabel('Avoided CO2 (tonnes/year)', fontsize=11)
    ax.set_title('Incinerator Heterogeneity: Avoided Emissions by Facility Age',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(-2, ax.get_xlim()[1])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig02_heterogeneity_shot.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


# ================================================================
# PHASE 3: PRE-REGRESSION DECISION
# ================================================================

def phase3_decision(df):
    """Write the pre-regression decision paragraph."""
    print("\n" + "=" * 60)
    print("PHASE 3: Pre-Regression Decision")
    print("=" * 60)

    power = df[df['has_power_gen'] == True].copy()
    obs_per_fac = power.groupby('facility_code').size()

    within_sd_eff = power.groupby('facility_code')['energy_efficiency_mwh_per_t'].std().dropna()
    overall_sd_eff = power['energy_efficiency_mwh_per_t'].std()
    ratio = within_sd_eff.median() / overall_sd_eff if overall_sd_eff > 0 else 0

    n_fac_10plus = (obs_per_fac >= 10).sum()

    decision = []
    decision.append(f"Power-gen subsample: {len(power):,} obs, "
                    f"{power['facility_code'].nunique()} facilities.")
    decision.append(f"Facilities with 10+ years: {n_fac_10plus}.")
    decision.append(f"Within/overall efficiency SD ratio: {ratio:.3f}.")

    if ratio >= 0.10:
        decision.append("DECISION: Sufficient within-facility variation. "
                        "Proceed with two-way FE.")
    elif ratio >= 0.05:
        decision.append("DECISION: Marginal within-facility variation. "
                        "Run FE but compare with pooled OLS and RE. "
                        "Report Hausman test.")
    else:
        decision.append("DECISION: Insufficient within-facility variation. "
                        "FE will be imprecise. Consider pooled OLS or RE as primary.")

    for line in decision:
        print(f"  {line}")

    # Save decision
    path = os.path.join(OUTPUT_DIR, 'pre_regression_decision.md')
    with open(path, 'w') as f:
        f.write("# Pre-Regression Decision\n\n")
        for line in decision:
            f.write(f"- {line}\n")
    print(f"\n  Saved: {path}")


# ================================================================
# MAIN
# ================================================================

def main():
    df = load_panel()

    # Phase 1
    df = phase1_hard_rule(df)
    phase1_missingness(df)
    eff = phase1_bounds(df)
    phase1_panel_balance(df)

    # Phase 2
    figure1_establishing_shot(df)
    figure2_heterogeneity_shot(df)

    # Phase 3
    phase3_decision(df)

    print("\n" + "=" * 60)
    print("EDA COMPLETE. Review output/ for figures and decisions.")
    print("=" * 60)


if __name__ == '__main__':
    main()
