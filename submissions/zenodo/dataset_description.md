# Zenodo deposit — pxr-effector-uncoupling (v0.2.0)

## Summary

This deposit archives the complete software, processed data, figures, and manuscript text for an end-to-end reproducible analysis of pregnane X receptor (PXR; NR1I2) target-gene coupling across 446,672 single human cells (10 cell types). The deposit accompanies the manuscript "Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response" by Amit Shenoy (Northeastern University, 2026).

The Zenodo DOI is intended as the canonical, persistent citation point for the software and the derived data, complementing the GitHub repository (which provides ongoing development).

## What is in the deposit

The deposit is a ZIP archive of the project repository at tag v0.2.0:

### Source code (`src/pxr_uncoupling/`)
Reusable Python modules implementing the metacell-coupling framework: Census data access (`cellxgene.py`), metacell construction + per-cell-type Spearman correlation (`coupling.py`), bootstrap CIs / permutation p-values / Benjamini-Hochberg FDR (`statistics.py`), parameter sweep and subsample stability (`sensitivity.py`), and main + supplementary plotting (`plotting.py`, `supplementary_plots.py`).

### Entry-point scripts (`scripts/`)
Twelve runnable scripts that drive the analysis end-to-end:
- `fetch_atlas.py` — CELLxGENE Census fetch (Ubuntu/glibc)
- `run_analysis.py` — coupling, decoupling, main heatmap
- `run_robustness.py` — bootstrap, permutation, sensitivity, subsample
- `render_supp_figures.py` — supplementary figure render
- `run_negative_control.py`, `run_gtex.py`, `run_geo_rifampicin.py`, `run_lincs.py`, `run_opentargets.py` — five external validation pipelines
- `run_per_dataset.py`, `build_provenance.py`, `render_annotated_figs.py` — provenance and figure annotation

### Notebooks (`notebooks/`)
Five Jupyter notebooks walking through atlas QC, coupling computation, decoupling scores, heatmap rendering, and robustness diagnostics.

### Processed data (`data/processed/`)
- `coupling.csv`, `coupling_ci_lower.csv`, `coupling_ci_median.csv`, `coupling_ci_upper.csv`, `coupling_pvalues.csv`, `coupling_qvalues.csv` — main coupling matrix with 500-resample bootstrap CIs and permutation-derived BH-FDR q-values
- `decoupling.csv` — decoupling score DS_g per gene
- `control_coupling.csv`, `control_decoupling.csv`, `control_comparison.json`, `control_comparison_per_cell_type.csv` — matched-control replication (Mann-Whitney U p = 1.0 x 10^-31)
- `gtex_coupling.csv`, `gtex_coupling_pvalues.csv`, `gtex_per_tissue_n.csv`, `gtex_summary.csv` — GTEx v8 bulk-tissue replication
- `geo_rifamycin_logFC.csv`, `geo_rifamycin_stats.csv`, `geo_rifamycin_summary.json` — direct rifamycin perturbation in primary human hepatocytes (GSE139896)
- `lincs_signature_strength.csv`, `lincs_summary.json` — LINCS L1000 rifampicin response across 18 cell lines
- `opentargets_per_gene.csv`, `opentargets_top_diseases.csv`, `opentargets_summary.json` — Open Targets disease-association validation
- `sensitivity_sweep.csv`, `sensitivity_agreement.csv` — parameter sweep agreement
- `subsample_stability.csv`, `subsample_summary.csv` — 80% subsample stability
- `per_dataset_hepatocyte.csv`, `per_dataset_summary.json` — per-dataset hepatocyte coupling stability
- `atlas_provenance.csv`, `atlas_summary.json` — per-dataset cell counts

### Curated gene tables (`data/targets/`)
- `pxr_canonical_targets.tsv` — 20 PXR target genes graded A/B with PMID-tagged evidence
- `negative_control_genes.tsv` — 20 matched negative-control genes (10 liver-enriched non-PXR + 5 hepatocyte master TFs + 5 housekeeping)

### Figures (`figures/`)
All seven main and three supplementary PNG figures referenced in the manuscript, rendered from the processed CSVs.

### Manuscript (`manuscript/`)
Full Markdown source of the manuscript, including all sections, references, and figure callouts.

### Reproducibility infrastructure
- `pyproject.toml`, `uv.lock` — pinned Python 3.12 environment (scanpy 1.10, anndata 0.10, scikit-learn 1.5, scipy 1.13, statsmodels 0.14, httpx 0.27, matplotlib 3.9)
- `tests/` — 16 passing pytest unit tests
- `.github/workflows/` — CI (lint + tests) and `fetch_atlas.yml` (Ubuntu-only Census fetch workaround for the musl/TileDB-SOMA pthreads deadlock)
- `CITATION.cff` — citation metadata (Citation File Format)
- `LICENSE` — MIT license for source code

## What is NOT in the deposit (and why)

- **Raw CELLxGENE Census H5AD** (`data/raw/nr1i2_atlas.h5ad`, ~600 MB): excluded because it is mechanically reproducible from CELLxGENE Census v2025-01-30 by re-running the fetch workflow on Ubuntu. Including it would duplicate publicly addressable data that is itself versioned.
- **Local virtualenv** (`.venv/`): excluded; recreate via `uv sync`.
- **Local cache files** (`__pycache__/`, `.pytest_cache/`): excluded.

## Licensing

| Asset class | License |
|-------------|---------|
| Source code, scripts, notebooks | MIT |
| Figures, processed data, manuscript text | CC-BY-4.0 |
| Curated gene tables (`data/targets/`) | CC-BY-4.0 |

The MIT license file is in the repository root; the CC-BY-4.0 designation applies to the non-code artefacts as noted in the deposit metadata.

## How to reproduce from the deposit

```bash
unzip pxr-effector-uncoupling-v0.2.0.zip
cd pxr-effector-uncoupling
uv sync
uv run pytest -v                              # 16 tests, all pass
uv run python scripts/render_supp_figures.py  # re-render figures from cached CSVs
```

To re-derive from CELLxGENE Census on a fresh machine, follow the GitHub Actions workflow `fetch_atlas.yml` (the fetch step requires Ubuntu/glibc).

## Citation

If you use this software or its results, please cite both:

1. **This Zenodo deposit** (DOI: assigned upon deposit; see CITATION.cff in the deposit for the citation block).
2. **The manuscript** (see `manuscript/manuscript.md`).

A `CITATION.cff` file is included for automated citation extraction.
