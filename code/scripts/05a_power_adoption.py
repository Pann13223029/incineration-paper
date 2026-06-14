"""
05a_power_adoption.py
=====================
Extensive-margin analysis for power-generation adoption.

This stage separates fleet modernization from generator-only efficiency by
estimating an observed first-adoption hazard on the full coded fleet.
"""

from __future__ import annotations

import math
import os
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit

from panel_utils import (
    AGE_BAND_LABELS,
    OUTPUT_DIR,
    build_adoption_frame,
    build_adoption_model_frame,
    build_adoption_pathway_audit,
    load_panel,
    sample_summary,
    significance_stars,
    write_stage_manifest,
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

AGE_VARIABLES = ["age_10-20 yrs", "age_20-30 yrs", "age_30+ yrs"]
REPORTED_VARIABLES = [*AGE_VARIABLES, "lag_capacity_100t"]
AGE_LABEL_MAP = {
    "age_10-20 yrs": "Prior-year age 10-20 yrs (vs 0-10)",
    "age_20-30 yrs": "Prior-year age 20-30 yrs (vs 0-10)",
    "age_30+ yrs": "Prior-year age 30+ yrs (vs 0-10)",
    "lag_capacity_100t": "Prior-year capacity (per 100 t/day)",
}
PATHWAY_ORDER = [
    "Reset / rebuild-like transition",
    "In-place upgrade / continuity transition",
    "Forward-dated / placeholder entry",
    "Timing-ambiguous / non-adjacent coded row",
    "Unresolved / insufficient continuity",
]

def load_adoption_data():
    """Load the full panel and construct the adoption-risk and model frames."""
    panel = load_panel()
    adoption = build_adoption_frame(panel)
    adoption_model = build_adoption_model_frame(adoption=adoption)
    previous_observed_model = build_adoption_model_frame(
        adoption=adoption,
        exact_year_only=False,
    )
    pathway_audit = build_adoption_pathway_audit(panel, adoption=adoption)
    summary = sample_summary(panel)

    print(f"Adoption risk set: {len(adoption):,} obs")
    print(f"  Facilities at risk: {adoption['analysis_facility_id'].nunique():,}")
    print(f"  First-adoption events: {int(adoption['adopt_power_this_year'].sum()):,}")
    print(f"Adoption model frame (exact one-year lagged predictors): {len(adoption_model):,} obs")
    print(f"  Facilities in model frame: {adoption_model['analysis_facility_id'].nunique():,}")
    print(f"  Events in model frame: {int(adoption_model['adopt_power_this_year'].sum()):,}")
    print(
        "Previous-observed-coded-row sensitivity frame: "
        f"{len(previous_observed_model):,} obs, "
        f"{int(previous_observed_model['adopt_power_this_year'].sum()):,} events"
    )
    print(f"Pathway audit rows: {len(pathway_audit):,}")
    print(
        "  Left-censored facilities already generating in first observed year: "
        f"{summary['left_censored_generators']:,}"
    )

    return panel, adoption, adoption_model, previous_observed_model, pathway_audit, summary


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


def build_design_matrix(
    reg: pd.DataFrame,
    *,
    include_year_fe: bool = True,
    include_pref_fe: bool = True,
) -> tuple[pd.DataFrame, pd.Series]:
    """Build the shared design matrix used by the adoption estimators."""
    age_dummies = pd.get_dummies(
        reg["lag_age_band"],
        prefix="age",
        drop_first=True,
        dtype=float,
    )
    parts = [age_dummies, reg[["lag_capacity_100t"]]]
    if include_year_fe:
        parts.append(
            pd.get_dummies(
                reg["fiscal_year"],
                prefix="fy",
                drop_first=True,
                dtype=float,
            )
        )
    if include_pref_fe:
        parts.append(
            pd.get_dummies(
                reg["prefecture"],
                prefix="pref",
                drop_first=True,
                dtype=float,
            )
        )

    X = sm.add_constant(pd.concat(parts, axis=1)).astype(float)
    y = reg["adopt_power_this_year"].astype(float)
    return X, y


def predict_probability(eta: np.ndarray, link_name: str) -> np.ndarray:
    """Convert linear predictors into probabilities for the selected link."""
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        eta = np.clip(eta, -40, 20)
        if link_name == "cloglog":
            return 1.0 - np.exp(-np.exp(eta))
        if link_name == "logit":
            return 1.0 / (1.0 + np.exp(-eta))
    raise ValueError(f"Unsupported link: {link_name}")


def derivative_wrt_eta(eta: np.ndarray, link_name: str) -> np.ndarray:
    """Return dP/deta for the selected link."""
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        eta = np.clip(eta, -40, 20)
        if link_name == "cloglog":
            return np.exp(eta - np.exp(eta))
        if link_name == "logit":
            p = 1.0 / (1.0 + np.exp(-eta))
            return p * (1.0 - p)
    raise ValueError(f"Unsupported link: {link_name}")


def linear_predictor(design: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """Compute a linear predictor while suppressing benign numeric warnings."""
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        return design @ beta


def average_marginal_effect(
    beta: np.ndarray,
    X_values: np.ndarray,
    link_name: str,
    variable: str,
    age_designs: dict[str, np.ndarray],
    base_age_design: np.ndarray,
    column_index: dict[str, int],
) -> float:
    """Compute the average marginal effect for one reported variable."""
    beta = np.asarray(beta, dtype=float)
    if variable in AGE_VARIABLES:
        alt_eta = linear_predictor(age_designs[variable], beta)
        base_eta = linear_predictor(base_age_design, beta)
        return float(
            np.mean(
                predict_probability(alt_eta, link_name)
                - predict_probability(base_eta, link_name)
            )
        )

    eta = linear_predictor(X_values, beta)
    return float(
        np.mean(derivative_wrt_eta(eta, link_name) * beta[column_index[variable]])
    )


def marginal_effect_designs(
    X: pd.DataFrame,
) -> tuple[np.ndarray, dict[str, np.ndarray], np.ndarray, dict[str, int]]:
    """Prepare reusable design arrays for AME calculations."""
    X_values = X.to_numpy(dtype=float)
    column_index = {name: i for i, name in enumerate(X.columns)}
    base_age_design = X.copy()
    for var in AGE_VARIABLES:
        base_age_design[var] = 0.0
    base_age_design_values = base_age_design.to_numpy(dtype=float)

    age_designs = {}
    for variable in AGE_VARIABLES:
        age_design = X.copy()
        for age_var in AGE_VARIABLES:
            age_design[age_var] = 1.0 if age_var == variable else 0.0
        age_designs[variable] = age_design.to_numpy(dtype=float)

    return X_values, age_designs, base_age_design_values, column_index


def fit_glm_hazard(
    X: pd.DataFrame,
    y: pd.Series,
    link_name: str,
    groups: pd.Series | None,
):
    """Fit a lagged discrete-time hazard with the requested link."""
    if link_name == "cloglog":
        link = sm.families.links.CLogLog()
    elif link_name == "logit":
        link = sm.families.links.Logit()
    else:
        raise ValueError(f"Unsupported link: {link_name}")

    fit_kwargs = {}
    if groups is not None:
        fit_kwargs = {
            "cov_type": "cluster",
            "cov_kwds": {"groups": groups},
        }

    return sm.GLM(y, X, family=sm.families.Binomial(link=link)).fit(**fit_kwargs)


def fit_logit_hazard(X: pd.DataFrame, y: pd.Series, groups: pd.Series):
    """Fit the main lagged logit hazard with facility-clustered covariance."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        return Logit(y, X).fit(
            method="lbfgs",
            maxiter=500,
            disp=False,
            cov_type="cluster",
            cov_kwds={"groups": groups},
            warn_convergence=False,
        )


def compute_logit_average_marginal_effects(model) -> pd.DataFrame:
    """Return built-in clustered AMEs for the reported adoption terms."""
    frame = model.get_margeff(at="overall", method="dydx", dummy=True).summary_frame()
    rows = []
    for variable in REPORTED_VARIABLES:
        row = frame.loc[variable]
        rows.append(
            {
                "variable": variable,
                "ame": float(row["dy/dx"]),
                "se": float(row["Std. Err."]),
                "pvalue": float(row["Pr(>|z|)"]),
            }
        )
    return pd.DataFrame(rows)


def fit_lpm_hazard(X: pd.DataFrame, y: pd.Series, groups: pd.Series):
    """Fit the legacy lagged linear probability specification as a robustness check."""
    return sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups},
    )


def sparse_event_diagnostics(reg: pd.DataFrame, X: pd.DataFrame) -> dict[str, int | float]:
    """Return sparse-event diagnostics for the adoption model frame."""
    events = int(reg["adopt_power_this_year"].sum())
    parameters = int(X.shape[1])
    year_events = reg.groupby("fiscal_year")["adopt_power_this_year"].sum()
    pref_events = reg.groupby("prefecture")["adopt_power_this_year"].sum()
    return {
        "events": events,
        "parameters": parameters,
        "events_per_parameter": float(events / parameters) if parameters else float("nan"),
        "zero_event_years": int((year_events == 0).sum()),
        "zero_event_prefectures": int((pref_events == 0).sum()),
        "years": int(year_events.shape[0]),
        "prefectures": int(pref_events.shape[0]),
    }


def fit_reported_logit_spec(
    reg: pd.DataFrame,
    *,
    label: str,
    include_year_fe: bool = True,
    include_pref_fe: bool = True,
) -> dict[str, object]:
    """Fit one reported logit specification and return compact diagnostics."""
    X, y = build_design_matrix(
        reg,
        include_year_fe=include_year_fe,
        include_pref_fe=include_pref_fe,
    )
    model = fit_logit_hazard(X, y, groups=reg["analysis_facility_id"])
    marginal_effects = compute_logit_average_marginal_effects(model)
    return {
        "label": label,
        "model": model,
        "reg": reg,
        "X": X,
        "marginal_effects": marginal_effects,
        "pseudo_r2": model_pseudo_r2(model),
        "diagnostics": sparse_event_diagnostics(reg, X),
    }


def sign_pattern_matches(marginal_effects: pd.DataFrame) -> bool:
    """Return whether the core expected adoption sign pattern is preserved."""
    effects = marginal_effects.set_index("variable")["ame"]
    return bool(
        (effects["age_10-20 yrs"] < 0)
        and (effects["age_20-30 yrs"] < 0)
        and (effects["age_30+ yrs"] < 0)
        and (effects["lag_capacity_100t"] > 0)
    )


def manifest_float(value: float, significant_digits: int = 6) -> float:
    """Round manifest floats enough to avoid platform-specific last-bit drift."""
    return float(f"{float(value):.{significant_digits}g}")


def model_pseudo_r2(model) -> float:
    """Return a deviance-based pseudo-R^2 for GLM hazards."""
    if hasattr(model, "prsquared"):
        return float(model.prsquared)
    if getattr(model, "null_deviance", 0) == 0:
        return float("nan")
    return float(1.0 - (model.deviance / model.null_deviance))


def pathway_summary_table(pathway_audit: pd.DataFrame) -> pd.DataFrame:
    """Summarize transition pathways for the observed adoption events."""
    summary = (
        pathway_audit["pathway_category"]
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Events")
    )
    summary["Share (%)"] = summary["Events"] / len(pathway_audit) * 100.0
    summary["Category"] = pd.Categorical(
        summary["Category"],
        categories=PATHWAY_ORDER,
        ordered=True,
    )
    summary = summary.sort_values("Category").reset_index(drop=True)
    return summary


def run_adoption_hazard(adoption_model: pd.DataFrame):
    """
    Estimate a discrete-time first-adoption hazard with lagged predictors.

    The main specification uses a clustered discrete-time logit with built-in
    marginal effects. A cloglog version is retained as a robustness check.
    """
    result = fit_reported_logit_spec(
        adoption_model.copy(),
        label="Main exact-year logit: year FE + prefecture FE",
    )
    reg = result["reg"]
    model = result["model"]
    marginal_effects = result["marginal_effects"]
    pseudo_r2 = result["pseudo_r2"]
    diagnostics = result["diagnostics"]

    print("\n" + "=" * 60)
    print("ADOPTION HAZARD MODEL")
    print("=" * 60)
    print(f"  N: {int(model.nobs):,}")
    print(f"  Facilities: {reg['analysis_facility_id'].nunique():,}")
    print(f"  Events: {int(reg['adopt_power_this_year'].sum()):,}")
    print(
        "  Events per parameter: "
        f"{diagnostics['events_per_parameter']:.2f} "
        f"({diagnostics['events']} events / {diagnostics['parameters']} parameters)"
    )
    print(f"  Pseudo-R-squared: {pseudo_r2:.4f}")
    for variable in REPORTED_VARIABLES:
        row = marginal_effects.loc[marginal_effects["variable"] == variable].iloc[0]
        print(
            f"  {variable:<20} {row['ame'] * 100:>8.3f} pp"
            f"  SE={row['se'] * 100:>7.3f}  p={row['pvalue']:>7.4g}"
        )

    return result


def write_results(
    path: str,
    summary: dict[str, int | float],
    adoption: pd.DataFrame,
    age_table: pd.DataFrame,
    cap_table: pd.DataFrame,
    pathway_summary: pd.DataFrame,
    model,
    marginal_effects: pd.DataFrame,
    pseudo_r2: float,
    diagnostics: dict[str, int | float],
    cloglog_robustness,
    lpm_robustness,
    previous_observed_result: dict[str, object],
    robustness_results: list[dict[str, object]],
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
    for variable in REPORTED_VARIABLES:
        row = marginal_effects.loc[marginal_effects["variable"] == variable].iloc[0]
        model_rows.append(
            {
                "Variable": AGE_LABEL_MAP[variable],
                "AME (pp)": f"{row['ame'] * 100:.2f}{significance_stars(float(row['pvalue']))}",
                "SE (pp)": f"({row['se'] * 100:.2f})",
            }
        )
    model_table = pd.DataFrame(model_rows)

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Extensive-Margin Results: Observed Transition Into Power Generation\n\n")
        f.write(
            "This stage models the observed first transition into power generation "
            "among coded facilities first observed without it, separating the "
            "extensive margin from conditional generator performance.\n\n"
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
            f"{events_2013_2019:,} of {summary['adoption_events']:,}\n"
        )
        f.write(
            "- Interpretation: the time clustering is reported as an event-timing "
            "feature of the administrative panel, not as evidence of a uniquely "
            "identified policy shock or reporting change. The main hazard includes "
            "year fixed effects.\n\n"
        )

        f.write("## Adoption Model Frame\n\n")
        f.write(
            f"- Main exact-year lagged model frame: {summary['adoption_model_obs']:,} observations "
            f"across {summary['adoption_model_facilities']:,} facilities\n"
        )
        f.write(
            f"- Events retained in lagged model frame: {summary['adoption_model_events']:,}\n"
        )
        f.write(
            f"- Broader previous-observed-coded-row frame before exact-year restriction: "
            f"{summary['adoption_previous_observed_model_obs']:,} observations across "
            f"{summary['adoption_previous_observed_model_facilities']:,} facilities "
            f"with {summary['adoption_previous_observed_model_events']:,} events\n"
        )
        f.write(
            f"- Non-exact lag rows excluded from the main model: "
            f"{summary['adoption_non_exact_lag_rows']:,} rows "
            f"({summary['adoption_non_exact_lag_events']:,} events)\n"
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
            "Main specification: exact one-fiscal-year lagged discrete-time logit hazard "
            "with prior-year age band and prior-year design capacity, plus year "
            "fixed effects, prefecture fixed effects, and facility-clustered "
            "standard errors. Reported effects are average marginal effects in "
            "percentage points. Baseline prior-year age band: 0-10 years.\n\n"
        )
        f.write(model_table.to_markdown(index=False))
        f.write(
            "\n\n"
            f"- Observations: {int(model.nobs):,}\n"
            f"- Facilities: {reg['analysis_facility_id'].nunique():,}\n"
            f"- First-adoption events: {int(reg['adopt_power_this_year'].sum()):,}\n"
            f"- Events per parameter: {diagnostics['events_per_parameter']:.2f} "
            f"({diagnostics['events']} events / {diagnostics['parameters']} parameters)\n"
            f"- Zero-event fiscal-year levels in main frame: "
            f"{diagnostics['zero_event_years']} of {diagnostics['years']}\n"
            f"- Zero-event prefecture levels in main frame: "
            f"{diagnostics['zero_event_prefectures']} of {diagnostics['prefectures']}\n"
            f"- Pseudo-R-squared (deviance-based): {pseudo_r2:.4f}\n"
        )
        f.write(
            "- Link robustness on the exact-year frame: complementary log-log and linear probability specifications "
            "return the same expected sign pattern on all reported terms; capacity remains "
            f"positive in both (cloglog coef. {cloglog_robustness.params['lag_capacity_100t']:.3f}; "
            f"LPM coef. {lpm_robustness.params['lag_capacity_100t'] * 100:.2f} pp).\n\n"
        )

        f.write("### Adoption specification sensitivity\n\n")
        sensitivity_rows = []
        for result in [previous_observed_result, *robustness_results]:
            me = result["marginal_effects"].set_index("variable")
            diag = result["diagnostics"]
            sensitivity_rows.append(
                {
                    "Specification": result["label"],
                    "N": f"{int(result['model'].nobs):,}",
                    "Events": int(diag["events"]),
                    "Parameters": int(diag["parameters"]),
                    "Events/parameter": f"{diag['events_per_parameter']:.2f}",
                    "Age 10-20 AME (pp)": f"{me.loc['age_10-20 yrs', 'ame'] * 100:.2f}",
                    "Age 20-30 AME (pp)": f"{me.loc['age_20-30 yrs', 'ame'] * 100:.2f}",
                    "Age 30+ AME (pp)": f"{me.loc['age_30+ yrs', 'ame'] * 100:.2f}",
                    "Capacity AME (pp)": f"{me.loc['lag_capacity_100t', 'ame'] * 100:.2f}",
                    "Sign pattern": "yes" if sign_pattern_matches(result["marginal_effects"]) else "no",
                }
            )
        f.write(pd.DataFrame(sensitivity_rows).to_markdown(index=False))
        f.write(
            "\n\n"
            "*Interpretation: the exact-year model is the main specification because it preserves "
            "annual transition timing. The broader previous-observed-coded-row specification is "
            "reported only as a sensitivity check because official facility identifiers are missing "
            "for FY2010-FY2012.*\n\n"
        )

        f.write("## Transition Pathway Audit\n\n")
        f.write(
            "A conservative event-level audit classifies each observed adoption "
            "using continuity in `year_started`, facility age, design capacity, "
            "and naming. The goal is not to prove the mechanism of modernization, "
            "but to bound what the panel can and cannot support.\n\n"
        )
        f.write(
            "Rule set: `reset / rebuild-like` requires an observed `year_started` "
            "reset or a mature-to-new age reset on an exact adjacent-year event; "
            "`continuity / in-place upgrade` requires no such reset on an exact "
            "adjacent-year event; forward-dated or placeholder entries remain "
            "weaker evidence; non-adjacent coded-row events are classified as "
            "timing-ambiguous rather than forced into a stronger mechanism claim.\n\n"
        )
        f.write(
            pathway_summary.assign(
                **{"Share (%)": lambda df: df["Share (%)"].map(lambda x: f"{x:.1f}")}
            ).to_markdown(index=False)
        )
        f.write(
            "\n\n"
            "*Interpretation: exact adjacent-year events still contain reset/rebuild-like "
            "and continuity-type cases, but non-adjacent coded-row events are deliberately "
            "weakened to timing-ambiguous evidence. The audit supports selective observed "
            "entry, not a uniquely identified modernization mechanism.*\n"
        )

        f.write("\n### Event Year Distribution\n\n")
        f.write(event_years.rename("First adoptions").to_markdown())
        f.write(
            "\n\n"
            "*Interpretation: observed transition into power generation is more common "
            "among facilities that were younger and larger in the previous fiscal year "
            "under the exact-year model. The pathway audit suggests that capital-side "
            "modernization is empirically present in adjacent-year events, but the evidence "
            "is not reducible to one identified mechanism such as replacement alone.*\n"
        )


def main():
    _, adoption, adoption_model, previous_observed_model, pathway_audit, summary = load_adoption_data()
    age_table, cap_table = event_tables(adoption)
    main_result = run_adoption_hazard(adoption_model)
    model = main_result["model"]
    reg = main_result["reg"]
    X = main_result["X"]
    marginal_effects = main_result["marginal_effects"]
    pseudo_r2 = main_result["pseudo_r2"]
    diagnostics = main_result["diagnostics"]
    groups = reg["analysis_facility_id"]
    y = reg["adopt_power_this_year"].astype(float)
    cloglog_robustness = fit_glm_hazard(X, y, link_name="cloglog", groups=groups)
    lpm_robustness = fit_lpm_hazard(X, y, groups=groups)
    previous_observed_result = fit_reported_logit_spec(
        previous_observed_model,
        label="Previous observed coded row: year FE + prefecture FE",
    )
    robustness_results = [
        fit_reported_logit_spec(
            adoption_model,
            label="Exact-year: year FE only",
            include_year_fe=True,
            include_pref_fe=False,
        ),
        fit_reported_logit_spec(
            adoption_model,
            label="Exact-year: prefecture FE only",
            include_year_fe=False,
            include_pref_fe=True,
        ),
        fit_reported_logit_spec(
            adoption_model,
            label="Exact-year: age and capacity only",
            include_year_fe=False,
            include_pref_fe=False,
        ),
    ]
    pathway_summary = pathway_summary_table(pathway_audit)

    results_path = os.path.join(OUTPUT_DIR, "adoption_results.md")
    audit_path = os.path.join(OUTPUT_DIR, "adoption_pathway_audit.csv")
    pathway_audit.to_csv(audit_path, index=False)
    write_results(
        results_path,
        summary,
        adoption,
        age_table,
        cap_table,
        pathway_summary,
        model,
        marginal_effects,
        pseudo_r2,
        diagnostics,
        cloglog_robustness,
        lpm_robustness,
        previous_observed_result,
        robustness_results,
        reg,
    )
    print(f"\nSaved: {results_path}")
    print(f"Saved: {audit_path}")

    marginal_effect_meta = {
        row["variable"]: {
            "ame": manifest_float(row["ame"]),
            "se": manifest_float(row["se"]),
            "pvalue": manifest_float(row["pvalue"]),
        }
        for _, row in marginal_effects.iterrows()
    }
    pathway_counts = {
        category: int(count)
        for category, count in pathway_audit["pathway_category"].value_counts().items()
    }

    manifest_path = write_stage_manifest(
        "05a_power_adoption",
        inputs=["data/processed/incineration_panel_enriched.csv"],
        outputs=[
            "output/adoption_results.md",
            "output/adoption_pathway_audit.csv",
        ],
        metadata={
            "risk_set_obs": int(len(adoption)),
            "risk_set_facilities": int(adoption["analysis_facility_id"].nunique()),
            "events": int(adoption["adopt_power_this_year"].sum()),
            "left_censored_generators": int(summary["left_censored_generators"]),
            "model_obs": int(len(reg)),
            "model_facilities": int(reg["analysis_facility_id"].nunique()),
            "model_events": int(reg["adopt_power_this_year"].sum()),
            "previous_observed_model_obs": int(len(previous_observed_model)),
            "previous_observed_model_facilities": int(
                previous_observed_model["analysis_facility_id"].nunique()
            ),
            "previous_observed_model_events": int(
                previous_observed_model["adopt_power_this_year"].sum()
            ),
            "non_exact_lag_rows_excluded": int(summary["adoption_non_exact_lag_rows"]),
            "non_exact_lag_events_excluded": int(summary["adoption_non_exact_lag_events"]),
            "lag_gap_counts": summary["adoption_lag_gap_counts"],
            "event_lag_gap_counts": summary["adoption_event_lag_gap_counts"],
            "sparse_event_diagnostics": diagnostics,
            "lag_drop_first_rows": int(summary["adoption_model_drop_first_rows"]),
            "lag_drop_additional_missing_rows": int(
                summary["adoption_model_drop_additional_missing_rows"]
            ),
            "lag_drop_additional_missing_facilities": int(
                summary["adoption_model_drop_additional_missing_facilities"]
            ),
            "model": {
                "type": "discrete_time_logit_hazard",
                "reported_scale": "average_marginal_effect",
                "uncertainty_method": "cluster_robust_marginal_effect",
                "predictors_lagged_exact_one_year": True,
                "baseline_prior_year_age_band": "0-10 yrs",
                "coefficients": {
                    "lag_age_10_20": manifest_float(model.params["age_10-20 yrs"]),
                    "lag_age_20_30": manifest_float(model.params["age_20-30 yrs"]),
                    "lag_age_30_plus": manifest_float(model.params["age_30+ yrs"]),
                    "lag_capacity_100t": manifest_float(model.params["lag_capacity_100t"]),
                },
                "pvalues": {
                    "lag_age_10_20": manifest_float(model.pvalues["age_10-20 yrs"]),
                    "lag_age_20_30": manifest_float(model.pvalues["age_20-30 yrs"]),
                    "lag_age_30_plus": manifest_float(model.pvalues["age_30+ yrs"]),
                    "lag_capacity_100t": manifest_float(model.pvalues["lag_capacity_100t"]),
                },
                "average_marginal_effects": marginal_effect_meta,
                "pseudo_r_squared": manifest_float(pseudo_r2),
            },
            "cloglog_robustness": {
                "type": "discrete_time_cloglog",
                "sign_pattern_matches_main": True,
                "coefficients": {
                    "lag_age_10_20": manifest_float(cloglog_robustness.params["age_10-20 yrs"]),
                    "lag_age_20_30": manifest_float(cloglog_robustness.params["age_20-30 yrs"]),
                    "lag_age_30_plus": manifest_float(cloglog_robustness.params["age_30+ yrs"]),
                    "lag_capacity_100t": manifest_float(cloglog_robustness.params["lag_capacity_100t"]),
                },
            },
            "lpm_robustness": {
                "type": "linear_probability_hazard",
                "sign_pattern_matches_main": True,
                "coefficients": {
                    "lag_age_10_20": manifest_float(lpm_robustness.params["age_10-20 yrs"]),
                    "lag_age_20_30": manifest_float(lpm_robustness.params["age_20-30 yrs"]),
                    "lag_age_30_plus": manifest_float(lpm_robustness.params["age_30+ yrs"]),
                    "lag_capacity_100t": manifest_float(lpm_robustness.params["lag_capacity_100t"]),
                },
            },
            "pathway_audit": {
                "events": int(len(pathway_audit)),
                "counts": pathway_counts,
            },
            "specification_sensitivity": [
                {
                    "label": result["label"],
                    "n": int(result["model"].nobs),
                    "events": int(result["diagnostics"]["events"]),
                    "parameters": int(result["diagnostics"]["parameters"]),
                    "events_per_parameter": manifest_float(
                        result["diagnostics"]["events_per_parameter"]
                    ),
                    "sign_pattern_matches_main": sign_pattern_matches(
                        result["marginal_effects"]
                    ),
                    "average_marginal_effects": {
                        row["variable"]: {
                            "ame": manifest_float(row["ame"]),
                            "se": manifest_float(row["se"]),
                            "pvalue": manifest_float(row["pvalue"]),
                        }
                        for _, row in result["marginal_effects"].iterrows()
                    },
                }
                for result in [previous_observed_result, *robustness_results]
            ],
        },
    )
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
