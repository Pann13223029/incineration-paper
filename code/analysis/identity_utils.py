"""Deterministic longitudinal identity resolution for MOE facility records."""

from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from difflib import SequenceMatcher
from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment


MAX_MATCH_GAP_YEARS = 4
MIN_MATCH_SCORE = 90.0
MIN_AMBIGUOUS_MATCH_MARGIN = 3.0
_FORBIDDEN_ASSIGNMENT_UTILITY = -1_000_000_000.0
_MATCH_SELECTION_EPSILON = 1e-9


def normalize_identifier(value: Any, *, width: int | None = None) -> str:
    """Normalize spreadsheet identifiers while optionally restoring leading zeros."""
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not text or text.lower() in {"nan", "none", "<na>"}:
        return ""
    if width is not None and text.isdigit():
        return text.zfill(width)
    return text


def normalize_text(value: Any) -> str:
    """Create a conservative comparison key for Japanese facility labels."""
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKC", str(value)).lower().strip()
    return re.sub(r"[\s\u3000・･,，、。()（）\[\]【】「」『』'\"\-‐‑–—ー]+", "", text)


def _number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _relative_difference(left: Any, right: Any) -> float | None:
    a = _number(left)
    b = _number(right)
    if a is None or b is None:
        return None
    scale = max(abs(a), abs(b), 1.0)
    return abs(a - b) / scale


def _numeric_similarity(left: Any, right: Any, bands: tuple[tuple[float, float], ...]) -> float:
    difference = _relative_difference(left, right)
    if difference is None:
        return 0.0
    for threshold, points in bands:
        if difference <= threshold:
            return points
    return 0.0


def _absolute_similarity(left: Any, right: Any, bands: tuple[tuple[float, float], ...]) -> float:
    a = _number(left)
    b = _number(right)
    if a is None or b is None:
        return 0.0
    difference = abs(a - b)
    for threshold, points in bands:
        if difference <= threshold:
            return points
    return 0.0


def score_identity_match(current: pd.Series, previous: pd.Series) -> tuple[float, str]:
    """Score whether two rows represent the same enduring incineration site."""
    if current["_prefecture_key"] != previous["_prefecture_key"]:
        return float("-inf"), "prefecture_mismatch"

    code_equal = bool(
        current["_facility_code_key"]
        and current["_facility_code_key"] == previous["_facility_code_key"]
    )
    muni_equal = bool(
        current["_muni_code_key"]
        and current["_muni_code_key"] == previous["_muni_code_key"]
    )
    name_equal = bool(
        current["_facility_name_key"]
        and current["_facility_name_key"] == previous["_facility_name_key"]
    )
    name_ratio = SequenceMatcher(
        None,
        current["_facility_name_key"],
        previous["_facility_name_key"],
    ).ratio()
    start_difference = _absolute_similarity(
        current.get("year_started"),
        previous.get("year_started"),
        ((1.0, 1.0),),
    )
    capacity_difference = _relative_difference(
        current.get("capacity_t_day"),
        previous.get("capacity_t_day"),
    )

    start_points = _absolute_similarity(
        current.get("year_started"),
        previous.get("year_started"),
        ((0.0, 20.0), (1.0, 16.0), (3.0, 9.0), (8.0, 3.0)),
    )
    capacity_points = _numeric_similarity(
        current.get("capacity_t_day"),
        previous.get("capacity_t_day"),
        ((0.02, 20.0), (0.10, 13.0), (0.25, 7.0), (0.50, 2.0)),
    )
    furnace_points = _absolute_similarity(
        current.get("n_furnaces"),
        previous.get("n_furnaces"),
        ((0.0, 5.0),),
    )
    type_equal = bool(
        current["_facility_type_key"]
        and current["_facility_type_key"] == previous["_facility_type_key"]
    )

    both_names = bool(
        current["_facility_name_key"] and previous["_facility_name_key"]
    )
    both_municipalities = bool(
        current["_muni_code_key"] and previous["_muni_code_key"]
    )
    strong_non_name_support = bool(
        muni_equal
        and start_difference
        and capacity_difference is not None
        and capacity_difference <= 0.10
        and furnace_points >= 5.0
    )
    code_name_contradiction = bool(
        code_equal
        and both_names
        and name_ratio < 0.35
        and not strong_non_name_support
    )
    code_municipality_contradiction = bool(
        code_equal
        and both_municipalities
        and not muni_equal
        and name_ratio < 0.68
    )
    if code_name_contradiction or code_municipality_contradiction:
        return float("-inf"), "contradictory_official_code"

    eligible = (
        (code_equal and (not both_names or name_ratio >= 0.35 or strong_non_name_support))
        or name_equal
        or name_ratio >= 0.88
        or (muni_equal and name_ratio >= 0.68)
        or (
            muni_equal
            and name_ratio >= 0.55
            and start_points >= 9.0
            and capacity_points >= 7.0
        )
    )
    if not eligible:
        return float("-inf"), "insufficient_evidence"

    score = 0.0
    reasons: list[str] = []
    if code_equal:
        score += 30.0
        reasons.append("code")
    if name_equal:
        score += 120.0
        reasons.append("name_exact")
    else:
        score += 70.0 * name_ratio
        reasons.append(f"name_fuzzy={name_ratio:.3f}")
    if muni_equal:
        score += 25.0
        reasons.append("municipality")
    score += start_points + capacity_points + furnace_points
    if start_points:
        reasons.append("start_year")
    if capacity_points:
        reasons.append("capacity")
    if furnace_points:
        reasons.append("furnaces")
    if type_equal:
        score += 5.0
        reasons.append("facility_type")

    return score, "+".join(reasons)


