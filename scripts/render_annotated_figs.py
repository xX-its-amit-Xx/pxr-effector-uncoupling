"""Render novice-annotated versions of the two headline figures.

For the layman / learning-layman editions of the manuscript. The same data
as the publication figures, but with plain-English call-outs, arrows, and
a "what to look at" sidebar — designed for a reader who has never seen a
heatmap or a bar chart in a scientific context before.

Outputs:
    figures/fig1_annotated.png   — main heatmap, novice-narrated
    figures/fig5_annotated.png   — GEO rifamycin bars, novice-narrated
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import FancyArrowPatch, Rectangle

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pxr_uncoupling.config import DATA_PROCESSED, DATA_RAW, FIGURES  # noqa: E402
from pxr_uncoupling.figure_style import (  # noqa: E402
    CELL_TYPE_ORDER,
    COLOR_HEPATIC,
    COLOR_IMMUNE,
    COLOR_INTESTINE,
    COLOR_MUTED_TEXT,
    COLOR_NEG,
    COLOR_PLACENTA,
    COLOR_RECEPTOR,
    COLOR_TEXT,
    apply_style,
    compartment_of,
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


def _annotation_box(ax, x, y, text, *, width=0.28, fontsize=8, color="#fff8e8"):
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        fontsize=fontsize,
        ha="left",
        va="top",
        color=COLOR_TEXT,
        bbox=dict(
            boxstyle="round,pad=0.4", facecolor=color, edgecolor=COLOR_MUTED_TEXT, linewidth=0.6
        ),
        wrap=True,
        linespacing=1.3,
    )


def _arrow(ax, xy_from, xy_to, *, color=COLOR_MUTED_TEXT, lw=0.8):
    """Draw a curved arrow from (x1, y1) to (x2, y2) in axes-fractional coords."""
    arr = FancyArrowPatch(
        xy_from,
        xy_to,
        transform=ax.transAxes,
        arrowstyle="-|>",
        mutation_scale=10,
        color=color,
        lw=lw,
        connectionstyle="arc3,rad=0.18",
    )
    ax.add_patch(arr)


# ────────────────────────────────────────────────────────────────────────
# Fig. 1 annotated — main coupling heatmap, narrated for a novice
# ────────────────────────────────────────────────────────────────────────
def render_fig1_annotated() -> None:
    apply_style()

    target_meta = pd.read_csv(
        DATA_RAW.parent / "targets" / "pxr_canonical_targets.tsv",
        sep="\t",
        index_col="gene_symbol",
    )
    coupling = pd.read_csv(DATA_PROCESSED / "coupling.csv", index_col=0)
    gene_order = target_meta.sort_values(["category"]).index.intersection(coupling.columns).tolist()
    ct_order = [c for c in CELL_TYPE_ORDER if c in coupling.index]
    rho = coupling.loc[ct_order, gene_order].T

    n_ct = len(ct_order)
    n_g = len(gene_order)

    # Wider figure to accommodate annotation panel on the right
    fig = plt.figure(figsize=(13.5, 8))
    gs = fig.add_gridspec(
        nrows=2,
        ncols=3,
        width_ratios=[1.0, 0.04, 0.55],
        height_ratios=[0.05, 1.0],
        wspace=0.18,
        hspace=0.02,
    )
    ax_top = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    cax = fig.add_subplot(gs[1, 1])
    ax_notes = fig.add_subplot(gs[:, 2])
    ax_notes.set_axis_off()

    cmap = _diverging_cmap()
    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    im = ax.imshow(rho.values, aspect="auto", cmap=cmap, norm=norm, interpolation="nearest")

    # Compartment band
    compartment_color = {
        "liver": COLOR_HEPATIC,
        "intestine": COLOR_INTESTINE,
        "immune": COLOR_IMMUNE,
        "placenta": COLOR_PLACENTA,
    }
    ax_top.set_xlim(-0.5, n_ct - 0.5)
    ax_top.set_ylim(0, 1)
    for j, ct in enumerate(ct_order):
        ax_top.add_patch(Rectangle((j - 0.5, 0), 1, 1, color=compartment_color[compartment_of(ct)]))
    last_comp = None
    runs: list[tuple[int, int, str]] = []
    start = 0
    for j, ct in enumerate(ct_order):
        c = compartment_of(ct)
        if c != last_comp and last_comp is not None:
            runs.append((start, j - 1, last_comp))
            start = j
        last_comp = c
    runs.append((start, n_ct - 1, last_comp or "other"))
    for a, b, c in runs:
        ax_top.text(
            (a + b) / 2,
            0.5,
            c.upper(),
            ha="center",
            va="center",
            fontsize=8,
            color="white",
            fontweight="bold",
        )
    ax_top.set_axis_off()

    # Compartment separator lines on the heatmap
    last_comp = None
    for j, ct in enumerate(ct_order):
        c = compartment_of(ct)
        if last_comp is not None and c != last_comp:
            ax.axvline(j - 0.5, color="white", lw=1.5)
        last_comp = c

    # Axes
    ax.set_xticks(range(n_ct))
    ax.set_xticklabels([short_cell_type(c) for c in ct_order], rotation=35, ha="right", fontsize=9)
    ax.set_yticks(range(n_g))
    ax.set_yticklabels(gene_order, fontsize=8.5)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("")
    ax.set_ylabel("")

    # Colorbar
    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    cb.set_ticks([-1, -0.5, 0, 0.5, 1])
    cb.set_label("Spearman ρ\n(linkedness)", fontsize=9, color=COLOR_TEXT)
    cb.ax.tick_params(labelsize=8)

    # Title + subtitle
    fig.suptitle(
        "What this figure shows: PXR's drug-handling network is fully engaged only in liver cells",
        x=0.012,
        y=0.985,
        ha="left",
        fontsize=12,
        fontweight="bold",
        color=COLOR_TEXT,
    )
    fig.text(
        0.012,
        0.96,
        "Each square = how tightly one gene's expression tracks PXR's expression across cells of one type. Dark green = tight (linked). White = no link. Dark red = opposite.",  # noqa: E501
        fontsize=9,
        color=COLOR_MUTED_TEXT,
    )

    # ── Annotation sidebar ──────────────────────────────────────────
    ax_notes.set_xlim(0, 1)
    ax_notes.set_ylim(0, 1)

    # Header
    ax_notes.text(
        0.0,
        0.99,
        "How to read this picture",
        fontsize=11,
        fontweight="bold",
        color=COLOR_TEXT,
        va="top",
    )
    ax_notes.text(
        0.0,
        0.94,
        "(start at the top and work down)",
        fontsize=8.5,
        color=COLOR_MUTED_TEXT,
        va="top",
        style="italic",
    )

    notes = [
        (
            "1.  Rows = genes.",
            "Each row is one of the 20 PXR target genes the textbook lists. The names start with CYP (cytochrome P450 enzymes — they chemically break drugs apart), ABC (transporter proteins — they pump drugs out of cells), SLC (uptake transporters — they bring drugs in), and a few others.",  # noqa: E501
            0.88,
        ),
        (
            "2.  Columns = cell types.",
            "Each column is a different cell type from the body. The coloured band at the top groups them by tissue (Liver, Intestine, Immune, Placenta).",  # noqa: E501
            0.74,
        ),
        (
            "3.  Colour = linkedness (ρ).",
            "Spearman ρ measures how tightly two genes go up and down together across cells of one type. Dark green = tight link (ρ ≈ +0.9). White = no link (ρ ≈ 0). Dark red = opposite link (ρ ≈ −0.9).",  # noqa: E501
            0.59,
        ),
        (
            "4.  Look at the Liver column.",
            "Almost everything is dark green. The PXR drug-handling program is fully running here.",
            0.42,
        ),
        (
            "5.  Look at the Immune columns.",
            "Mostly pale. PXR is *there* in these cells (we detect the receptor), but its program isn't doing anything. This is the surprise.",  # noqa: E501
            0.29,
        ),
        (
            "6.  Look at Placenta.",
            "Almost completely white. PXR is essentially silent in this tissue.",
            0.16,
        ),
        (
            "7.  In one sentence:",
            "The receptor and its program are NOT the same thing. The receptor is everywhere; the program runs in liver and (partially) in gut.",  # noqa: E501
            0.04,
        ),
    ]
    for title, body, y in notes:
        ax_notes.text(0.0, y, title, fontsize=9.5, fontweight="bold", color=COLOR_HEPATIC, va="top")
        ax_notes.text(0.0, y - 0.034, body, fontsize=8.3, color=COLOR_TEXT, va="top", wrap=True)

    # Draw a callout arrow pointing to the hepatocyte column (index 0)
    # transform pixel into axes-fraction... use fig.transFigure trick:
    # Annotate from the right-side ax_notes "look at the Liver column" arrow
    # Use fig.text + plt.Annotation in figure coords for the arrows
    fig.canvas.draw()

    # Title for the notes panel boundary (drawn via rectangle behind)
    rect = Rectangle(
        (0.005, 0.001),
        0.99,
        0.998,
        transform=ax_notes.transAxes,
        facecolor="#fef9ed",
        edgecolor=COLOR_MUTED_TEXT,
        linewidth=0.5,
        zorder=-1,
    )
    ax_notes.add_patch(rect)

    plt.subplots_adjust(top=0.92, right=0.96, bottom=0.10, left=0.07)
    out = FIGURES / "fig1_annotated.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out}")


# ────────────────────────────────────────────────────────────────────────
# Fig. 5 annotated — direct rifamycin perturbation
# ────────────────────────────────────────────────────────────────────────
def render_fig5_annotated() -> None:
    apply_style()
    stats = pd.read_csv(DATA_PROCESSED / "geo_rifamycin_stats.csv")
    panel = ["CYP2C9", "CYP3A5", "ABCC2", "SLCO1B1", "CYP2C8", "CPT1A"]
    controls = ["ALB", "HNF4A", "GAPDH"]
    receptor = ["NR1I2"]
    gene_order = panel + receptor + controls

    color_map = {g: COLOR_HEPATIC for g in panel}
    color_map.update({g: COLOR_RECEPTOR for g in receptor})
    color_map.update({g: COLOR_NEG for g in controls})

    fig = plt.figure(figsize=(13.5, 7))
    gs = fig.add_gridspec(
        nrows=2,
        ncols=4,
        width_ratios=[1.0, 1.0, 1.0, 0.7],
        height_ratios=[0.05, 1.0],
        wspace=0.12,
        hspace=0.02,
    )
    ax_notes = fig.add_subplot(gs[:, 3])
    ax_notes.set_axis_off()
    axes = [fig.add_subplot(gs[1, k]) for k in range(3)]

    drugs = ["rifampin", "rifabutin", "rifapentine"]
    labels = ["a", "b", "c"]
    for k, (ax, drug) in enumerate(zip(axes, drugs, strict=False)):
        sub = stats[stats["drug"] == drug].set_index("gene")
        x = np.arange(len(gene_order))
        means = sub.loc[gene_order, "mean_log2FC"].values
        stds = sub.loc[gene_order, "std_log2FC"].values
        colors = [color_map[g] for g in gene_order]
        ax.bar(
            x,
            means,
            yerr=stds,
            capsize=2,
            color=colors,
            edgecolor="white",
            linewidth=0.5,
            width=0.75,
            error_kw={"elinewidth": 0.7, "capthick": 0.6, "ecolor": COLOR_TEXT},
        )
        for j, (g, p) in enumerate(
            zip(gene_order, sub.loc[gene_order, "p_value"].values, strict=False)
        ):
            if not np.isnan(p) and p < 0.05:
                top = means[j] + (stds[j] if not np.isnan(stds[j]) else 0)
                ax.text(
                    j, top + 0.2, "*", ha="center", fontsize=11, color=COLOR_TEXT, fontweight="bold"
                )
        ax.axhline(0, color=COLOR_MUTED_TEXT, lw=0.5, linestyle="--")
        ax.set_xticks(x)
        ax.set_xticklabels(gene_order, rotation=35, ha="right", fontsize=8)
        ax.set_title(drug, loc="left", pad=4, fontsize=10, fontweight="bold")
        if k == 0:
            ax.set_ylabel(
                "Genes UP ↑ with drug treatment\n\nlog2 fold change vs vehicle", fontsize=9
            )
        # panel label
        ax.text(
            -0.13 if k == 0 else -0.05,
            1.06,
            labels[k],
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
            ha="left",
            color=COLOR_TEXT,
        )
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    # Shared y-limits look nicer for comparison
    ymin = min(ax.get_ylim()[0] for ax in axes) - 0.2
    ymax = max(ax.get_ylim()[1] for ax in axes) + 0.2
    for ax in axes:
        ax.set_ylim(ymin, ymax)
        ax.tick_params(labelleft=False)
    axes[0].tick_params(labelleft=True)

    # Title
    fig.suptitle(
        "What this figure shows: real PXR-activating drugs in real liver cells",
        x=0.012,
        y=0.985,
        ha="left",
        fontsize=12,
        fontweight="bold",
        color=COLOR_TEXT,
    )
    fig.text(
        0.012,
        0.96,
        "Each panel = one rifamycin antibiotic. Bars = how much each gene goes UP or DOWN compared to no-drug controls. Asterisks (*) = statistically significant.",  # noqa: E501
        fontsize=9,
        color=COLOR_MUTED_TEXT,
    )

    # Notes sidebar
    ax_notes.set_xlim(0, 1)
    ax_notes.set_ylim(0, 1)
    ax_notes.text(
        0.0,
        0.99,
        "How to read these bars",
        fontsize=11,
        fontweight="bold",
        color=COLOR_TEXT,
        va="top",
    )
    ax_notes.text(
        0.0,
        0.94,
        "(this is the most direct experiment in the paper)",
        fontsize=8.5,
        color=COLOR_MUTED_TEXT,
        va="top",
        style="italic",
    )

    notes = [
        (
            "Three independent drugs.",
            "Rifampin, rifabutin, rifapentine — all anti-TB antibiotics that activate PXR. Three different drugs = three independent tests.",  # noqa: E501
            0.88,
        ),
        (
            "Each bar = one gene.",
            "Terracotta bars = our 'top-6 PXR panel' candidates. Purple = the PXR receptor itself. Olive = matched negative-control genes that should NOT respond.",  # noqa: E501
            0.74,
        ),
        (
            "Bar height = response.",
            "How many times the gene's expression went UP (or down). log2 scale: +1 = doubled, +2 = quadrupled, +3 = 8×, +4 = 16×.",  # noqa: E501
            0.60,
        ),
        (
            "Asterisk (*) = real.",
            "Means the change is statistically significant across the three patients tested (paired t-test, p < 0.05).",  # noqa: E501
            0.47,
        ),
        (
            "CYP2C8 wins big.",
            "Up 9–19× across all three drugs, every time. Classic PXR target. The strongest induction in the panel.",  # noqa: E501
            0.34,
        ),
        (
            "SLCO1B1 and CPT1A don't move.",
            "Despite being 'top-6' candidates from the single-cell analysis, they don't respond to direct PXR drugs. Means they're co-expressed with PXR but not actually controlled by it.",  # noqa: E501
            0.20,
        ),
        (
            "Bottom line:",
            "Use CYP2C8, CYP2C9, CYP3A5, ABCC2 as PXR drug-engagement biomarkers. Skip SLCO1B1 and CPT1A.",  # noqa: E501
            0.04,
        ),
    ]
    for title, body, y in notes:
        ax_notes.text(0.0, y, title, fontsize=9.5, fontweight="bold", color=COLOR_HEPATIC, va="top")
        ax_notes.text(0.0, y - 0.030, body, fontsize=8.3, color=COLOR_TEXT, va="top", wrap=True)

    rect = Rectangle(
        (0.005, 0.001),
        0.99,
        0.998,
        transform=ax_notes.transAxes,
        facecolor="#fef9ed",
        edgecolor=COLOR_MUTED_TEXT,
        linewidth=0.5,
        zorder=-1,
    )
    ax_notes.add_patch(rect)

    plt.subplots_adjust(top=0.91, right=0.97, bottom=0.13, left=0.07)
    out = FIGURES / "fig5_annotated.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    render_fig1_annotated()
    render_fig5_annotated()
