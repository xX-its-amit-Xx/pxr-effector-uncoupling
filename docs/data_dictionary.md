# Data dictionary — `data/processed/`

Every CSV/JSON in `data/processed/` is regenerated deterministically by
`scripts/run_*.py` (see [`reproducibility.md`](reproducibility.md)). The schemas
below describe every column and the formula behind each derived metric. Index
columns appear first (an empty leading column name `""` denotes that the first
CSV column is the unnamed index — pandas writes it without a header).

All cell-type-by-gene matrices use the Cell Ontology labels listed in
`src/pxr_uncoupling/config.py::CELL_TYPE_TISSUE_MAP`. All gene names are HGNC
symbols (occasional `<SYMBOL>_<ENSEMBL>` collisions, e.g. `F2_ENSG00000180210`,
arise where the atlas carries two records for one symbol).

## 1. Conventions and shared formulas

| Symbol / metric          | Definition                                                                                                                                                                                                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cell type *c*            | Cell Ontology label from CELLxGENE Census `obs.cell_type`.                                                                                                                                                                                                                                              |
| Metacell                 | k-means cluster of cells in 30-dim PCA space, target size 30 cells/metacell (`TARGET_CELLS_PER_METACELL`). See `src/pxr_uncoupling/coupling.py::build_metacells`.                                                                                                                                        |
| Coupling ρ<sub>c,g</sub> | Spearman correlation between the per-metacell mean expression of NR1I2 and gene *g*, computed within cell type *c*. Cells with fewer than `MIN_METACELLS = 20` metacells are dropped.                                                                                                                   |
| Decoupling score DS      | DS<sub>c,g</sub> = ρ<sub>hepatocyte,g</sub> − ρ<sub>c,g</sub>. Large positive ⇒ gene is hepatocyte-coupled but uncoupled in *c*. See `coupling.py::decoupling_score`.                                                                                                                                   |
| Bootstrap CI             | 500-resample percentile bootstrap over metacell rows; ρ recomputed on resampled rows; α/2 and 1−α/2 quantiles (α = 0.05). See `statistics.py::bootstrap_coupling_ci`.                                                                                                                                   |
| Empirical p-value        | Two-sided fraction of |ρ<sub>null</sub>| ≥ |ρ<sub>obs</sub>|. Null: NR1I2 metacell vector permuted 500× within the cell type. Add-one smoothing: p = (extreme + 1) / (n<sub>perm</sub> + 1). See `statistics.py::permutation_pvalues`.                                                                  |
| q-value                  | Benjamini–Hochberg FDR adjustment over the full (cell-type × gene) family of non-NaN p-values. See `statistics.py::benjamini_hochberg`.                                                                                                                                                                 |
| log<sub>2</sub>FC        | log<sub>2</sub>(CPM + 1) of treated minus log<sub>2</sub>(CPM + 1) of vehicle, averaged across donor technical replicates then differenced per donor. CPM = counts × 10⁶ / library size. See `scripts/run_geo_rifampicin.py::_log2_cpm`, `_per_donor_logfc`.                                            |
| Signature strength L1    | Mean absolute value across landmark genes of the centroid LINCS L1000 signature: ⟨|x̄<sub>g</sub>|⟩<sub>g∈landmarks</sub>. Higher ⇒ more coherent transcriptional shift. See `scripts/run_lincs.py`.                                                                                                    |
| Signature strength L2    | √(⟨x̄<sub>g</sub>²⟩<sub>g</sub>) of the centroid signature vector. Penalises few high-magnitude features less than L1.                                                                                                                                                                                  |
| intra-line ρ             | Median pairwise Spearman ρ between replicate rifampicin signatures from the same cell line; characterises signal-to-noise.                                                                                                                                                                              |
| Open Targets score       | Per-disease association score from the Open Targets Platform GraphQL API (`associatedDiseases.rows[].score`); 0 = no evidence, 1 = strong multi-evidence.                                                                                                                                               |

## 2. Cell-type × gene matrices (10 rows × 20 genes)

All five matrices below share the same structure: index = cell type label,
columns = the 20 canonical PXR target genes (see
`data/targets/pxr_canonical_targets.tsv`). The first CSV column is the unnamed
cell-type index (pandas default), and values are floats in [−1, 1] (or [0, 1]
for the p/q matrices). NaN is emitted when a cell type was dropped (too few
metacells) or a gene was missing from the atlas.

### `coupling.csv`

Per-cell-type Spearman ρ(NR1I2, gene) from metacell means. Generated by
`scripts/run_analysis.py` via `coupling_per_cell_type`.

