"""GTEx bulk RNA-seq tissue-level validation of single-cell coupling.

For each gene (NR1I2 + top-5 hep-selective targets + 3 controls), pull per-sample
TPM across all 54 GTEx v8 tissues, then compute within-tissue Spearman
rho(NR1I2, target) — a bulk-tissue analogue of the per-cell-type metacell
coupling. If the single-cell pattern is biology and not artifact, hepatic
tissue rho should mirror hepatocyte rho, while immune/placental tissues
remain decoupled.

Reads  : (GTEx API, cached)
Writes : data/processed/gtex_coupling.csv             # rows=tissue, cols=gene
         data/processed/gtex_per_tissue_n.csv         # sample sizes
         data/cache/gtex_<symbol>.json                # per-gene cache
         figures/supp_gtex_validation.png
"""

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

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    COLOR_ACCENT,
    COLOR_CREAM,
    COLOR_SAGE,
    DATA_PROCESSED,
    FIGURES,
)
from pxr_uncoupling.gtex import fetch_many  # noqa: E402

PXR_TARGETS = ["CYP2C8", "CYP2C9", "SLCO1B1", "ABCC2", "CYP3A5"]
CONTROLS = ["ALB", "HNF4A", "GAPDH"]

# Tissue groupings to mirror the single-cell cell-type taxonomy.
TISSUE_GROUP: dict[str, str] = {
    "Liver": "liver",
    "Small_Intestine_Terminal_Ileum": "intestine",
    "Colon_Sigmoid": "intestine",
    "Colon_Transverse": "intestine",
    "Esophagus_Mucosa": "intestine",  # epithelial barrier
    "Stomach": "intestine",
    "Whole_Blood": "immune",
    "Spleen": "immune",
    "Cells_EBV-transformed_lymphocytes": "immune",
    "Kidney_Cortex": "kidney",
    "Kidney_Medulla": "kidney",
    "Adrenal_Gland": "adrenal",
}


def _spearman_or_nan(x: list[float], y: list[float]) -> tuple[float, float]:
    if len(x) != len(y) or len(x) < 5:
        return (np.nan, np.nan)
    xa = np.asarray(x)
    ya = np.asarray(y)
    mask = np.isfinite(xa) & np.isfinite(ya)
    if mask.sum() < 5:
        return (np.nan, np.nan)
    rho, pval = spearmanr(xa[mask], ya[mask])
    return (float(rho), float(pval))


