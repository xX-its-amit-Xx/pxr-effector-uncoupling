"""Publication-grade figure styling — Nature/Cell tier defaults.

Design choices (Nature house style):
  - Pure white background (#ffffff). No decorative cream.
  - Helvetica / Arial throughout. Body 7 pt, ticks 6.5 pt, titles 8 pt,
    panel labels 9 pt bold.
  - Lower-case bold panel labels ("a", "b", "c") in the top-left.
  - Top + right spines hidden; left + bottom kept thin (0.6 pt).
  - Restrained, colourblind-friendly palette.
  - No gridlines unless data-bearing (Tufte minimalism).
  - Figure sizes in inches that align with single-column (3.5") and
    double-column (7.2") Nature figure widths.

All plotting modules call ``apply_style()`` once at the top of their main
function so that subsequent plt calls inherit the style.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

# ── Palette ────────────────────────────────────────────────────────────────
# Project accents kept as data colours; background is white.
COLOR_HEPATIC = "#c0533a"  # deep terracotta — hepatic / PXR-positive
COLOR_INTESTINE = "#d89a4e"  # warm ochre — intestinal tissues
COLOR_IMMUNE = "#5a7592"  # slate blue — immune cells
COLOR_PLACENTA = "#7a5b8a"  # muted plum — placental
COLOR_NEG = "#7d8c6a"  # olive — negative control
COLOR_RECEPTOR = "#5a4a82"  # indigo — receptor highlight

COLOR_BG = "#ffffff"  # figure background
COLOR_AXES_BG = "#ffffff"  # axes background
COLOR_TEXT = "#1a1a1a"  # primary text
COLOR_MUTED_TEXT = "#525252"  # subtitle / caption text
COLOR_GRID = "#e0e0e0"  # subtle grid
COLOR_ZERO_LINE = "#9a9a9a"  # reference / zero line

# Legacy aliases for files that still import these names.
COLOR_ACCENT = COLOR_HEPATIC
COLOR_SAGE = COLOR_NEG
COLOR_CREAM = COLOR_BG  # was cream; now white — same role
COLOR_PURPLE = COLOR_RECEPTOR


# ── Cell-type labelling shortcuts ──────────────────────────────────────────
CELL_TYPE_SHORT: dict[str, str] = {
    "hepatocyte": "Hepatocyte",
    "enterocyte of epithelium of small intestine": "SI enterocyte",
    "enterocyte of epithelium of large intestine": "LI enterocyte",
    "intestinal crypt stem cell": "Crypt stem",
    "macrophage": "Macrophage",
    "monocyte": "Monocyte",
    "natural killer cell": "NK cell",
    "CD4-positive, alpha-beta T cell": "CD4+ T",
    "CD8-positive, alpha-beta T cell": "CD8+ T",
    "extravillous trophoblast": "EVT",
}

CELL_TYPE_ORDER = [
    "hepatocyte",
    "enterocyte of epithelium of small intestine",
    "intestinal crypt stem cell",
    "enterocyte of epithelium of large intestine",
    "macrophage",
    "monocyte",
    "natural killer cell",
    "CD4-positive, alpha-beta T cell",
    "CD8-positive, alpha-beta T cell",
    "extravillous trophoblast",
]

CELL_TYPE_COMPARTMENT: dict[str, str] = {
    "hepatocyte": "liver",
    "enterocyte of epithelium of small intestine": "intestine",
    "enterocyte of epithelium of large intestine": "intestine",
    "intestinal crypt stem cell": "intestine",
    "macrophage": "immune",
    "monocyte": "immune",
    "natural killer cell": "immune",
    "CD4-positive, alpha-beta T cell": "immune",
    "CD8-positive, alpha-beta T cell": "immune",
    "extravillous trophoblast": "placenta",
}

COMPARTMENT_COLOR: dict[str, str] = {
    "liver": COLOR_HEPATIC,
    "intestine": COLOR_INTESTINE,
    "immune": COLOR_IMMUNE,
    "placenta": COLOR_PLACENTA,
}

# Standard Nature figure widths (inches)
SINGLE_COL = 3.5
ONE_AND_A_HALF_COL = 5.0
DOUBLE_COL = 7.2


def apply_style() -> None:
    """Apply Nature-tier matplotlib defaults globally."""
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Helvetica",
                "Helvetica Neue",
                "Arial",
                "Segoe UI",
                "DejaVu Sans",
            ],
            "font.size": 7,
            "axes.titlesize": 8,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 6,
            "axes.titley": None,
            "axes.labelsize": 7.5,
            "axes.labelweight": "regular",
            "axes.labelcolor": COLOR_TEXT,
            "axes.labelpad": 4,
            "axes.edgecolor": COLOR_TEXT,
            "axes.linewidth": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.facecolor": COLOR_AXES_BG,
            "axes.grid": False,
            "xtick.color": COLOR_TEXT,
            "ytick.color": COLOR_TEXT,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.major.pad": 2.5,
            "ytick.major.pad": 2.5,
            "legend.frameon": False,
            "legend.fontsize": 6.5,
            "legend.title_fontsize": 7,
            "legend.handlelength": 1.4,
            "legend.handleheight": 0.8,
            "legend.borderpad": 0.3,
            "legend.columnspacing": 0.9,
            "figure.facecolor": COLOR_BG,
            "figure.edgecolor": "none",
            "figure.dpi": 150,
            "savefig.facecolor": COLOR_BG,
            "savefig.edgecolor": "none",
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            "savefig.dpi": 300,
            "image.cmap": "RdBu_r",
            "pdf.fonttype": 42,  # embed TrueType for Illustrator-editable text
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def polish_axes(ax: plt.Axes, *, hide_top: bool = True, hide_right: bool = True) -> None:
    ax.set_facecolor(COLOR_AXES_BG)
    if hide_top:
        ax.spines["top"].set_visible(False)
    if hide_right:
        ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        if ax.spines[s].get_visible():
            ax.spines[s].set_linewidth(0.6)
            ax.spines[s].set_color(COLOR_TEXT)
    ax.tick_params(colors=COLOR_TEXT, length=2.5, width=0.6, pad=2.5)


def add_panel_label(ax: plt.Axes, label: str, *, dx: float = -0.10, dy: float = 1.04) -> None:
    """Lower-case bold panel label (Nature convention)."""
    ax.text(
        dx,
        dy,
        label,
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        va="top",
        ha="left",
        color=COLOR_TEXT,
    )


def add_subtitle(fig: plt.Figure, text: str, *, x: float = 0.012, y: float = 0.95) -> None:
    """Caption-like subtitle below a figure-level title."""
    fig.text(x, y, text, fontsize=7.5, color=COLOR_MUTED_TEXT, ha="left")


def short_cell_type(name: str) -> str:
    return CELL_TYPE_SHORT.get(name, name)


def compartment_of(name: str) -> str:
    return CELL_TYPE_COMPARTMENT.get(name, "other")
