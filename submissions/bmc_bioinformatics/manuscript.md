# A reusable metacell-coupling pipeline for cell-type-resolved nuclear-receptor target analysis at single-cell atlas scale, applied to PXR (NR1I2) across 446,672 human cells

**Authors:** Amit Shenoy¹*

¹ Northeastern University, Boston, MA, USA.

\* Correspondence: shenoy.am@husky.neu.edu

---

## Abstract

**Background.** Single-cell RNA-seq atlases of unprecedented scale (CELLxGENE Census, ~75 million cells) now make it possible to ask cell-type-resolved questions about transcription-factor / target-gene coupling that bulk-tissue analyses cannot answer. The computational obstacle is that per-cell count sparsity precludes stable per-gene correlation estimates. Metacell aggregation has been proposed as a remedy, but a complete, statistically grounded, parameter-validated, and orthogonally cross-checked pipeline for nuclear-receptor / target-gene coupling at atlas scale — together with an end-to-end reproducible reference implementation — has not been demonstrated.

**Results.** We present a metacell-coupling pipeline that (i) constructs cell-type-stratified metacells by k-means in PCA space, (ii) computes per (cell type, gene) Spearman rank correlation between a receptor of interest and its candidate target panel, (iii) ranks genes by a decoupling score relative to a reference cell type, and (iv) quantifies confidence by a 500-resample percentile bootstrap of metacell rows, statistical significance by a label-shuffling permutation null with Benjamini-Hochberg FDR control across the full cell-type x gene family, parameter robustness by a sweep over (cells_per_metacell, min_metacells, seed), and subsample stability by 20-round 80% cell-level resampling. We additionally provide orchestration scripts for four independent external validations of any candidate gene panel produced by the pipeline: GTEx v8 bulk RNA-seq cross-tissue replication, GEO direct perturbation overlay, LINCS L1000 cell-line signature analysis, and Open Targets disease-association overlay. As a worked example and methods-validation case, we applied the pipeline to PXR (NR1I2) and a curated 20-gene canonical target panel across 446,672 single cells from 10 cell types in CELLxGENE Census v2025-01-30. The pipeline recovered a hepatocyte-selective coupling pattern (six genes with Spearman rho 0.77 to 0.89, BH q approximately 0.004) that was: stable across a 17-combination parameter sweep (median Spearman rho of decoupling rankings vs reference = 0.95); discriminated from a matched 20-gene negative-control set (Mann-Whitney U one-sided p = 1.0 x 10^-31, including correct decoupling of hepatocyte master TFs HNF4A and HNF1A); replicated in GTEx v8 across 54 tissues (liver-immune rho delta +0.21 to +0.56 for all five top genes); confirmed for four of the six top genes (CYP2C8, CYP2C9, CYP3A5, ABCC2) by direct rifamycin perturbation of primary human hepatocytes (GSE139896); and consistent with HEPG2 ranking first of 18 LINCS L1000 cell lines for rifampicin signature strength. The pipeline runs end-to-end in under five minutes on a workstation once the input H5AD is cached.

**Conclusions.** The metacell-coupling pipeline is reusable for any (nuclear receptor or transcription factor) x (target panel) x (cell-type atlas) combination with sufficient cell-type coverage. The reference implementation is MIT-licensed, CI-tested, and pinned to specific dependency versions through `uv.lock`. As a methods-validation by-product, the PXR application identifies a four-gene hepatocyte-selective biomarker panel (CYP2C8, CYP2C9, CYP3A5, ABCC2) for next-generation PXR-targeted drug development.

**Keywords:** metacells, single-cell RNA-seq, coupling analysis, nuclear receptor, PXR, NR1I2, CELLxGENE, reproducible bioinformatics, pharmacogenomics.

---

## Background

A central use of single-cell RNA-seq atlases is to ask, for each cell type independently, whether a regulator of interest is functionally coupled to its candidate target genes — a question bulk tissue cannot answer because it averages over heterogeneous cell populations. The pregnane X receptor (PXR; NR1I2) — the master transcriptional sensor of xenobiotic exposure [1,2] — provides a motivating example: NR1I2 transcript is detected in hepatocytes, intestinal epithelia, immune cells, and placental cells, yet it is unknown whether the canonical PXR target program (CYP3A4, CYP2C, ABC transporters, etc.) is engaged in all four compartments or selectively in hepatic and intestinal barriers. The clinical stakes are large: PXR-driven CYP3A4 induction underlies the rifampicin-warfarin, rifampicin-oral contraceptive, and St. John's wort-cyclosporine drug-drug interactions that motivate FDA guidance [3,4].

