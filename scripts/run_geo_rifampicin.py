"""GEO GSE139896 — rifamycin treatment of primary human hepatocytes (direct panel overlay).

Dataset: Dyavar et al. (2019) profiled the transcriptional response of primary
human hepatocytes (3 healthy donors x 2 technical replicates) to three PXR
agonists used in tuberculosis therapy:
    - rifampin     (10 µM, 72 h)
    - rifabutin    (5  µM, 72 h)
    - rifapentine  (10 µM, 72 h)
versus methanol vehicle and untreated controls.

The processed Excel matrix at GEO contains raw RNA-seq counts for ~33,000
human genes per sample — the full transcriptome, so our top-6 hep-selective
panel (CYP2C9, CYP3A5, ABCC2, SLCO1B1, CYP2C8, CPT1A) is directly measurable
here. This is the direct perturbation overlay that LINCS L1000 (978
landmark-only) could not provide.

Hypothesis: in primary hepatocytes, all three rifamycins (PXR agonists) should
upregulate the top-6 panel, while matched negative controls (ALB, HNF4A,
GAPDH) and a housekeeping reference (NR1I2 itself — autoregulated but modest)
should not show comparable induction.

Reads  : data/cache/GSE139896_processed.xlsx (downloaded from NCBI GEO FTP)
Writes : data/processed/geo_rifamycin_logFC.csv
         data/processed/geo_rifamycin_stats.csv
         data/processed/geo_rifamycin_summary.json
         figures/fig5_rifamycin_perturbation.png
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

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import ttest_rel  # noqa: E402

from pxr_uncoupling.config import DATA_PROCESSED, FIGURES  # noqa: E402
from pxr_uncoupling.figure_style import (  # noqa: E402
    COLOR_HEPATIC,
    COLOR_NEG,
    COLOR_RECEPTOR,
    COLOR_TEXT,
    COLOR_ZERO_LINE,
    DOUBLE_COL,
    add_panel_label,
    add_subtitle,
    apply_style,
    polish_axes,
)

XLSX = DATA_PROCESSED.parent / "cache" / "GSE139896_processed.xlsx"

# Top-6 hep-selective PXR panel from the scRNA-seq decoupling score, and the
# matched controls used elsewhere in the paper.
PANEL = ["CYP2C9", "CYP3A5", "ABCC2", "SLCO1B1", "CYP2C8", "CPT1A"]
CONTROLS = ["ALB", "HNF4A", "GAPDH"]
RECEPTOR = ["NR1I2"]
GENES_OF_INTEREST = PANEL + CONTROLS + RECEPTOR

# Sample columns within each "<drug> vs Vehicle" sheet, in fixed order: the
# first 6 columns after gene name are the 6 vehicle samples (3 donors x 2 tech
# reps), the next 6 are the treated samples in matched order.
N_VEHICLE = 6
N_TREATED = 6
DONORS = ["8210", "4119B", "4079"]


def _read_sheet(sheet: str) -> tuple[pd.DataFrame, list[str]]:
    """Return (counts_df indexed by gene, sample_columns)."""
    raw = pd.read_excel(XLSX, sheet, header=None)
    sample_cols = raw.iloc[1, 1:].tolist()
    counts = raw.iloc[2:].copy()
    counts.columns = ["gene"] + list(sample_cols)
    counts = counts.set_index("gene")
    counts = counts.apply(pd.to_numeric, errors="coerce").dropna(how="any")
    return counts, list(sample_cols)


def _log2_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    """Convert raw counts to log2(CPM + 1) per column."""
    libsize = counts.sum(axis=0)
    cpm = counts.divide(libsize, axis=1) * 1e6
    return np.log2(cpm + 1.0)


def _per_donor_logfc(log_counts: pd.DataFrame) -> pd.DataFrame:
    """Collapse 2 tech reps per donor, then logFC(treated − vehicle) per donor.

    The standard GSE139896 sheet column order is the first 6 columns =
    vehicle (3 donors x 2 reps interleaved by donor), columns 7-12 = matched
    treated. Within each block, columns are in donor order 8210, 4119B, 4079.
    """
    cols = list(log_counts.columns)
    veh_cols = cols[:N_VEHICLE]
    trt_cols = cols[N_VEHICLE : N_VEHICLE + N_TREATED]
    out = pd.DataFrame(index=log_counts.index)
    for i, donor in enumerate(DONORS):
        veh_pair = veh_cols[2 * i : 2 * i + 2]
        trt_pair = trt_cols[2 * i : 2 * i + 2]
        veh_mean = log_counts[veh_pair].mean(axis=1)
        trt_mean = log_counts[trt_pair].mean(axis=1)
        out[donor] = trt_mean - veh_mean
    return out


def _gene_class(g: str) -> str:
    if g in PANEL:
        return "PXR panel"
    if g in CONTROLS:
        return "negative control"
    if g in RECEPTOR:
        return "receptor (NR1I2)"
    return "other"


def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    drug_sheets = {
        "rifampin": "Rifampin vs Vehicle",
        "rifabutin": "Rifabutin vs Vehicle",
        "rifapentine": "Rifapentine vs Vehicle",
    }

    rows: list[dict] = []
    stats_rows: list[dict] = []
    for drug, sheet in drug_sheets.items():
        log.info("Reading sheet %s ...", sheet)
        counts, sample_cols = _read_sheet(sheet)
        log.info("  shape: %s, sample cols: %s", counts.shape, sample_cols)
        log_cpm = _log2_cpm(counts)
        logfc = _per_donor_logfc(log_cpm)

        for gene in GENES_OF_INTEREST:
            if gene not in logfc.index:
                log.warning("%s not in %s", gene, sheet)
                continue
            vals = logfc.loc[gene].values.astype(float)
            mean_lfc = float(vals.mean())
            median_lfc = float(np.median(vals))
            std_lfc = float(vals.std(ddof=1)) if len(vals) > 1 else float("nan")
            for d, v in zip(DONORS, vals, strict=False):
                rows.append(
                    {
                        "drug": drug,
                        "gene": gene,
                        "gene_class": _gene_class(gene),
                        "donor": d,
                        "log2FC": float(v),
                    }
                )

            # paired t-test on per-donor logFC vs 0 (i.e. is the effect
            # significantly different from no change)
            t_stat, p_val = ttest_rel(vals, np.zeros_like(vals))
            stats_rows.append(
                {
                    "drug": drug,
                    "gene": gene,
                    "gene_class": _gene_class(gene),
                    "n_donors": int(len(vals)),
                    "mean_log2FC": mean_lfc,
                    "median_log2FC": median_lfc,
                    "std_log2FC": std_lfc,
                    "t_stat": float(t_stat),
                    "p_value": float(p_val),
                }
            )

    per_donor = pd.DataFrame(rows)
    per_donor.to_csv(DATA_PROCESSED / "geo_rifamycin_logFC.csv", index=False)
    stats = pd.DataFrame(stats_rows)
    stats.to_csv(DATA_PROCESSED / "geo_rifamycin_stats.csv", index=False)
    log.info("Wrote geo_rifamycin_logFC.csv (%d rows) and geo_rifamycin_stats.csv", len(per_donor))

    # Summary: panel vs control mean across the three drugs ────────────────
    panel_means = stats[stats["gene_class"] == "PXR panel"].groupby("drug")["mean_log2FC"].mean()
    ctrl_means = (
        stats[stats["gene_class"] == "negative control"].groupby("drug")["mean_log2FC"].mean()
    )
    summary = {
        "n_donors": len(DONORS),
        "drugs_tested": list(drug_sheets.keys()),
        "panel_mean_log2FC_per_drug": panel_means.round(3).to_dict(),
        "control_mean_log2FC_per_drug": ctrl_means.round(3).to_dict(),
        "panel_minus_control_per_drug": (panel_means - ctrl_means).round(3).to_dict(),
        "note": (
            "Direct primary-hepatocyte rifamycin perturbation overlay. "
            "Sheet 'Rifampin vs Vehicle' uses 10 µM at 72 h; Rifabutin 5 µM at "
            "72 h; Rifapentine 10 µM at 72 h. n=3 donors; tech reps collapsed."
        ),
    }
    with (DATA_PROCESSED / "geo_rifamycin_summary.json").open("w") as fh:
        json.dump(summary, fh, indent=2)
    log.info("Summary: %s", json.dumps(summary, indent=2))

    # Figure ───────────────────────────────────────────────────────────────────
    apply_style()
    from matplotlib.patches import Patch

    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE_COL, 3.6), sharey=True)
    for ax in axes:
        polish_axes(ax)

    gene_order = PANEL + RECEPTOR + CONTROLS
    color_map = {
        "PXR panel": COLOR_HEPATIC,
        "negative control": COLOR_NEG,
        "receptor (NR1I2)": COLOR_RECEPTOR,
    }

    panel_labels = ["a", "b", "c"]
    for k, (ax, drug) in enumerate(zip(axes, drug_sheets.keys(), strict=False)):
        sub = stats[stats["drug"] == drug].set_index("gene")
        x = np.arange(len(gene_order))
        means = sub.loc[gene_order, "mean_log2FC"].values
        stds = sub.loc[gene_order, "std_log2FC"].values
        colors = [color_map[_gene_class(g)] for g in gene_order]
        ax.bar(
            x,
            means,
            yerr=stds,
            capsize=2,
            color=colors,
            edgecolor="white",
            linewidth=0.5,
            width=0.75,
            error_kw={"elinewidth": 0.6, "capthick": 0.5, "ecolor": COLOR_TEXT},
        )
        for j, (g, p) in enumerate(
            zip(gene_order, sub.loc[gene_order, "p_value"].values, strict=False)
        ):
            if not np.isnan(p) and p < 0.05:
                top = means[j] + (stds[j] if not np.isnan(stds[j]) else 0)
                ax.text(
                    j,
                    top + 0.2,
                    "*",
                    ha="center",
                    fontsize=9,
                    color=COLOR_TEXT,
                    fontweight="bold",
                )
        ax.axhline(0, color=COLOR_ZERO_LINE, lw=0.5, linestyle="--")
        ax.set_xticks(x)
        ax.set_xticklabels(gene_order, rotation=35, ha="right", fontsize=6.5)
        ax.set_title(drug, loc="left", pad=4)
        add_panel_label(ax, panel_labels[k], dx=-0.16 if k == 0 else -0.05, dy=1.06)

    axes[0].set_ylabel(r"log$_2$ fold change vs vehicle")

    leg = [
        Patch(facecolor=COLOR_HEPATIC, label="Top-6 PXR panel"),
        Patch(facecolor=COLOR_RECEPTOR, label="Receptor (NR1I2)"),
        Patch(facecolor=COLOR_NEG, label="Matched controls"),
    ]
    axes[-1].legend(handles=leg, loc="upper right", handlelength=0.9, handleheight=0.7)

    fig.suptitle(
        "Direct rifamycin perturbation of primary human hepatocytes",
        x=0.012,
        y=0.97,
        ha="left",
        fontsize=9,
        fontweight="bold",
        color=COLOR_TEXT,
    )
    add_subtitle(
        fig,
        "GSE139896 (Dyavar et al. 2020). 3 donors, mean ± SD, 72 h treatment. `*` paired t-test p < 0.05.",  # noqa: E501
        x=0.012,
        y=0.93,
    )

    plt.tight_layout(rect=(0, 0, 1, 0.88))
    out = FIGURES / "fig5_rifamycin_perturbation.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    log.info("Wrote %s", out)


if __name__ == "__main__":
    main()