def _canonical_value(value: Any) -> str:
    if pd.isna(value):
        return "<NA>"
    if isinstance(value, (float, np.floating)):
        return format(float(value), ".15g")
    return unicodedata.normalize("NFKC", str(value)).strip()


def _record_fingerprint(row: pd.Series, columns: list[str]) -> str:
    signature = "|".join(
        f"{column}={_canonical_value(row.get(column))}" for column in columns
    )
    return hashlib.sha256(signature.encode("utf-8")).hexdigest()


def _site_id(row: pd.Series) -> str:
    """Derive a reproducible ID from the canonical seed record, never row order."""
    return "site_" + hashlib.sha256(
        str(row["source_record_id"]).encode("utf-8")
    ).hexdigest()[:12]


def _prepare_identity_columns(panel: pd.DataFrame) -> pd.DataFrame:
    source_columns = list(panel.columns)
    frame = panel.copy()
    frame["source_record_id"] = frame.apply(
        lambda row: "record_" + _record_fingerprint(row, source_columns)[:20],
        axis=1,
    )
    frame["source_record_multiplicity"] = frame.groupby(
        "source_record_id",
        dropna=False,
    )["source_record_id"].transform("size")
    frame = frame.drop_duplicates("source_record_id", keep="first").copy()
    if frame["source_record_id"].duplicated().any():
        raise ValueError("Canonical source-record hashes are not unique")
    frame["source_row_id"] = frame["source_record_id"]
    frame["_facility_code_key"] = frame["facility_code"].map(normalize_identifier)
    frame["_muni_code_key"] = frame["muni_code"].map(
        lambda value: normalize_identifier(value, width=5)
    )
    frame["_prefecture_key"] = frame["prefecture"].map(normalize_text)
    frame["_facility_name_key"] = frame["facility_name"].map(normalize_text)
    frame["_facility_type_key"] = frame["facility_type"].map(normalize_text)
    frame["_source_sort_key"] = frame["source_record_id"]
    return frame.sort_values(
        [
            "fiscal_year",
            "_prefecture_key",
            "_muni_code_key",
            "_facility_name_key",
            "_facility_code_key",
            "_source_sort_key",
        ],
        kind="mergesort",
    ).reset_index(drop=True)


def _reason_has_strong_key(reason: str) -> bool:
    tokens = set(reason.split("+"))
    return "name_exact" in tokens or "code" in tokens


