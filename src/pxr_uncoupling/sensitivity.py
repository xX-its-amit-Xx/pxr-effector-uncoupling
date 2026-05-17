"""Sensitivity analyses for the coupling pipeline.

Reviewers will ask: does the headline pattern survive different choices of
metacell size, number of PCs, random seed, and cell-type subsampling? This
module computes coupling matrices across a grid of parameters and quantifies
agreement.
"""

from __future__ import annotations

import logging
from itertools import product

import numpy as np
import pandas as pd
from anndata import AnnData
from scipy.stats import spearmanr

from .config import MIN_METACELLS, TARGET_CELLS_PER_METACELL
from .coupling import coupling_per_cell_type

log = logging.getLogger(__name__)


def parameter_sweep(
    adata: AnnData,
    target_genes: list[str],
    cells_per_metacell_grid: tuple[int, ...] = (15, 30, 60),
    min_metacells_grid: tuple[int, ...] = (10, 20),
    seeds: tuple[int, ...] = (0, 42, 123),
) -> pd.DataFrame:
    """
    Run the coupling pipeline across a grid of (cells_per_metacell, min_metacells, seed).

    Returns a long-form DataFrame with columns:
        cells_per_metacell, min_metacells, seed,
        cell_type, gene, rho
    """
    rows: list[dict] = []
    for cpm, mm, seed in product(cells_per_metacell_grid, min_metacells_grid, seeds):
        log.info("sweep cpm=%d mm=%d seed=%d", cpm, mm, seed)
        # Inject seed via monkey-patched random_state in build_metacells
        # The public coupling_per_cell_type doesn't expose random_state; we
        # work around by running the pipeline once per seed via numpy global
        # state — KMeans uses the param directly so we patch via a closure.
        from . import coupling as _coupling

        original = _coupling.build_metacells

        def seeded_build(ad, cells_per_metacell=cpm, n_pcs=30, random_state=seed):
            return original(
                ad, cells_per_metacell=cells_per_metacell, n_pcs=n_pcs, random_state=random_state
            )

        _coupling.build_metacells = seeded_build
        try:
            cm = coupling_per_cell_type(
                adata,
                target_genes=target_genes,
                cells_per_metacell=cpm,
                min_metacells=mm,
            )
        finally:
            _coupling.build_metacells = original

        for ct in cm.index:
            for gene in cm.columns:
                rows.append(
                    {
                        "cells_per_metacell": cpm,
                        "min_metacells": mm,
                        "seed": seed,
                        "cell_type": ct,
                        "gene": gene,
                        "rho": cm.loc[ct, gene],
                    }
                )

    return pd.DataFrame(rows)


