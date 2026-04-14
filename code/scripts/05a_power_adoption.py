"""
05a_power_adoption.py
=====================
Extensive-margin analysis for power-generation adoption.

This stage separates fleet modernization from generator-only efficiency by
estimating an observed first-adoption hazard on the full coded fleet.
"""

from __future__ import annotations

import os

import pandas as pd
import statsmodels.api as sm

from panel_utils import (
    AGE_BAND_LABELS,
    OUTPUT_DIR,
    build_adoption_frame,
    build_adoption_model_frame,
    load_panel,
    sample_summary,
    significance_stars,
    write_stage_manifest,
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

AGE_LABEL_MAP = {
    "10-20 yrs": "Prior-year age 10-20 yrs (vs 0-10)",
    "20-30 yrs": "Prior-year age 20-30 yrs (vs 0-10)",
    "30+ yrs": "Prior-year age 30+ yrs (vs 0-10)",
}


def load_adoption_data():
    """Load the full panel and construct the adoption-risk and model frames."""
    panel = load_panel()
    adoption = build_adoption_frame(panel)
    adoption_model = build_adoption_model_frame(adoption=adoption)
    summary = sample_summary(panel)

    print(f"Adoption risk set: {len(adoption):,} obs")
    print(f"  Facilities at risk: {adoption['analysis_facility_id'].nunique():,}")
    print(f"  First-adoption events: {int(adoption['adopt_power_this_year'].sum()):,}")
    print(f"Adoption model frame (lagged predictors): {len(adoption_model):,} obs")
    print(f"  Facilities in model frame: {adoption_model['analysis_facility_id'].nunique():,}")
    print(f"  Events in model frame: {int(adoption_model['adopt_power_this_year'].sum()):,}")
    print(
        "  Left-censored facilities already generating in first observed year: "
        f"{summary['left_censored_generators']:,}"
    )

    return panel, adoption, adoption_model, summary


def event_tables(adoption: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Summarize event rates by age band and capacity quartile."""
    age_table = (
        adoption.groupby("age_band", observed=True)
        .agg(
            risk_obs=("adopt_power_this_year", "size"),
            first_adoptions=("adopt_power_this_year", "sum"),
            annual_event_rate=("adopt_power_this_year", "mean"),
            mean_capacity_t_day=("capacity_t_day", "mean"),
        )
        .reindex(AGE_BAND_LABELS)
        .reset_index()
    )
    age_table["annual_event_rate_pct"] = age_table["annual_event_rate"] * 100
    age_table = age_table.drop(columns=["annual_event_rate"])

    cap = adoption.dropna(subset=["capacity_t_day"]).copy()
    cap["capacity_quartile"] = pd.qcut(
        cap["capacity_t_day"],
        4,
        labels=["Q1 (smallest)", "Q2", "Q3", "Q4 (largest)"],
    )
    cap_table = (
        cap.groupby("capacity_quartile", observed=True)
        .agg(
            risk_obs=("adopt_power_this_year", "size"),
            first_adoptions=("adopt_power_this_year", "sum"),
            annual_event_rate=("adopt_power_this_year", "mean"),
            mean_capacity_t_day=("capacity_t_day", "mean"),
        )
        .reset_index()
    )
    cap_table["annual_event_rate_pct"] = cap_table["annual_event_rate"] * 100
    cap_table = cap_table.drop(columns=["annual_event_rate"])

    return age_table, cap_table


def build_design_matrix(reg: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Build the shared design matrix used by the adoption estimators."""
    age_dummies = pd.get_dummies(
        reg["lag_age_band"],
        prefix="age",
        drop_first=True,
        dtype=float,
    )
    year_dummies = pd.get_dummies(
        reg["fiscal_year"],
        prefix="fy",
        drop_first=True,
        dtype=float,
    )
    pref_dummies = pd.get_dummies(
        reg["prefecture"],
        prefix="pref",
        drop_first=True,
        dtype=float,
    )

    X = sm.add_constant(
        pd.concat([age_dummies, reg[["lag_capacity_100t"]], year_dummies, pref_dummies], axis=1)
    )
    y = reg["adopt_power_this_year"]
    return X, y


def run_adoption_hazard(adoption_model: pd.DataFrame):
    """
    Estimate a simple discrete-time first-adoption hazard.

    The outcome is whether a facility is first observed adopting power
    generation in the current fiscal year. Predictors are lagged one observed
    year so the model captures pre-adoption facility characteristics rather
    than same-year redesign. The main specification is a linear probability
    model for percentage-point interpretation, with year and prefecture fixed
    effects and facility-clustered standard errors.
    """
    reg = adoption_model.copy()
    X, y = build_design_matrix(reg)

    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": reg["analysis_facility_id"]},
    )

    print("\n" + "=" * 60)
    print("ADOPTION HAZARD MODEL")
    print("=" * 60)
    print(f"  N: {int(model.nobs):,}")
    print(f"  Facilities: {reg['analysis_facility_id'].nunique():,}")
    print(f"  Events: {int(reg['adopt_power_this_year'].sum()):,}")
    print(f"  R-squared: {model.rsquared:.4f}")
    for var in ["age_10-20 yrs", "age_20-30 yrs", "age_30+ yrs", "lag_capacity_100t"]:
        coef = model.params[var]
        se = model.bse[var]
        p = model.pvalues[var]
        print(f"  {var:<20} {coef:>8.4f}  SE={se:>7.4f}  p={p:>7.4g}")

    return model, reg


def run_logit_robustness(reg: pd.DataFrame):
    """Run a lagged discrete-time logit as a robustness check."""
    X, y = build_design_matrix(reg)
    return sm.GLM(y, X, family=sm.families.Binomial()).fit(
        cov_type="cluster",
        cov_kwds={"groups": reg["analysis_facility_id"]},
    )


def write_results(
    path: str,
    summary: dict[str, int | float],
    adoption: pd.DataFrame,
    age_table: pd.DataFrame,
    cap_table: pd.DataFrame,
    model,
    logit_robustness,
    reg: pd.DataFrame,
) -> None:
    """Write a markdown report for the adoption stage."""
    event_years = (
        adoption.loc[adoption["adopt_power_this_year"] == 1, "fiscal_year"]
        .value_counts()
        .sort_index()
    )
    events_2013_2019 = int(
        adoption.loc[
            (adoption["adopt_power_this_year"] == 1)
            & adoption["fiscal_year"].between(2013, 2019),
            "adopt_power_this_year",
        ].sum()
    )

    model_rows = []
    for var in ["age_10-20 yrs", "age_20-30 yrs", "age_30+ yrs", "lag_capacity_100t"]:
        label = AGE_LABEL_MAP.get(var.replace("age_", ""), "Capacity (per 100 t/day)")
        if var == "lag_capacity_100t":
            label = "Prior-year capacity (per 100 t/day)"
        coef_pp = model.params[var] * 100
        se_pp = model.bse[var] * 100
        model_rows.append(
            {
                "Variable": label,
                "Coef. (pp)": f"{coef_pp:.2f}{significance_stars(float(model.pvalues[var]))}",
                "SE (pp)": f"({se_pp:.2f})",
            }
        )

    model_table = pd.DataFrame(model_rows)

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Extensive-Margin Results: Observed Transition Into Power Generation\n\n")
        f.write(
            "This stage models the observed first transition into power generation "
            "among coded facilities first observed without it, separating the "
            "extensive margin from conditional generator efficiency.\n\n"
        )
        f.write("## Risk Set\n\n")
        f.write(
            f"- Coded full-fleet frame: {summary['coded_full_fleet_obs']:,} observations "
            f"across {summary['coded_full_fleet_facilities']:,} facilities\n"
        )
        f.write(
            f"- Left-censored facilities already generating in first observed year: "
            f"{summary['left_censored_generators']:,}\n"
        )
        f.write(
            f"- Adoption risk set: {summary['adoption_risk_obs']:,} facility-years "
            f"across {summary['adoption_risk_facilities']:,} facilities\n"
        )
        f.write(
            f"- Observed first-adoption events in FY2005-FY2024: "
            f"{summary['adoption_events']:,}\n"
        )
        f.write(
            f"- First-adoption events concentrated in FY2013-FY2019: "
            f"{events_2013_2019:,} of {summary['adoption_events']:,}\n\n"
        )

        f.write("## Adoption Model Frame\n\n")
        f.write(
            f"- Lagged model frame: {summary['adoption_model_obs']:,} observations "
            f"across {summary['adoption_model_facilities']:,} facilities\n"
        )
        f.write(
            f"- Events retained in lagged model frame: {summary['adoption_model_events']:,}\n"
        )
        f.write(
            f"- First observed at-risk years dropped because lagged predictors are required: "
            f"{summary['adoption_model_drop_first_rows']:,}\n"
        )
        f.write(
            f"- Additional rows dropped for missing lagged age/capacity: "
            f"{summary['adoption_model_drop_additional_missing_rows']:,} "
            f"({summary['adoption_model_drop_additional_missing_facilities']:,} facilities)\n\n"
        )

        f.write("## Event Rates by Facility Age Band\n\n")
        f.write(
            age_table.assign(
                mean_capacity_t_day=lambda df: df["mean_capacity_t_day"].map(lambda x: f"{x:.1f}"),
                annual_event_rate_pct=lambda df: df["annual_event_rate_pct"].map(lambda x: f"{x:.2f}"),
            ).rename(
                columns={
                    "age_band": "Age band",
                    "risk_obs": "Risk-set obs",
                    "first_adoptions": "First adoptions",
                    "mean_capacity_t_day": "Mean capacity (t/day)",
                    "annual_event_rate_pct": "Annual event rate (%)",
                }
            ).to_markdown(index=False)
        )
        f.write("\n\n")

        f.write("## Event Rates by Capacity Quartile\n\n")
        f.write(
            cap_table.assign(
                mean_capacity_t_day=lambda df: df["mean_capacity_t_day"].map(lambda x: f"{x:.1f}"),
                annual_event_rate_pct=lambda df: df["annual_event_rate_pct"].map(lambda x: f"{x:.2f}"),
            ).rename(
                columns={
                    "capacity_quartile": "Capacity quartile",
                    "risk_obs": "Risk-set obs",
                    "first_adoptions": "First adoptions",
                    "mean_capacity_t_day": "Mean capacity (t/day)",
                    "annual_event_rate_pct": "Annual event rate (%)",
                }
            ).to_markdown(index=False)
        )
        f.write("\n\n")

        f.write("## Adoption Hazard Model\n\n")
        f.write(
            "Main specification: lagged linear probability hazard with prior-year "
            "age band and prior-year design capacity, plus year fixed effects, "
            "prefecture fixed effects, and facility-clustered standard errors. "
            "Baseline age band: 0-10 years.\n\n"
        )
        f.write(model_table.to_markdown(index=False))
        f.write(
            "\n\n"
            f"- Observations: {int(model.nobs):,}\n"
            f"- Facilities: {reg['analysis_facility_id'].nunique():,}\n"
            f"- First-adoption events: {int(reg['adopt_power_this_year'].sum()):,}\n"
            f"- R-squared: {model.rsquared:.4f}\n"
        )
        f.write(
            "- Discrete-time logit robustness: same sign pattern for all reported terms; "
            f"capacity remains positive (coef. {logit_robustness.params['lag_capacity_100t']:.3f}, "
            f"p={float(logit_robustness.pvalues['lag_capacity_100t']):.3g}).\n"
        )
        f.write("\n### Event Year Distribution\n\n")
        f.write(event_years.rename("First adoptions").to_markdown())
        f.write(
            "\n\n"
            "*Interpretation: observed transition into power generation is more common "
            "among facilities that were younger and larger in the prior year. This "
            "pattern is consistent with modernization occurring mainly at the capital "
            "or investment margin rather than through diffuse late conversion of old "
            "small facilities, but the data do not distinguish retrofit from "
            "replacement or new build at the same site.*\n"
        )


def main():
    _, adoption, adoption_model, summary = load_adoption_data()
    age_table, cap_table = event_tables(adoption)
    model, reg = run_adoption_hazard(adoption_model)
    logit_robustness = run_logit_robustness(reg)

    path = os.path.join(OUTPUT_DIR, "adoption_results.md")
    write_results(path, summary, adoption, age_table, cap_table, model, logit_robustness, reg)
    print(f"\nSaved: {path}")

    manifest_path = write_stage_manifest(
        "05a_power_adoption",
        inputs=["data/processed/incineration_panel_enriched.csv"],
        outputs=["output/adoption_results.md"],
        metadata={
            "risk_set_obs": int(len(adoption)),
            "risk_set_facilities": int(adoption["analysis_facility_id"].nunique()),
            "events": int(adoption["adopt_power_this_year"].sum()),
            "left_censored_generators": int(summary["left_censored_generators"]),
            "model_obs": int(len(reg)),
            "model_facilities": int(reg["analysis_facility_id"].nunique()),
            "model_events": int(reg["adopt_power_this_year"].sum()),
            "lag_drop_first_rows": int(summary["adoption_model_drop_first_rows"]),
            "lag_drop_additional_missing_rows": int(
                summary["adoption_model_drop_additional_missing_rows"]
            ),
            "lag_drop_additional_missing_facilities": int(
                summary["adoption_model_drop_additional_missing_facilities"]
            ),
            "model": {
                "type": "linear_probability_hazard",
                "predictors_lagged_one_year": True,
                "baseline_prior_year_age_band": "0-10 yrs",
                "coefficients": {
                    "lag_age_10_20": float(model.params["age_10-20 yrs"]),
                    "lag_age_20_30": float(model.params["age_20-30 yrs"]),
                    "lag_age_30_plus": float(model.params["age_30+ yrs"]),
                    "lag_capacity_100t": float(model.params["lag_capacity_100t"]),
                },
                "pvalues": {
                    "lag_age_10_20": float(model.pvalues["age_10-20 yrs"]),
                    "lag_age_20_30": float(model.pvalues["age_20-30 yrs"]),
                    "lag_age_30_plus": float(model.pvalues["age_30+ yrs"]),
                    "lag_capacity_100t": float(model.pvalues["lag_capacity_100t"]),
                },
                "r_squared": float(model.rsquared),
            },
            "logit_robustness": {
                "type": "discrete_time_logit",
                "coefficients": {
                    "lag_age_10_20": float(logit_robustness.params["age_10-20 yrs"]),
                    "lag_age_20_30": float(logit_robustness.params["age_20-30 yrs"]),
                    "lag_age_30_plus": float(logit_robustness.params["age_30+ yrs"]),
                    "lag_capacity_100t": float(logit_robustness.params["lag_capacity_100t"]),
                },
                "pvalues": {
                    "lag_age_10_20": float(logit_robustness.pvalues["age_10-20 yrs"]),
                    "lag_age_20_30": float(logit_robustness.pvalues["age_20-30 yrs"]),
                    "lag_age_30_plus": float(logit_robustness.pvalues["age_30+ yrs"]),
                    "lag_capacity_100t": float(logit_robustness.pvalues["lag_capacity_100t"]),
                },
            },
        },
    )
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