def _edge_ambiguity(
    scores: np.ndarray,
    eligible_edges: np.ndarray,
    row_position: int,
    column_position: int,
) -> tuple[float, int | None, float, int | None]:
    """Return row-side and predecessor-side margins and their competitors."""
    score = float(scores[row_position, column_position])

    row_alternatives = np.flatnonzero(eligible_edges[row_position])
    row_alternatives = row_alternatives[row_alternatives != column_position]
    if len(row_alternatives):
        row_scores = scores[row_position, row_alternatives]
        row_alternative_position = int(row_alternatives[int(np.argmax(row_scores))])
        current_row_margin = score - float(
            scores[row_position, row_alternative_position]
        )
    else:
        row_alternative_position = None
        current_row_margin = np.inf

    prior_competitors = np.flatnonzero(eligible_edges[:, column_position])
    prior_competitors = prior_competitors[prior_competitors != row_position]
    if len(prior_competitors):
        competitor_scores = scores[prior_competitors, column_position]
        prior_competitor_position = int(
            prior_competitors[int(np.argmax(competitor_scores))]
        )
        prior_record_margin = score - float(
            scores[prior_competitor_position, column_position]
        )
    else:
        prior_competitor_position = None
        prior_record_margin = np.inf

    return (
        current_row_margin,
        row_alternative_position,
        prior_record_margin,
        prior_competitor_position,
    )


def _solve_optional_assignment(
    scores: np.ndarray,
    accepted_edges: np.ndarray,
) -> list[tuple[int, int]]:
    """Solve one-to-one links with a unique unmatched choice on both sides."""
    current_count, prior_count = scores.shape
    assignment_size = current_count + prior_count
    utility = np.full(
        (assignment_size, assignment_size),
        _FORBIDDEN_ASSIGNMENT_UTILITY,
        dtype=float,
    )

    # Scores are measured relative to the acceptance threshold. The epsilon makes
    # an edge exactly at the threshold deterministically preferable to no link.
    real_edge_utility = scores - MIN_MATCH_SCORE + _MATCH_SELECTION_EPSILON
    utility[:current_count, :prior_count] = np.where(
        accepted_edges,
        real_edge_utility,
        _FORBIDDEN_ASSIGNMENT_UTILITY,
    )

    # Each real record has its own zero-utility unmatched edge. Dummy-to-dummy
    # assignments complete the square problem without sharing an unmatched slot.
    for row_position in range(current_count):
        utility[row_position, prior_count + row_position] = 0.0
    for column_position in range(prior_count):
        utility[current_count + column_position, column_position] = 0.0
    utility[current_count:, prior_count:] = 0.0

    row_positions, column_positions = linear_sum_assignment(-utility)
    if np.any(utility[row_positions, column_positions] <= _FORBIDDEN_ASSIGNMENT_UTILITY):
        raise ValueError("Optional identity assignment selected a forbidden edge")

    links: list[tuple[int, int]] = []
    for row_position, column_position in zip(row_positions, column_positions):
        if row_position < current_count and column_position < prior_count:
            if not accepted_edges[row_position, column_position]:
                raise ValueError("Identity assignment selected an excluded record link")
            links.append((int(row_position), int(column_position)))
    return links


def _uncertainty_reason(current_row_margin: float, prior_record_margin: float) -> str:
    reasons = []
    if current_row_margin < MIN_AMBIGUOUS_MATCH_MARGIN:
        reasons.append("low_current_row_margin")
    if prior_record_margin < MIN_AMBIGUOUS_MATCH_MARGIN:
        reasons.append("low_prior_record_competitor_margin")
    return "+".join(reasons)


