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
    target_genes = [g for g in adata.var_names if g != NR1I2_SYMBOL]
    log.info("Computing coupling for %d target genes across cell types ...", len(target_genes))

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
    print("\n=== CHECKPOINT 3: ANALYSIS COMPLETE ===")
    print(f"Cell types analysed : {coupling.shape[0]}")
    print(f"Target genes        : {coupling.shape[1]}")
    if "hepatocyte" in coupling.index:
        hep_mean = coupling.loc["hepatocyte"].mean()
        print(f"Mean hepatocyte ρ   : {hep_mean:.3f}")
        if ds is not None:
            best_gene = gene_mean_ds.index[0]
            print(f"Top decoupled gene  : {best_gene} (mean DS={gene_mean_ds.iloc[0]:.3f})")
    print("Outputs:")
    print(f"  {coupling_path}")
    if ds is not None:
        print(f"  {ds_path}")
    print(f"  {FIGURES / 'final_heatmap.png'}")


if __name__ == "__main__":
    main()
