"""Bias-reduced logistic regression helpers for sparse transition events."""

from __future__ import annotations

from dataclasses import dataclass
import warnings

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import chi2, norm


warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"numpy\.linalg.*")


@dataclass
class FirthLogitResult:
    params: pd.Series
    covariance: pd.DataFrame
    standard_errors: pd.Series
    pvalues: pd.Series
    converged: bool
    iterations: int
    penalized_log_likelihood: float

    def predict(self, design: pd.DataFrame) -> pd.Series:
        values = expit(design[self.params.index].to_numpy(float) @ self.params.to_numpy())
        return pd.Series(values, index=design.index)


def _penalized_log_likelihood(
    design: np.ndarray,
    outcome: np.ndarray,
    coefficients: np.ndarray,
) -> float:
    if not np.isfinite(coefficients).all():
        return float("-inf")
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        linear_predictor = design @ coefficients
        if not np.isfinite(linear_predictor).all():
            return float("-inf")
        probability = np.clip(expit(linear_predictor), 1e-12, 1 - 1e-12)
        weights = probability * (1 - probability)
        information = design.T @ (weights[:, None] * design)
    if not np.isfinite(information).all():
        return float("-inf")
    sign, log_determinant = np.linalg.slogdet(information)
    if sign <= 0:
        return float("-inf")
    likelihood = np.sum(
        outcome * np.log(probability) + (1 - outcome) * np.log1p(-probability)
    )
    return float(likelihood + 0.5 * log_determinant)


def fit_firth_logit(
    design: pd.DataFrame,
    outcome: pd.Series,
    *,
    max_iterations: int = 100,
    tolerance: float = 1e-8,
) -> FirthLogitResult:
    """Fit Firth's Jeffreys-prior penalized logistic regression."""
    columns = list(design.columns)
    x = design.to_numpy(dtype=float)
    y = outcome.to_numpy(dtype=float)
    coefficients = np.zeros(x.shape[1], dtype=float)
    converged = False
    current_likelihood = _penalized_log_likelihood(x, y, coefficients)

    for iteration in range(1, max_iterations + 1):
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            linear_predictor = x @ coefficients
        if not np.isfinite(linear_predictor).all():
            break
        probability = np.clip(expit(linear_predictor), 1e-10, 1 - 1e-10)
        weights = probability * (1 - probability)
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            information = x.T @ (weights[:, None] * x)
        information += np.eye(information.shape[0]) * 1e-10
        if not np.isfinite(information).all():
            raise ValueError("Firth information matrix became non-finite")
        inverse_information = np.linalg.pinv(information, rcond=1e-10)
        leverage = weights * np.einsum("ij,jk,ik->i", x, inverse_information, x)
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            adjusted_score = x.T @ (
                y - probability + leverage * (0.5 - probability)
            )
        if not np.isfinite(adjusted_score).all():
            raise ValueError("Firth adjusted score became non-finite")
        step = inverse_information @ adjusted_score
        largest_step = float(np.max(np.abs(step)))
        if largest_step > 5.0:
            step *= 5.0 / largest_step

        step_scale = 1.0
        accepted = False
        while step_scale >= 1e-8:
            candidate = coefficients + step_scale * step
            candidate_likelihood = _penalized_log_likelihood(x, y, candidate)
            if np.isfinite(candidate_likelihood) and (
                candidate_likelihood >= current_likelihood - 1e-10
            ):
                coefficients = candidate
                current_likelihood = candidate_likelihood
                accepted = True
                break
            step_scale /= 2.0
        if not accepted:
            break
        if float(np.max(np.abs(step_scale * step))) < tolerance:
            converged = True
            break

    if not np.isfinite(coefficients).all() or np.max(np.abs(coefficients)) > 50:
        raise ValueError("Firth logistic regression diverged")
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        linear_predictor = x @ coefficients
    if not np.isfinite(linear_predictor).all():
        raise ValueError("Firth linear predictor became non-finite")
    probability = np.clip(expit(linear_predictor), 1e-10, 1 - 1e-10)
    weights = probability * (1 - probability)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        information = x.T @ (weights[:, None] * x)
    if not np.isfinite(information).all():
        raise ValueError("Firth final information matrix became non-finite")
    information += np.eye(information.shape[0]) * 1e-10
    covariance_array = np.linalg.pinv(information, rcond=1e-10)
    standard_errors_array = np.sqrt(np.maximum(np.diag(covariance_array), 0))
    z_values = np.divide(
        coefficients,
        standard_errors_array,
        out=np.zeros_like(coefficients),
        where=standard_errors_array > 0,
    )
    pvalues_array = 2 * norm.sf(np.abs(z_values))
    return FirthLogitResult(
        params=pd.Series(coefficients, index=columns),
        covariance=pd.DataFrame(covariance_array, index=columns, columns=columns),
        standard_errors=pd.Series(standard_errors_array, index=columns),
        pvalues=pd.Series(pvalues_array, index=columns),
        converged=converged,
        iterations=iteration,
        penalized_log_likelihood=current_likelihood,
    )