def _validate_identity_match_invariants(frame: pd.DataFrame) -> None:
    """Enforce linkage rules directly instead of accepting a count tolerance."""
    matched = ~frame["identity_match_method"].eq("new_site")
    if frame.loc[matched, "identity_match_score"].lt(MIN_MATCH_SCORE).any():
        raise ValueError("Identity resolution accepted a sub-threshold record link")

    margin_columns = [
        "identity_match_current_row_margin",
        "identity_match_prior_record_margin",
        "identity_match_margin",
    ]
    if frame.loc[matched, margin_columns].isna().any().any():
        raise ValueError("Matched identity rows are missing ambiguity margins")

    expected_margin = np.minimum(
        frame.loc[matched, "identity_match_current_row_margin"].to_numpy(dtype=float),
        frame.loc[matched, "identity_match_prior_record_margin"].to_numpy(dtype=float),
    )
    observed_margin = frame.loc[matched, "identity_match_margin"].to_numpy(dtype=float)
    if not np.array_equal(expected_margin, observed_margin):
        raise ValueError("Two-sided identity margins do not equal their exposed minimum")

    expected_uncertain = matched & frame["identity_match_margin"].lt(
        MIN_AMBIGUOUS_MATCH_MARGIN
    )
    observed_uncertain = frame["identity_match_uncertain"].astype(bool)
    if not expected_uncertain.equals(observed_uncertain):
        raise ValueError("Identity uncertainty flags do not match the margin rule")

    strong_method = frame["identity_match_method"].map(_reason_has_strong_key)
    if (observed_uncertain & ~strong_method).any():
        raise ValueError("A weak ambiguous identity edge survived global assignment")
    expected_override = observed_uncertain & strong_method
    if not expected_override.equals(
        frame["identity_match_strong_evidence_override"].astype(bool)
    ):
        raise ValueError("Strong-evidence ambiguity override flags are inconsistent")

    linked_predecessors = frame.loc[
        matched,
        ["fiscal_year", "identity_predecessor_record_id"],
    ]
    if linked_predecessors.duplicated(keep=False).any():
        raise ValueError("A prior record was linked more than once in one fiscal year")