The technical obstacle is that per-cell single-cell counts are too sparse to support stable per-gene correlation estimates: any single cell expresses only ~10 to 20% of detected transcripts, and dropout swamps the per-cell correlation between two genes. Metacell construction — grouping transcriptionally similar cells before computing co-expression statistics — has been shown to recover regulatory structure [5,6]. CELLxGENE Census [7] unifies hundreds of studies under a common ontology with ~75 million cells, removing the per-dataset bottleneck. Yet a complete pipeline that combines these advances and additionally provides parameter-robustness diagnostics, subsample stability, multiple-testing correction, and orchestrated external validation against bulk RNA-seq, perturbation, drug-signature, and disease-association databases — together with a working open-source reference implementation — has not been published in unified form.

Here we present such a pipeline and validate it on the PXR / NR1I2 question. The methodological contribution is the pipeline, its diagnostics, and the orchestrated validation scripts; the biological by-product (an actionable hepatocyte-selective four-gene PXR pharmacodynamic panel) is itself useful for drug discovery but is presented here primarily as a methods-validation case.

---

## Implementation

### Pipeline overview

The pipeline takes three user inputs:
1. A list of Cell Ontology terms specifying which cell types to query.
2. A regulator gene of interest (e.g., NR1I2).
3. A candidate target gene panel and (optionally) a matched negative-control gene panel.

It produces:
1. A coupling matrix (cell types x genes) of Spearman rho values.
2. A decoupling score per gene (rho in a reference cell type minus mean rho in the others).
3. Bootstrap 95% CIs (lower/upper/median) and permutation-derived BH-FDR q-values.
4. Parameter-sweep agreement and subsample stability summaries.
5. Optional external-validation reports (GTEx, GEO, LINCS, Open Targets).
6. Publication-grade figures.

### Modules (`src/pxr_uncoupling/`)

- `cellxgene.py` — CELLxGENE Census data access. Subsets the Census to user-specified Cell Ontology terms and target genes, with primary-data filtering (`is_primary_data == True`), per-(cell type, dataset_id) capping (default 1,500 cells; configurable), and reproducible random subsampling.

- `coupling.py` — Per cell type, log1p-normalises raw counts, projects onto 30 principal components, partitions cells into metacells by k-means with k = n_cells / `cells_per_metacell` (default 30), computes metacell-mean expression, and returns a per-(cell type, gene) Spearman rho versus the regulator gene's metacell-mean profile. Cell types with fewer than `min_metacells` (default 20) are excluded.

- `statistics.py` — Confidence intervals via 500-resample percentile bootstrap over metacell rows. Permutation null shuffles regulator-gene expression across metacells within each cell type 500 times (preserving marginal distributions). Two-sided empirical p-values with add-one smoothing. Benjamini-Hochberg [8] FDR correction across the full cell-type x gene test family.

- `sensitivity.py` — Parameter sweep over (cells_per_metacell, min_metacells, random_state). Computes Spearman rho of decoupling-rank vectors vs reference, Jaccard overlap of top-N gene sets, and Frobenius distance of coupling matrices. Subsample stability via N-round x% cell-level resampling.

- `plotting.py` + `supplementary_plots.py` — Main coupling heatmap, BH-FDR overlay, top-N forest plot with bootstrap CIs, negative-control comparison panel, parameter-sensitivity panel, subsample-stability panel.

### Orchestration scripts (`scripts/`)