def matrix_agreement(sweep_df: pd.DataFrame, reference_key: dict) -> pd.DataFrame:
    """
    Quantify how much coupling matrices vary across the sweep, relative to a
    reference parameter combination.

    `reference_key` is a dict like {"cells_per_metacell": 30, "min_metacells": 20, "seed": 42}.

    Returns a DataFrame (one row per non-reference parameter combination) with:
        - frobenius_distance: ||A - A_ref||_F over common (cell_type, gene) cells
        - spearman_of_decoupling: Spearman ρ between per-gene mean decoupling
          rankings (top genes should agree across parameters)
        - jaccard_top5: overlap of top-5 decoupled genes
    """

    def to_matrix(df_slice: pd.DataFrame) -> pd.DataFrame:
        return df_slice.pivot_table(index="cell_type", columns="gene", values="rho")

    ref_mask = (
        (sweep_df["cells_per_metacell"] == reference_key["cells_per_metacell"])
        & (sweep_df["min_metacells"] == reference_key["min_metacells"])
        & (sweep_df["seed"] == reference_key["seed"])
    )
    ref_mat = to_matrix(sweep_df[ref_mask])
    if "hepatocyte" in ref_mat.index:
        ref_ds = (
            (ref_mat.loc["hepatocyte"] - ref_mat.drop(index="hepatocyte")).mean(axis=0).dropna()
        )
        ref_top5 = set(ref_ds.sort_values(ascending=False).head(5).index)
    else:
        ref_ds = None
        ref_top5 = set()

    out_rows: list[dict] = []
    for (cpm, mm, seed), grp in sweep_df.groupby(["cells_per_metacell", "min_metacells", "seed"]):
        if (cpm, mm, seed) == (
            reference_key["cells_per_metacell"],
            reference_key["min_metacells"],
            reference_key["seed"],
        ):
            continue
        mat = to_matrix(grp)
        common_idx = ref_mat.index.intersection(mat.index)
        common_cols = ref_mat.columns.intersection(mat.columns)
        a = ref_mat.loc[common_idx, common_cols].values
        b = mat.loc[common_idx, common_cols].values
        mask = ~(np.isnan(a) | np.isnan(b))
        if mask.sum() == 0:
            frob = float("nan")
        else:
            frob = float(np.sqrt(((a[mask] - b[mask]) ** 2).sum()))

        spr_ds = float("nan")
        jacc = float("nan")
        if ref_ds is not None and "hepatocyte" in mat.index:
            ds_here = (mat.loc["hepatocyte"] - mat.drop(index="hepatocyte")).mean(axis=0).dropna()
            common_genes = ref_ds.index.intersection(ds_here.index)
            if len(common_genes) >= 3:
                r, _ = spearmanr(ref_ds.loc[common_genes], ds_here.loc[common_genes])
                spr_ds = float(r) if np.isfinite(r) else float("nan")
            top5_here = set(ds_here.sort_values(ascending=False).head(5).index)
            jacc = (
                (len(ref_top5 & top5_here) / len(ref_top5 | top5_here))
                if ref_top5 | top5_here
                else float("nan")
            )

        out_rows.append(
            {
                "cells_per_metacell": cpm,
                "min_metacells": mm,
                "seed": seed,
                "frobenius_distance": frob,
                "spearman_of_decoupling": spr_ds,
                "jaccard_top5": jacc,
            }
        )

    return pd.DataFrame(out_rows)


def subsample_stability(
    adata: AnnData,
    target_genes: list[str],
    n_iterations: int = 20,
    fraction: float = 0.8,
    cells_per_metacell: int = TARGET_CELLS_PER_METACELL,
    min_metacells: int = MIN_METACELLS,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Subsample `fraction` of cells per cell type `n_iterations` times and
    recompute coupling. Returns long-form DataFrame with columns:
        iteration, cell_type, gene, rho.
    """
    rng = np.random.default_rng(random_state)
    rows: list[dict] = []
    cell_types = adata.obs["cell_type"].unique()

    for it in range(n_iterations):
        keep_idx = []
        for ct in cell_types:
            ct_idx = np.where(adata.obs["cell_type"].values == ct)[0]
            n_keep = max(1, int(len(ct_idx) * fraction))
            keep_idx.extend(rng.choice(ct_idx, size=n_keep, replace=False).tolist())
        sub = adata[keep_idx].copy()
        cm = coupling_per_cell_type(
            sub,
            target_genes=target_genes,
            cells_per_metacell=cells_per_metacell,
            min_metacells=min_metacells,
        )
        for ct in cm.index:
            for gene in cm.columns:
                rows.append(
                    {
                        "iteration": it,
                        "cell_type": ct,
                        "gene": gene,
                        "rho": cm.loc[ct, gene],
                    }
                )

    return pd.DataFrame(rows)


def stability_summary(stability_df: pd.DataFrame) -> pd.DataFrame:
    """Per-(cell_type, gene) summary: mean, std, [2.5%, 97.5%] across subsample iters."""
    g = stability_df.groupby(["cell_type", "gene"])["rho"]
    return pd.DataFrame(
        {
            "mean": g.mean(),
            "std": g.std(),
            "ci_low": g.quantile(0.025),
            "ci_high": g.quantile(0.975),
            "n_iter": g.size(),
        }
    ).reset_index()
