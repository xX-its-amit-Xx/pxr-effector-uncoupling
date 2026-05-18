"""Run the full coupling / decoupling / heatmap pipeline.

Reads  : data/raw/nr1i2_atlas.h5ad
Writes : data/processed/coupling.csv
         data/processed/decoupling.csv
         figures/final_heatmap.png
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
import pandas as pd  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    CELL_TYPE_TISSUE_MAP,
    DATA_PROCESSED,
    DATA_RAW,
    FIGURES,
    MIN_METACELLS,
    NR1I2_SYMBOL,
    TARGET_CELLS_PER_METACELL,
)
from pxr_uncoupling.coupling import (  # noqa: E402
    coupling_per_cell_type,
    decoupling_score,
)
from pxr_uncoupling.plotting import decoupling_heatmap  # noqa: E402


def main() -> None:
    # ── 1. Load atlas ──────────────────────────────────────────────────────────
    h5ad_path = DATA_RAW / "nr1i2_atlas.h5ad"
    log.info("Loading %s", h5ad_path)
    adata = ad.read_h5ad(h5ad_path)
    log.info("Loaded: %d cells × %d genes", adata.n_obs, adata.n_vars)
    log.info("Cell types present: %s", sorted(adata.obs["cell_type"].unique()))
    log.info("Genes: %s", adata.var_names.tolist())

    # ── 2. Coupling ρ per cell type ────────────────────────────────────────────
    # Restrict to the curated PXR target set. The atlas may also contain
    # negative-control genes (handled separately by run_negative_control.py).
    target_meta_path = DATA_RAW.parent / "targets" / "pxr_canonical_targets.tsv"
    pxr_targets = pd.read_csv(target_meta_path, sep="\t")["gene_symbol"].tolist()
    target_genes = [g for g in pxr_targets if g in adata.var_names and g != NR1I2_SYMBOL]
    log.info(
        "Computing coupling for %d PXR target genes (of %d curated) across cell types",
        len(target_genes),
        len(pxr_targets),
    )

    coupling = coupling_per_cell_type(
        adata,
        target_genes=target_genes,
        cells_per_metacell=TARGET_CELLS_PER_METACELL,
        min_metacells=MIN_METACELLS,
    )
    log.info("Coupling matrix shape: %s", coupling.shape)
    log.info("Cell types with coupling: %s", coupling.index.tolist())

    if coupling.empty:
        log.error("Coupling matrix is empty — no cell type passed min_metacells=%d", MIN_METACELLS)
        sys.exit(1)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    coupling_path = DATA_PROCESSED / "coupling.csv"
    coupling.to_csv(coupling_path)
    log.info("Saved coupling to %s", coupling_path)

    # ── 3. Decoupling scores ────────────────────────────────────────────────────
    if "hepatocyte" in coupling.index:
        ds = decoupling_score(coupling, reference_cell_type="hepatocyte")
        ds_path = DATA_PROCESSED / "decoupling.csv"
        ds.to_csv(ds_path)
        log.info("Saved decoupling scores to %s", ds_path)
        log.info("\nTop decoupled genes (hepatocyte-selective):")
        gene_mean_ds = ds.mean(axis=0).sort_values(ascending=False)
        log.info("\n%s", gene_mean_ds.head(10).to_string())
    else:
        log.warning("hepatocyte not in coupling index; skipping decoupling score")
        ds = None

    # ── 4. Heatmap ──────────────────────────────────────────────────────────────
    target_meta = pd.read_csv(
        DATA_RAW.parent / "targets" / "pxr_canonical_targets.tsv",
        sep="\t",
        index_col="gene_symbol",
    )

    FIGURES.mkdir(parents=True, exist_ok=True)
    decoupling_heatmap(
        coupling_df=coupling,
        target_meta=target_meta,
        cell_type_tissue_map=CELL_TYPE_TISSUE_MAP,
        output_path=FIGURES / "final_heatmap.png",
    )
    log.info("Heatmap saved to %s", FIGURES / "final_heatmap.png")

    # ── 5. Summary ──────────────────────────────────────────────────────────────
    log.info("=== CHECKPOINT 3: ANALYSIS COMPLETE ===")
    log.info("Cell types analysed : %d", coupling.shape[0])
    log.info("Target genes        : %d", coupling.shape[1])
    if "hepatocyte" in coupling.index:
        hep_mean = coupling.loc["hepatocyte"].mean()
        log.info("Mean hepatocyte rho : %.3f", hep_mean)
        if ds is not None:
            best_gene = gene_mean_ds.index[0]
            log.info("Top decoupled gene  : %s (mean DS=%.3f)", best_gene, gene_mean_ds.iloc[0])
    log.info(
        "Outputs: %s, %s, %s",
        coupling_path,
        ds_path if ds is not None else "(no decoupling)",
        FIGURES / "final_heatmap.png",
    )


if __name__ == "__main__":
    main()