- `fetch_atlas.py` — CELLxGENE Census fetch (Ubuntu/glibc; workaround for the musl/TileDB-SOMA pthreads deadlock via GitHub Actions).
- `run_analysis.py` — End-to-end: coupling, decoupling, main heatmap (~2 min).
- `run_robustness.py` — Bootstrap, permutation, sensitivity, subsample (~2 min).
- `render_supp_figures.py` — Supplementary panels (~30 s).
- `run_negative_control.py` — Re-runs the pipeline on a matched-control gene panel and computes the Mann-Whitney U test of decoupling-score distributions.
- `run_gtex.py`, `run_geo_rifampicin.py`, `run_lincs.py`, `run_opentargets.py` — Four external-validation pipelines, each taking the candidate top genes from `run_analysis.py` as input.
- `run_per_dataset.py`, `build_provenance.py`, `render_annotated_figs.py` — Per-dataset analyses and figure annotation.

### Reproducibility infrastructure

- **Pinned environment:** Python 3.12; scanpy 1.10; anndata 0.10; scikit-learn 1.5; scipy 1.13; statsmodels 0.14; httpx 0.27; matplotlib 3.9. Lock file (`uv.lock`) committed.
- **Continuous integration:** `.github/workflows/ci.yml` runs lint + 16 pytest unit tests on every push and pull request.
- **Atlas-fetch workflow:** `.github/workflows/fetch_atlas.yml` runs the Census fetch on Ubuntu (cellxgene-census on musl deadlocks because of a TileDB-SOMA pthreads bug; the cached H5AD is committed to a `data/atlas` branch).
- **Citation:** `CITATION.cff` at the repository root.
- **License:** MIT for code; CC-BY-4.0 for figures, processed data, and manuscript.

### Demonstration application

The PXR demonstration was run with cell types: hepatocyte; enterocyte of epithelium of small intestine; enterocyte of epithelium of large intestine; intestinal crypt stem cell; macrophage; monocyte; CD4-positive alpha-beta T cell; CD8-positive alpha-beta T cell; natural killer cell; extravillous trophoblast. Regulator: NR1I2. Target panel: 20 canonical PXR targets, PMID-graded A/B. Control panel: 20 matched controls (10 liver-enriched non-PXR genes; 5 hepatocyte master TFs; 5 housekeeping). Atlas size after subsampling: 446,672 cells.

---

## Results

### Pipeline output: coupling, decoupling, and stability

The pipeline identified six PXR target genes with strong hepatocyte coupling — CYP2C9 (rho = 0.89, 95% CI 0.880 to 0.921, BH q = 0.004), CYP3A5 (0.87, 0.861 to 0.890, q = 0.004), ABCC2 (0.85, 0.824 to 0.857, q = 0.004), SLCO1B1 (0.85, 0.820 to 0.859, q = 0.004), CYP2C8 (0.81, 0.804 to 0.849, q = 0.004), and CPT1A (0.77, 0.755 to 0.810, q = 0.004) — all crossing q approximately 0.004 after BH correction across the full 10 x 20 cell-type-by-gene test family (Fig. 1; Fig. 2). The top six genes by decoupling score — SLCO1B1 (0.756), CYP2C9 (0.698), CYP2C8 (0.695), ABCC2 (0.677), CPT1A (0.658), and CYP3A5 (0.631) — separated cleanly from the remaining 14 targets (all with DS < 0.6).

In immune cell types, the same genes reached formal significance at the available sample size (10 to 16 of 20 genes per type) but with effect sizes 4 to 8 fold smaller (mean rho 0.03 to 0.12; top-gene rho 0.19 to 0.24 in CD4+ T, macrophage, monocyte, NK; ~0.09 in CD8+ T). Intestinal epithelia recovered an intermediate signal (12/20, 10/20, 7/20 across small intestine, crypt stem cell, large intestine). Extravillous trophoblast showed 0/20 significant (mean rho 0.014).

### Pipeline diagnostics: parameter and subsample robustness

The parameter sweep over 17 combinations (cells_per_metacell in {15, 30, 60} x min_metacells in {10, 20} x seed in {0, 42, 123}; one cpm = 60 combination dropped because k-means could not recover >= 10 metacells from the smallest cell types) yielded median Spearman rho of decoupling rankings vs the reference combination of **0.95** (range 0.90 to 1.00; Fig. S1). The top-4 panel was recovered in every parameter combination; the 5th-slot Jaccard had median 0.67 because CPT1A and CYP3A5 sit at the boundary of selectivity (DS within ~0.03) and swap rank under different metacell granularity. The 80% cell-level subsampling check (20 rounds per cell type) yielded median per-(cell type, gene) rho standard deviation of **0.022** (Fig. S2), well below the effect-size differences of interest.