### `decoupling.csv`

DS<sub>c,g</sub> = ρ<sub>hepatocyte,g</sub> − ρ<sub>c,g</sub>. 9 rows × 20
columns (the hepatocyte row is removed during subtraction). Positive ⇒
hepatocyte-selective coupling.

### `coupling_pvalues.csv`

Two-sided empirical p-values per (cell type, gene). See "Empirical p-value"
formula above. Generated by `scripts/run_robustness.py` via
`permutation_pvalues`.

### `coupling_qvalues.csv`

Benjamini–Hochberg FDR q-values over the entire matrix of p-values (single
combined family, n_tests = number of finite p-values). Generated by
`scripts/run_robustness.py` via `benjamini_hochberg`.

### `coupling_ci_lower.csv`, `coupling_ci_median.csv`, `coupling_ci_upper.csv`

Per-cell-type 95 % percentile-bootstrap interval bounds on ρ. The triple is
emitted together: `lower` = 2.5th percentile of bootstrap ρ values, `median` =
50th percentile, `upper` = 97.5th percentile. Generated by
`scripts/run_robustness.py` via `bootstrap_coupling_ci` (500 resamples by
default; matches the production run).

## 3. Negative-control comparison

### `control_coupling.csv`

Same shape and columns as `coupling.csv` but for the 20 matched negative-control
genes (10 liver-enriched non-PXR-targets, 5 hepatocyte master TFs, 5
housekeeping genes). Header row begins:
`ALB, TF, APOA1, APOA2, APOB, HP, FGB, F2_ENSG00000180210, SERPINA1, TTR,
HNF4A, HNF1A, FOXA1, FOXA2, CEBPA, GAPDH, ACTB, B2M, PPIA, HPRT1`. See
`data/targets/negative_control_genes.tsv` for the curation rationale.

### `control_decoupling.csv`

DS<sub>c,g</sub> for the same 20 control genes, with hepatocyte as the
reference. Should be near zero or negative for genes that are
hepatocyte-broad-active (HNF4A) and negative for housekeeping genes.

### `control_comparison.json`

Mann–Whitney U test (one-sided, "PXR-target DS > control DS") comparing the
flattened DS distributions. Fields:

| Field                     | Meaning                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `u`                       | Mann–Whitney U statistic.                                                                                     |
| `pvalue`                  | One-sided p-value (`alternative="greater"`).                                                                  |
| `median_target`           | Median DS across all non-NaN PXR-target (cell type × gene) cells.                                             |
| `median_null`             | Median DS across all non-NaN control (cell type × gene) cells.                                                |
| `n_target`, `n_null`      | Sample sizes after NaN removal.                                                                               |
| `target_genes_used`       | Ordered list of the 20 PXR-target gene symbols.                                                               |
| `control_genes_used`      | Ordered list of the 20 control gene symbols.                                                                  |
| `target_genes_missing`    | PXR-target symbols requested but absent from the atlas (currently empty).                                     |
| `control_genes_missing`   | Control symbols requested but absent from the atlas (currently empty).                                        |
| `per_cell_type`           | Per-cell-type sub-dict: `target_mean_DS`, `control_mean_DS`, `target_minus_control` (each is a float).        |

### `control_comparison_per_cell_type.csv`

Flat table version of the `per_cell_type` map above. Index column (unnamed) =
cell type. Columns:

| Column                 | Meaning                                                          |
| ---------------------- | ---------------------------------------------------------------- |
| `target_mean_DS`       | Mean DS across PXR-target genes for that cell type.              |
| `control_mean_DS`      | Mean DS across control genes for that cell type.                 |
| `target_minus_control` | Difference; positive ⇒ PXR targets right-shifted over controls.  |

## 4. GTEx bulk-tissue validation

All three files are indexed by GTEx tissue label (e.g. `Liver`,
`Small_Intestine_Terminal_Ileum`, `Whole_Blood`). The gene column set is
`CYP2C8, CYP2C9, SLCO1B1, ABCC2, CYP3A5, ALB, HNF4A, GAPDH` (5 top hep-selective
PXR targets + 3 controls). See `scripts/run_gtex.py`.

### `gtex_coupling.csv`

Within-tissue Spearman ρ(NR1I2, gene) across donors. NaN ⇒ <5 paired samples
available for that tissue/gene.

### `gtex_coupling_pvalues.csv`

Two-sided p-value from the same `scipy.stats.spearmanr` call (asymptotic
approximation; no permutation null because GTEx donor-level sample sizes
permit it).

### `gtex_per_tissue_n.csv`

