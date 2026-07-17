"""Unit checks for denominator and entry-scale revision contracts."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
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
            row["active_positive_output_facility_share_pct"], 50.0
        )
        self.assertAlmostEqual(row["throughput_coverage_pct"], 100 / 1.5)

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


if __name__ == "__main__":
    unittest.main()
