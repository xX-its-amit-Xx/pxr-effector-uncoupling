"""Run robustness analyses: bootstrap CIs, permutation p-values, sensitivity sweep,
and subsample stability. Outputs feed Notebook 05 and the README.

Reads  : data/raw/nr1i2_atlas.h5ad
Writes : data/processed/coupling_ci_lower.csv
         data/processed/coupling_ci_upper.csv
         data/processed/coupling_pvalues.csv
         data/processed/coupling_qvalues.csv
         data/processed/sensitivity_sweep.csv
         data/processed/sensitivity_agreement.csv
         data/processed/subsample_stability.csv
         data/processed/subsample_summary.csv
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

import anndata as ad  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    DATA_PROCESSED,
    DATA_RAW,
    MIN_METACELLS,
    NR1I2_SYMBOL,
    TARGET_CELLS_PER_METACELL,
)
from pxr_uncoupling.sensitivity import (  # noqa: E402
    matrix_agreement,
    parameter_sweep,
    stability_summary,
    subsample_stability,
)
from pxr_uncoupling.statistics import (  # noqa: E402
    benjamini_hochberg,
    bootstrap_coupling_ci,
    permutation_pvalues,
)


def main() -> None:
    h5ad_path = DATA_RAW / "nr1i2_atlas.h5ad"
    log.info("Loading %s", h5ad_path)
    adata = ad.read_h5ad(h5ad_path)
    # Restrict to the curated PXR target set; negative controls are handled by
    # run_negative_control.py, not this script.
    import pandas as pd

    pxr_targets = pd.read_csv(DATA_RAW.parent / "targets" / "pxr_canonical_targets.tsv", sep="\t")[
        "gene_symbol"
    ].tolist()
    target_genes = [g for g in pxr_targets if g in adata.var_names and g != NR1I2_SYMBOL]
    log.info(
        "Atlas: %d cells × %d genes; using %d PXR target genes",
        adata.n_obs,
        adata.n_vars,
        len(target_genes),
    )

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    # 1. Bootstrap CIs ─────────────────────────────────────────────────────────
    log.info("Bootstrap CIs (n=500) ...")
    ci = bootstrap_coupling_ci(adata, target_genes, n_bootstrap=500)
    ci["lower"].to_csv(DATA_PROCESSED / "coupling_ci_lower.csv")
    ci["upper"].to_csv(DATA_PROCESSED / "coupling_ci_upper.csv")
    ci["median"].to_csv(DATA_PROCESSED / "coupling_ci_median.csv")
    log.info("  saved coupling_ci_{lower,upper,median}.csv")

    # 2. Permutation p-values + BH-FDR ─────────────────────────────────────────
    log.info("Permutation p-values (n=500) ...")
    pvals = permutation_pvalues(adata, target_genes, n_permutations=500)
    qvals = benjamini_hochberg(pvals)
    pvals.to_csv(DATA_PROCESSED / "coupling_pvalues.csv")
    qvals.to_csv(DATA_PROCESSED / "coupling_qvalues.csv")
    n_sig = int((qvals < 0.05).sum().sum())
    log.info("  q<0.05: %d (cell_type, gene) pairs", n_sig)

    # 3. Parameter sensitivity sweep ────────────────────────────────────────────
    log.info("Parameter sensitivity sweep ...")
    sweep = parameter_sweep(
        adata,
        target_genes,
        cells_per_metacell_grid=(15, 30, 60),
        min_metacells_grid=(10, 20),
        seeds=(0, 42, 123),
    )
    sweep.to_csv(DATA_PROCESSED / "sensitivity_sweep.csv", index=False)
    agreement = matrix_agreement(
        sweep,
        reference_key={
            "cells_per_metacell": TARGET_CELLS_PER_METACELL,
            "min_metacells": MIN_METACELLS,
            "seed": 42,
        },
    )
    agreement.to_csv(DATA_PROCESSED / "sensitivity_agreement.csv", index=False)
    log.info("  sweep rows: %d; agreement rows: %d", len(sweep), len(agreement))
    if not agreement.empty:
        log.info(
            "  median Spearman of decoupling rankings vs ref: %.3f",
            agreement["spearman_of_decoupling"].median(),
        )
        log.info(
            "  median Jaccard of top-5 hepatocyte-selective genes: %.3f",
            agreement["jaccard_top5"].median(),
        )

    # 4. Subsample stability ───────────────────────────────────────────────────
    log.info("Subsample stability (20 iters, 80%%) ...")
    stab = subsample_stability(
        adata,
        target_genes,
        n_iterations=20,
        fraction=0.8,
    )
    stab.to_csv(DATA_PROCESSED / "subsample_stability.csv", index=False)
    summary = stability_summary(stab)
    summary.to_csv(DATA_PROCESSED / "subsample_summary.csv", index=False)
    log.info(
        "  median per-(cell_type,gene) std across 20 subsamples: %.3f", summary["std"].median()
    )

    print("\n=== ROBUSTNESS COMPLETE ===")
    print(f"Outputs in {DATA_PROCESSED}")


if __name__ == "__main__":
    main()
