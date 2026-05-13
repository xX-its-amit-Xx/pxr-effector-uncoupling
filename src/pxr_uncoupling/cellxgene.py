"""CELLxGENE Census data access utilities."""

from __future__ import annotations

import logging
from pathlib import Path

import anndata as ad
import cellxgene_census
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from .config import (
    CENSUS_VERSION,
    DATA_PROCESSED,
    DATA_RAW,
    DATA_TARGETS,
    MIN_CELLS_PER_TYPE,
    NR1I2_ENSEMBL,
    NR1I2_SYMBOL,
    TISSUES_OF_INTEREST,
)

log = logging.getLogger(__name__)


def load_target_genes() -> pd.DataFrame:
    """Return the curated PXR target gene TSV as a DataFrame."""
    path = DATA_TARGETS / "pxr_canonical_targets.tsv"
    return pd.read_csv(path, sep="\t")


def get_gene_symbols(ensembl_ids: list[str]) -> dict[str, str]:
    """Map Ensembl IDs → gene symbols via Census var table (no data pull)."""
    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        var = (
            census["census_data"]["homo_sapiens"]
            .ms["RNA"]
            .var.read(
                column_names=["feature_id", "feature_name"],
                value_filter=f"feature_id in {ensembl_ids!r}",
            )
            .concat()
            .to_pandas()
        )
    return dict(zip(var["feature_id"], var["feature_name"]))


def fetch_expression(
    gene_ensembl_ids: list[str],
    cell_types: list[str] | None = None,
    tissues: list[str] | None = None,
    min_cells_per_type: int = MIN_CELLS_PER_TYPE,
) -> ad.AnnData:
    """
    Pull expression matrix for given genes from CELLxGENE Census.

    Filters to primary data only. Returns AnnData with gene-symbol var_names
    and cell_type / tissue_general obs columns.

    Parameters
    ----------
    gene_ensembl_ids:
        Ensembl IDs to pull. NR1I2 will be prepended if not already present.
    cell_types:
        Optional list of Cell Ontology cell_type labels to restrict to.
    tissues:
        Optional list of tissue_general labels to restrict to.
    min_cells_per_type:
        Drop cell types with fewer than this many cells after filtering.
    """
    if NR1I2_ENSEMBL not in gene_ensembl_ids:
        gene_ensembl_ids = [NR1I2_ENSEMBL] + list(gene_ensembl_ids)

    # organism is scoped by organism= in get_anndata(); omit organism_ontology_term_id.
    value_filter = "is_primary_data == True"
    if tissues:
        value_filter += f" and tissue_general in {tissues!r}"
    if cell_types:
        value_filter += f" and cell_type in {cell_types!r}"

    log.info("Opening Census version %s", CENSUS_VERSION)
    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        adata = cellxgene_census.get_anndata(
            census,
            organism="Homo sapiens",
            var_value_filter=f"feature_id in {gene_ensembl_ids!r}",
            obs_value_filter=value_filter,
            obs_column_names=["cell_type", "tissue_general", "donor_id", "dataset_id"],
        )

    # tiledbsoma 2.x uses integer soma IDs as var index; use feature_name directly.
    adata.var_names = adata.var["feature_name"].tolist()
    adata.var.index.name = "gene_symbol"

    # drop under-represented cell types
    counts = adata.obs["cell_type"].value_counts()
    keep = counts[counts >= min_cells_per_type].index
    adata = adata[adata.obs["cell_type"].isin(keep)].copy()
    log.info("After cell type filter: %d cells, %d cell types", adata.n_obs, adata.obs["cell_type"].nunique())

    return adata


def cache_expression(adata: ad.AnnData, tag: str) -> Path:
    """Write AnnData to data/raw/<tag>.h5ad and return the path."""
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    path = DATA_RAW / f"{tag}.h5ad"
    adata.write_h5ad(path)
    log.info("Cached %d cells to %s", adata.n_obs, path)
    return path


def load_cached(tag: str) -> ad.AnnData:
    """Load a previously cached AnnData from data/raw/<tag>.h5ad."""
    path = DATA_RAW / f"{tag}.h5ad"
    if not path.exists():
        raise FileNotFoundError(f"No cached file at {path}. Run fetch_expression first.")
    return ad.read_h5ad(path)
