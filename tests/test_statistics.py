"""Unit tests for statistics.py — synthetic data with known statistical properties."""

import numpy as np
import pandas as pd
from anndata import AnnData

from pxr_uncoupling.config import NR1I2_SYMBOL
from pxr_uncoupling.statistics import (
    benjamini_hochberg,
    bootstrap_coupling_ci,
    compare_to_null_genes,
    permutation_pvalues,
)


def _make_correlated_adata(n_cells: int, rho_target: float, seed: int = 0) -> AnnData:
    """Build a single-cell-type AnnData where NR1I2 and TARGET co-vary at given ρ."""
    rng = np.random.default_rng(seed)
    nr = rng.normal(size=n_cells)
    noise = rng.normal(size=n_cells)
    target = rho_target * nr + np.sqrt(max(0, 1 - rho_target**2)) * noise
    # shift positive to mimic count data; log1p safe
    nr = np.abs(nr) + 0.5
    target = np.abs(target) + 0.5
    # add background genes to give PCA real structure
    extras = {f"BG_{i}": np.abs(rng.normal(size=n_cells)) + 0.5 for i in range(15)}
    cols = {NR1I2_SYMBOL: nr, "TARGET": target, **extras}
    X = np.column_stack(list(cols.values())).astype(np.float32)
    obs = pd.DataFrame({"cell_type": ["only_ct"] * n_cells})
    var = pd.DataFrame(index=list(cols.keys()))
    var.index.name = "gene_symbol"
    return AnnData(X=X, obs=obs, var=var)


# ── bootstrap CI ──────────────────────────────────────────────────────────────


def test_bootstrap_ci_brackets_truth_for_strong_correlation():
    """When the true ρ ≈ 0.9, the 95% bootstrap CI should bracket a high value."""
    adata = _make_correlated_adata(900, rho_target=0.9, seed=1)
    ci = bootstrap_coupling_ci(
        adata,
        ["TARGET"],
        n_bootstrap=200,
        cells_per_metacell=15,
        min_metacells=10,
    )
    assert "only_ct" in ci["lower"].index
    lo = ci["lower"].loc["only_ct", "TARGET"]
    hi = ci["upper"].loc["only_ct", "TARGET"]
    med = ci["median"].loc["only_ct", "TARGET"]
    assert lo < hi, "lower must be < upper"
    assert med > 0.5, f"median CI should be high for ρ=0.9 truth, got {med}"
    assert lo > 0, f"lower bound should exclude 0 for ρ=0.9, got {lo}"


def test_bootstrap_ci_brackets_zero_for_null():
    """When NR1I2 and TARGET are independent, CI should include zero."""
    adata = _make_correlated_adata(900, rho_target=0.0, seed=2)
    ci = bootstrap_coupling_ci(
        adata,
        ["TARGET"],
        n_bootstrap=200,
        cells_per_metacell=15,
        min_metacells=10,
    )
    lo = ci["lower"].loc["only_ct", "TARGET"]
    hi = ci["upper"].loc["only_ct", "TARGET"]
    assert lo < 0 < hi or abs(ci["median"].loc["only_ct", "TARGET"]) < 0.4, (
        f"Null CI should bracket 0 or be small; got [{lo}, {hi}]"
    )


# ── permutation p-values ──────────────────────────────────────────────────────


def test_permutation_pvalue_significant_for_strong_correlation():
    """ρ ≈ 0.9 should produce p well below 0.05."""
    adata = _make_correlated_adata(900, rho_target=0.9, seed=3)
    pvals = permutation_pvalues(
        adata,
        ["TARGET"],
        n_permutations=200,
        cells_per_metacell=15,
        min_metacells=10,
    )
    p = pvals.loc["only_ct", "TARGET"]
    assert p < 0.05, f"Expected p<0.05 for ρ=0.9 truth, got p={p}"


def test_permutation_pvalue_uniform_under_null():
    """When ρ=0 truly, p-value should not be << 0.05 on a single test."""
    adata = _make_correlated_adata(900, rho_target=0.0, seed=4)
    pvals = permutation_pvalues(
        adata,
        ["TARGET"],
        n_permutations=200,
        cells_per_metacell=15,
        min_metacells=10,
    )
    p = pvals.loc["only_ct", "TARGET"]
    # not strict — one realization — but should typically exceed 0.01
    assert p > 0.01, f"Single null test should rarely have p<0.01, got p={p}"


# ── Benjamini-Hochberg ────────────────────────────────────────────────────────


def test_bh_monotone_and_bounded():
    """BH-adjusted values must be in [0,1] and BH(p) >= p."""
    rng = np.random.default_rng(5)
    pvals = pd.DataFrame(
        rng.uniform(size=(4, 5)),
        index=[f"ct{i}" for i in range(4)],
        columns=[f"g{j}" for j in range(5)],
    )
    q = benjamini_hochberg(pvals)
    assert q.shape == pvals.shape
    assert ((q >= 0) & (q <= 1)).all().all()
    # all q-values must be >= the corresponding p-value (BH only inflates)
    assert (q.values + 1e-10 >= pvals.values).all()


def test_bh_handles_nan():
    """NaN cells should pass through; the rest of the matrix is adjusted."""
    pvals = pd.DataFrame(
        [[0.001, np.nan, 0.5], [0.01, 0.04, np.nan]],
        index=["a", "b"],
        columns=["x", "y", "z"],
    )
    q = benjamini_hochberg(pvals)
    assert np.isnan(q.loc["a", "y"])
    assert np.isnan(q.loc["b", "z"])
    assert not np.isnan(q.loc["a", "x"])


# ── null comparison ──────────────────────────────────────────────────────────


def test_compare_to_null_distinguishes_shifted_distributions():
    """Target distribution shifted right of null → small p, positive median diff."""
    rng = np.random.default_rng(6)
    target = pd.DataFrame(rng.normal(loc=0.5, scale=0.1, size=(5, 4)))
    null = pd.DataFrame(rng.normal(loc=0.0, scale=0.1, size=(5, 4)))
    out = compare_to_null_genes(target, null)
    assert out["pvalue"] < 0.01
    assert out["median_target"] > out["median_null"]
