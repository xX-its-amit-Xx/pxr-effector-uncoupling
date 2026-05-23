"""Main coupling heatmap (Fig. 1) — Nature-tier rendering."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Patch

from .config import FIGURES
from .figure_style import (
    CELL_TYPE_ORDER,
    COLOR_HEPATIC,
    COLOR_INTESTINE,
    COLOR_MUTED_TEXT,
    COLOR_NEG,
    COLOR_TEXT,
    COMPARTMENT_COLOR,
    DOUBLE_COL,
    apply_style,
    compartment_of,
    short_cell_type,
)


def _diverging_cmap() -> LinearSegmentedColormap:
    """Warm-to-cool diverging map (terracotta ↔ teal) for ρ ∈ [-1, 1]."""
    return LinearSegmentedColormap.from_list(
        "pxr_div",
        [
            (0.00, "#8a3220"),  # deep terracotta (ρ ≈ -1)
            (0.25, "#c0533a"),
            (0.50, "#ffffff"),  # white at zero
            (0.75, "#3d7a78"),
            (1.00, "#1d4d4c"),  # deep teal (ρ ≈ +1)
        ],
        N=256,
    )


def decoupling_heatmap(
    coupling_df: pd.DataFrame,
    target_meta: pd.DataFrame,
    cell_type_tissue_map: dict[str, str],  # noqa: ARG001 -- kept for back-compat
    disease_annotations: dict[str, str] | None = None,  # noqa: ARG001
    output_path: Path | None = None,
    dpi: int = 300,
) -> plt.Figure:
    """Main coupling heatmap with tissue-compartment grouping (Fig. 1)."""
    apply_style()
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "final_heatmap.png"

    gene_order = (
        target_meta.sort_values(["category"]).index.intersection(coupling_df.columns).tolist()
    )
    ct_order = [c for c in CELL_TYPE_ORDER if c in coupling_df.index]
    rho = coupling_df.loc[ct_order, gene_order].T  # genes × cell_types

    n_ct = len(ct_order)
    n_g = len(gene_order)
    fig_w = min(DOUBLE_COL, 0.42 * n_ct + 3.4)
    fig_h = 0.24 * n_g + 1.8
    fig = plt.figure(figsize=(fig_w, fig_h))
    # main heatmap axes leave room top for compartment band and right for cbar
    gs = fig.add_gridspec(
        nrows=2,
        ncols=2,
        width_ratios=[1.0, 0.04],
        height_ratios=[0.04, 1.0],
        wspace=0.04,
        hspace=0.02,
    )
    ax_top = fig.add_subplot(gs[0, 0])  # compartment band
    ax = fig.add_subplot(gs[1, 0])
    cax = fig.add_subplot(gs[1, 1])

    cmap = _diverging_cmap()
    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)

    im = ax.imshow(
        rho.values,
        aspect="auto",
        cmap=cmap,
        norm=norm,
        interpolation="nearest",
    )

    # Compartment band (top)
    ax_top.set_xlim(-0.5, n_ct - 0.5)
    ax_top.set_ylim(0, 1)
    for j, ct in enumerate(ct_order):
        comp = compartment_of(ct)
        color = COMPARTMENT_COLOR.get(comp, "#bbb")
        ax_top.add_patch(plt.Rectangle((j - 0.5, 0), 1, 1, color=color))
    # Compartment label centred over its run of cell types
    last_comp = None
    run_start = 0
    runs: list[tuple[int, int, str]] = []
    for j, ct in enumerate(ct_order):
        comp = compartment_of(ct)
        if comp != last_comp and last_comp is not None:
            runs.append((run_start, j - 1, last_comp))
            run_start = j
        last_comp = comp
    runs.append((run_start, n_ct - 1, last_comp or "other"))
    for a, b, c in runs:
        ax_top.text(
            (a + b) / 2,
            0.45,
            c.capitalize(),
            ha="center",
            va="center",
            fontsize=6.5,
            color="white",
            fontweight="bold",
        )
    ax_top.set_axis_off()

    # Gene-row regulation: colour the y-axis tick labels themselves
    reg_colors: dict[str, str] = {}
    if "regulation" in target_meta.columns:
        for gene in gene_order:
            reg = target_meta.loc[gene, "regulation"] if gene in target_meta.index else None
            reg_colors[gene] = COLOR_HEPATIC if reg == "induced" else COLOR_NEG

    ax.set_xticks(range(n_ct))
    ax.set_xticklabels(
        [short_cell_type(c) for c in ct_order],
        rotation=35,
        ha="right",
        fontsize=6.5,
    )
    ax.set_yticks(range(n_g))
    ax.set_yticklabels(gene_order, fontsize=6.5)
    for tick_label, gene in zip(ax.get_yticklabels(), gene_order, strict=False):
        if gene in reg_colors:
            tick_label.set_color(reg_colors[gene])
            tick_label.set_fontweight("medium")
    ax.tick_params(axis="both", length=0)
    ax.set_xlabel("")
    ax.set_ylabel("")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Compartment separator lines on the heatmap itself
    last_comp = None
    for j, ct in enumerate(ct_order):
        comp = compartment_of(ct)
        if last_comp is not None and comp != last_comp:
            ax.axvline(j - 0.5, color="white", lw=1.2)
        last_comp = comp

    # Colorbar
    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    cb.set_label("Spearman ρ (NR1I2 ~ target)", fontsize=7, color=COLOR_TEXT, labelpad=4)
    cb.ax.tick_params(labelsize=6, length=2.5, color=COLOR_TEXT)
    cb.set_ticks([-1, -0.5, 0, 0.5, 1])

    # Title block (figure-level)
    fig.suptitle(
        "PXR target coupling to NR1I2 across cell types",
        x=0.012,
        y=0.97,
        ha="left",
        fontsize=9,
        fontweight="bold",
        color=COLOR_TEXT,
    )
    fig.text(
        0.012,
        0.95,
        "Spearman ρ between NR1I2 and each canonical target, computed over metacells; n = 446,672 cells across 10 cell types.",  # noqa: E501
        fontsize=6.5,
        color=COLOR_MUTED_TEXT,
        ha="left",
    )

    # Regulation legend (under the colorbar)
    reg_handles = [
        Patch(facecolor=COLOR_HEPATIC, label="induced"),
        Patch(facecolor=COLOR_NEG, label="repressed"),
    ]
    leg = fig.legend(
        handles=reg_handles,
        title="Regulation",
        loc="lower right",
        bbox_to_anchor=(0.99, 0.02),
        fontsize=6.5,
        title_fontsize=7,
        handlelength=1.0,
        handleheight=0.7,
    )
    leg.get_title().set_fontweight("bold")
    leg.get_title().set_color(COLOR_TEXT)

    # silence unused import linters
    _ = COLOR_INTESTINE
    plt.subplots_adjust(top=0.92, right=0.92, bottom=0.16, left=0.18)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return fig
