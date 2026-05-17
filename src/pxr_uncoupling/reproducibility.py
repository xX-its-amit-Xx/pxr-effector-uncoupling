"""Per-dataset reproducibility checks.

Does the headline hepatocyte coupling pattern hold within individual donor
cohorts / studies? A reviewer's first concern with public single-cell atlases
is that a strong signal could come from one large study with idiosyncratic
processing.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from anndata import AnnData
from scipy.stats import spearmanr

from .config import MIN_METACELLS, TARGET_CELLS_PER_METACELL
from .coupling import coupling_per_cell_type

log = logging.getLogger(__name__)


def per_dataset_coupling(
    adata: AnnData,
    target_genes: list[str],
    cell_type: str = "hepatocyte",
    min_cells_per_dataset: int = 600,
    cells_per_metacell: int = TARGET_CELLS_PER_METACELL,
    min_metacells: int = MIN_METACELLS,
) -> pd.DataFrame:
    """
    Recompute coupling within each `dataset_id` that contributes at least
    `min_cells_per_dataset` cells of the given cell type.

    Returns DataFrame (dataset_id × gene) of Spearman ρ values. Datasets with
    insufficient cells are skipped.
    """
    sub = adata[adata.obs["cell_type"] == cell_type].copy()
    log.info("%s cells available for %s: %d", cell_type, cell_type, sub.n_obs)
    if sub.n_obs == 0:
        return pd.DataFrame()

    counts = sub.obs["dataset_id"].value_counts()
    eligible = counts[counts >= min_cells_per_dataset].index.tolist()
    log.info(
        "Datasets with >= %d %s cells: %d (of %d total)",
        min_cells_per_dataset,
        cell_type,
        len(eligible),
        counts.size,
    )

    results: dict[str, dict[str, float]] = {}
    for ds_id in eligible:
        ds_sub = sub[sub.obs["dataset_id"] == ds_id].copy()
        # The coupling pipeline expects a cell_type column; reuse it.
        cm = coupling_per_cell_type(
            ds_sub,
            target_genes=target_genes,
            cells_per_metacell=cells_per_metacell,
            min_metacells=min_metacells,
        )
        if cell_type in cm.index:
            results[ds_id] = cm.loc[cell_type].to_dict()
        else:
            log.warning("Dataset %s yielded too few metacells; skipped", ds_id)

    return pd.DataFrame(results).T


def cross_dataset_agreement(per_ds: pd.DataFrame) -> dict[str, float]:
    """Pairwise Spearman ρ of coupling vectors across datasets — summary stats."""
    datasets = per_ds.index.tolist()
    if len(datasets) < 2:
        return {"n_datasets": len(datasets), "median_pairwise_rho": float("nan")}
    rhos: list[float] = []
    for i in range(len(datasets)):
        for j in range(i + 1, len(datasets)):
            a = per_ds.iloc[i].values
            b = per_ds.iloc[j].values
            mask = ~(np.isnan(a) | np.isnan(b))
            if mask.sum() < 3:
                continue
            r, _ = spearmanr(a[mask], b[mask])
            if np.isfinite(r):
                rhos.append(float(r))
    return {
        "n_datasets": len(datasets),
        "n_pairs": len(rhos),
        "median_pairwise_rho": float(np.median(rhos)) if rhos else float("nan"),
        "min_pairwise_rho": float(np.min(rhos)) if rhos else float("nan"),
        "max_pairwise_rho": float(np.max(rhos)) if rhos else float("nan"),
    }
