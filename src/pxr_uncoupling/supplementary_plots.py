"""Supplementary figures — Nature-tier rendering."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

from .config import FIGURES
from .figure_style import (
    CELL_TYPE_ORDER,
    COLOR_HEPATIC,
    COLOR_IMMUNE,
    COLOR_NEG,
    COLOR_TEXT,
    COLOR_ZERO_LINE,
    COMPARTMENT_COLOR,
    DOUBLE_COL,
    ONE_AND_A_HALF_COL,
    SINGLE_COL,
    add_panel_label,
    add_subtitle,
    apply_style,
    compartment_of,
    polish_axes,
    short_cell_type,
)


def _diverging_cmap() -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(
        "pxr_div",
        [
            (0.00, "#8a3220"),
            (0.25, "#c0533a"),
            (0.50, "#ffffff"),
            (0.75, "#3d7a78"),
            (1.00, "#1d4d4c"),
        ],
        N=256,
    )


def heatmap_with_significance(
    coupling: pd.DataFrame,
    qvalues: pd.DataFrame,
    output_path: Path | None = None,
    q_threshold: float = 0.05,
    dpi: int = 300,
) -> plt.Figure:
    """Heatmap of ρ with FDR significance stars."""
    apply_style()
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_heatmap_significance.png"

    common_ct = [c for c in CELL_TYPE_ORDER if c in coupling.index and c in qvalues.index]
    common_g = coupling.columns.intersection(qvalues.columns)
    rho = coupling.loc[common_ct, common_g].T
    q = qvalues.loc[common_ct, common_g].T

    n_ct = len(common_ct)
    n_g = len(common_g)
    fig_w = min(DOUBLE_COL, 0.42 * n_ct + 3.0)
    fig_h = 0.22 * n_g + 1.4
    fig = plt.figure(figsize=(fig_w, fig_h))
    gs = fig.add_gridspec(
        nrows=2,
        ncols=2,
        width_ratios=[1.0, 0.04],
        height_ratios=[0.04, 1.0],
        wspace=0.04,
        hspace=0.02,
    )
    ax_top = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    cax = fig.add_subplot(gs[1, 1])

    cmap = _diverging_cmap()
    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    im = ax.imshow(rho.values, aspect="auto", cmap=cmap, norm=norm, interpolation="nearest")

    # compartment band
    ax_top.set_xlim(-0.5, n_ct - 0.5)
    ax_top.set_ylim(0, 1)
    for j, ct in enumerate(common_ct):
        comp = compartment_of(ct)
        ax_top.add_patch(
            plt.Rectangle((j - 0.5, 0), 1, 1, color=COMPARTMENT_COLOR.get(comp, "#bbb"))
        )
    ax_top.set_axis_off()

    # significance markers
    for i in range(n_g):
        for j in range(n_ct):
            qv = q.iat[i, j]
            if pd.isna(qv):
                continue
            mark = "**" if qv < 0.01 else ("*" if qv < q_threshold else "")
            if not mark:
                continue
            v = rho.iat[i, j]
            text_color = "white" if not np.isnan(v) and abs(v) > 0.55 else COLOR_TEXT
            ax.text(
                j,
                i,
                mark,
                ha="center",
                va="center",
                fontsize=7,
                color=text_color,
                fontweight="bold",
            )

    last_comp = None
    for j, ct in enumerate(common_ct):
        comp = compartment_of(ct)
        if last_comp is not None and comp != last_comp:
            ax.axvline(j - 0.5, color="white", lw=1.2)
        last_comp = comp

    ax.set_xticks(range(n_ct))
    ax.set_xticklabels(
        [short_cell_type(c) for c in common_ct], rotation=35, ha="right", fontsize=6.5
    )
    ax.set_yticks(range(n_g))
    ax.set_yticklabels(list(rho.index), fontsize=6.5)
    ax.tick_params(length=0)
    ax.set_xlabel("")
    ax.set_ylabel("")
    for s in ax.spines.values():
        s.set_visible(False)

    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    cb.set_label("Spearman ρ", fontsize=7, color=COLOR_TEXT, labelpad=4)
    cb.ax.tick_params(labelsize=6, length=2.5)
    cb.set_ticks([-1, -0.5, 0, 0.5, 1])

    fig.suptitle(
        "Coupling ρ with FDR-significance overlay",
        x=0.012,
        y=0.97,
        ha="left",
        fontsize=9,
        fontweight="bold",
        color=COLOR_TEXT,
    )
    add_subtitle(
        fig,
        f"`*` q < {q_threshold},  `**` q < 0.01 ; BH-FDR over the 10 × 20 (cell type × gene) family.",  # noqa: E501
        y=0.93,
    )

    plt.subplots_adjust(top=0.92, right=0.92, bottom=0.16, left=0.18)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    # consume unused names so linters stay quiet
    _ = (COLOR_IMMUNE, COLOR_HEPATIC)
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
    """Forest plot of hepatocyte ρ with 95% CIs for the top decoupled genes."""
    apply_style()
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_forest_hepatocyte.png"

    ds = coupling.loc[reference_cell_type] - coupling.drop(index=reference_cell_type)
    ranking = ds.mean(axis=0).sort_values(ascending=False).head(top_n).index.tolist()
    rho = coupling.loc[reference_cell_type, ranking]
    lo = ci_lower.loc[reference_cell_type, ranking]
    hi = ci_upper.loc[reference_cell_type, ranking]
    q = qvalues.loc[reference_cell_type, ranking] if reference_cell_type in qvalues.index else None

    fig, ax = plt.subplots(figsize=(SINGLE_COL + 1.2, max(2.4, 0.28 * top_n + 0.8)))
    polish_axes(ax)
    y = np.arange(len(ranking))
    err_lo = (rho - lo).clip(lower=0).values
    err_hi = (hi - rho).clip(lower=0).values

    ax.errorbar(
        rho.values,
        y,
        xerr=[err_lo, err_hi],
        fmt="o",
        color=COLOR_HEPATIC,
        ecolor=COLOR_HEPATIC,
        elinewidth=1.0,
        capsize=2.5,
        capthick=0.7,
        markersize=4.5,
        markeredgecolor="white",
        markeredgewidth=0.7,
    )
    ax.axvline(0, color=COLOR_ZERO_LINE, ls="--", lw=0.5)
    ax.set_yticks(y)
    labels = list(ranking)
    if q is not None:
        labels = [
            f"{g}  {'***' if q[g] < 0.001 else '**' if q[g] < 0.01 else '*' if q[g] < 0.05 else ''}"
            for g in ranking
        ]
    ax.set_yticklabels(labels, fontsize=6.5)
    ax.invert_yaxis()
    ax.set_xlabel(f"Spearman ρ in {reference_cell_type}  (95% bootstrap CI)")
    ax.set_xlim(-0.2, 1.05)
    ax.set_title(f"Top {top_n} hepatocyte-coupled PXR targets", loc="left", pad=4)
    add_subtitle(
        fig,
        "Bars: 95% percentile bootstrap CI over metacell rows. `*` q<0.05, `**` q<0.01, `***` q<0.001.",  # noqa: E501
        x=0.02,
        y=0.94,
    )

    plt.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return fig


def sensitivity_plot(
    agreement: pd.DataFrame,
    output_path: Path | None = None,
    dpi: int = 300,
) -> plt.Figure:
    """Decoupling-rank agreement + top-5 Jaccard across the parameter sweep."""
    apply_style()
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_sensitivity.png"

    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_COL, 2.6))
    for ax in axes:
        polish_axes(ax)

    palette = {15: COLOR_HEPATIC, 30: COLOR_NEG, 60: COLOR_IMMUNE}
    seeds_observed = sorted(agreement["seed"].unique().tolist())
    for cpm, grp in agreement.groupby("cells_per_metacell"):
        c = palette.get(cpm, "#555")
        jit = 6 * (cpm - 30) / 30
        axes[0].scatter(
            grp["seed"] + jit,
            grp["spearman_of_decoupling"],
            color=c,
            label=str(cpm),
            s=28,
            alpha=0.95,
            edgecolors="white",
            linewidth=0.6,
        )
        axes[1].scatter(
            grp["seed"] + jit,
            grp["jaccard_top5"],
            color=c,
            label=str(cpm),
            s=28,
            alpha=0.95,
            edgecolors="white",
            linewidth=0.6,
        )

    for ax in axes:
        ax.axhline(1.0, ls="--", lw=0.5, color=COLOR_ZERO_LINE)
        ax.set_xticks(seeds_observed)
        ax.set_xlabel("Random seed")

    axes[0].set_ylim(0.85, 1.02)
    axes[0].set_ylabel("Spearman ρ of decoupling rankings\nvs reference parameters")
    axes[0].set_title("Rank stability across parameter sweep", loc="left", pad=4)
    add_panel_label(axes[0], "a", dx=-0.15)

    axes[1].set_ylim(0.4, 1.08)
    axes[1].set_ylabel("Jaccard overlap of top-5 hep-selective set")
    axes[1].set_title("Top-5 overlap vs reference", loc="left", pad=4)
    add_panel_label(axes[1], "b", dx=-0.15)

    leg = axes[1].legend(
        title="cells / metacell",
        fontsize=6,
        title_fontsize=6.5,
        loc="lower right",
        handlelength=0.8,
    )
    leg.get_title().set_fontweight("bold")

    plt.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return fig


def subsample_stability_plot(
    summary: pd.DataFrame,
    output_path: Path | None = None,
    dpi: int = 300,
) -> plt.Figure:
    """Per-cell-type ρ-std under 80% cell-level resampling."""
    apply_style()
    if output_path is None:
        FIGURES.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES / "supp_subsample_stability.png"

    cts = summary["cell_type"].unique().tolist()
    order = [c for c in CELL_TYPE_ORDER if c in cts]
    palette = {c: COMPARTMENT_COLOR.get(compartment_of(c), COLOR_HEPATIC) for c in order}

    fig, ax = plt.subplots(figsize=(ONE_AND_A_HALF_COL + 2.2, 3.2))
    polish_axes(ax)
    sns.boxplot(
        data=summary,
        x="cell_type",
        y="std",
        order=order,
        ax=ax,
        palette=palette,
        linewidth=0.6,
        fliersize=1.8,
        hue="cell_type",
        legend=False,
        width=0.65,
    )
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([short_cell_type(c) for c in order], rotation=25, ha="right", fontsize=6.5)
    ax.set_xlabel("")
    ax.set_ylabel("Std of ρ across 20 × 80% subsamples")
    ax.set_title("Coupling stability under cell-level subsampling", loc="left", pad=4)
    add_subtitle(
        fig,
        "Each box: distribution of per-gene ρ standard deviation across 20 independent 80%-subsamples within a cell type.",  # noqa: E501
        x=0.02,
        y=0.93,
    )

    plt.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return fig