The per-dataset hepatocyte analysis (Fig. S3) yielded median pairwise rho of 0.337 across five datasets contributing >= 300 cells (range -0.19 to +0.74), indicating between-dataset variance is study-level heterogeneity (donor characteristics; sample handling; sequencing platform) rather than a sample-size limitation. Top-5 gene identity was preserved across this variance.

### Negative-control discrimination

Re-running the identical pipeline on a curated 20-gene matched control set showed the PXR-target decoupling distribution shifted markedly right of the control distribution: median DS 0.575 vs -0.126; Mann-Whitney U one-sided p = 1.0 x 10^-31 (Fig. 3). The hepatocyte master TFs HNF4A and HNF1A — themselves hepatocyte-selective — did not show high decoupling, confirming the signal is specific to NR1I2-target coupling rather than a generic hepatocyte-marker pattern. This is, by design, the strongest internal-specificity check the pipeline can run: matched controls drawn from the same tissue with no PXR-target curation should produce zero decoupling signal, and indeed they do.

### External validation: four independent modalities recover the prediction

The pipeline's external-validation modules each take the top-ranked output genes and overlay them on a different external dataset.

- **GTEx v8 (bulk RNA-seq across 54 tissues; `run_gtex.py`).** Within-tissue Spearman rho(NR1I2, target) across donors recovered the same liver-vs-immune contrast for all five top genes (delta +0.21 to +0.56; Fig. 4).
- **GSE139896 (direct rifamycin perturbation of primary human hepatocytes; `run_geo_rifampicin.py`).** Four of the six top genes (CYP2C8, CYP2C9, CYP3A5, ABCC2) were directionally induced by all three rifamycins (rifampin, rifabutin, rifapentine; 1.5 to 19-fold induction across drugs; CYP2C8 reached p < 0.05 across all three rifamycins despite n = 3 donors; Fig. 5) [9]. SLCO1B1 and CPT1A did not respond — a useful refinement: their hepatocyte coupling most likely reflects shared regulation by HNF4A and FOXA1/2 rather than direct PXR control.
- **LINCS L1000 (18 cell lines; `run_lincs.py`).** HEPG2 ranked first of 18 cell lines in rifampicin signature strength (mean |log fold change| over 978 landmark genes = 0.59 vs non-hepatic mean 0.40, 1.47x; replicate consistency median pairwise Spearman rho = 0.31 across 15 within-HEPG2 pairs; Fig. 6). HT29 (the only intestinal line, poorly-differentiated colorectal-adenocarcinoma) ranked lowest.
- **Open Targets v4 (`run_opentargets.py`).** The top 5 hep-selective genes recovered textbook PXR pharmacology in the curated disease graph (warfarin/CYP2C9, statins/SLCO1B1, Dubin-Johnson/ABCC2, tacrolimus and HIV/CYP3A5, drug-metabolism cancers/CYP2C8; Fig. 7); matched controls (ALB, HNF4A, GAPDH) showed no pharmacology signature.

### Worked-example output: the actionable biomarker panel

By coupling the metacell pipeline output to direct perturbation, the worked example identifies four genes — CYP2C8, CYP2C9, CYP3A5, ABCC2 — as the actionable hepatocyte-selective PXR pharmacodynamic readouts. This is the kind of biological output the pipeline is designed to produce: a small, validated, decision-relevant gene panel ranked by cell-type selectivity and triangulated against orthogonal evidence.

---

## Discussion

The pipeline is general. It can be applied to any (regulator x target panel x cell-atlas) combination provided the atlas covers the cell types of interest with enough cells per type to support metacell construction at the default `cells_per_metacell = 30` (i.e., at least ~600 cells per cell type to recover the minimum 20 metacells). For receptors with substantial transcript sparsity (such as NR1I2 in immune cell types; detected in 5 to 22% of cells in our atlas), the pipeline correctly identifies coupling on the order of effect size rather than on significance alone, which is critical when sample sizes vary by orders of magnitude across cell types.

