"""Build per-dataset provenance table from the cached atlas.

For each (cell_type × dataset_id) pair, count cells and donors. This is the
table reviewers will want to see when asking 'is this signal driven by a single
dataset or donor?'

Inputs : data/raw/nr1i2_atlas.h5ad
Outputs: data/processed/atlas_provenance.csv
         data/processed/atlas_summary.json
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

from pxr_uncoupling.config import DATA_PROCESSED, DATA_RAW  # noqa: E402


def main() -> None:
    h5ad = DATA_RAW / "nr1i2_atlas.h5ad"
    adata = ad.read_h5ad(h5ad)
    log.info("Loaded %d cells × %d genes", adata.n_obs, adata.n_vars)

    obs = adata.obs.copy()

    prov = (
        obs.groupby(["cell_type", "dataset_id"], observed=True)
        .agg(n_cells=("donor_id", "size"), n_donors=("donor_id", "nunique"))
        .reset_index()
        .sort_values(["cell_type", "n_cells"], ascending=[True, False])
    )
    out = DATA_PROCESSED / "atlas_provenance.csv"
    prov.to_csv(out, index=False)
    log.info("Wrote %s (%d rows)", out, len(prov))

    summary = {
        "n_cells_total": int(adata.n_obs),
        "n_genes": int(adata.n_vars),
        "n_cell_types": int(obs["cell_type"].nunique()),
        "n_datasets": int(obs["dataset_id"].nunique()),
        "n_donors": int(obs["donor_id"].nunique()),
        "cells_per_cell_type": obs["cell_type"].value_counts().to_dict(),
        "donors_per_cell_type": (
            obs.groupby("cell_type", observed=True)["donor_id"].nunique().to_dict()
        ),
        "datasets_per_cell_type": (
            obs.groupby("cell_type", observed=True)["dataset_id"].nunique().to_dict()
        ),
    }
    sum_out = DATA_PROCESSED / "atlas_summary.json"
    with sum_out.open("w") as fh:
        json.dump(summary, fh, indent=2, default=str)
    log.info("Wrote %s", sum_out)

    print("\n=== ATLAS PROVENANCE ===")
    print(f"Cells       : {summary['n_cells_total']:,}")
    print(f"Cell types  : {summary['n_cell_types']}")
    print(f"Datasets    : {summary['n_datasets']}")
    print(f"Donors      : {summary['n_donors']}")
    print("\nPer cell type (cells / donors / datasets):")
    for ct, n in sorted(summary["cells_per_cell_type"].items(), key=lambda kv: -kv[1]):
        d = summary["donors_per_cell_type"].get(ct, 0)
        ds = summary["datasets_per_cell_type"].get(ct, 0)
        print(f"  {ct:<50} {n:>6,}  {d:>3}d  {ds:>2}ds")


if __name__ == "__main__":
    main()
