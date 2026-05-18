# pxr-effector-uncoupling

A cell-type-resolved, statistically-grounded map of which PXR (NR1I2) target genes stay coupled to receptor expression vs. which decouple — distinguishing epithelial-barrier tissues (liver + intestine) where PXR drives a transcriptional program from immune and placental tissues where it does not, and nominating hepatocyte-selective readouts for next-generation PXR modulators.

![Decoupling heatmap](figures/final_heatmap.png)

## Key Finding

Five canonical PXR target genes show strong, statistically significant coupling to NR1I2 in hepatocytes and effectively no coupling in other cell types:

| Gene | Mean DS | Hepatocyte ρ (95% CI) | BH q-value (hepatocyte) |
|------|---------|------------------------|--------------------------|
| CYP2C8  | 0.866 | 0.89 (0.82 – 0.93) | 0.0105 |
| CYP2C9  | 0.821 | 0.93 (0.88 – 0.96) | 0.0105 |
| SLCO1B1 | 0.790 | 0.87 (0.83 – 0.91) | 0.0105 |
| ABCC2   | 0.769 | 0.86 (0.81 – 0.91) | 0.0105 |
| CYP3A5  | 0.724 | 0.90 (0.86 – 0.93) | 0.0105 |

CIs from 500-resample percentile bootstrap of metacells; q-values from a metacell-label permutation null (500 permutations, two-sided), BH-adjusted across the full (cell type × gene) family of 200 tests.

After BH-FDR correction, **16 of 20** PXR target genes reach q < 0.05 in hepatocytes. The next most-coupled cell types are intestinal epithelium — **11/20** in small-intestine enterocytes, **10/20** in intestinal crypt stem cells, **3/20** in large-intestine enterocytes — exactly the tissues with documented PXR-driven CYP3A4 induction and clinical drug-drug interactions (Lehmann et al. 1998, Geick et al. 2001). **0/20** in any of the four immune cell types (CD4 T, CD8 T, NK, macrophage), 0/20 in monocytes, 0/20 in extravillous trophoblast, 1/20 (likely false positive) in NK cells. The pattern is **epithelial barrier vs. circulating/immune** — PXR-coupled where it matters for xenobiotic exposure (liver + gut), decoupled where the receptor is transcribed but has no programmatic readout (blood / placenta).

These results support hepatocyte-selective target engagement as a design criterion for tissue-restricted PXR agonists in cholestasis and metabolic indications.

### Specificity vs. matched negative controls

We re-ran the same pipeline on a curated 20-gene negative-control set (10 liver-enriched non-PXR-target genes — ALB, TF, APOA1/2, APOB, HP, FGB, F2, SERPINA1, TTR; 5 hepatocyte master TFs — HNF4A, HNF1A, FOXA1/2, CEBPA; 5 housekeeping genes — GAPDH, ACTB, B2M, PPIA, HPRT1) and tested whether the PXR-target decoupling distribution is shifted right of the control distribution.

| Metric | PXR targets (n=20) | Negative controls (n=20) |
|--------|--------------------|--------------------------|
| Median decoupling score | **0.665** | −0.029 |
| Per-cell-type mean DS (range) | 0.26 – 0.66 | −0.34 – 0.07 |

**Mann-Whitney U (one-sided): p = 5.7 × 10⁻²⁷**. In every cell type the mean PXR-target decoupling score exceeds the matched-control mean by 0.37 to 0.64 units. This rules out the alternative explanation that decoupling reflects a generic hepatocyte-vs-others signature; it is specific to PXR target genes.

See `figures/supp_negative_control.png` for the distribution comparison and per-cell-type breakdown, and `data/targets/negative_control_genes.tsv` for the control-gene curation.

## Robustness

The headline pattern is stable across analytical choices:

| Check | Result |
|-------|--------|
| Bootstrap CI excludes 0 (top-5 genes, hepatocyte) | All 5 |
| BH-FDR q < 0.05 (top-5 genes, hepatocyte) | All 5 |
| Spearman of decoupling rankings vs. reference, across 18 parameter combinations | median **0.97** |
| Top-5 hepatocyte-selective gene set Jaccard vs. reference, across 18 combinations | 1.00 at every combination |
| Std of ρ across 20 × 80% cell-level subsamples, per (cell_type, gene) | median **0.051** |

See `figures/supp_*.png` and `notebooks/05_robustness.ipynb` for full diagnostics.

## Methods

### Data
- **Source**: CELLxGENE Census v2025-01-30 (`cellxgene-census` 1.17.x)
- **Filter**: `is_primary_data == True`, organism = *Homo sapiens*
- **Subsampling**: capped at 5,000 cells per cell type (random seed 42) to keep the H5AD < 100 MB
- **Final atlas**: 46,884 cells × 41 genes (NR1I2 + 20 curated PXR canonical targets + 20 negative-control genes); see `data/targets/pxr_canonical_targets.tsv` for evidence-graded target curation (PMIDs included) and `data/targets/negative_control_genes.tsv` for the matched control set