def wald_test(result: FirthLogitResult, terms: list[str]) -> tuple[float, int, float]:
    """Return a joint Wald statistic, degrees of freedom, and p-value."""
    coefficients = result.params.loc[terms].to_numpy(float)
    covariance = result.covariance.loc[terms, terms].to_numpy(float)
    statistic = float(coefficients.T @ np.linalg.pinv(covariance) @ coefficients)
    degrees = len(terms)
    return statistic, degrees, float(chi2.sf(statistic, degrees))


def bootstrap_covariance_wald_test(
    point_estimates: pd.Series,
    bootstrap: pd.DataFrame,
    terms: list[str],
) -> tuple[float, int, float, int]:
    """Return a joint Wald test using cluster-bootstrap coefficient covariance."""
    samples = bootstrap[terms].replace([np.inf, -np.inf], np.nan).dropna()
    if len(samples) < max(50, 10 * len(terms)):
        raise ValueError(
            f"Too few complete bootstrap replications for joint test: {len(samples)}"
        )
    covariance = samples.cov().to_numpy(float)
    if (
        not np.isfinite(covariance).all()
        or np.linalg.matrix_rank(covariance) < len(terms)
    ):
        raise ValueError("Bootstrap covariance is non-finite or rank deficient")
    coefficients = point_estimates.loc[terms].to_numpy(float)
    statistic = float(coefficients.T @ np.linalg.pinv(covariance) @ coefficients)
    degrees = len(terms)
    return statistic, degrees, float(chi2.sf(statistic, degrees)), int(len(samples))


def cluster_bootstrap_coefficients(
    frame: pd.DataFrame,
    design_columns: list[str],
    outcome_column: str,
    cluster_column: str,
    *,
    repetitions: int = 499,
    seed: int = 20260710,
) -> pd.DataFrame:
    """Cluster-bootstrap Firth coefficients with deterministic resampling."""
    rng = np.random.default_rng(seed)
    clusters = frame[cluster_column].drop_duplicates().to_numpy()
    rows: list[dict[str, float | int | bool]] = []
    grouped_indices = {
        cluster: group.index.to_numpy()
        for cluster, group in frame.groupby(cluster_column)
    }
    for repetition in range(repetitions):
        sampled = rng.choice(clusters, size=len(clusters), replace=True)
        sampled_indices = np.concatenate(
            [grouped_indices[cluster] for cluster in sampled]
        )
        bootstrap = frame.loc[sampled_indices].reset_index(drop=True)
        event_count = int(bootstrap[outcome_column].sum())
        if event_count <= 0 or event_count >= len(bootstrap):
            raise RuntimeError(
                f"Bootstrap repetition {repetition} has a degenerate outcome"
            )
        varying_columns = [
            column
            for column in design_columns
            if column == "const" or bootstrap[column].nunique(dropna=False) > 1
        ]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                fit = fit_firth_logit(
                    bootstrap[varying_columns],
                    bootstrap[outcome_column],
                    max_iterations=150,
                    tolerance=1e-7,
                )
        except (np.linalg.LinAlgError, ValueError, FloatingPointError) as error:
            raise RuntimeError(
                f"Bootstrap Firth fit failed at repetition {repetition}"
            ) from error
        if not fit.converged:
            raise RuntimeError(
                f"Bootstrap Firth fit did not converge at repetition {repetition}"
            )
        focal_values = fit.params.to_numpy(float)
        if not np.isfinite(focal_values).all():
            raise RuntimeError(
                f"Bootstrap Firth fit is non-finite at repetition {repetition}"
            )
        row: dict[str, float | int | bool] = {
            "repetition": repetition,
            "converged": True,
            "iterations": int(fit.iterations),
            "events": event_count,
        }
        row.update(
            {
                column: (
                    # LAPACK implementations can differ below the precision used
                    # for inference or reporting. Canonicalize at the analysis
                    # boundary so tracked evidence rebuilds identically across OSes.
                    float(np.round(fit.params[column], 8))
                    if column in fit.params
                    else np.nan
                )
                for column in design_columns
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)
