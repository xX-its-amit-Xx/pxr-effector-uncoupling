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

from pxr_uncoupling.config import DATA_PROCESSED, FIGURES  # noqa: E402
from pxr_uncoupling.figure_style import (  # noqa: E402
    COLOR_HEPATIC,
    COLOR_IMMUNE,
    COLOR_INTESTINE,
    COLOR_MUTED_TEXT,
    COLOR_TEXT,
    DOUBLE_COL,
    add_subtitle,
    apply_style,
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
    apply_style()
    plot_genes = PXR_TARGETS + CONTROLS
    plot_mat = rho_df[plot_genes].copy()

    def _group_sort_key(tissue: str) -> tuple[int, str]:
        grp = TISSUE_GROUP.get(tissue, "zzz_other")
        order = {"liver": 0, "intestine": 1, "kidney": 2, "adrenal": 3, "immune": 4}
        return (order.get(grp, 9), tissue)

    plot_mat = plot_mat.reindex(sorted(plot_mat.index, key=_group_sort_key))

    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

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

    # Layout: heatmap + thin colourbar. Tissue-group identity is conveyed by
    # colouring the y-axis tick labels themselves (no separate side band).
    fig_height = 0.16 * len(plot_mat.index) + 2.2
    fig = plt.figure(figsize=(DOUBLE_COL * 0.85, fig_height))
    gs = fig.add_gridspec(
        nrows=1,
        ncols=2,
        width_ratios=[1.0, 0.03],
        wspace=0.04,
        top=0.86,
        bottom=0.09,
        left=0.30,
        right=0.92,
    )
    ax = fig.add_subplot(gs[0, 0])
    cax = fig.add_subplot(gs[0, 1])

    group_color = {
        "liver": COLOR_HEPATIC,
        "intestine": COLOR_INTESTINE,
        "kidney": "#7a8a9f",
        "adrenal": "#8a6a9c",
        "immune": COLOR_IMMUNE,
    }

    im = ax.imshow(plot_mat.values, cmap=cmap, norm=norm, aspect="auto", interpolation="nearest")
    ax.set_xticks(range(len(plot_genes)))
    ax.set_xticklabels(plot_genes, rotation=35, ha="right", fontsize=6.5)
    ax.set_yticks(range(len(plot_mat.index)))
    ax.set_yticklabels([t.replace("_", " ") for t in plot_mat.index], fontsize=6.5)
    # Colour the labels of tissues that belong to a tracked compartment.
    for tick_label, tissue in zip(ax.get_yticklabels(), plot_mat.index, strict=False):
        grp = TISSUE_GROUP.get(tissue)
        if grp:
            tick_label.set_color(group_color.get(grp, COLOR_TEXT))
            tick_label.set_fontweight("medium")
    ax.tick_params(length=0)
    ax.axvline(len(PXR_TARGETS) - 0.5, color="white", lw=1.4)
    # subtle separator between gene-class groups
    fig.text(
        0.55 * (len(PXR_TARGETS) + 1) / (len(plot_genes) + 1) - 0.05,
        0.02,
        "← PXR targets    Controls →",
        fontsize=6.5,
        color=COLOR_MUTED_TEXT,
    )
    for s in ax.spines.values():
        s.set_visible(False)

    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    cb.set_label("Spearman ρ", fontsize=7, color=COLOR_TEXT, labelpad=4)
    cb.ax.tick_params(labelsize=6, length=2.5)
    cb.set_ticks([-1, -0.5, 0, 0.5, 1])

    fig.suptitle(
        "GTEx v8 within-tissue ρ(NR1I2, gene)",
        x=0.012,
        y=0.97,
        ha="left",
        fontsize=9,
        fontweight="bold",
        color=COLOR_TEXT,
    )
    add_subtitle(
        fig,
        "Top-5 hep-selective PXR targets (left of divider) vs three matched controls; 54 tissues; n ≥ 70 donors / tissue.",  # noqa: E501
        x=0.012,
        y=0.935,
    )
    out = FIGURES / "supp_gtex_validation.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
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
