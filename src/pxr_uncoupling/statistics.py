"""Statistical tests for coupling and decoupling scores.

Provides:
- bootstrap_coupling_ci: percentile bootstrap CIs on per-cell-type ρ values
- permutation_pvalues: empirical p-values via metacell-label shuffling
- benjamini_hochberg: BH-FDR adjustment of a p-value matrix
- compare_to_null_genes: compare PXR-target decoupling distribution to a control gene set
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import scipy.sparse as sp
from anndata import AnnData
from scipy.stats import mannwhitneyu, spearmanr
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from .config import MIN_METACELLS, NR1I2_SYMBOL, TARGET_CELLS_PER_METACELL


def _build_metacell_matrix(
    adata: AnnData,
    cells_per_metacell: int,
    n_pcs: int,
    random_state: int,
) -> pd.DataFrame:
    """Inline metacell builder (avoids the public API dependency cycle)."""
    X = adata.X
    if sp.issparse(X):
        X = X.toarray()
    X = np.log1p(X)

    n_metacells = max(1, X.shape[0] // cells_per_metacell)
    n_pcs_actual = min(n_pcs, X.shape[1] - 1, X.shape[0] - 1)
    pca = PCA(n_components=n_pcs_actual, random_state=random_state)
    coords = pca.fit_transform(X)
    km = KMeans(n_clusters=n_metacells, random_state=random_state, n_init="auto")
    labels = km.fit_predict(coords)
    meta = pd.DataFrame(X, columns=adata.var_names)
    meta["_cluster"] = labels
    return meta.groupby("_cluster").mean()


def bootstrap_coupling_ci(
    adata: AnnData,
    target_genes: list[str],
    n_bootstrap: int = 1000,
    cells_per_metacell: int = TARGET_CELLS_PER_METACELL,
    min_metacells: int = MIN_METACELLS,
    random_state: int = 42,
    confidence: float = 0.95,
) -> dict[str, pd.DataFrame]:
    """
    Bootstrap percentile confidence intervals on coupling ρ per cell type.

    For each cell type, sample metacells with replacement `n_bootstrap` times
    and recompute ρ on the resampled metacell rows. Returns lower / upper /
    median tables (cell_type × gene).

    Method follows the standard percentile bootstrap (Efron 1979). CIs are
    *conditional on the metacell partition* — they do not capture metacell
    construction uncertainty (see permutation_pvalues for that). Use both.
    """
    alpha = (1 - confidence) / 2
    target_genes = [g for g in target_genes if g in adata.var_names]
    rng = np.random.default_rng(random_state)

    lower: dict[str, dict[str, float]] = {}
    upper: dict[str, dict[str, float]] = {}
    median: dict[str, dict[str, float]] = {}

    for ct in adata.obs["cell_type"].unique():
        sub = adata[adata.obs["cell_type"] == ct]
        if sub.n_obs < cells_per_metacell * min_metacells:
            continue
        meta = _build_metacell_matrix(sub, cells_per_metacell, n_pcs=30, random_state=random_state)
        if len(meta) < min_metacells or NR1I2_SYMBOL not in meta.columns:
            continue

        nr_vals = meta[NR1I2_SYMBOL].values
        row_lo: dict[str, float] = {}
        row_hi: dict[str, float] = {}
        row_med: dict[str, float] = {}

        for gene in target_genes:
            if gene not in meta.columns:
                row_lo[gene] = row_hi[gene] = row_med[gene] = float("nan")
                continue
            g_vals = meta[gene].values
            n = len(nr_vals)
            rhos = np.empty(n_bootstrap, dtype=float)
            for b in range(n_bootstrap):
                idx = rng.integers(0, n, size=n)
                r, _ = spearmanr(nr_vals[idx], g_vals[idx])
                rhos[b] = r if np.isfinite(r) else 0.0
            row_lo[gene] = float(np.quantile(rhos, alpha))
            row_hi[gene] = float(np.quantile(rhos, 1 - alpha))
            row_med[gene] = float(np.median(rhos))

        lower[ct] = row_lo
        upper[ct] = row_hi
        median[ct] = row_med

    return {
        "lower": pd.DataFrame(lower).T,
        "upper": pd.DataFrame(upper).T,
        "median": pd.DataFrame(median).T,
    }


def permutation_pvalues(
    adata: AnnData,
    target_genes: list[str],
    n_permutations: int = 1000,
    cells_per_metacell: int = TARGET_CELLS_PER_METACELL,
    min_metacells: int = MIN_METACELLS,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Two-sided empirical p-value per (cell_type, gene) under the null:
    NR1I2 and target are independent within the cell type.

    The null is constructed by shuffling NR1I2 across metacell rows (not cells),
    which preserves the marginal expression distribution while breaking any
    NR1I2-target relationship. This is the appropriate null for "is ρ greater
    than what you'd get by chance given the same metacells?"

    Returns DataFrame (cell_type × gene) of two-sided p-values. Use
    `benjamini_hochberg` for multiple-testing adjustment.
    """
    target_genes = [g for g in target_genes if g in adata.var_names]
    rng = np.random.default_rng(random_state)
    pvals: dict[str, dict[str, float]] = {}

    for ct in adata.obs["cell_type"].unique():
        sub = adata[adata.obs["cell_type"] == ct]
        if sub.n_obs < cells_per_metacell * min_metacells:
            continue
        meta = _build_metacell_matrix(sub, cells_per_metacell, n_pcs=30, random_state=random_state)
        if len(meta) < min_metacells or NR1I2_SYMBOL not in meta.columns:
            continue

        nr_vals = meta[NR1I2_SYMBOL].values
        row: dict[str, float] = {}

        for gene in target_genes:
            if gene not in meta.columns:
                row[gene] = float("nan")
                continue
            g_vals = meta[gene].values
            obs_rho, _ = spearmanr(nr_vals, g_vals)
            if not np.isfinite(obs_rho):
                row[gene] = 1.0
                continue
            null_rhos = np.empty(n_permutations, dtype=float)
            nr_copy = nr_vals.copy()
            for k in range(n_permutations):
                rng.shuffle(nr_copy)
                r, _ = spearmanr(nr_copy, g_vals)
                null_rhos[k] = r if np.isfinite(r) else 0.0
            # two-sided: fraction of |null| >= |obs| (with +1 / +1 add-one smoothing)
            extreme = (np.abs(null_rhos) >= abs(obs_rho)).sum()
            row[gene] = (extreme + 1) / (n_permutations + 1)
        pvals[ct] = row

    return pd.DataFrame(pvals).T