### Cell types profiled (n = 10)

| Cell type | Tissue grouping |
|-----------|-----------------|
| hepatocyte | liver |
| enterocyte of epithelium of small intestine | intestine |
| enterocyte of epithelium of large intestine | intestine |
| intestinal crypt stem cell | intestine |
| macrophage | immune |
| monocyte | immune |
| natural killer cell | immune |
| CD4-positive, alpha-beta T cell | immune |
| CD8-positive, alpha-beta T cell | immune |
| extravillous trophoblast | placenta |

Cell types with fewer than `MIN_CELLS_PER_TYPE=50` cells in the Census query are dropped. See `scripts/build_provenance.py` for per-dataset cell counts.

### Coupling score
Per cell type:
1. Log1p-transform counts, then 30-dim PCA.
2. k-means in PCA space with `k = n_cells / cells_per_metacell` (`cells_per_metacell = 30`).
3. Mean expression per metacell (genes × metacells).
4. Spearman ρ between NR1I2 metacell profile and each target gene profile.
5. Cell types with fewer than `MIN_METACELLS = 20` metacells are dropped.

Metacelling controls for technical sparsity in single-cell counts and yields stable correlation estimates (Baran et al. 2019; Persad et al. 2023).

### Decoupling score
For each non-hepatocyte cell type *c* and gene *g*:

$$\text{DS}_{c,g} \;=\; \rho_{\text{hepatocyte},\,g} \;-\; \rho_{c,\,g}$$

Positive values flag genes coupled in hepatocytes but uncoupled in *c*. The mean over *c* ranks genes by hepatocyte selectivity.

### Statistical inference
- **CIs**: 500-resample percentile bootstrap over metacell rows.
- **Null distribution**: NR1I2 expression is shuffled across metacells within a cell type 500 times, breaking the NR1I2-target relationship while preserving marginal distributions and metacell structure.
- **Two-sided empirical p-values**: fraction of |ρ_null| ≥ |ρ_observed| (add-one smoothing).
- **Multiple-testing correction**: Benjamini-Hochberg FDR over the full 10 × 20 cell-type-gene family.

### Sensitivity sweep
The pipeline is re-run with `cells_per_metacell ∈ {15, 30, 60}`, `min_metacells ∈ {10, 20}`, and `random_state ∈ {0, 42, 123}` (18 combinations). Agreement vs. the reference combination (cpm=30, mm=20, seed=42) is quantified by Frobenius distance of coupling matrices, Spearman ρ of decoupling rankings, and Jaccard overlap of the top-5 hepatocyte-selective genes.

### Subsample stability
Cells are subsampled to 80% within each cell type 20 times and the coupling pipeline is re-run on each subsample. Per-(cell_type, gene) std characterizes the contribution of cell-sampling noise.

## Limitations

- **No experimental perturbation.** Spearman ρ is a co-expression measure, not a causal claim. Genes flagged as decoupled may still be PXR-responsive under appropriate ligand exposure; the analysis identifies *baseline transcriptional coupling*, which is a necessary-but-not-sufficient condition for a useful pharmacodynamic readout.
- **Census composition bias.** Cell-type counts reflect the studies deposited in CELLxGENE; hepatocyte numbers (and donor diversity) are dominated by a handful of large liver atlases. Per-dataset stability (`figures/supp_per_dataset_hepatocyte.png`) shows that the coupling pattern strength **varies considerably across datasets** (median pairwise ρ of coupling vectors = 0.33 across 5 eligible hepatocyte datasets, range −0.09 to 0.66). One large dataset carries most of the signal; smaller datasets show weaker but directionally-consistent coupling. This is a real limitation: a future iteration should re-fetch without the 5,000-cell-per-type subsampling cap so each dataset retains its full cell complement, and should extend per-dataset analysis to intestinal cell types. See `data/processed/atlas_provenance.csv` for the full dataset breakdown.
- **NR1I2 sparsity in immune cells.** PXR transcript is rarely detected in T/NK cells; "no coupling" can reflect *no signal* rather than *real independence*. We avoid this trap by requiring `MIN_METACELLS ≥ 20`, but power is still asymmetric across cell types — interpret null calls cautiously.
- **Curated target set.** The 20-gene panel is conservative (evidence grade A/B from PMID-tagged primary literature). Adding speculative targets would inflate FDR cost without changing the headline.
- **Single ontology.** All cell types are Cell Ontology labels from CELLxGENE. The hepatocyte label aggregates periportal/pericentral zones that may differ in PXR activity; future work could re-run within published zonation labels.
- **musl/Alpine fetch deadlock.** TileDB-SOMA's thread pool deadlocks on musl pthreads, so the *fetch* must run on glibc (e.g. GitHub Actions Ubuntu). Once the H5AD is cached, all downstream analysis runs on any platform.