Per-tissue sample sizes. Columns: `n_nr1i2` (NR1I2 sample count) and one
`n_<GENE>` column per gene. Differences between `n_nr1i2` and `n_<gene>`
indicate the GTEx API returned mismatched sample sets for that gene/tissue
pair; affected rows are flagged in the run log.

### `gtex_summary.csv`

Per-gene roll-up. Index column = gene symbol. Columns:

| Column               | Meaning                                                                                            |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| `liver_rho`          | ρ(NR1I2, gene) in GTEx `Liver`.                                                                    |
| `intestine_mean_rho` | Mean ρ across intestinal-grouped tissues (small intestine, colon, stomach, oesophagus mucosa).     |
| `immune_mean_rho`    | Mean ρ across immune-grouped tissues (whole blood, spleen, EBV-transformed lymphocytes).           |
| `liver_minus_immune` | Headline contrast: `liver_rho` − `immune_mean_rho`.                                                |

## 5. GEO GSE139896 — direct rifamycin perturbation of primary hepatocytes

Source: Dyavar et al. (2020), 3 donors × {rifampin 10 µM, rifabutin 5 µM,
rifapentine 10 µM} × methanol vehicle, 72 h, primary human hepatocytes.
Generated by `scripts/run_geo_rifampicin.py` from
`data/cache/GSE139896_processed.xlsx`.

### `geo_rifamycin_logFC.csv`

Long-form per-donor log<sub>2</sub>FC table. Columns:

| Column       | Meaning                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------- |
| `drug`       | One of `rifampin`, `rifabutin`, `rifapentine`.                                                       |
| `gene`       | HGNC symbol of the queried gene (panel + controls + NR1I2).                                          |
| `gene_class` | `PXR panel`, `negative control`, or `receptor (NR1I2)`.                                              |
| `donor`      | Donor ID (`8210`, `4119B`, `4079`).                                                                  |
| `log2FC`     | log<sub>2</sub>(CPM<sub>treated</sub> + 1) − log<sub>2</sub>(CPM<sub>vehicle</sub> + 1) for the donor (mean over the 2 tech reps). |

### `geo_rifamycin_stats.csv`

Per-(drug, gene) summary. Columns:

| Column          | Meaning                                                                                |
| --------------- | -------------------------------------------------------------------------------------- |
| `drug`          | One of `rifampin`, `rifabutin`, `rifapentine`.                                         |
| `gene`          | HGNC symbol.                                                                           |
| `gene_class`    | `PXR panel`, `negative control`, or `receptor (NR1I2)`.                                |
| `n_donors`      | Number of donors contributing to the stats row (3 by design).                          |
| `mean_log2FC`   | Mean of the 3 donor log<sub>2</sub>FC values.                                          |
| `median_log2FC` | Median of the 3 donor log<sub>2</sub>FC values.                                        |
| `std_log2FC`    | Sample SD (ddof=1) of the donor log<sub>2</sub>FC values.                              |
| `t_stat`        | One-sample paired t-statistic of `log2FC` vs 0 (`scipy.stats.ttest_rel(vals, 0)`).     |
| `p_value`       | Two-sided p-value from the same test (df = 2).                                         |

### `geo_rifamycin_summary.json`

Top-level summary. Fields:

| Field                              | Meaning                                                                                |
| ---------------------------------- | -------------------------------------------------------------------------------------- |
| `n_donors`                         | Donor count (3).                                                                       |
| `drugs_tested`                     | Ordered drug list.                                                                     |
| `panel_mean_log2FC_per_drug`       | Mean log<sub>2</sub>FC across the 6 PXR-panel genes, per drug.                         |
| `control_mean_log2FC_per_drug`     | Same averaging for the 3 control genes.                                                |
| `panel_minus_control_per_drug`     | Per-drug difference (`panel - control`).                                               |
| `note`                             | Dataset-level methods note (concentrations, exposure time, replicate collapse).        |

## 6. LINCS L1000 rifampicin signatures

Generated by `scripts/run_lincs.py` from the per-signature TSVs cached in
`data/cache/lincs_LINCSCP_*.tsv`.

### `lincs_signature_strength.csv`

Per-cell-line summary, sorted descending by `signature_strength_L1`.