def resolve_stable_identities(panel: pd.DataFrame) -> pd.DataFrame:
    """Resolve a stable administrative-lineage ID across fiscal years."""
    frame = _prepare_identity_columns(panel)
    frame["stable_site_id"] = pd.Series(pd.NA, index=frame.index, dtype="string")
    frame["identity_match_method"] = ""
    frame["identity_match_score"] = np.nan
    frame["identity_match_current_row_margin"] = np.nan
    frame["identity_match_prior_record_margin"] = np.nan
    frame["identity_match_margin"] = np.nan
    frame["identity_match_uncertain"] = False
    frame["identity_match_uncertainty_reason"] = ""
    frame["identity_match_strong_evidence_override"] = False
    frame["identity_predecessor_year"] = pd.Series(pd.NA, index=frame.index, dtype="Int64")
    frame["identity_predecessor_record_id"] = pd.Series(
        pd.NA,
        index=frame.index,
        dtype="string",
    )
    frame["identity_match_current_alternative_record_id"] = pd.Series(
        pd.NA,
        index=frame.index,
        dtype="string",
    )
    frame["identity_match_current_alternative_score"] = np.nan
    frame["identity_match_prior_competitor_record_id"] = pd.Series(
        pd.NA,
        index=frame.index,
        dtype="string",
    )
    frame["identity_match_prior_competitor_score"] = np.nan

    resolution_metadata: dict[str, float | int] = {
        "minimum_match_score": MIN_MATCH_SCORE,
        "minimum_unambiguous_margin": MIN_AMBIGUOUS_MATCH_MARGIN,
        "finite_candidate_edges": 0,
        "subthreshold_candidate_edges_excluded": 0,
        "weak_ambiguous_candidate_edges_excluded": 0,
        "strong_ambiguous_candidate_edges_retained": 0,
    }

    site_last_row: dict[str, int] = {}
    years = sorted(int(year) for year in frame["fiscal_year"].dropna().unique())

    for year in years:
        current_indices = frame.index[frame["fiscal_year"].eq(year)].tolist()
        assigned_current: set[int] = set()

        # Adjacent years are resolved before short gaps so stale histories cannot
        # win a tie against an otherwise identical immediately preceding record.
        for gap in range(1, MAX_MATCH_GAP_YEARS + 1):
            candidates = sorted(
                [
                    (site_id, row_index)
                    for site_id, row_index in site_last_row.items()
                    if year - int(frame.at[row_index, "fiscal_year"]) == gap
                ],
                key=lambda item: item[0],
            )
            remaining = [
                index for index in current_indices if index not in assigned_current
            ]
            if not remaining or not candidates:
                continue

            prefectures = sorted(frame.loc[remaining, "_prefecture_key"].unique())
            for prefecture in prefectures:
                current_pref = [
                    index
                    for index in remaining
                    if frame.at[index, "_prefecture_key"] == prefecture
                ]
                candidate_pref = [
                    (site_id, index)
                    for site_id, index in candidates
                    if frame.at[index, "_prefecture_key"] == prefecture
                ]
                if not current_pref or not candidate_pref:
                    continue

                scores = np.full(
                    (len(current_pref), len(candidate_pref)),
                    np.nan,
                )
                reasons: dict[tuple[int, int], str] = {}
                for row_position, current_index in enumerate(current_pref):
                    current_row = frame.loc[current_index]
                    for column_position, (_, previous_index) in enumerate(candidate_pref):
                        score, reason = score_identity_match(
                            current_row,
                            frame.loc[previous_index],
                        )
                        if math.isfinite(score):
                            scores[row_position, column_position] = score
                            reasons[(row_position, column_position)] = reason

                finite_edges = np.isfinite(scores)
                eligible_edges = finite_edges & (scores >= MIN_MATCH_SCORE)
                resolution_metadata["finite_candidate_edges"] += int(
                    finite_edges.sum()
                )
                resolution_metadata["subthreshold_candidate_edges_excluded"] += int(
                    (finite_edges & ~eligible_edges).sum()
                )

                accepted_edges = eligible_edges.copy()
                edge_diagnostics: dict[
                    tuple[int, int],
                    tuple[float, int | None, float, int | None, str, bool],
                ] = {}
                for row_position, column_position in np.argwhere(eligible_edges):
                    row_position = int(row_position)
                    column_position = int(column_position)
                    (
                        current_row_margin,
                        row_alternative_position,
                        prior_record_margin,
                        prior_competitor_position,
                    ) = _edge_ambiguity(
                        scores,
                        eligible_edges,
                        row_position,
                        column_position,
                    )
                    uncertainty_reason = _uncertainty_reason(
                        current_row_margin,
                        prior_record_margin,
                    )
                    strong_key = _reason_has_strong_key(
                        reasons[(row_position, column_position)]
                    )
                    if uncertainty_reason and not strong_key:
                        accepted_edges[row_position, column_position] = False
                        resolution_metadata[
                            "weak_ambiguous_candidate_edges_excluded"
                        ] += 1
                    elif uncertainty_reason:
                        resolution_metadata[
                            "strong_ambiguous_candidate_edges_retained"
                        ] += 1
                    edge_diagnostics[(row_position, column_position)] = (
                        current_row_margin,
                        row_alternative_position,
                        prior_record_margin,
                        prior_competitor_position,
                        uncertainty_reason,
                        strong_key,
                    )

                for row_position, column_position in _solve_optional_assignment(
                    scores,
                    accepted_edges,
                ):
                    score = float(scores[row_position, column_position])
                    reason = reasons[(row_position, column_position)]
                    (
                        current_row_margin,
                        row_alternative_position,
                        prior_record_margin,
                        prior_competitor_position,
                        uncertainty_reason,
                        strong_key,
                    ) = edge_diagnostics[(row_position, column_position)]
                    margin = min(current_row_margin, prior_record_margin)

                    current_index = current_pref[row_position]
                    site_id, previous_index = candidate_pref[column_position]
                    frame.at[current_index, "stable_site_id"] = site_id
                    frame.at[current_index, "identity_match_method"] = (
                        f"{reason}+gap={gap}"
                    )
                    frame.at[current_index, "identity_match_score"] = score
                    frame.at[
                        current_index,
                        "identity_match_current_row_margin",
                    ] = current_row_margin
                    frame.at[
                        current_index,
                        "identity_match_prior_record_margin",
                    ] = prior_record_margin
                    frame.at[current_index, "identity_match_margin"] = margin
                    frame.at[current_index, "identity_match_uncertain"] = bool(
                        uncertainty_reason
                    )
                    frame.at[
                        current_index,
                        "identity_match_uncertainty_reason",
                    ] = uncertainty_reason
                    frame.at[
                        current_index,
                        "identity_match_strong_evidence_override",
                    ] = bool(uncertainty_reason and strong_key)
                    frame.at[current_index, "identity_predecessor_year"] = int(
                        frame.at[previous_index, "fiscal_year"]
                    )
                    frame.at[current_index, "identity_predecessor_record_id"] = str(
                        frame.at[previous_index, "source_record_id"]
                    )
                    if row_alternative_position is not None:
                        _, alternative_index = candidate_pref[row_alternative_position]
                        frame.at[
                            current_index,
                            "identity_match_current_alternative_record_id",
                        ] = str(frame.at[alternative_index, "source_record_id"])
                        frame.at[
                            current_index,
                            "identity_match_current_alternative_score",
                        ] = float(scores[row_position, row_alternative_position])
                    if prior_competitor_position is not None:
                        competitor_index = current_pref[prior_competitor_position]
                        frame.at[
                            current_index,
                            "identity_match_prior_competitor_record_id",
                        ] = str(frame.at[competitor_index, "source_record_id"])
                        frame.at[
                            current_index,
                            "identity_match_prior_competitor_score",
                        ] = float(scores[prior_competitor_position, column_position])
                    assigned_current.add(current_index)

        for current_index in current_indices:
            if current_index not in assigned_current:
                frame.at[current_index, "stable_site_id"] = _site_id(frame.loc[current_index])
                frame.at[current_index, "identity_match_method"] = "new_site"
                frame.at[current_index, "identity_match_score"] = 0.0
                frame.at[current_index, "identity_match_current_row_margin"] = np.nan
                frame.at[current_index, "identity_match_prior_record_margin"] = np.nan
                frame.at[current_index, "identity_match_margin"] = np.nan

        for current_index in current_indices:
            site_last_row[str(frame.at[current_index, "stable_site_id"])] = current_index

    if frame["stable_site_id"].isna().any():
        raise ValueError("Stable identity resolution left rows without a site ID")
    _validate_identity_match_invariants(frame)
    duplicate_site_year = frame.duplicated(["stable_site_id", "fiscal_year"], keep=False)
    if duplicate_site_year.any():
        examples = frame.loc[
            duplicate_site_year,
            ["stable_site_id", "fiscal_year", "facility_code", "facility_name"],
        ].head(20)
        raise ValueError(
            "Stable identity resolution produced duplicate lineage-years:\n"
            + examples.to_string(index=False)
        )

    frame = assign_asset_episodes(frame)
    result = frame.drop(
        columns=[
            "_facility_code_key",
            "_muni_code_key",
            "_prefecture_key",
            "_facility_name_key",
            "_facility_type_key",
            "_source_sort_key",
        ]
    )
    resolution_metadata["accepted_uncertain_links"] = int(
        result["identity_match_uncertain"].sum()
    )
    result.attrs["identity_resolution_metadata"] = resolution_metadata
    return result


