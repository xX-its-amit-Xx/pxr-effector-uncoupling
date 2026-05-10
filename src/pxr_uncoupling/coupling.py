"""Metacell construction and coupling analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
import scipy.sparse as sp
from anndata import AnnData
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from .config import MIN_METACELLS, NR1I2_SYMBOL, TARGET_CELLS_PER_METACELL


def build_metacells(
    adata: AnnData,
    cells_per_metacell: int = TARGET_CELLS_PER_METACELL,
    n_pcs: int = 30,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Aggregate cells into metacells via k-means in PCA space.

    Implements the lightweight metacell approach described in:
    - MetaCell (Baran et al. 2019, doi:10.1186/s13059-019-1812-2)
    - SEACells (Persad et al. 2023, doi:10.1038/s41587-023-01716-9)

    Returns a DataFrame (metacells × genes) with summed then mean-normalized counts.
    """
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


def coupling_per_cell_type(
    adata: AnnData,
    target_genes: list[str],
    cells_per_metacell: int = TARGET_CELLS_PER_METACELL,
    min_metacells: int = MIN_METACELLS,
) -> pd.DataFrame:
    """
    Compute Spearman ρ between NR1I2 and each target gene per cell type.

    Parameters
    ----------
    adata:
        AnnData with NR1I2 and target genes as var_names, cell_type in obs.
    target_genes:
        List of gene symbols to correlate with NR1I2.
    cells_per_metacell:
        Target cells per metacell for k-means aggregation.
    min_metacells:
        Skip cell types yielding fewer metacells than this.

    Returns
    -------
    DataFrame with index = cell_type, columns = target genes, values = Spearman ρ.
    """
    results: dict[str, dict[str, float]] = {}
    missing = [g for g in target_genes if g not in adata.var_names]
    if missing:
        target_genes = [g for g in target_genes if g in adata.var_names]

    for ct in adata.obs["cell_type"].unique():
        sub = adata[adata.obs["cell_type"] == ct]
        meta = build_metacells(sub, cells_per_metacell=cells_per_metacell)
        if len(meta) < min_metacells:
            continue
        if NR1I2_SYMBOL not in meta.columns:
            continue

        row: dict[str, float] = {}
        nr_vals = meta[NR1I2_SYMBOL].values
        for gene in target_genes:
            if gene not in meta.columns:
                row[gene] = float("nan")
                continue
            rho, _ = spearmanr(nr_vals, meta[gene].values)
            row[gene] = float(rho)
        results[ct] = row

    return pd.DataFrame(results).T  # cell_type × gene


def decoupling_score(
    coupling_df: pd.DataFrame,
    reference_cell_type: str = "hepatocyte",
) -> pd.DataFrame:
    """
    Compute per-gene decoupling score: ρ_reference − ρ_other.

    Large positive values indicate genes tightly coupled in the reference
    (hepatocyte) but uncoupled elsewhere — candidate tissue-selective readouts.

    Returns DataFrame with same shape as coupling_df minus the reference row.
    """
    if reference_cell_type not in coupling_df.index:
        raise ValueError(
            f"Reference cell type '{reference_cell_type}' not in coupling matrix. "
            f"Available: {list(coupling_df.index)}"
        )
    ref_row = coupling_df.loc[reference_cell_type]
    other = coupling_df.drop(index=reference_cell_type)
    return ref_row - other  # broadcasts across rows
