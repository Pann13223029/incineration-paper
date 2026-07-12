"""Independent numerical benchmarks for the custom Firth-logit estimator."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

from rare_event_utils import fit_firth_logit  # noqa: E402


def reference_objective(
    coefficients: np.ndarray,
    design: np.ndarray,
    outcome: np.ndarray,
) -> float:
    """Evaluate the Jeffreys-prior objective independently of production code."""
    probability = np.clip(expit(design @ coefficients), 1e-12, 1 - 1e-12)
    weights = probability * (1 - probability)
    information = design.T @ (weights[:, None] * design)
    sign, log_determinant = np.linalg.slogdet(information)
    if sign <= 0:
        return float("inf")
    log_likelihood = np.sum(
        outcome * np.log(probability)
        + (1 - outcome) * np.log1p(-probability)
    )
    return float(-(log_likelihood + 0.5 * log_determinant))


class FirthLogitBenchmarkTest(unittest.TestCase):
    def test_complete_separation_matches_closed_form(self) -> None:
        """A separated 2x2 table equals the 0.5-cell corrected log odds."""
        predictor = np.r_[np.zeros(10), np.ones(10)]
        outcome = pd.Series(predictor.copy())
        design = pd.DataFrame({"const": 1.0, "predictor": predictor})

        result = fit_firth_logit(design, outcome)

        # With 10/0 and 0/10 cells, Firth's saturated-table estimates are
        # intercept=-log(21) and slope=2*log(21).
        expected = np.array([-np.log(21.0), 2.0 * np.log(21.0)])
        np.testing.assert_allclose(result.params.to_numpy(), expected, atol=1e-7)
        self.assertTrue(result.converged)
        self.assertTrue(np.isfinite(result.standard_errors).all())

    def test_matches_independent_penalized_likelihood_optimization(self) -> None:
        predictor = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.4, 0.8, 1.2, 1.6, 2.0])
        outcome = pd.Series([0, 0, 1, 0, 0, 1, 0, 1, 1, 1], dtype=float)
        design = pd.DataFrame({"const": 1.0, "predictor": predictor})

        result = fit_firth_logit(design, outcome)
        reference = minimize(
            reference_objective,
            np.zeros(design.shape[1]),
            args=(design.to_numpy(float), outcome.to_numpy(float)),
            method="BFGS",
            options={"gtol": 1e-10, "maxiter": 1000},
        )

        self.assertTrue(np.isfinite(reference.fun))
        np.testing.assert_allclose(result.params.to_numpy(), reference.x, atol=2e-6)
        self.assertAlmostEqual(
            -result.penalized_log_likelihood,
            float(reference.fun),
            places=8,
        )


if __name__ == "__main__":
    unittest.main()
