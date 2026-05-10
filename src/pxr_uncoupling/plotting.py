"""Plotting utilities for pxr-uncoupling."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Patch

from .config import COLOR_ACCENT, COLOR_CREAM, COLOR_SAGE, FIGURES

DISEASE_COLORS = {
    "IBD/GI": "#6a8fa5",
    "cancer": "#b05c5c",
    "metabolic": "#8a9a7b",
    "other": "#c8b89a",
}


def decoupling_heatmap(
    coupling_df: pd.DataFrame,
    target_meta: pd.DataFrame,
    cell_type_tissue_map: dict[str, str],
    disease_annotations: dict[str, str] | None = None,
    output_path: Path | None = None,
    dpi: int = 300,
) -> plt.Figure:
    """
    Render the final decoupling heatmap.

    Parameters
    ----------
    coupling_df:
        DataFrame (cell_type × gene) of Spearman ρ values.
    target_meta:
        DataFrame with gene metadata (category, regulation) indexed by gene_symbol.
    cell_type_tissue_map:
        Maps cell_type labels to tissue groupings for column ordering.
    disease_annotations:
        Maps cell_type → disease category string for column annotation boxes.
    output_path:
        Where to save. Defaults to figures/final_heatmap.png.
    """
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "final_heatmap.png"

    # order genes by category
    gene_order = (
        target_meta.sort_values("category")
        .index.intersection(coupling_df.columns)
        .tolist()
    )
    # order cell types by tissue
    ct_order = sorted(
        coupling_df.index,
        key=lambda ct: (cell_type_tissue_map.get(ct, "z_other"), ct),
    )

    plot_df = coupling_df.loc[ct_order, gene_order].T  # genes × cell_types

    fig_w = max(10, len(ct_order) * 0.6 + 4)
    fig_h = max(8, len(gene_order) * 0.45 + 3)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor(COLOR_CREAM)
    ax.set_facecolor(COLOR_CREAM)

    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    cmap = sns.diverging_palette(
        h_neg=20, h_pos=145, s=60, l=45, sep=1, as_cmap=True
    )

    sns.heatmap(
        plot_df,
        ax=ax,
        cmap=cmap,
        norm=norm,
        linewidths=0.4,
        linecolor="#e0d5c5",
        cbar_kws={"label": "Spearman ρ (NR1I2 ~ target)", "shrink": 0.6},
        mask=plot_df.isna(),
    )

    # row annotations: regulation direction
    if "regulation" in target_meta.columns:
        for i, gene in enumerate(gene_order):
            if gene in target_meta.index:
                reg = target_meta.loc[gene, "regulation"]
                color = COLOR_ACCENT if reg == "induced" else COLOR_SAGE
                ax.add_patch(
                    plt.Rectangle((-0.5, i), 0.4, 1, color=color, clip_on=False)
                )

    # column annotations: disease category
    if disease_annotations:
        for j, ct in enumerate(ct_order):
            cat = disease_annotations.get(ct)
            if cat:
                color = DISEASE_COLORS.get(cat, "#cccccc")
                ax.add_patch(
                    plt.Rectangle(
                        (j, len(gene_order) + 0.1),
                        1,
                        0.4,
                        color=color,
                        clip_on=False,
                    )
                )

    ax.set_xlabel("Cell type", fontsize=10)
    ax.set_ylabel("")
    ax.tick_params(axis="x", labelrotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)

    # legends
    reg_handles = [
        Patch(color=COLOR_ACCENT, label="induced"),
        Patch(color=COLOR_SAGE, label="repressed"),
    ]
    legend1 = ax.legend(
        handles=reg_handles,
        title="regulation",
        loc="upper left",
        bbox_to_anchor=(1.15, 1),
        fontsize=8,
    )
    if disease_annotations:
        dis_handles = [Patch(color=v, label=k) for k, v in DISEASE_COLORS.items()]
        ax.legend(
            handles=dis_handles,
            title="disease relevance",
            loc="upper left",
            bbox_to_anchor=(1.15, 0.7),
            fontsize=8,
        )
        ax.add_artist(legend1)

    plt.title(
        "PXR target coupling to NR1I2 across cell types\n"
        "(Spearman ρ over metacells; diverging from hepatocyte baseline)",
        fontsize=10,
        pad=12,
    )
    plt.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor=COLOR_CREAM)
    return fig
