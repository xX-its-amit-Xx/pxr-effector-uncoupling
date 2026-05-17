"""Fetch NR1I2 expression atlas from CELLxGENE Census.

Designed to run on a glibc environment (Ubuntu/GitHub Actions).
Writes data/raw/nr1i2_atlas.h5ad.
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

# Allow running from repo root without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import cellxgene_census  # noqa: E402
import pandas as pd  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    CELL_TYPE_TISSUE_MAP,
    CENSUS_VERSION,
    DATA_RAW,
    DATA_TARGETS,
    MIN_CELLS_PER_TYPE,
    NR1I2_ENSEMBL,
)


def load_target_genes() -> pd.DataFrame:
    return pd.read_csv(DATA_TARGETS / "pxr_canonical_targets.tsv", sep="\t")


def main() -> None:
    targets = load_target_genes()
    ensembl_ids = targets["ensembl_id"].tolist()
    if NR1I2_ENSEMBL not in ensembl_ids:
        ensembl_ids = [NR1I2_ENSEMBL] + ensembl_ids

    cell_types = list(CELL_TYPE_TISSUE_MAP.keys())
    log.info("Fetching %d genes for %d curated cell types", len(ensembl_ids), len(cell_types))
    log.info("Cell types: %s", cell_types)

    # organism_ontology_term_id is not in per-organism obs; organism is already
    # scoped by the organism= argument to get_anndata().
    value_filter = f"is_primary_data == True and cell_type in {cell_types!r}"

    log.info("Opening Census version %s", CENSUS_VERSION)
    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        log.info("Fetching expression matrix ...")
        adata = cellxgene_census.get_anndata(
            census,
            organism="Homo sapiens",
            var_value_filter=f"feature_id in {ensembl_ids!r}",
            obs_value_filter=value_filter,
            obs_column_names=["cell_type", "tissue_general", "donor_id", "dataset_id"],
        )

    log.info("Raw fetch: %d cells x %d genes", adata.n_obs, adata.n_vars)

    # tiledbsoma 2.x uses integer soma IDs as var index; rename to gene symbols directly.
    adata.var_names = adata.var["feature_name"].tolist()
    adata.var.index.name = "gene_symbol"
    log.info("Gene symbols: %s", adata.var_names)

    # Drop under-represented cell types
    counts = adata.obs["cell_type"].value_counts()
    keep = counts[counts >= MIN_CELLS_PER_TYPE].index
    adata = adata[adata.obs["cell_type"].isin(keep)].copy()
    log.info(
        "After min-cells filter: %d cells, %d cell types",
        adata.n_obs,
        adata.obs["cell_type"].nunique(),
    )

    # Subsample to at most MAX_CELLS_PER_TYPE per cell type to keep H5AD < 100 MB.
    # 5000 cells per type >> the 600 needed for stable metacell correlations.
    MAX_CELLS_PER_TYPE = 5000
    import numpy as np

    rng = np.random.default_rng(42)
    idx = []
    for ct, grp in adata.obs.groupby("cell_type"):
        n = len(grp)
        if n > MAX_CELLS_PER_TYPE:
            chosen = rng.choice(grp.index, size=MAX_CELLS_PER_TYPE, replace=False)
        else:
            chosen = grp.index.values
        idx.extend(chosen.tolist())
    adata = adata[idx].copy()
    log.info(
        "After subsample (max %d/type): %d cells, %d cell types",
        MAX_CELLS_PER_TYPE,
        adata.n_obs,
        adata.obs["cell_type"].nunique(),
    )

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out = DATA_RAW / "nr1i2_atlas.h5ad"
    adata.write_h5ad(out)
    log.info("Wrote %s  (%.1f MB)", out, out.stat().st_size / 1e6)


if __name__ == "__main__":
    main()