The most natural extensions are: applying the pipeline to other nuclear receptors with cell-type-selective biology (CAR/NR1I3, FXR/NR1H4, GR/NR3C1, RORs); applying it to non-receptor transcription factors; coupling the metacell aggregation step to alternative algorithms (e.g., SEACells [6] or MetaCell-2) and quantifying the impact on the decoupling-rank stability; and incorporating cell-type-matched chromatin-accessibility data to test mechanistic hypotheses about why a regulator is transcribed but not coupled in certain cell types.

Limitations of the pipeline as currently implemented are: (i) per-cell-type metacelling assumes a single regulatory programme within each cell type, which may break down for highly heterogeneous compartments (e.g., dendritic cells); (ii) the coupling measure is correlational by construction and should not be confused with causation; (iii) the per-dataset stability analysis bounds rather than estimates the true population coupling magnitude, particularly for atlases dominated by a small number of large studies. The negative-control specificity check, parameter sweep, subsample stability, and four external-validation modules together address these limitations to the extent possible without additional experimental data.

---

## Conclusions

We present a complete, reusable, methodologically grounded pipeline for cell-type-resolved regulator / target-gene coupling analysis at single-cell atlas scale, validated by application to PXR (NR1I2) across 446,672 cells. The PXR application identifies a four-gene biomarker panel for hepatocyte-selective PXR engagement (CYP2C8, CYP2C9, CYP3A5, ABCC2), confirmed by direct rifamycin perturbation. The pipeline runs end-to-end in under five minutes on a standard workstation once the input atlas is cached, is MIT-licensed and CI-tested, and is structured for direct re-use on any analogous regulator x cell-atlas question.

---

## Availability of data and materials

The complete reproducible pipeline is available at https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling under the MIT license, with locked dependencies in `pyproject.toml` and `uv.lock`. A Zenodo DOI will be minted upon acceptance to provide a persistent citation point.