def assign_asset_episodes(frame: pd.DataFrame) -> pd.DataFrame:
    """Split lineages at symmetric start-year or major configuration resets."""
    result = frame.copy()
    result["asset_episode_number"] = 1
    result["asset_episode_reason"] = "initial_observation"

    for _, indices in result.groupby("stable_site_id", sort=False).groups.items():
        ordered = result.loc[list(indices)].sort_values("fiscal_year")
        episode = 1
        previous_index: int | None = None
        for current_index in ordered.index:
            if previous_index is None:
                result.at[current_index, "asset_episode_number"] = episode
                previous_index = current_index
                continue

            previous_start = _number(result.at[previous_index, "year_started"])
            current_start = _number(result.at[current_index, "year_started"])
            previous_age = _number(result.at[previous_index, "facility_age"])
            current_age = _number(result.at[current_index, "facility_age"])
            start_reset = (
                previous_start is not None
                and current_start is not None
                and abs(current_start - previous_start) >= 3
            )
            mature_to_new = (
                previous_age is not None
                and current_age is not None
                and previous_age >= 10
                and current_age <= 3
            )
            capacity_difference = _relative_difference(
                result.at[previous_index, "capacity_t_day"],
                result.at[current_index, "capacity_t_day"],
            )
            furnace_changed = (
                _number(result.at[previous_index, "n_furnaces"])
                != _number(result.at[current_index, "n_furnaces"])
            )
            furnace_type_changed = normalize_text(
                result.at[previous_index, "furnace_type"]
            ) != normalize_text(result.at[current_index, "furnace_type"])
            facility_type_changed = normalize_text(
                result.at[previous_index, "facility_type"]
            ) != normalize_text(result.at[current_index, "facility_type"])
            previous_name = normalize_text(result.at[previous_index, "facility_name"])
            current_name = normalize_text(result.at[current_index, "facility_name"])
            name_ratio = SequenceMatcher(None, previous_name, current_name).ratio()
            major_configuration_reset = bool(
                capacity_difference is not None
                and capacity_difference >= 0.60
                and (furnace_changed or furnace_type_changed or facility_type_changed)
                and name_ratio < 0.88
            )
            if start_reset or mature_to_new or major_configuration_reset:
                episode += 1
                reasons = []
                if start_reset:
                    reasons.append("reported_start_year_reset")
                if mature_to_new:
                    reasons.append("mature_to_new_age_reset")
                if major_configuration_reset:
                    reasons.append("major_configuration_reset")
                result.at[current_index, "asset_episode_reason"] = "+".join(reasons)
            else:
                result.at[current_index, "asset_episode_reason"] = "continued_episode"
            result.at[current_index, "asset_episode_number"] = episode
            previous_index = current_index

    result["asset_episode_id"] = (
        result["stable_site_id"].astype(str)
        + "-a"
        + result["asset_episode_number"].astype(int).astype(str).str.zfill(2)
    )
    return result