## Repository Layout

```
data/
  raw/                    nr1i2_atlas.h5ad (not committed; fetched via gh workflow)
  targets/                pxr_canonical_targets.tsv  (PMID-tagged target curation)
  processed/              coupling.csv, decoupling.csv, coupling_ci_*.csv,
                          coupling_{p,q}values.csv, sensitivity_*.csv,
                          subsample_*.csv, atlas_provenance.csv
figures/
  final_heatmap.png       Main figure
  supp_heatmap_significance.png   Coupling ρ with q-value overlay
  supp_forest_hepatocyte.png      Top-10 ρ with 95% CIs
  supp_sensitivity.png            Decoupling-rank agreement across parameter sweep
  supp_subsample_stability.png    Per-cell-type ρ std under 80% subsampling
  supp_negative_control.png       PXR targets vs 20 matched negative controls
  supp_per_dataset_hepatocyte.png Coupling vectors per CELLxGENE dataset
notebooks/
  01_nr1i2_atlas.ipynb    Atlas QC and NR1I2 detection
  02_coupling.ipynb       Metacell coupling — walkthrough + full computation
  03_decoupling.ipynb     Decoupling score, gene ranking
  04_heatmap.ipynb        Final heatmap render
  05_robustness.ipynb     Bootstrap CIs, FDR, sensitivity, stability
scripts/
  fetch_atlas.py          CELLxGENE Census fetch (Ubuntu/glibc)
  run_analysis.py         End-to-end coupling → decoupling → heatmap
  run_robustness.py       Bootstrap + permutation + sensitivity + subsample
  render_supp_figures.py  Render supplementary figures
  build_provenance.py     Per-dataset cell-count table
src/pxr_uncoupling/
  config.py               Constants, gene lists, palettes
  coupling.py             Metacell builder + per-cell-type Spearman ρ
  statistics.py           Bootstrap CIs, permutation p-values, BH-FDR
  sensitivity.py          Parameter sweep + subsample stability
  plotting.py             Main heatmap
  supplementary_plots.py  Forest, FDR overlay, sensitivity, stability
  cellxgene.py            Census data access utilities
tests/                    pytest unit tests (16 tests, all passing)
.github/workflows/
  fetch_atlas.yml         Census fetch on Ubuntu (workaround for musl)
  ci.yml                  Lint + tests on push / PR
CITATION.cff              Citation metadata
```

## Reproducing

### Option A — start from cached outputs (no Census fetch required)

`data/processed/` already contains every CSV generated by the analysis. The heatmaps in `figures/` can be re-rendered from those CSVs:

```bash
uv sync --extra dev
uv run python scripts/run_analysis.py        # only re-derives if H5AD present
uv run python scripts/render_supp_figures.py
```

### Option B — full re-derivation from CELLxGENE Census

```bash
# 1. Fetch the atlas — runs on Ubuntu via GitHub Actions
gh workflow run fetch_atlas.yml
gh run watch
git fetch origin data/atlas
git checkout origin/data/atlas -- data/raw/nr1i2_atlas.h5ad

# 2. Compute coupling, decoupling, heatmap
uv run python scripts/run_analysis.py

# 3. Run robustness analyses (≈ 2 min)
uv run python scripts/run_robustness.py

# 4. Render supplementary figures
uv run python scripts/render_supp_figures.py

# 5. Tests
uv run pytest -v
```

> **musl/Alpine note**: `cellxgene-census` uses TileDB's C++ thread pool, which deadlocks on musl pthreads. The fetch workflow runs on `ubuntu-latest` to avoid this. Once the H5AD is local, all downstream analysis runs fine on Alpine, Windows, or macOS.

## Citation

Please cite as described in [`CITATION.cff`](CITATION.cff).

## References

- Lehmann JM et al. (1998) The human orphan nuclear receptor PXR is activated by compounds that regulate CYP3A4 gene expression and cause drug interactions. *J Clin Invest* **102**:1016–1023. doi:10.1172/JCI3703
- Baran Y et al. (2019) MetaCell: analysis of single-cell RNA-seq data using K-nn graph partitions. *Genome Biol* **20**:206. doi:10.1186/s13059-019-1812-2
- Persad S et al. (2023) SEACells infers transcriptional and epigenomic cellular states from single-cell genomics data. *Nat Biotechnol* **41**:1746–1757. doi:10.1038/s41587-023-01716-9
- Benjamini Y, Hochberg Y (1995) Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J R Stat Soc B* **57**:289–300.
- Efron B (1979) Bootstrap methods: another look at the jackknife. *Ann Stat* **7**:1–26.
- CZI Single-Cell Biology Program et al. (2023) CZ CELLxGENE Discover: A single-cell data platform for scalable exploration, analysis and modeling of aggregated data. *bioRxiv*. doi:10.1101/2023.10.30.563174

## License

MIT. Copyright 2026 Amit Shenoy.