def benjamini_hochberg(pvals: pd.DataFrame) -> pd.DataFrame:
    """BH-FDR adjustment over all non-NaN p-values in the matrix.

    Treats the entire matrix as one family. Returns DataFrame of same shape
    with NaN preserved.
    """
    flat = pvals.values.flatten()
    mask = ~np.isnan(flat)
    valid = flat[mask]
    n = len(valid)
    if n == 0:
        return pvals.copy()
    order = np.argsort(valid)
    ranked = valid[order]
    bh = np.minimum.accumulate((ranked * n / (np.arange(n) + 1))[::-1])[::-1]
    bh = np.clip(bh, 0, 1)
    adjusted = np.empty_like(valid)
    adjusted[order] = bh
    out_flat = np.full_like(flat, np.nan)
    out_flat[mask] = adjusted
    return pd.DataFrame(
        out_flat.reshape(pvals.shape),
        index=pvals.index,
        columns=pvals.columns,
    )


def compare_to_null_genes(
    target_decoupling: pd.DataFrame,
    null_decoupling: pd.DataFrame,
) -> dict[str, float]:
    """
    Mann-Whitney U test: is the PXR-target decoupling distribution shifted
    above a matched null gene distribution?

    Both inputs are (cell_type × gene) matrices of decoupling scores. We flatten
    and test mean-rank shift with a one-sided alternative.
    """
    t = target_decoupling.values.flatten()
    n = null_decoupling.values.flatten()
    t = t[~np.isnan(t)]
    n = n[~np.isnan(n)]
    if len(t) == 0 or len(n) == 0:
        return {
            "u": float("nan"),
            "pvalue": float("nan"),
            "median_target": float("nan"),
            "median_null": float("nan"),
        }
    stat, p = mannwhitneyu(t, n, alternative="greater")
    return {
        "u": float(stat),
        "pvalue": float(p),
        "median_target": float(np.median(t)),
        "median_null": float(np.median(n)),
        "n_target": int(len(t)),
        "n_null": int(len(n)),
    }