def identity_audit_tables(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build compact audit tables for annual continuity and match quality."""
    annual_rows: list[dict[str, Any]] = []
    years = sorted(int(year) for year in frame["fiscal_year"].unique())
    for year in years:
        current = frame[frame["fiscal_year"].eq(year)]
        previous = frame[frame["fiscal_year"].eq(year - 1)]
        overlap = len(
            set(current["stable_site_id"].astype(str))
            & set(previous["stable_site_id"].astype(str))
        )
        code_overlap = len(
            set(current["facility_code"].dropna().astype(str))
            & set(previous["facility_code"].dropna().astype(str))
        )
        annual_rows.append(
            {
                "fiscal_year": year,
                "rows": len(current),
                "stable_sites": current["stable_site_id"].nunique(),
                "official_code_overlap_prior_year": code_overlap if len(previous) else np.nan,
                "stable_site_overlap_prior_year": overlap if len(previous) else np.nan,
                "stable_overlap_share_current_pct": (
                    overlap / len(current) * 100 if len(previous) and len(current) else np.nan
                ),
                "new_site_rows": int(current["identity_match_method"].eq("new_site").sum()),
                "uncertain_link_rows": int(current["identity_match_uncertain"].sum()),
                "missing_official_code_rows": int(current["facility_code"].isna().sum()),
            }
        )

    methods = (
        frame.assign(
            match_family=np.select(
                [
                    frame["identity_match_method"].eq("new_site"),
                    frame["identity_match_method"].str.contains(
                        r"code\+name_exact", regex=True, na=False
                    ),
                    frame["identity_match_method"].str.contains("code", na=False),
                    frame["identity_match_method"].str.contains(
                        "name_exact", na=False
                    ),
                    frame["identity_match_method"].str.contains(
                        "name_fuzzy", na=False
                    ),
                ],
                [
                    "new_site",
                    "official_code_and_exact_name",
                    "official_code_with_other_support",
                    "exact_name_without_code",
                    "fuzzy_name_without_code",
                ],
                default="other",
            )
        )
        .groupby("match_family", as_index=False)
        .agg(
            rows=("stable_site_id", "size"),
            uncertain_links=("identity_match_uncertain", "sum"),
            strong_evidence_overrides=(
                "identity_match_strong_evidence_override",
                "sum",
            ),
            min_score=("identity_match_score", "min"),
            min_current_row_margin=("identity_match_current_row_margin", "min"),
            min_prior_record_margin=("identity_match_prior_record_margin", "min"),
            min_margin=("identity_match_margin", "min"),
        )
    )
    duplicate_records = (
        frame.loc[frame["source_record_multiplicity"].gt(1)]
        .groupby("source_record_id", as_index=False)
        .agg(
            retained_rows=("stable_site_id", "size"),
            source_multiplicity=("source_record_multiplicity", "max"),
            fiscal_year=("fiscal_year", "first"),
            prefecture=("prefecture", "first"),
            facility_name=("facility_name", "first"),
        )
    )
    return {
        "annual": pd.DataFrame(annual_rows),
        "methods": methods,
        "duplicate_records": duplicate_records,
    }
