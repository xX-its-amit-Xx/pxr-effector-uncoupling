"""Compare PXR target coupling to a matched negative-control gene set.

Reads  : data/raw/nr1i2_atlas.h5ad  (must include negative_control_genes)
         data/targets/pxr_canonical_targets.tsv
         data/targets/negative_control_genes.tsv
Writes : data/processed/control_coupling.csv
         data/processed/control_decoupling.csv
         data/processed/control_comparison.json
         figures/supp_negative_control.png

Reviewer ask: prove the hepatocyte-selective decoupling pattern is specific
to PXR target genes, not a generic 'hepatocyte vs everyone else' transcriptional
signature. We use the same metacell-coupling pipeline on a curated control set
(liver-enriched non-PXR genes, hepatocyte TFs, housekeeping genes) and test
whether PXR-target decoupling scores are right-shifted vs controls (Mann-Whitney U).
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
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    COLOR_ACCENT,
    COLOR_CREAM,
    COLOR_SAGE,
    DATA_PROCESSED,
    DATA_RAW,
    DATA_TARGETS,
    FIGURES,
    MIN_METACELLS,
    NR1I2_SYMBOL,
    TARGET_CELLS_PER_METACELL,
)
from pxr_uncoupling.coupling import coupling_per_cell_type, decoupling_score  # noqa: E402
from pxr_uncoupling.statistics import compare_to_null_genes  # noqa: E402


def main() -> None:
    h5ad = DATA_RAW / "nr1i2_atlas.h5ad"
    adata = ad.read_h5ad(h5ad)
    log.info("Atlas: %d cells x %d genes", adata.n_obs, adata.n_vars)

    targets = pd.read_csv(DATA_TARGETS / "pxr_canonical_targets.tsv", sep="\t")
    controls = pd.read_csv(DATA_TARGETS / "negative_control_genes.tsv", sep="\t")
    target_syms = targets["gene_symbol"].tolist()
    control_syms = controls["gene_symbol"].tolist()

    present = set(adata.var_names)
    missing_t = [g for g in target_syms if g not in present]
    missing_c = [g for g in control_syms if g not in present]
    if missing_t:
        log.warning("PXR targets missing from atlas: %s", missing_t)
    if missing_c:
        log.warning("Control genes missing from atlas: %s", missing_c)
    target_genes = [g for g in target_syms if g in present]
    control_genes = [g for g in control_syms if g in present]
    log.info("Atlas contains %d PXR targets + %d controls", len(target_genes), len(control_genes))

    if NR1I2_SYMBOL not in present:
        raise RuntimeError(f"{NR1I2_SYMBOL} missing from atlas — fetch is broken")

    # 1. Coupling for both gene sets
    log.info("Computing coupling for control genes ...")
    control_coupling = coupling_per_cell_type(
        adata,
        target_genes=control_genes,
        cells_per_metacell=TARGET_CELLS_PER_METACELL,
        min_metacells=MIN_METACELLS,
    )
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    control_coupling.to_csv(DATA_PROCESSED / "control_coupling.csv")
    log.info("Saved control_coupling.csv")

    # Reuse cached target coupling if present, else recompute
    target_csv = DATA_PROCESSED / "coupling.csv"
    if target_csv.exists():
        target_coupling = pd.read_csv(target_csv, index_col=0)
        # Restrict to target genes only (atlas may now include controls)
        target_coupling = target_coupling[[g for g in target_genes if g in target_coupling.columns]]
        log.info("Loaded existing coupling.csv (%d cell types x %d genes)", *target_coupling.shape)
    else:
        target_coupling = coupling_per_cell_type(
            adata,
            target_genes=target_genes,
            cells_per_metacell=TARGET_CELLS_PER_METACELL,
            min_metacells=MIN_METACELLS,
        )

    # 2. Decoupling vs hepatocyte for both
    if "hepatocyte" not in target_coupling.index or "hepatocyte" not in control_coupling.index:
        raise RuntimeError("hepatocyte missing from one of the coupling matrices")
    target_ds = decoupling_score(target_coupling, reference_cell_type="hepatocyte")
    control_ds = decoupling_score(control_coupling, reference_cell_type="hepatocyte")
    control_ds.to_csv(DATA_PROCESSED / "control_decoupling.csv")
    log.info("Saved control_decoupling.csv")

    # 3. Distribution comparison
    summary = compare_to_null_genes(target_ds, control_ds)
    log.info("Mann-Whitney (target > control): U=%.1f  p=%.3g", summary["u"], summary["pvalue"])
    log.info(
        "Median target DS=%.3f vs median control DS=%.3f",
        summary["median_target"],
        summary["median_null"],
    )

    # 4. Per-cell-type mean DS comparison
    per_ct = pd.DataFrame(
        {
            "target_mean_DS": target_ds.mean(axis=1),
            "control_mean_DS": control_ds.mean(axis=1),
        }
    )
    per_ct["target_minus_control"] = per_ct["target_mean_DS"] - per_ct["control_mean_DS"]
    per_ct.to_csv(DATA_PROCESSED / "control_comparison_per_cell_type.csv")
    log.info("Per-cell-type comparison:\n%s", per_ct.round(3).to_string())

    full_summary = {
        **summary,
        "target_genes_used": target_genes,
        "control_genes_used": control_genes,
        "control_genes_missing": missing_c,
        "target_genes_missing": missing_t,
        "per_cell_type": per_ct.round(3).to_dict(orient="index"),
    }
    with (DATA_PROCESSED / "control_comparison.json").open("w") as fh:
        json.dump(full_summary, fh, indent=2, default=str)

    # 5. Figure: split violin of target vs control decoupling distributions
    FIGURES.mkdir(parents=True, exist_ok=True)
    target_long = target_ds.melt(value_name="DS", var_name="gene", ignore_index=False)
    target_long["set"] = "PXR target"
    control_long = control_ds.melt(value_name="DS", var_name="gene", ignore_index=False)
    control_long["set"] = "negative control"
    combined = pd.concat([target_long, control_long], axis=0).dropna()
    combined.index.name = "cell_type"
    combined = combined.reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [1, 1.4]})
    fig.patch.set_facecolor(COLOR_CREAM)
    for ax in axes:
        ax.set_facecolor(COLOR_CREAM)

    # Panel A: pooled distribution
    sns.violinplot(
        data=combined,
        x="set",
        y="DS",
        ax=axes[0],
        palette={"PXR target": COLOR_ACCENT, "negative control": COLOR_SAGE},
        inner="quartile",
        linewidth=0.8,
        cut=0,
    )
    sns.stripplot(
        data=combined,
        x="set",
        y="DS",
        ax=axes[0],
        color="#2a2a2a",
        size=2,
        alpha=0.35,
        jitter=0.25,
    )
    axes[0].axhline(0, color="#888", ls="--", lw=0.8)
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Decoupling score (ρ_hepatocyte − ρ_other)")
    p = summary["pvalue"]
    axes[0].set_title(
        f"PXR target decoupling vs. matched controls\n"
        f"Mann-Whitney U (one-sided): p = {p:.2g}  "
        f"(median {summary['median_target']:.2f} vs {summary['median_null']:.2f})",
        fontsize=10,
    )

    # Panel B: per-cell-type means
    per_ct_sorted = per_ct.sort_values("target_mean_DS")
    y = np.arange(len(per_ct_sorted))
    axes[1].scatter(
        per_ct_sorted["target_mean_DS"],
        y,
        color=COLOR_ACCENT,
        s=70,
        label="PXR targets",
        edgecolors="white",
        linewidths=0.8,
    )
    axes[1].scatter(
        per_ct_sorted["control_mean_DS"],
        y,
        color=COLOR_SAGE,
        s=70,
        label="Negative controls",
        edgecolors="white",
        linewidths=0.8,
    )
    for i in y:
        axes[1].plot(
            [per_ct_sorted["control_mean_DS"].iloc[i], per_ct_sorted["target_mean_DS"].iloc[i]],
            [i, i],
            color="#888",
            lw=0.6,
            alpha=0.6,
        )
    axes[1].axvline(0, color="#888", ls="--", lw=0.8)
    axes[1].set_yticks(y)
    axes[1].set_yticklabels(per_ct_sorted.index, fontsize=8)
    axes[1].set_xlabel("Mean decoupling score across genes")
    axes[1].legend(loc="lower right", fontsize=8)
    axes[1].set_title("Per cell type: PXR targets vs. controls", fontsize=10)

    plt.tight_layout()
    fig.savefig(
        FIGURES / "supp_negative_control.png",
        dpi=300,
        bbox_inches="tight",
        facecolor=COLOR_CREAM,
    )
    log.info("Wrote %s", FIGURES / "supp_negative_control.png")

    print("\n=== NEGATIVE-CONTROL COMPARISON ===")
    print(f"PXR targets         : {len(target_genes)} genes")
    print(f"Negative controls   : {len(control_genes)} genes")
    print(f"Median target DS    : {summary['median_target']:.3f}")
    print(f"Median control DS   : {summary['median_null']:.3f}")
    print(f"Mann-Whitney U      : {summary['u']:.1f}")
    print(f"One-sided p-value   : {summary['pvalue']:.3g}")


if __name__ == "__main__":
    main()
