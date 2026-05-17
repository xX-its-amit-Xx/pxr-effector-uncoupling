"""Supplementary / reviewer-facing figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm

from .config import COLOR_ACCENT, COLOR_CREAM, FIGURES


def _styled_fig(figsize: tuple[float, float]):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(COLOR_CREAM)
    ax.set_facecolor(COLOR_CREAM)
    return fig, ax


def heatmap_with_significance(
    coupling: pd.DataFrame,
    qvalues: pd.DataFrame,
    output_path: Path | None = None,
    q_threshold: float = 0.05,
    dpi: int = 300,
) -> plt.Figure:
    """
    Heatmap of ρ overlaid with stars on (cell_type, gene) cells where q<threshold.

    Cells with q<0.05 get a single asterisk; q<0.01 gets two.
    """
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_heatmap_significance.png"

    common_ct = coupling.index.intersection(qvalues.index)
    common_g = coupling.columns.intersection(qvalues.columns)
    rho = coupling.loc[common_ct, common_g].T  # genes × cell_types
    q = qvalues.loc[common_ct, common_g].T

    fig_w = max(10, len(common_ct) * 0.65 + 4)
    fig_h = max(7, len(common_g) * 0.42 + 2)
    fig, ax = _styled_fig((fig_w, fig_h))

    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    cmap = sns.diverging_palette(h_neg=20, h_pos=145, s=60, l=45, sep=1, as_cmap=True)

    sns.heatmap(
        rho,
        ax=ax,
        cmap=cmap,
        norm=norm,
        linewidths=0.4,
        linecolor="#e0d5c5",
        cbar_kws={"label": "Spearman ρ (NR1I2 ~ target)", "shrink": 0.6},
        mask=rho.isna(),
    )

    # overlay stars for significance
    for i, gene in enumerate(rho.index):
        for j, ct in enumerate(rho.columns):
            qv = q.loc[gene, ct] if (gene in q.index and ct in q.columns) else np.nan
            if pd.isna(qv):
                continue
            if qv < 0.01:
                mark = "**"
            elif qv < q_threshold:
                mark = "*"
            else:
                continue
            ax.text(j + 0.5, i + 0.5, mark, ha="center", va="center", fontsize=8, color="#222")

    ax.tick_params(axis="x", labelrotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_xlabel("Cell type")
    ax.set_ylabel("")
    ax.set_title(
        "Coupling ρ with FDR significance overlay\n"
        f"(* q<{q_threshold}, ** q<0.01; BH-FDR over (cell type × gene) family)",
        fontsize=10,
        pad=12,
    )
    plt.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor=COLOR_CREAM)
    return fig


def decoupling_with_ci_forest(
    coupling: pd.DataFrame,
    ci_lower: pd.DataFrame,
    ci_upper: pd.DataFrame,
    qvalues: pd.DataFrame,
    reference_cell_type: str = "hepatocyte",
    top_n: int = 10,
    output_path: Path | None = None,
    dpi: int = 300,
) -> plt.Figure:
    """Forest plot of hepatocyte ρ ± 95% CI for the top-N decoupled genes."""
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_forest_hepatocyte.png"

    # rank by mean decoupling score
    ds = coupling.loc[reference_cell_type] - coupling.drop(index=reference_cell_type)
    ranking = ds.mean(axis=0).sort_values(ascending=False).head(top_n).index.tolist()

    rho = coupling.loc[reference_cell_type, ranking]
    lo = ci_lower.loc[reference_cell_type, ranking]
    hi = ci_upper.loc[reference_cell_type, ranking]
    q = qvalues.loc[reference_cell_type, ranking] if reference_cell_type in qvalues.index else None

    fig, ax = _styled_fig((6, max(3, 0.45 * top_n + 1)))
    y = np.arange(len(ranking))
    err_lo = (rho - lo).clip(lower=0).values
    err_hi = (hi - rho).clip(lower=0).values

    ax.errorbar(
        rho.values,
        y,
        xerr=[err_lo, err_hi],
        fmt="o",
        color=COLOR_ACCENT,
        ecolor="#a0866a",
        capsize=4,
        markersize=7,
        lw=1.5,
    )
    ax.axvline(0, color="#888", ls="--", lw=0.8)
    ax.set_yticks(y)
    labels = list(ranking)
    if q is not None:
        labels = [
            f"{g} {'***' if q[g] < 0.001 else '**' if q[g] < 0.01 else '*' if q[g] < 0.05 else ''}"
            for g in ranking
        ]
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel(f"Spearman ρ in {reference_cell_type} (95% bootstrap CI)")
    ax.set_xlim(-0.2, 1.05)
    ax.set_title(
        f"Top {top_n} hepatocyte-selective PXR targets — point estimates with CIs",
        fontsize=10,
        pad=10,
    )
    plt.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor=COLOR_CREAM)
    return fig


def sensitivity_plot(
    agreement: pd.DataFrame,
    output_path: Path | None = None,
    dpi: int = 300,
) -> plt.Figure:
    """Scatter: Spearman of decoupling ranks vs reference across parameter sweep."""
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_sensitivity.png"

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.patch.set_facecolor(COLOR_CREAM)
    for ax in axes:
        ax.set_facecolor(COLOR_CREAM)

    # 1. Spearman of decoupling ranking, coloured by cells_per_metacell
    palette = {15: "#c87c5a", 30: "#8a9a7b", 60: "#6a8fa5"}
    for cpm, grp in agreement.groupby("cells_per_metacell"):
        axes[0].scatter(
            grp["seed"] + 0.1 * (cpm - 30) / 30,  # tiny jitter per cpm
            grp["spearman_of_decoupling"],
            color=palette.get(cpm, "#888"),
            label=f"cpm={cpm}",
            s=80,
            alpha=0.85,
            edgecolors="white",
        )
    axes[0].axhline(1.0, ls="--", lw=0.8, color="#888")
    axes[0].set_xlabel("Random seed")
    axes[0].set_ylabel("Spearman ρ of decoupling rankings vs. reference")
    axes[0].set_ylim(0.85, 1.02)
    axes[0].legend(title="cells/metacell", fontsize=8)
    axes[0].set_title("Decoupling-rank agreement across parameter sweep", fontsize=10)

    # 2. Jaccard of top-5 hepatocyte-selective genes
    for cpm, grp in agreement.groupby("cells_per_metacell"):
        axes[1].scatter(
            grp["seed"] + 0.1 * (cpm - 30) / 30,
            grp["jaccard_top5"],
            color=palette.get(cpm, "#888"),
            label=f"cpm={cpm}",
            s=80,
            alpha=0.85,
            edgecolors="white",
        )
    axes[1].axhline(1.0, ls="--", lw=0.8, color="#888")
    axes[1].set_xlabel("Random seed")
    axes[1].set_ylabel("Jaccard overlap of top-5 hepatocyte-selective genes")
    axes[1].set_ylim(0.5, 1.05)
    axes[1].legend(title="cells/metacell", fontsize=8)
    axes[1].set_title("Top-5 gene overlap with reference parameter set", fontsize=10)

    plt.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor=COLOR_CREAM)
    return fig


def subsample_stability_plot(
    summary: pd.DataFrame,
    output_path: Path | None = None,
    dpi: int = 300,
) -> plt.Figure:
    """Box of subsample std per cell type — how reproducible is each cell type's row?"""
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_subsample_stability.png"

    fig, ax = _styled_fig((9, 4.5))
    order = summary.groupby("cell_type")["std"].median().sort_values().index.tolist()
    sns.boxplot(
        data=summary,
        x="cell_type",
        y="std",
        order=order,
        ax=ax,
        color=COLOR_ACCENT,
        linewidth=0.8,
        fliersize=2,
    )
    ax.tick_params(axis="x", labelrotation=45, labelsize=8)
    ax.set_xlabel("")
    ax.set_ylabel("Std of ρ across 20 × 80% subsamples")
    ax.set_title(
        "Per-cell-type coupling stability under cell-level subsampling", fontsize=10, pad=10
    )
    plt.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor=COLOR_CREAM)
    return fig