All data sources used in the worked example are publicly accessible:
- CELLxGENE Census v2025-01-30 via the `cellxgene-census` Python API.
- GTEx v8 via the GTEx Portal v2 API (https://gtexportal.org/api/).
- GEO accession GSE139896 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE139896).
- iLINCS public API (https://ilincsdatasets.nih.gov/), library LIB_5.
- Open Targets Platform v4 GraphQL API (https://platform-api.opentargets.org/graphql).

All processed data files (coupling matrices, decoupling scores, bootstrap CIs, permutation p-values and BH-FDR q-values, parameter-sweep results, subsample-stability summaries, external-validation outputs, per-dataset analyses, and atlas provenance) are provided in `data/processed/` in the public repository.

Operating system: platform-independent (Linux, macOS, Windows) after the Census fetch step (which requires Ubuntu/glibc due to a TileDB-SOMA pthreads issue on musl; a GitHub Actions workflow is provided).
Programming language: Python 3.12.
Other requirements: scanpy 1.10, anndata 0.10, scikit-learn 1.5, scipy 1.13, statsmodels 0.14, httpx 0.27, matplotlib 3.9 (all pinned via `uv.lock`).
License: MIT.
Any restrictions to use by non-academics: none.

## Competing interests

The author declares no competing interests.

## Funding

This work received no external funding.

## Authors' contributions

**A.S.** designed the study, implemented the metacell-coupling pipeline, curated the target and control gene panels, performed all statistical analyses and external validations, generated all figures, and wrote the manuscript.

## Acknowledgements

The author acknowledges the CELLxGENE Census, GTEx, and Open Targets consortia for making their data and APIs publicly available.

---

## References

1. Kliewer SA, Moore JT, Wade L, Staudinger JL, Watson MA, Jones SA, et al. An orphan nuclear receptor activated by pregnanes defines a novel steroid signaling pathway. Cell. 1998;92:73-82.

2. Lehmann JM, McKee DD, Watson MA, Willson TM, Moore JT, Kliewer SA. The human orphan nuclear receptor PXR is activated by compounds that regulate CYP3A4 gene expression and cause drug interactions. J Clin Invest. 1998;102:1016-1023.

3. Geick A, Eichelbaum M, Burk O. Nuclear receptor response elements mediate induction of intestinal MDR1 by rifampin. J Biol Chem. 2001;276:14581-14587.

4. Tirona RG, Kim RB. Nuclear receptors and drug disposition gene regulation. J Pharm Sci. 2005;94:1169-1186.

5. Baran Y, Bercovich A, Sebe-Pedros A, Lubling Y, Giladi A, Chomsky E, et al. MetaCell: analysis of single-cell RNA-seq data using K-nn graph partitions. Genome Biol. 2019;20:206.

6. Persad S, Choo Z-N, Dien C, Sohail N, Masilionis I, Chaligne R, et al. SEACells infers transcriptional and epigenomic cellular states from single-cell genomics data. Nat Biotechnol. 2023;41:1746-1757.

7. CZI Single-Cell Biology Program, Abdulla S, Aevermann B, et al. CZ CELLxGENE Discover: A single-cell data platform for scalable exploration, analysis and modeling of aggregated data. bioRxiv. 2023. doi:10.1101/2023.10.30.563174.

8. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc B. 1995;57:289-300.

9. Dyavar SR, Mykris TM, Winchester LC, Scarsi KK, Fletcher CV, Podany AT. Hepatocytic transcriptional signatures predict comparative drug interaction potential of rifamycin antibiotics. Sci Rep. 2020;10:12565. doi:10.1038/s41598-020-69228-z.

10. Glaeser H, Drescher S, Eichelbaum M, Fromm MF. Influence of rifampicin on the expression and function of human intestinal cytochrome P450 enzymes. Br J Clin Pharmacol. 2005;59:199-206.

11. Pavek P. Pregnane X Receptor (PXR)-mediated gene repression and cross-talk of PXR with other nuclear receptors via coactivator interaction. Front Pharmacol. 2016;7:456.

12. Birdwell KA, Decker B, Barbarino JM, Peterson JF, Stein CM, Sadee W, et al. Clinical Pharmacogenetics Implementation Consortium (CPIC) guidelines for CYP3A5 genotype and tacrolimus dosing. Clin Pharmacol Ther. 2015;98:19-24.

13. Wang YM, Ong SS, Chai SC, Chen T. Role of CAR and PXR in xenobiotic sensing and metabolism. Expert Opin Drug Metab Toxicol. 2014;8:803-817.

14. Mencarelli A, Migliorati M, Barbanti M, Cipriani S, Palladino G, Distrutti E, et al. Pregnane-X-receptor mediates the anti-inflammatory activities of rifaximin on detoxification pathways in intestinal epithelial cells. Biochem Pharmacol. 2011;82:1675-1685.

15. Subramanian A, Narayan R, Corsello SM, et al. A next generation connectivity map: L1000 platform and the first 1,000,000 profiles. Cell. 2017;171:1437-1452.

16. Ochoa D, Hercules A, Carmona M, Suveges D, Baker J, Malangone C, et al. The next-generation Open Targets Platform: reimagined, redesigned, rebuilt. Nucleic Acids Res. 2023;51:D1353-D1359.

---

## Figures

**Figure 1.** Pipeline coupling output: PXR target coupling to NR1I2 across ten cell types (Spearman rho over metacells). See `figures/fig1_coupling_heatmap.png`.

**Figure 2.** Pipeline statistical diagnostics: BH-FDR overlay (a) and top-10 forest plot with 95% bootstrap CIs (b). See `figures/fig2a_significance_overlay.png` and `figures/fig2b_forest_hepatocyte.png`.

**Figure 3.** Pipeline negative-control discrimination: matched 20-gene control set decoupling distribution vs PXR-target distribution. See `figures/fig3_negative_control.png`.

**Figure 4.** External-validation module 1 (GTEx v8 bulk RNA-seq across 54 tissues). See `figures/fig4_gtex_validation.png`.

**Figure 5.** External-validation module 2 (GSE139896 direct rifamycin perturbation of primary human hepatocytes). See `figures/fig5_rifamycin_perturbation.png`.

**Figure 6.** External-validation module 3 (LINCS L1000 rifampicin signatures across 18 cell lines). See `figures/fig6_lincs_rifampicin.png`.

**Figure 7.** External-validation module 4 (Open Targets v4 disease-association graph). See `figures/fig7_opentargets.png`.

**Supplementary Figure S1.** Pipeline parameter-sweep diagnostics.

**Supplementary Figure S2.** Pipeline subsample-stability diagnostics.

**Supplementary Figure S3.** Pipeline per-dataset stability diagnostics.
