# pxr-effector-uncoupling

A cell-type-resolved map of which PXR (NR1I2) target genes stay coupled to receptor expression vs. which decouple — nominating hepatocyte-selective readouts for next-generation PXR modulators.

![Decoupling heatmap](figures/final_heatmap.png)

## Key Finding

Five PXR target genes show strong hepatocyte-selective coupling (high Spearman ρ in hepatocytes, near-zero in all other profiled cell types):

| Gene | Mean Decoupling Score | Hepatocyte ρ |
|------|-----------------------|--------------|
| CYP2C8 | 0.809 | 0.793 |
| CYP2C9 | 0.802 | 0.875 |
| SLCO1B1 | 0.746 | 0.739 |
| ABCC2 | 0.735 | 0.789 |
| CYP3A5 | 0.719 | 0.810 |

These genes are functionally coupled to PXR in hepatocytes but uncoupled in immune cells, enterocytes, and trophoblasts — supporting hepatocyte-selective target engagement as a design criterion for tissue-restricted PXR agonists.

## Methods

### Data
- **Source**: CELLxGENE Census v2025-01-30 (`cellxgene-census`)
- **Cells**: 46,884 human primary cells (≤5,000 per cell type, random seed 42)
- **Genes**: NR1I2 + 20 curated PXR canonical target genes (see `data/targets/pxr_canonical_targets.tsv`)

### Cell Types Profiled

| Cell type | Tissue |
|-----------|--------|
| hepatocyte | liver |
| enterocyte of epithelium of small intestine | small intestine |
| enterocyte of epithelium of large intestine | large intestine |
| intestinal crypt stem cell | small intestine |
| macrophage | liver |
| monocyte | blood |
| natural killer cell | blood |
| CD4-positive, alpha-beta T cell | blood |
| CD8-positive, alpha-beta T cell | blood |
| extravillous trophoblast | placenta |

### Coupling Score
For each cell type, cells are aggregated into metacells (k-means on log1p-PCA, `cells_per_metacell=30`, `min_metacells=10`). Spearman ρ between NR1I2 and each target gene is computed across metacell mean profiles. Coupling ρ ∈ [−1, 1]; high positive values indicate co-expression with the receptor.

### Decoupling Score
Decoupling score = ρ_hepatocyte − ρ_other. Positive values indicate stronger hepatocyte coupling relative to a given cell type. Mean decoupling score across all non-hepatocyte cell types is reported.

## Repository Layout

```
data/
  targets/          curated PXR target gene set (checked in)
  processed/        coupling.csv, decoupling.csv (checked in)
figures/            final_heatmap.png (checked in)
notebooks/          01_nr1i2_atlas.ipynb
scripts/
  fetch_atlas.py    CELLxGENE Census fetch (runs on Ubuntu/glibc)
  run_analysis.py   full coupling → decoupling → heatmap pipeline
src/pxr_uncoupling/ reusable Python package
  config.py         constants and gene lists
  coupling.py       metacell coupling math
  plotting.py       heatmap renderer
  cellxgene.py      Census data access utilities
tests/              unit tests for coupling math
```

## Reproducing

### 1. Fetch the atlas (requires Ubuntu/glibc — see note below)

```bash
# Trigger via GitHub Actions (handles the glibc requirement automatically)
gh workflow run fetch_atlas.yml

# Then pull the H5AD onto your local machine:
git fetch origin data/atlas
git checkout origin/data/atlas -- data/raw/nr1i2_atlas.h5ad
```

> **Alpine/musl note**: `cellxgene-census` uses TileDB's C++ thread pool, which deadlocks on musl pthreads. The fetch workflow runs on `ubuntu-latest` to avoid this. Once the H5AD is local, all downstream analysis (coupling, heatmap) runs fine on any platform.

### 2. Run the analysis

```bash
uv sync
uv run python scripts/run_analysis.py
```

Outputs written to `data/processed/` and `figures/`.

### 3. Explore in notebooks

```bash
uv run jupyter lab
# Open notebooks/01_nr1i2_atlas.ipynb
```

## References

- Lehmann JM et al. (1998) The human orphan nuclear receptor PXR is activated by compounds that regulate CYP3A4 gene expression. *J Clin Invest* 102:1016–1023.
- Baran Y et al. (2019) MetaCell: analysis of single-cell RNA-seq data using K-nn graph partitions. *Genome Biol* 20:206.
- CZI Single-Cell Biology Program et al. (2023) CZ CELLxGENE Discover: A single-cell data platform for scalable exploration, analysis and modeling. *bioRxiv*.

## License

MIT. Copyright 2026 Amit Shenoy.
