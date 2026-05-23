"""Per-dataset reproducibility check for hepatocyte coupling.

Inputs : data/raw/nr1i2_atlas.h5ad
Outputs: data/processed/per_dataset_hepatocyte.csv
         data/processed/per_dataset_summary.json
         figures/supp_per_dataset_hepatocyte.png
"""

import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import anndata as ad  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import TwoSlopeNorm  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    DATA_PROCESSED,
    DATA_RAW,
    FIGURES,
    NR1I2_SYMBOL,
)
from pxr_uncoupling.figure_style import (  # noqa: E402
    COLOR_MUTED_TEXT,
    COLOR_TEXT,
    DOUBLE_COL,
    add_subtitle,
    apply_style,
)
from pxr_uncoupling.reproducibility import (  # noqa: E402
    cross_dataset_agreement,
    per_dataset_coupling,
)


def main() -> None:
    import pandas as pd

    adata = ad.read_h5ad(DATA_RAW / "nr1i2_atlas.h5ad")
    pxr_targets = pd.read_csv(DATA_RAW.parent / "targets" / "pxr_canonical_targets.tsv", sep="\t")[
        "gene_symbol"
    ].tolist()
    target_genes = [g for g in pxr_targets if g in adata.var_names and g != NR1I2_SYMBOL]

    # Per-dataset coupling: use a smaller metacell size + more permissive
    # min_metacells so smaller datasets still produce a row. We accept lower
    # per-dataset power as the tradeoff for replication breadth.
    per_ds = per_dataset_coupling(
        adata,
        target_genes=target_genes,
        cell_type="hepatocyte",
        min_cells_per_dataset=300,
        cells_per_metacell=15,
        min_metacells=10,
    )
    if per_ds.empty:
        log.warning("No datasets passed the threshold — abort")
        return

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = DATA_PROCESSED / "per_dataset_hepatocyte.csv"
    per_ds.to_csv(out)
    log.info("Wrote %s (%d datasets × %d genes)", out, per_ds.shape[0], per_ds.shape[1])

    summary = cross_dataset_agreement(per_ds)
    sum_out = DATA_PROCESSED / "per_dataset_summary.json"
    with sum_out.open("w") as fh:
        json.dump(summary, fh, indent=2)
    log.info("Cross-dataset agreement summary: %s", summary)

    # Heatmap: datasets × genes ──────────────────────────────────────────────
    apply_style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list(
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
    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)

    fig_w = min(DOUBLE_COL, 0.28 * per_ds.shape[1] + 2.5)
    fig_h = 0.32 * per_ds.shape[0] + 2.6  # extra height for title block
    fig = plt.figure(figsize=(fig_w, fig_h))
    gs = fig.add_gridspec(
        nrows=1,
        ncols=2,
        width_ratios=[1.0, 0.04],
        wspace=0.04,
        top=0.78,
        bottom=0.18,
        left=0.22,
        right=0.92,
    )
    ax = fig.add_subplot(gs[0, 0])
    cax = fig.add_subplot(gs[0, 1])

    # Short dataset labels: last 8 chars of UUID
    short_idx = [f"…{x[-8:]}" if len(x) > 12 else x for x in per_ds.index]

    im = ax.imshow(per_ds.values, aspect="auto", cmap=cmap, norm=norm, interpolation="nearest")
    ax.set_xticks(range(per_ds.shape[1]))
    ax.set_xticklabels(per_ds.columns, rotation=35, ha="right", fontsize=6.5)
    ax.set_yticks(range(per_ds.shape[0]))
    ax.set_yticklabels(short_idx, fontsize=6, family="monospace")
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("")
    ax.set_ylabel("CELLxGENE dataset id  (truncated)", fontsize=6.5, color=COLOR_MUTED_TEXT)

    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    cb.set_label("Spearman ρ (hepatocyte)", fontsize=7, color=COLOR_TEXT, labelpad=4)
    cb.ax.tick_params(labelsize=6, length=2.5)
    cb.set_ticks([-1, -0.5, 0, 0.5, 1])

    fig.suptitle(
        "Per-dataset hepatocyte coupling",
        x=0.012,
        y=0.96,
        ha="left",
        fontsize=9,
        fontweight="bold",
        color=COLOR_TEXT,
    )
    add_subtitle(
        fig,
        f"{summary['n_datasets']} datasets ≥ 300 hepatocyte cells. "
        f"Median pairwise ρ across datasets = {summary['median_pairwise_rho']:.2f} "
        f"(range {summary['min_pairwise_rho']:.2f} to {summary['max_pairwise_rho']:.2f}).",
        x=0.012,
        y=0.88,
    )
    fig.savefig(
        FIGURES / "supp_per_dataset_hepatocyte.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
    )
    log.info("Wrote %s", FIGURES / "supp_per_dataset_hepatocyte.png")

    log.info("=== PER-DATASET REPRODUCIBILITY ===")
    log.info("Datasets analysed    : %d", summary["n_datasets"])
    log.info("Pairwise comparisons : %d", summary["n_pairs"])
    log.info("Median pairwise rho  : %.3f", summary["median_pairwise_rho"])
    log.info("Min   pairwise rho   : %.3f", summary["min_pairwise_rho"])
    log.info("Max   pairwise rho   : %.3f", summary["max_pairwise_rho"])


if __name__ == "__main__":
    main()
