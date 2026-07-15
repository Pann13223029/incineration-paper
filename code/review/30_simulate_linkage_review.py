#!/usr/bin/env python3
"""Simulate two blinded linkage reviews and a conservative adjudication.

This is a workflow stress test, not independent human validation. Outputs live
under paper/notes/review/simulations and never enter the canonical evidence
snapshot.
"""

from __future__ import annotations

import csv
import importlib.util
import math
import re
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = REPO_ROOT / "code" / "analysis"
OUTPUT_DIR = REPO_ROOT / "output"
SIMULATION_DIR = REPO_ROOT / "paper" / "notes" / "review" / "simulations"
PACKET_PATH = OUTPUT_DIR / "linkage_validation_packet.csv"
KEY_PATH = OUTPUT_DIR / "linkage_validation_key.csv"
INFLUENCE_PATH = OUTPUT_DIR / "revised_entry_influence.csv"

SAME = "same administrative facility history"
DIFFERENT = "different facility history"
INDETERMINATE = "indeterminate from available evidence"
RESET = "same lineage but probable asset/configuration reset"
UNRESOLVED = "unresolved: external evidence required"
DECISION_ORDER = [SAME, RESET, INDETERMINATE, DIFFERENT]
ROLE_COLUMNS = [
    "modeled_event_link",
    "identity_match_uncertain",
    "fuzzy_link",
    "gap_link",
    "fy2019_2020_bridge",
]


def normalize(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).lower()
    return re.sub(r"[\W_]+", "", text)


def equal_field(row: pd.Series, prior: str, current: str) -> bool:
    left = normalize(row[prior])
    return bool(left) and left == normalize(row[current])


