"""Unit checks for denominator and entry-scale revision contracts."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

import numpy as np
import pandas as pd


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))


def load_stage(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ANALYSIS_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load analysis stage: {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fleet_stage = load_stage("05_fleet_decomposition.py", "fleet_stage")
revision_stage = load_stage("05b_scientific_revision.py", "revision_stage")


class RevisionContractTest(unittest.TestCase):
    def test_active_facility_share_uses_positive_throughput_denominator(self) -> None:
        panel = pd.DataFrame(
            {
                "fiscal_year": [2024] * 4,
                "stable_site_id": ["a", "b", "c", "d"],
                "throughput_t_year": [1000.0, 500.0, 0.0, 0.0],
                "power_generated_mwh": [100.0, 0.0, 0.0, 0.0],
                "power_capacity_kw": [100.0, np.nan, 50.0, np.nan],
                "capacity_t_day": [20.0, 10.0, 5.0, 5.0],
                "has_power_gen": [True, False, True, False],
            }
        )

        row = fleet_stage.build_annual_decomposition(panel).iloc[0]

        self.assertEqual(int(row["positive_throughput_facilities"]), 2)
        self.assertAlmostEqual(row["facility_participation_pct"], 50.0)
        self.assertAlmostEqual(
            row["active_installed_generation_facility_share_pct"], 50.0
        )
        self.assertAlmostEqual(row["positive_output_facility_share_pct"], 25.0)
        self.assertAlmostEqual(
            row["active_positive_output_facility_share_pct"], 50.0
        )
        self.assertAlmostEqual(row["throughput_coverage_pct"], 100 / 1.5)

    def test_turnover_decomposition_separates_endpoint_composition(self) -> None:
        panel = pd.DataFrame(
            {
                "fiscal_year": [2005, 2024, 2005, 2024, 2005, 2024],
                "stable_site_id": ["a", "a", "b", "b", "c", "d"],
                "asset_episode_id": ["a1", "a1", "b1", "b2", "c1", "d1"],
                "has_power_gen": [False, True, False, False, False, True],
            }
        )

        result = fleet_stage.build_turnover_decomposition(panel)
        indexed = result.set_index(["analysis_group", "fiscal_year"])

        self.assertEqual(
            int(indexed.loc[("Endpoint-common lineages", 2024), "lineages"]), 2
        )
        self.assertEqual(
            int(
                indexed.loc[
                    ("Endpoint-common same-episode lineages", 2024), "lineages"
                ]
            ),
            1,
        )
        self.assertAlmostEqual(
            indexed.loc[("2024-only lineages", 2024), "installed_capacity_share_pct"],
            100.0,
        )

    def test_entry_scale_contrasts_match_100_to_300_change(self) -> None:
        frame = pd.DataFrame(
            {
                "lag_capacity_t_day": [100.0, 300.0],
                "lag_facility_age_years": [10.0, 10.0],
                "fiscal_year": [2020, 2020],
                "elapsed_at_risk_years": [2, 2],
            }
        )
        for transform in revision_stage.ENTRY_SCALE_TRANSFORMS:
            with self.subTest(transform=transform):
                design, contrast = revision_stage.diagnostic_entry_design(
                    frame, transform
                )
                observed = float(design.loc[1, "scale_term"] - design.loc[0, "scale_term"])
                self.assertAlmostEqual(observed, contrast, places=12)

    def test_standardized_entry_risk_preserves_noncapacity_covariates(self) -> None:
        frame = pd.DataFrame(
            {
                "lag_capacity_t_day": [50.0, 500.0],
                "lag_facility_age_years": [10.0, 30.0],
                "fiscal_year": [2018, 2022],
                "elapsed_at_risk_years": [1, 5],
            }
        )
        columns = list(revision_stage.primary_entry_design(frame).columns)
        coefficients = pd.Series(
            [0.0, 0.1, 1.0, -0.2, 0.05], index=columns
        )
        bootstrap = pd.DataFrame([coefficients, coefficients], columns=columns)
        bundle = {
            "frame": frame,
            "result": SimpleNamespace(params=coefficients),
            "bootstrap": bootstrap,
        }

        result = revision_stage.standardized_entry_probabilities(bundle)
        probabilities = result[
            result["estimand"].eq("standardized_annual_probability")
        ].set_index("capacity_t_day")
        difference = result[
            result["estimand"].str.contains("difference", na=False)
        ].iloc[0]

        self.assertGreater(
            probabilities.loc[300.0, "probability"],
            probabilities.loc[100.0, "probability"],
        )
        self.assertAlmostEqual(
            difference["probability"],
            probabilities.loc[300.0, "probability"]
            - probabilities.loc[100.0, "probability"],
            places=12,
        )
        self.assertTrue(result["bootstrap_repetitions"].eq(2).all())
        self.assertEqual(
            set(probabilities.index.astype(int)), {24, 60, 100, 120, 300}
        )

    def test_entry_sample_flow_exposes_left_censoring_and_nested_frame(self) -> None:
        panel = pd.DataFrame(
            {
                "stable_site_id": ["a", "a", "b", "b", "c"],
                "fiscal_year": [2020, 2021, 2020, 2021, 2020],
                "has_power_gen": [True, True, False, True, False],
            }
        )
        adoption = pd.DataFrame(
            {
                "analysis_facility_id": ["b", "b", "c"],
                "adopt_power_this_year": [0, 1, 0],
            }
        )
        exact = adoption.assign(lag_throughput_t_year=[0.0, 10.0, 5.0])

        flow = revision_stage.entry_sample_flow(panel, adoption, exact)

        left_censored = flow[
            flow["stage"].eq(
                "Left-censored: positive capacity in first observed year"
            )
        ].iloc[0]
        prior = flow[
            flow["stage"].eq("Positive-prior-throughput sensitivity")
        ].iloc[0]
        self.assertEqual(int(left_censored["lineages"]), 1)
        self.assertEqual(int(prior["facility_year_rows"]), 2)
        self.assertEqual(int(prior["lineages"]), 2)
        self.assertEqual(int(prior["events"]), 1)


if __name__ == "__main__":
    unittest.main()