| Column                  | Meaning                                                                                                                |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `cellline`              | iLINCS cell line name (e.g. `HEPG2`, `HT29`, `MCF7`).                                                                  |
| `tissue`                | Tissue of origin as returned by iLINCS (may be empty for some lines).                                                  |
| `n_signatures`          | Number of independent rifampicin signatures available for the line.                                                    |
| `signature_strength_L1` | Mean |log fold change| across landmark genes of the centroid signature (see §1).                                       |
| `signature_strength_L2` | √(mean squared log fold change) of the centroid signature.                                                             |
| `intra_line_rho_median` | Median pairwise Spearman ρ between same-line signatures across the 978 landmark genes (NaN if `n_signatures < 2`).     |
| `intra_line_n_pairs`    | Number of pairwise comparisons used (C(n_signatures, 2)).                                                              |

### `lincs_summary.json`

Headline metrics for the LINCS check. Fields:

| Field                                          | Meaning                                                                            |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| `n_signatures_total`                           | Total signatures successfully downloaded and aligned.                              |
| `n_landmark_genes`                             | Number of landmark genes present in every signature after intersection (≈ 978).    |
| `n_cell_lines`                                 | Cell line count.                                                                   |
| `HEPG2_signature_strength_L1`                  | L1 strength for HEPG2 (the only hepatic cell line in L1000 with multiple sigs).    |
| `HT29_signature_strength_L1`                   | L1 strength for HT29 (the only intestinal cell line; comparison baseline).         |
| `non_hepatic_signature_strength_L1_mean`       | Mean L1 strength across non-hepatic, non-intestinal cell lines.                    |
| `HEPG2_signature_strength_ratio_vs_others`     | `HEPG2_signature_strength_L1 / non_hepatic_signature_strength_L1_mean`.            |
| `HEPG2_intra_line_rho_median`                  | Median intra-line ρ for HEPG2 (signal-to-noise).                                   |
| `non_hepatic_intra_line_rho_median_mean`       | Mean of the per-line intra-line median ρ across non-hepatic, non-intestinal lines. |
| `note`                                         | Methods caveat about L1000 landmark coverage.                                      |

## 7. Per-dataset reproducibility (hepatocyte)

Generated by `scripts/run_per_dataset.py`.

### `per_dataset_hepatocyte.csv`

Hepatocyte coupling ρ recomputed within each CELLxGENE `dataset_id` that
contributes ≥ 300 hepatocyte cells, with metacell parameters relaxed
(`cells_per_metacell = 15`, `min_metacells = 10`) so small datasets still
yield a row. Index column = CELLxGENE dataset UUID; columns = the 20 PXR
target genes.

### `per_dataset_summary.json`

| Field                | Meaning                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------- |
| `n_datasets`         | Datasets included (≥ 300 hepatocyte cells, ≥ 10 metacells after k-means).                                  |
| `n_pairs`            | Number of pairwise inter-dataset comparisons used (C(n_datasets, 2), minus any with <3 finite genes).      |
| `median_pairwise_rho`| Median pairwise Spearman ρ between dataset coupling vectors — the "are datasets seeing the same signal?" headline. |
| `min_pairwise_rho`   | Minimum pairwise ρ across dataset pairs.                                                                   |
| `max_pairwise_rho`   | Maximum pairwise ρ across dataset pairs.                                                                   |

## 8. Robustness — parameter sensitivity sweep

Generated by `scripts/run_robustness.py` (`parameter_sweep` + `matrix_agreement`).

### `sensitivity_sweep.csv`

Long-form per-parameter coupling matrix dump. Columns:

| Column                | Meaning                                                                                |
| --------------------- | -------------------------------------------------------------------------------------- |
| `cells_per_metacell`  | k-means target metacell size (grid: 15, 30, 60).                                       |
| `min_metacells`       | Per-cell-type drop threshold (grid: 10, 20).                                           |
| `seed`                | Random seed for PCA + KMeans (grid: 0, 42, 123).                                       |
| `cell_type`           | Cell Ontology label.                                                                   |
| `gene`                | HGNC gene symbol.                                                                      |
| `rho`                 | Spearman ρ(NR1I2, gene) for this parameter combination.                                |

### `sensitivity_agreement.csv`

Per-parameter-combination agreement vs the reference setting
`(cells_per_metacell=30, min_metacells=20, seed=42)`. One row per non-reference
combination. Columns:

| Column                   | Meaning                                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------------- |
| `cells_per_metacell`     | Parameter value.                                                                                         |
| `min_metacells`          | Parameter value.                                                                                         |
| `seed`                   | Parameter value.                                                                                         |
| `frobenius_distance`     | Frobenius distance ‖A − A<sub>ref</sub>‖<sub>F</sub> over the common (cell type × gene) cells.           |
| `spearman_of_decoupling` | Spearman ρ between this run's per-gene mean DS ranking and the reference run's ranking.                  |
| `jaccard_top5`           | Jaccard overlap of the top-5 hepatocyte-selective genes between this run and the reference.              |