def number(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def pair_features(row: pd.Series) -> dict[str, float | bool | int]:
    prior_name = normalize(row["prior_facility_name"])
    current_name = normalize(row["current_facility_name"])
    name_similarity = SequenceMatcher(None, prior_name, current_name).ratio()
    same_municipality = equal_field(
        row, "prior_muni_code", "current_muni_code"
    )
    same_official_code = equal_field(
        row, "prior_facility_code", "current_facility_code"
    )
    configuration_matches = sum(
        equal_field(row, f"prior_{field}", f"current_{field}")
        for field in (
            "year_started",
            "n_furnaces",
            "furnace_type",
            "operation_mode",
            "facility_type",
        )
    )
    prior_capacity = number(row["prior_capacity_t_day"])
    current_capacity = number(row["current_capacity_t_day"])
    if prior_capacity > 0 and current_capacity > 0:
        capacity_relative_change = abs(current_capacity - prior_capacity) / max(
            current_capacity, prior_capacity
        )
    else:
        capacity_relative_change = 1.0
    prior_start = number(row["prior_year_started"])
    current_start = number(row["current_year_started"])
    if math.isfinite(prior_start) and math.isfinite(current_start):
        start_year_change = abs(current_start - prior_start)
    else:
        start_year_change = 99.0
    return {
        "name_similarity": name_similarity,
        "same_municipality": same_municipality,
        "same_official_code": same_official_code,
        "configuration_matches": configuration_matches,
        "capacity_relative_change": capacity_relative_change,
        "start_year_change": start_year_change,
    }


def reviewer_a(features: dict[str, float | bool | int]) -> str:
    """Continuity-focused reviewer that accepts corroborated name changes."""
    similarity = float(features["name_similarity"])
    same_municipality = bool(features["same_municipality"])
    same_code = bool(features["same_official_code"])
    configuration = int(features["configuration_matches"])
    capacity_change = float(features["capacity_relative_change"])
    start_change = float(features["start_year_change"])
    strong = (
        same_code
        or (same_municipality and similarity >= 0.55)
        or (same_municipality and configuration >= 4)
    )
    if strong and (
        start_change >= 5
        or capacity_change > 0.45
        or (configuration <= 2 and similarity < 0.70)
    ):
        return RESET
    if strong:
        return SAME
    if same_municipality and (similarity >= 0.30 or configuration >= 3):
        return INDETERMINATE
    return DIFFERENT


def reviewer_b(features: dict[str, float | bool | int]) -> str:
    """Skeptical reviewer requiring stronger agreement across visible fields."""
    similarity = float(features["name_similarity"])
    same_municipality = bool(features["same_municipality"])
    same_code = bool(features["same_official_code"])
    configuration = int(features["configuration_matches"])
    capacity_change = float(features["capacity_relative_change"])
    start_change = float(features["start_year_change"])
    strong = (
        (same_code and similarity >= 0.35)
        or (same_municipality and similarity >= 0.72 and configuration >= 3)
        or (same_municipality and configuration >= 5)
    )
    if strong and (
        start_change >= 3
        or capacity_change > 0.30
        or (configuration <= 3 and similarity < 0.60)
    ):
        return RESET
    if strong:
        return SAME
    if (same_code or same_municipality) and (
        similarity >= 0.25 or configuration >= 2
    ):
        return INDETERMINATE
    return DIFFERENT


def adjudicate(
    decision_a: str,
    decision_b: str,
    features: dict[str, float | bool | int],
) -> str:
    """Resolve visible-evidence disagreements; retain hard cases as unresolved."""
    if decision_a == decision_b and decision_a in (SAME, RESET):
        return decision_a
    if decision_a == decision_b == DIFFERENT:
        return UNRESOLVED
    similarity = float(features["name_similarity"])
    same_municipality = bool(features["same_municipality"])
    same_code = bool(features["same_official_code"])
    configuration = int(features["configuration_matches"])
    capacity_change = float(features["capacity_relative_change"])
    start_change = float(features["start_year_change"])
    strong = (
        same_code
        or (same_municipality and similarity >= 0.65 and configuration >= 3)
        or (same_municipality and configuration >= 4)
    )
    if not strong:
        return UNRESOLVED
    if start_change >= 3 or capacity_change > 0.30:
        return RESET
    return SAME


def cohen_kappa(left: pd.Series, right: pd.Series) -> float:
    observed = float((left == right).mean())
    left_share = left.value_counts(normalize=True)
    right_share = right.value_counts(normalize=True)
    expected = sum(
        float(left_share.get(category, 0.0) * right_share.get(category, 0.0))
        for category in set(left_share.index) | set(right_share.index)
    )
    if math.isclose(expected, 1.0):
        return 1.0
    return (observed - expected) / (1.0 - expected)


def agreement_rows(decisions: pd.DataFrame) -> pd.DataFrame:
    strata: list[tuple[str, pd.Series]] = [
        ("All packet pairs", pd.Series(True, index=decisions.index))
    ]
    strata.extend(
        (column, decisions[column].astype(bool)) for column in ROLE_COLUMNS
    )
    rows: list[dict[str, object]] = []
    for label, mask in strata:
        frame = decisions.loc[mask]
        exact_agreement = float(
            (frame["reviewer_a_decision"] == frame["reviewer_b_decision"]).mean()
        )
        collapse = {SAME: "same", RESET: "same", INDETERMINATE: "not same", DIFFERENT: "not same"}
        binary_a = frame["reviewer_a_decision"].map(collapse)
        binary_b = frame["reviewer_b_decision"].map(collapse)
        rows.append(
            {
                "stratum": label,
                "pairs": int(len(frame)),
                "exact_agreements": int(
                    (frame["reviewer_a_decision"] == frame["reviewer_b_decision"]).sum()
                ),
                "exact_agreement_pct": 100.0 * exact_agreement,
                "four_category_kappa": cohen_kappa(
                    frame["reviewer_a_decision"], frame["reviewer_b_decision"]
                ),
                "binary_same_lineage_agreement_pct": 100.0
                * float((binary_a == binary_b).mean()),
                "binary_same_lineage_kappa": cohen_kappa(binary_a, binary_b),
                "adjudicated_same": int(frame["adjudication"].eq(SAME).sum()),
                "adjudicated_reset": int(frame["adjudication"].eq(RESET).sum()),
                "unresolved": int(frame["adjudication"].eq(UNRESOLVED).sum()),
            }
        )
    return pd.DataFrame(rows)


def load_revision_module():
    sys.path.insert(0, str(ANALYSIS_DIR))
    path = ANALYSIS_DIR / "05b_scientific_revision.py"
    spec = importlib.util.spec_from_file_location("scientific_revision", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rerun_event_stress_test(unresolved_lineages: set[str]) -> dict[str, float | int]:
    revision = load_revision_module()
    panel = revision.load_panel()
    adoption = revision.build_adoption_frame(panel)
    exact = revision.build_adoption_model_frame(
        panel, adoption, exact_year_only=True
    )
    baseline_design = revision.primary_entry_design(exact)
    baseline_fit = revision.fit_firth_logit(
        baseline_design, exact["adopt_power_this_year"].astype(float)
    )
    stressed = exact[
        ~exact["analysis_facility_id"].astype(str).isin(unresolved_lineages)
    ].copy()
    stressed_design = revision.primary_entry_design(stressed)
    stressed_fit = revision.fit_firth_logit(
        stressed_design, stressed["adopt_power_this_year"].astype(float)
    )
    contrast = math.log(2.0)
    return {
        "baseline_rows": int(len(exact)),
        "baseline_events": int(exact["adopt_power_this_year"].sum()),
        "baseline_scale_or": float(
            np.exp(baseline_fit.params["log_processing_capacity"] * contrast)
        ),
        "stressed_rows": int(len(stressed)),
        "stressed_events": int(stressed["adopt_power_this_year"].sum()),
        "stressed_scale_or": float(
            np.exp(stressed_fit.params["log_processing_capacity"] * contrast)
        ),
        "stressed_age_coefficient": float(stressed_fit.params["age_per_10y"]),
    }


def write_report(
    decisions: pd.DataFrame,
    agreement: pd.DataFrame,
    stress: dict[str, float | int],
    unresolved_event_ids: list[str],
    unresolved_event_lineages: list[str],
) -> None:
    overall = agreement.iloc[0]
    reviewer_a_counts = decisions["reviewer_a_decision"].value_counts()
    reviewer_b_counts = decisions["reviewer_b_decision"].value_counts()
    adjudication_counts = decisions["adjudication"].value_counts()
    event_frame = decisions[decisions["modeled_event_link"]]
    event_unresolved = event_frame[event_frame["adjudication"].eq(UNRESOLVED)]
    report = f"""# Simulated Linkage Review And Adjudication

Simulation date: 15 July 2026

## Status Warning

This is a deterministic workflow simulation, not independent human validation.
Both synthetic reviewers use only fields visible in the blinded packet. The
answer key is opened only after their decisions to map unresolved pairs to
lineages and run a conservative model stress test. These results must not be
reported as inter-rater reliability or external validation in the manuscript.

## Simulation Design

- Reviewer A is continuity-focused and accepts corroborated name changes.
- Reviewer B is more skeptical and requires stronger agreement across visible
  name, municipality, official-code, timing, capacity, and configuration fields.
- Exact agreement preserves all four allowed decisions.
- Binary agreement collapses `same` and `probable reset` into one same-lineage
  class.
- The adjudicator resolves only pairs with strong visible corroboration. Hard
  cases remain unresolved and require an archived municipal or Ministry source.

## Agreement Results

{agreement.to_markdown(index=False, floatfmt='.3f')}

Overall exact agreement is {int(overall['exact_agreements'])}/{int(overall['pairs'])}
({overall['exact_agreement_pct']:.2f}%), with four-category Cohen's kappa
{overall['four_category_kappa']:.3f}. This high value is partly structural:
the packet contains accepted candidate links rather than a balanced set of
matches and non-matches.

The modeled-event binary kappa is zero despite 97.14% binary agreement because
Reviewer A assigns all 35 pairs to the same-lineage class while Reviewer B
assigns only one pair outside it. This is a prevalence/marginal-distribution
artifact; the raw agreement and four-category table are more informative here.

## Decision Distribution

| Decision | Reviewer A | Reviewer B | Adjudicated |
|:--|--:|--:|--:|
| Same administrative history | {reviewer_a_counts.get(SAME, 0)} | {reviewer_b_counts.get(SAME, 0)} | {adjudication_counts.get(SAME, 0)} |
| Same lineage, probable reset | {reviewer_a_counts.get(RESET, 0)} | {reviewer_b_counts.get(RESET, 0)} | {adjudication_counts.get(RESET, 0)} |
| Indeterminate | {reviewer_a_counts.get(INDETERMINATE, 0)} | {reviewer_b_counts.get(INDETERMINATE, 0)} | 0 |
| Different | {reviewer_a_counts.get(DIFFERENT, 0)} | {reviewer_b_counts.get(DIFFERENT, 0)} | 0 |
| Unresolved pending external source | 0 | 0 | {adjudication_counts.get(UNRESOLVED, 0)} |

## Modeled-Event Adjudication

Among 35 modeled-event links, {len(event_frame) - len(event_unresolved)} are
accepted as the same administrative history or same lineage with a probable
reset. {len(event_unresolved)} remains unresolved: {', '.join(unresolved_event_ids)}.
After unblinding for the stress test, this pair maps to
{', '.join(unresolved_event_lineages)}.

## Conservative Model Rerun

The primary five-parameter Firth point model was rerun after deleting every
lineage attached to an unresolved modeled-event pair. The baseline contains
{stress['baseline_rows']:,} rows and {stress['baseline_events']} events, with a
300-versus-100 t/day odds ratio of {stress['baseline_scale_or']:.3f}. The
conservative rerun contains {stress['stressed_rows']:,} rows and
{stress['stressed_events']} events; its scale odds ratio is
{stress['stressed_scale_or']:.3f}, and its age-per-decade coefficient is
{stress['stressed_age_coefficient']:.3f}.

This adverse simulated exclusion does not reverse the scale result. It is not a
substitute for adjudication: the unresolved event pair still requires an
independent reviewer and an archived source before the linkage layer can be
called externally validated.

## Real Review Handoff

1. Give reviewers only `output/linkage_validation_packet.csv` and the protocol.
2. Require independent decisions for all 35 modeled-event and 16 uncertain
   links, plus the agreed sample of other strata.
3. Archive evidence URLs and notes for every disagreement.
4. Open the answer key only after decisions are locked.
5. Rerun the canonical pipeline if any event lineage is rejected or split.
"""
    (SIMULATION_DIR / "linkage-review-simulation-2026-07-15.md").write_text(
        report, encoding="utf-8"
    )


def main() -> None:
    SIMULATION_DIR.mkdir(parents=True, exist_ok=True)
    packet = pd.read_csv(PACKET_PATH)
    for column in ROLE_COLUMNS:
        packet[column] = packet[column].astype(bool)

    rows: list[dict[str, object]] = []
    for _, row in packet.iterrows():
        features = pair_features(row)
        decision_a = reviewer_a(features)
        decision_b = reviewer_b(features)
        rows.append(
            {
                "validation_pair_id": row["validation_pair_id"],
                **{column: bool(row[column]) for column in ROLE_COLUMNS},
                **features,
                "reviewer_a_decision": decision_a,
                "reviewer_b_decision": decision_b,
                "adjudication": adjudicate(decision_a, decision_b, features),
            }
        )
    decisions = pd.DataFrame(rows)
    agreement = agreement_rows(decisions)

    key = pd.read_csv(KEY_PATH)[
        ["validation_pair_id", "stable_site_id", "match_family"]
    ]
    decisions = decisions.merge(
        key, on="validation_pair_id", how="left", validate="one_to_one"
    )
    unresolved_events = decisions[
        decisions["modeled_event_link"] & decisions["adjudication"].eq(UNRESOLVED)
    ]
    unresolved_event_ids = unresolved_events["validation_pair_id"].tolist()
    unresolved_event_lineages = unresolved_events["stable_site_id"].tolist()
    if not unresolved_event_lineages:
        raise RuntimeError("Simulation did not generate an event-lineage stress case")
    stress = rerun_event_stress_test(set(unresolved_event_lineages))

    influence = pd.read_csv(INFLUENCE_PATH)
    expected = influence[
        influence["deletion"].eq("event_lineage_removed")
        & influence["omitted_lineage"].isin(unresolved_event_lineages)
    ]
    if len(expected) != len(unresolved_event_lineages):
        raise RuntimeError("Precomputed influence comparison is incomplete")
    if not np.allclose(
        expected["odds_ratio_300_vs_100"].to_numpy(float),
        stress["stressed_scale_or"],
        rtol=0,
        atol=1e-8,
    ):
        raise RuntimeError("Simulation rerun disagrees with canonical influence fit")

    decisions.to_csv(
        SIMULATION_DIR / "linkage-review-simulation-decisions.csv",
        index=False,
        quoting=csv.QUOTE_MINIMAL,
        float_format="%.6f",
    )
    agreement.to_csv(
        SIMULATION_DIR / "linkage-review-simulation-summary.csv",
        index=False,
        float_format="%.6f",
    )
    write_report(
        decisions,
        agreement,
        stress,
        unresolved_event_ids,
        unresolved_event_lineages,
    )
    print(f"Simulation pairs: {len(decisions):,}")
    print(
        "Exact agreement: "
        f"{agreement.iloc[0]['exact_agreements']:.0f}/{agreement.iloc[0]['pairs']:.0f}"
    )
    print(f"Unresolved modeled-event links: {len(unresolved_event_ids)}")
    print(f"Stressed scale OR: {stress['stressed_scale_or']:.6f}")


if __name__ == "__main__":
    main()
