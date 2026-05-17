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
import seaborn as sns  # noqa: E402
from matplotlib.colors import TwoSlopeNorm  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    COLOR_CREAM,
    DATA_PROCESSED,
    DATA_RAW,
    FIGURES,
    NR1I2_SYMBOL,
)
from pxr_uncoupling.reproducibility import (  # noqa: E402
    cross_dataset_agreement,
    per_dataset_coupling,
)


def main() -> None:
    adata = ad.read_h5ad(DATA_RAW / "nr1i2_atlas.h5ad")
    target_genes = [g for g in adata.var_names if g != NR1I2_SYMBOL]

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

    # Heatmap: datasets × genes
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig_w = max(8, per_ds.shape[1] * 0.45 + 2)
    fig_h = max(3, per_ds.shape[0] * 0.45 + 1.5)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor(COLOR_CREAM)
    ax.set_facecolor(COLOR_CREAM)
    norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    cmap = sns.diverging_palette(h_neg=20, h_pos=145, s=60, l=45, sep=1, as_cmap=True)
    sns.heatmap(
        per_ds,
        ax=ax,
        cmap=cmap,
        norm=norm,
        linewidths=0.4,
        linecolor="#e0d5c5",
        cbar_kws={"label": "Spearman ρ (hepatocyte)", "shrink": 0.6},
        mask=per_ds.isna(),
    )
    ax.set_title(
        "Hepatocyte coupling within individual datasets\n"
        f"({summary['n_datasets']} datasets ≥ 300 hepatocyte cells; "
        f"median pairwise ρ = {summary['median_pairwise_rho']:.2f}, "
        f"range {summary['min_pairwise_rho']:.2f}–{summary['max_pairwise_rho']:.2f})",
        fontsize=10,
        pad=12,
    )
    ax.set_xlabel("PXR target gene")
    ax.set_ylabel("CELLxGENE dataset_id")
    ax.tick_params(axis="x", labelrotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    plt.tight_layout()
    fig.savefig(
        FIGURES / "supp_per_dataset_hepatocyte.png",
        dpi=300,
        bbox_inches="tight",
        facecolor=COLOR_CREAM,
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