def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    symbols = ["NR1I2"] + PXR_TARGETS + CONTROLS
    log.info("Fetching %d genes from GTEx v8", len(symbols))
    arrays = fetch_many(symbols)

    # 1. Compute within-tissue Spearman rho(NR1I2, target) per tissue ──────────
    nr1i2 = arrays["NR1I2"]
    tissues = sorted(nr1i2.keys())
    log.info("GTEx returned %d tissues", len(tissues))

    rho_rows: list[dict] = []
    n_rows: list[dict] = []
    pval_rows: list[dict] = []

    for tissue in tissues:
        rho_rec = {"tissue": tissue}
        pval_rec = {"tissue": tissue}
        n_rec = {"tissue": tissue, "n_nr1i2": len(nr1i2.get(tissue, []))}
        for gene in PXR_TARGETS + CONTROLS:
            target_arr = arrays[gene].get(tissue, [])
            ref_arr = nr1i2.get(tissue, [])
            if len(target_arr) != len(ref_arr):
                log.warning(
                    "%s: sample count mismatch NR1I2=%d %s=%d — skipping",
                    tissue,
                    len(ref_arr),
                    gene,
                    len(target_arr),
                )
                rho_rec[gene] = np.nan
                pval_rec[gene] = np.nan
                continue
            rho, pval = _spearman_or_nan(ref_arr, target_arr)
            rho_rec[gene] = rho
            pval_rec[gene] = pval
            n_rec[f"n_{gene}"] = len(target_arr)
        rho_rows.append(rho_rec)
        pval_rows.append(pval_rec)
        n_rows.append(n_rec)

    rho_df = pd.DataFrame(rho_rows).set_index("tissue")
    pval_df = pd.DataFrame(pval_rows).set_index("tissue")
    n_df = pd.DataFrame(n_rows).set_index("tissue")

    rho_df.to_csv(DATA_PROCESSED / "gtex_coupling.csv")
    pval_df.to_csv(DATA_PROCESSED / "gtex_coupling_pvalues.csv")
    n_df.to_csv(DATA_PROCESSED / "gtex_per_tissue_n.csv")
    log.info("Wrote gtex_coupling.csv (%d tissues x %d genes)", *rho_df.shape)

    # 2. Liver vs immune/other comparison for headline ─────────────────────────
    summary: dict[str, dict[str, float]] = {}
    for gene in PXR_TARGETS:
        liver_rho = float(rho_df.loc["Liver", gene]) if "Liver" in rho_df.index else np.nan
        immune_tissues = [t for t in rho_df.index if TISSUE_GROUP.get(t) == "immune"]
        immune_rho = rho_df.loc[immune_tissues, gene].mean() if immune_tissues else np.nan
        intestinal_tissues = [t for t in rho_df.index if TISSUE_GROUP.get(t) == "intestine"]
        intestinal_rho = (
            rho_df.loc[intestinal_tissues, gene].mean() if intestinal_tissues else np.nan
        )
        summary[gene] = {
            "liver_rho": liver_rho,
            "intestine_mean_rho": float(intestinal_rho) if not np.isnan(intestinal_rho) else np.nan,
            "immune_mean_rho": float(immune_rho) if not np.isnan(immune_rho) else np.nan,
            "liver_minus_immune": float(liver_rho - immune_rho)
            if not (np.isnan(liver_rho) or np.isnan(immune_rho))
            else np.nan,
        }
        log.info(
            "%s: liver rho=%.2f, intestine mean=%.2f, immune mean=%.2f",
            gene,
            liver_rho,
            intestinal_rho,
            immune_rho,
        )

    summary_df = pd.DataFrame(summary).T
    summary_df.to_csv(DATA_PROCESSED / "gtex_summary.csv")

    # 3. Heatmap figure ────────────────────────────────────────────────────────
    plot_genes = PXR_TARGETS + CONTROLS
    plot_mat = rho_df[plot_genes].copy()

    def _group_sort_key(tissue: str) -> tuple[int, str]:
        grp = TISSUE_GROUP.get(tissue, "zzz_other")
        order = {"liver": 0, "intestine": 1, "kidney": 2, "adrenal": 3, "immune": 4}
        return (order.get(grp, 9), tissue)

    plot_mat = plot_mat.reindex(sorted(plot_mat.index, key=_group_sort_key))

    fig, ax = plt.subplots(figsize=(8, 14))
    fig.patch.set_facecolor(COLOR_CREAM)
    ax.set_facecolor(COLOR_CREAM)
    cmap = plt.cm.RdBu_r
    im = ax.imshow(plot_mat.values, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(plot_genes)))
    ax.set_xticklabels(plot_genes, rotation=45, ha="right")
    ax.set_yticks(range(len(plot_mat.index)))
    ax.set_yticklabels([t.replace("_", " ") for t in plot_mat.index], fontsize=8)
    ax.set_title(
        "GTEx v8 within-tissue Spearman rho(NR1I2, gene)\n"
        "top-5 PXR targets (left) vs negative controls (right)",
        fontsize=11,
        loc="left",
        pad=10,
    )
    ax.axvline(len(PXR_TARGETS) - 0.5, color="k", lw=1.5)
    for i, tissue in enumerate(plot_mat.index):
        grp = TISSUE_GROUP.get(tissue, "")
        if grp == "liver":
            ax.add_patch(
                plt.Rectangle(
                    (-0.5, i - 0.5),
                    len(plot_genes),
                    1.0,
                    fill=False,
                    edgecolor=COLOR_ACCENT,
                    lw=2,
                )
            )
        elif grp == "immune":
            ax.add_patch(
                plt.Rectangle(
                    (-0.5, i - 0.5),
                    len(plot_genes),
                    1.0,
                    fill=False,
                    edgecolor=COLOR_SAGE,
                    lw=1.5,
                    linestyle="--",
                )
            )
    cbar = fig.colorbar(im, ax=ax, shrink=0.4, label="Spearman rho")
    cbar.outline.set_visible(False)
    plt.tight_layout()
    out = FIGURES / "supp_gtex_validation.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=COLOR_CREAM)
    log.info("Wrote %s", out)

    # 4. Console summary ──────────────────────────────────────────────────────
    print("\n=== GTEX EXTERNAL VALIDATION ===")
    print(f"Tissues: {len(rho_df.index)}; genes: {len(PXR_TARGETS) + len(CONTROLS)}")
    print("\nPer-gene liver vs immune (mean of immune tissues):")
    print(summary_df.round(3).to_string())
    print(
        "\nKey single-cell vs bulk comparison: "
        "hepatocyte (scRNA-seq) and liver (GTEx bulk) should both be ~0.7-0.9; "
        "immune tissues should be near zero."
    )


if __name__ == "__main__":
    main()