## 9. Robustness — 80 % cell subsample stability

Generated by `scripts/run_robustness.py` (`subsample_stability` +
`stability_summary`).

### `subsample_stability.csv`

Long-form per-iteration ρ values. Columns:

| Column      | Meaning                                                                              |
| ----------- | ------------------------------------------------------------------------------------ |
| `iteration` | 0…(n_iterations − 1); n_iterations = 20 by default.                                  |
| `cell_type` | Cell Ontology label.                                                                 |
| `gene`      | HGNC gene symbol.                                                                    |
| `rho`       | Spearman ρ(NR1I2, gene) on the 80 %-subsampled cell set, per iteration.              |

### `subsample_summary.csv`

Per-(cell type, gene) collapse of the 20 iterations. Columns:

| Column      | Meaning                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------- |
| `cell_type` | Cell Ontology label.                                                                              |
| `gene`      | HGNC gene symbol.                                                                                 |
| `mean`      | Mean of `rho` across iterations.                                                                  |
| `std`       | Sample SD (ddof=1) of `rho` — the headline noise metric (median ≈ 0.022 in production).           |
| `ci_low`    | 2.5th-percentile ρ across iterations.                                                             |
| `ci_high`   | 97.5th-percentile ρ across iterations.                                                            |
| `n_iter`    | Iterations contributing (20 unless a cell type was dropped on some iterations).                   |

## 10. Open Targets external validation

Generated by `scripts/run_opentargets.py` against the per-gene cache in
`data/cache/opentargets_<SYMBOL>.json`.

### `opentargets_per_gene.csv`

One row per queried gene. Columns:

| Column                    | Meaning                                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| `gene_symbol`             | HGNC symbol.                                                                                         |
| `ensembl_id`              | Ensembl gene identifier used for the API query.                                                      |
| `group`                   | `receptor` (NR1I2), `PXR target (top hepatocyte-selective)`, or `negative control`.                  |
| `n_disease_associations`  | Total associated diseases returned by Open Targets for the gene (`target.associatedDiseases.count`). |
| `n_drug_response_top50`   | Number of "drug response / pharmacogenomics" phenotypes in the top-50 associated diseases.           |
| `drug_response_fraction`  | `n_drug_response_top50 / 50`.                                                                        |

### `opentargets_top_diseases.csv`

One row per (gene, top-5 disease). Columns:

| Column              | Meaning                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| `gene_symbol`       | HGNC symbol.                                                           |
| `group`             | Same gene group as in `opentargets_per_gene.csv`.                      |
| `disease_name`      | Disease label (EFO ontology).                                          |
| `score`             | Open Targets association score (0–1).                                  |
| `therapeutic_areas` | Semicolon-joined list of EFO therapeutic-area annotations.             |

### `opentargets_summary.json`

Nested structure with two keys:

- `per_gene` — dict keyed by gene symbol with the same fields as
  `opentargets_per_gene.csv` (Ensembl ID, group, counts, fractions).
- `top_diseases` — dict keyed by gene symbol; each value is a list of up-to-5
  `{disease_name, score, therapeutic_areas}` records (one per top disease).

## 11. Atlas provenance

Generated by `scripts/build_provenance.py` from the cached
`data/raw/nr1i2_atlas.h5ad`.

### `atlas_provenance.csv`

Per (cell type, CELLxGENE dataset) row. Columns:

| Column        | Meaning                                                          |
| ------------- | ---------------------------------------------------------------- |
| `cell_type`   | Cell Ontology label.                                             |
| `dataset_id`  | CELLxGENE dataset UUID.                                          |
| `n_cells`     | Cells contributed by that dataset to that cell type (post 1,500 cap). |
| `n_donors`    | Unique donors contributing.                                      |

### `atlas_summary.json`

| Field                    | Meaning                                                              |
| ------------------------ | -------------------------------------------------------------------- |
| `n_cells_total`          | Total cells in the cached atlas.                                     |
| `n_genes`                | Total genes (NR1I2 + 20 PXR targets + 20 controls).                  |
| `n_cell_types`           | Distinct cell-ontology labels passing the `MIN_CELLS_PER_TYPE` cut.  |
| `n_datasets`             | Distinct CELLxGENE datasets contributing.                            |
| `n_donors`               | Distinct donors contributing.                                        |
| `cells_per_cell_type`    | Dict: cell type → cell count.                                        |
| `donors_per_cell_type`   | Dict: cell type → unique donor count.                                |
| `datasets_per_cell_type` | Dict: cell type → unique dataset count.                              |
