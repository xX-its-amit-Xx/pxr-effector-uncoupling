# Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response

**Authors:** Amit Shenoy¹*

¹ Northeastern University, Boston, MA, USA.

\* shenoy.am@husky.neu.edu

---

## Abstract

The pregnane X receptor (PXR; NR1I2) regulates xenobiotic metabolism, but target-gene responses are typically studied in bulk liver or transformed cell lines and assumed to generalise across cell types where the receptor is detected. We tested this assumption at single-cell resolution. Using CELLxGENE Census v2025-01-30, we computed per-cell-type metacell correlations between NR1I2 and 20 canonical PXR target genes across 446,672 single human cells (10 cell types). Six canonical targets — CYP2C9, CYP3A5, ABCC2, SLCO1B1, CYP2C8, and CPT1A — show strong coupling in hepatocytes (Spearman rho = 0.77 to 0.89, BH q approximately 0.004) and only weak baseline coupling in immune and placental cells (mean rho 0.03 to 0.12 in immune; 0.014 in placenta), a 4 to 8 fold effect-size differential even though immune cells reach formal significance at our sample sizes (50 to 110 k cells per type). Intestinal epithelia recover an intermediate signal. The pattern is epithelial-barrier-selective, not generically hepatic: a matched 20-gene negative-control set is decoupled (PXR vs control median DS 0.575 vs -0.126; Mann-Whitney U one-sided p = 1.0 x 10^-31). The headline replicates in GTEx v8 bulk RNA-seq across 54 tissues (liver-immune rho differential +0.21 to +0.56 for all five genes); direct rifamycin perturbation of primary human hepatocytes (GSE139896) confirms four of the six top genes (CYP2C8, CYP2C9, CYP3A5, ABCC2) as PXR-responsive with up to 19-fold induction; HEPG2 ranks first of 18 LINCS L1000 cell lines for rifampicin signature strength; and Open Targets flags the top genes as drug-response loci. The four-gene panel CYP2C8 / CYP2C9 / CYP3A5 / ABCC2 is identified as the actionable hepatocyte-selective pharmacodynamic readout for next-generation PXR modulators; the metacell-coupling framework is reusable for any receptor x cell-atlas pair.

---

## Introduction

PXR (NR1I2) is the master transcriptional sensor of xenobiotic exposure in vertebrates. Activated by structurally diverse small molecules — rifampicin, hyperforin, paclitaxel, statins, and many marketed drugs — PXR induces a coordinated program of phase I/II metabolism (CYP3A4, CYP2C, UGTs, GSTs) and phase III efflux transport (MDR1, MRP2/3, OATPs)^1,2^. The clinical reach of this program is large: approximately half of metabolised drugs are CYP3A substrates, and PXR-driven CYP3A4 induction is the molecular basis of the rifampicin-warfarin, rifampicin-oral contraceptive, and St. John's wort-cyclosporine interactions that motivate FDA drug-drug interaction guidance^3,4^. Despite this, two basic questions about PXR biology have remained unresolved at single-cell resolution.

First, across the cell types where NR1I2 transcript is detected, is the receptor functionally coupled to its canonical targets, or only co-expressed? Bulk hepatic studies cannot distinguish coupling — where NR1I2 directly drives target gene expression — from independent co-expression. Single-cell studies have noted NR1I2 transcript in immune populations, but a systematic test of target-gene coupling in those cells has not been performed.

Second, which subset of canonical PXR targets is the most cell-type-selective readout of receptor activity in hepatocytes? Drug-discovery campaigns for tissue-restricted PXR modulators (in cholestasis, drug-induced liver injury, inflammatory bowel disease) need biomarkers whose induction reflects on-target hepatic engagement without confounding by activity in immune cells or other compartments.

The computational obstacle is that single-cell RNA-seq counts are too sparse for stable per-gene correlation estimates: any single cell expresses only ~10 to 20% of detected transcripts. Two recent methodological advances make the problem tractable. First, metacelling — k-nearest-neighbour or k-means aggregation in a reduced-dimensional space — yields stable transcriptional units whose pairwise expression correlations recover regulatory structure^5,6^. Second, CELLxGENE Census^7^ unifies hundreds of single-cell studies under a common ontology with ~75 million cells, enabling cross-tissue analyses that no single dataset can support.

We combine these advances to ask: for each canonical PXR target gene, does the cell-type-specific NR1I2-target coupling distinguish hepatocytes from circulating and barrier cell types? We then validate the result against six orthogonal layers — parameter and subsampling robustness, a matched 20-gene negative-control set, GTEx bulk RNA-seq across 54 tissues, direct rifamycin perturbation of primary human hepatocytes (GSE139896^8^), LINCS L1000 rifampicin perturbation responses across 18 cell lines^9^, and the Open Targets Platform v4 disease-association graph^10^. The convergence of these lines of evidence supports a small set of hepatocyte-selective transcriptional readouts for PXR engagement and challenges the implicit assumption that NR1I2 detection in non-hepatic cell types reflects functional coupling.

---

## Results

### A unified single-cell atlas of NR1I2 and its canonical targets across ten cell types

The final atlas contained 446,672 cells across 10 Cell Ontology classes (hepatocyte; small/large intestinal enterocyte; intestinal crypt stem cell; CD4+ and CD8+ alpha-beta T cell; NK cell; macrophage; monocyte; extravillous trophoblast), drawn from ~20 underlying CELLxGENE Census datasets and capped at 1,500 cells per (cell type, dataset_id) to balance representation. NR1I2 was detected (count > 0) in 78% of hepatocytes, 31 to 55% of intestinal cells, and 5 to 22% of immune cells, reflecting the well-known transcript sparsity of NR1I2 outside the liver.

### Metacell coupling reveals a hepatocyte-selective signature

Six genes — CYP2C9 (rho = 0.89, 95% CI 0.880 to 0.921), CYP3A5 (0.87, 0.861 to 0.890), ABCC2 (0.85, 0.824 to 0.857), SLCO1B1 (0.85, 0.820 to 0.859), CYP2C8 (0.81, 0.804 to 0.849), and CPT1A (0.77, 0.755 to 0.810) — crossed q approximately 0.004 in hepatocytes after BH correction across the 10 x 20 cell-type-by-gene test family (Fig. 1; see Methods). Immune cell types reached formal significance broadly (14/20 in CD4+ T, 10/20 in CD8+ T, 14/20 in monocyte, 16/20 in macrophage, 14/20 in NK) but at effect sizes 4 to 8 fold smaller (mean rho 0.03 to 0.12; top-gene rho 0.19 to 0.24 in CD4+ T, macrophage, monocyte, NK; ~0.09 in CD8+ T). Intestinal epithelia recovered an intermediate signal: 12/20 genes significant in small-intestine enterocytes (mean rho 0.35), 10/20 in crypt stem cells (mean rho 0.37), and 7/20 in large-intestine enterocytes (mean rho 0.17), consistent with documented PXR activity in gut^3,11^. Extravillous trophoblast (placenta) showed 0/20 significant with mean rho 0.014, consistent with prior reports that placental PXR is transcribed but transcriptionally inert at baseline^12^.

### Decoupling score quantifies hepatocyte-vs-other selectivity

The top six genes by decoupling score (DS_g = mean over non-hepatocyte cell types c of rho_hep,g - rho_c,g) — SLCO1B1 (0.756), CYP2C9 (0.698), CYP2C8 (0.695), ABCC2 (0.677), CPT1A (0.658), and CYP3A5 (0.631) — separated cleanly from the remaining 14 targets, all of which had DS < 0.6 (Fig. 2). These genes encode the canonical hepatic xenobiotic-handling machinery (two phase I CYPs; SLCO1B1; ABCC2/MRP2; the polymorphic CYP3A5 critical to tacrolimus dosing^13^) together with CPT1A, the rate-limiting enzyme in mitochondrial fatty-acid beta-oxidation.

### Robustness across analytical choices

The decoupling-score ranking was stable across analytical parameter choices. A 17-combination parameter sweep yielded median Spearman rho of decoupling rankings vs. the reference combination of 0.95 (range 0.90 to 1.00; Fig. S1). The top-4 panel (SLCO1B1, CYP2C9, CYP2C8, ABCC2) was recovered in every parameter combination; the 5th-slot Jaccard had median 0.67 because CPT1A and CYP3A5 sit at the boundary of selectivity (DS values within ~0.03 of each other) and swap rank under different metacell granularity. The 80% subsample stability check (20 rounds per cell type) yielded median per-(cell type, gene) rho standard deviation of 0.022 (Fig. S2). Per-dataset hepatocyte analysis (Fig. S3) showed median pairwise rho of 0.337 across five datasets, indicating between-dataset variance is study-level heterogeneity (donor characteristics; sample handling; sequencing platform), with the top-5 gene identity preserved across this variance.

### Specificity vs matched negative controls

A re-run of the identical metacell-coupling pipeline on a curated 20-gene matched control set (10 liver-enriched non-PXR-target genes; 5 hepatocyte master TFs; 5 housekeeping genes) showed the PXR-target decoupling distribution shifted markedly right of the control distribution: median DS 0.575 vs -0.126; Mann-Whitney U one-sided p = 1.0 x 10^-31 (Fig. 3). Crucially, the hepatocyte master TFs HNF4A and HNF1A — themselves hepatocyte-selective — did not show high decoupling, confirming the signal is specific to NR1I2-target coupling rather than a generic hepatocyte-marker pattern.

### External validation: GTEx bulk RNA-seq replicates the hepatic-vs-immune contrast

All five top hep-selective genes showed the same hepatic-vs-immune contrast in GTEx v8 bulk RNA-seq across 54 tissues (Table 1; Fig. 4). Absolute magnitudes were lower than the scRNA-seq metacell rho — donor-level bulk samples carry confounders (age, sex, ischaemia time) that attenuate rho — so finding the directional pattern at bulk resolution is a conservative replication.

**Table 1.** GTEx v8 within-tissue rho(NR1I2, target) across donors.

| Gene | Liver rho | Intestinal mean rho | Immune mean rho | Delta (liver - immune) |
|------|-----------|---------------------|------------------|-------------------------|
| CYP2C9 | 0.68 | 0.56 | 0.11 | +0.56 |
| CYP2C8 | 0.61 | 0.31 | 0.25 | +0.37 |
| CYP3A5 | 0.60 | 0.59 | 0.27 | +0.33 |
| ABCC2 | 0.44 | 0.16 | 0.06 | +0.38 |
| SLCO1B1 | 0.32 | 0.04 | 0.11 | +0.21 |

### External validation: direct rifamycin perturbation confirms four of six top genes

Re-analysis of GSE139896^8^ (primary human hepatocytes from 3 donors treated for 72 h with rifampin 10 uM, rifabutin 5 uM, or rifapentine 10 uM vs methanol vehicle) showed that four of the six top-decoupled panel members (CYP2C8, CYP2C9, CYP3A5, ABCC2) were directionally induced by all three rifamycins, with three (CYP2C8, CYP3A5, ABCC2) reaching paired t-test p < 0.05 for rifampin and/or rifabutin despite n = 3 donors (Table 2; Fig. 5). CYP2C8 showed the most dramatic induction (9 to 19-fold across all three drugs, p < 0.05 for all three).

**Table 2.** log2 fold change in primary human hepatocytes treated with three PXR agonists.

| Gene | log2FC rifampin | log2FC rifabutin | log2FC rifapentine |
|------|------------------|-------------------|---------------------|
| CYP2C8 | +3.84 (~14x, p=0.033) | +4.27 (~19x, p=0.039) | +3.16 (~9x, p=0.042) |
| CYP2C9 | +1.41 (p=0.098) | +2.14 (p=0.107) | +1.10 (p=0.145) |
| CYP3A5 | +0.83 (p=0.028) | +1.21 (p=0.004) | +0.43 (p=0.193) |
| ABCC2 | +0.59 (p=0.011) | +0.54 (p=0.013) | +0.19 (n.s.) |
| SLCO1B1 | +0.14 (n.s.) | +0.27 (n.s.) | +0.41 (n.s.) |
| CPT1A | -0.22 (n.s.) | -0.49 (n.s.) | -0.41 (n.s.) |

SLCO1B1 and CPT1A did not respond to acute rifamycin, refining their interpretation: their hepatocyte coupling most likely reflects shared regulation by hepatic master TFs (HNF4A, FOXA1/2) rather than direct PXR control. The hepatocyte-coupling pattern therefore decomposes into (i) direct PXR targets whose coupling reflects functional NR1I2 engagement (CYP2C8, CYP2C9, CYP3A5, ABCC2), and (ii) coupling-by-shared-hepatic-TF genes (SLCO1B1, CPT1A) that should not be used as PXR engagement biomarkers.

### External validation: LINCS L1000 rifampicin perturbation strength

HEPG2 ranked first of 18 cell lines in rifampicin signature strength (mean |log fold change| over 978 landmark genes = 0.59 vs non-hepatic mean 0.40, 1.47x the non-hepatic average) with replicate consistency in the top tier (median pairwise Spearman rho = 0.31 across 15 within-HEPG2 pairs from 6 signatures; Fig. 6). HT29, the only intestinal L1000 line and a poorly-differentiated colorectal-adenocarcinoma line with reduced endogenous PXR, ranked lowest. The L1000 landmark set deliberately excludes most drug-metabolism genes, so a direct overlay of the top-6 panel on rifampicin signatures requires authenticated clue.io BING-inferred expression and is left as future work.

### External validation: Open Targets recovers textbook PXR pharmacology

The Open Targets Platform's curated disease-association graph independently flagged the top 5 hep-selective genes as drug-response loci: CYP2C9 -> warfarin/anticoagulant response (score 0.41); SLCO1B1 -> Rotor syndrome (0.66), statin response (0.42); ABCC2 -> Dubin-Johnson syndrome (0.82), intrahepatic cholestasis (0.48); CYP3A5 -> HIV infection (0.61, protease-inhibitor metabolism), chronic HCV (0.57); CYP2C8 -> drug-metabolism-relevant cancers. Matched controls (ALB, HNF4A, GAPDH) showed no comparable pharmacology signature (Fig. 7).

---

## Discussion

Canonical PXR target coupling is restricted to epithelial-barrier tissues (liver, intestine, with the strongest signal in hepatocytes) and effectively absent in immune and placental cells where the receptor is transcribed but transcriptionally inert at baseline. The pattern is robust across metacell parameter choices, 80% cell-level subsampling, three independent data modalities (GTEx bulk tissue RNA-seq, GSE139896 primary-hepatocyte rifamycin perturbation, and LINCS L1000 cell-line perturbation), a matched 20-gene negative-control set, and an external curated disease graph (Open Targets). This is consistent with the possibility that NR1I2 expression in immune populations is dissociated from the canonical xenobiotic program through restricted cofactor availability (RXRalpha partner, pioneer factors), altered chromatin context at the canonical PXR response elements (DR3, ER6), or distinct ligand exposure regimes^14^.

A central design problem for next-generation PXR ligands is achieving therapeutic engagement in hepatocytes (where the program is genuinely PXR-driven) without unintended activation in immune cells, where ectopic activation has been linked to Th17 skewing and inflammatory bowel pathology^15^. The direct perturbation overlay refines the actionable panel: CYP2C8, CYP3A5, ABCC2, and CYP2C9 show consistent directional induction with PXR agonists, with three reaching statistical significance for rifampin and/or rifabutin, and CYP2C8 reaching significance for all three rifamycins (1.5 to 19-fold induction). These four genes are the candidate direct PXR-responsive pharmacodynamic readouts and should be used to score on-target hepatic engagement in vitro and in vivo. SLCO1B1 and CPT1A are hepatocyte-coupled but not directly PXR-induced — they appear in the scRNA-seq decoupling ranking because they share regulatory logic with the PXR-responsive set, but they will not respond to a clean PXR ligand. Importantly, the four candidate direct-PXR-responsive genes are *not* expected to respond in PBMC-based assays — a useful negative control for tissue-restricted compounds.

The metacell-coupling framework is general: it can be applied to any receptor (or transcription factor more broadly) and any single-cell atlas with sufficient cell-type coverage. The pipeline is fully reproducible (MIT-licensed code, locked dependencies, CI tests), uses only publicly accessible Census, Open Targets, and GTEx data, and runs end-to-end on a workstation in under five minutes once the H5AD is cached. It is expected to be reusable for analogous questions in other nuclear receptors (CAR/NR1I3, FXR/NR1H4, GR/NR3C1) where cell-type-specific coupling structure is biologically critical but currently undocumented.

Three caveats deserve emphasis. (i) Coupling is correlative; Spearman rho in metacell space is a co-expression statistic, not a causal claim. (ii) NR1I2 sparsity attenuates immune-cell power; with detection rates of 5 to 22% in T/NK/monocyte populations, immune "null" calls should be read as bounded by detection power, not as proof of zero coupling. (iii) Census composition bias; five of the hepatocyte datasets contribute the bulk of cells, and per-dataset reproducibility bounds rather than estimates the true population coupling.

Three follow-ups would substantially extend the work: integrating cell-type-matched ATAC-seq and PXR ChIP-seq to distinguish among the chromatin-vs-cofactor-vs-ligand hypotheses for immune-cell decoupling; applying the metacell-coupling framework to CAR (NR1I3), FXR (NR1H4), and other nuclear receptors; and single-cell CRISPRi/a perturbation of NR1I2 in hepatocyte organoids and PBMCs to convert the correlative coupling map into a causal one.

---

## Methods

**Data source and curation.** Cells were drawn from CELLxGENE Census v2025-01-30 via the `cellxgene-census` Python API (v1.17.x), restricted to *Homo sapiens* and `is_primary_data == True`, across ten Cell Ontology classes. Cells per (cell type, dataset_id) were capped at 1,500 (random seed 42), yielding 446,672 cells from ~20 underlying datasets. The target panel comprises 20 canonical PXR genes graded A/B by PMID-tagged literature curation plus 20 matched negative controls (10 liver-enriched non-PXR-target genes; 5 hepatocyte master TFs; 5 housekeeping genes).

**Metacell aggregation.** Per cell type, raw counts were log1p-normalised and projected onto 30 principal components. Cells were partitioned into metacells by k-means with k = n_cells / 30. Cell types with fewer than 20 metacells were excluded.

**Coupling and decoupling scores.** Per (cell type, gene), Spearman rho was computed between NR1I2 and target metacell profiles. Decoupling score DS_g = mean over non-hepatocyte cell types c of rho_hep,g - rho_c,g.

**Statistical inference.** Confidence intervals from a 500-resample percentile bootstrap of metacell rows. Permutation null shuffles NR1I2 labels across metacells within each cell type 500 times, preserving marginal distributions; two-sided empirical p-values use add-one smoothing. Benjamini-Hochberg FDR correction^16^ applied across the full 10 x 20 cell-type-gene family.

**Robustness.** Parameter sweep over (cells_per_metacell in {15, 30, 60}, min_metacells in {10, 20}, random_state in {0, 42, 123}); 20 rounds of 80% cell-level subsampling per cell type; per-dataset coupling on hepatocyte datasets with >= 300 cells.

**External validations.** GTEx v8 per-sample TPM and sample metadata queried via the GTEx Portal v2 API; within-tissue Spearman rho computed across donors. GSE139896^8^ primary-hepatocyte RNA-seq raw counts downloaded from GEO; log2(CPM + 1) computed per sample; technical replicates collapsed per (donor x condition); per-donor log2 fold change vs methanol vehicle calculated for rifampin, rifabutin, and rifapentine; per-gene significance assessed by paired t-test across the three donors. LINCS L1000 rifampicin signatures (all 121 across 18 cell lines, library LIB_5) fetched from the iLINCS public API; per-cell-line signature strength computed as mean |log fold change| across the 978-gene landmark set; intra-cell-line consistency as median pairwise Spearman rho between within-line replicates. Open Targets disease associations fetched via the v4 GraphQL API for the top-5 hep-selective genes plus three representative controls.

**Software.** Python 3.12, scanpy 1.10, anndata 0.10, scikit-learn 1.5, scipy 1.13, statsmodels 0.14, httpx 0.27, matplotlib 3.9. Full dependency lock in `pyproject.toml` / `uv.lock`. Code MIT-licensed and CI-tested (16 pytest tests).

---

## Data availability

All data sources are publicly accessible. CELLxGENE Census v2025-01-30 was queried via the Python `cellxgene-census` API; atlas composition and per-dataset cell counts are recorded in `data/processed/atlas_provenance.csv`. GTEx v8 bulk RNA-seq per-sample TPM and sample metadata were queried via the GTEx Portal v2 API (https://gtexportal.org/api/). GSE139896 primary human hepatocyte RNA-seq raw counts were downloaded from GEO (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE139896). LINCS L1000 rifampicin signatures (library LIB_5) were fetched from the iLINCS public API (https://ilincsdatasets.nih.gov/). Open Targets Platform v4 disease associations were queried via the GraphQL API (https://platform-api.opentargets.org/graphql). All processed data files are provided in the public GitHub repository (https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling) and will receive a Zenodo DOI upon acceptance.

## Code availability

The complete reproducible pipeline is available at https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling under the MIT license. All dependencies are pinned in `pyproject.toml` and `uv.lock` (Python 3.12). The codebase is CI-tested with 16 pytest unit tests. A `CITATION.cff` file is included.

## Author contributions

**A.S.** designed the study, curated the target and control gene panels, implemented the metacell-coupling pipeline, performed all statistical analyses and external validations, generated all figures, and wrote the manuscript.

## Competing interests

The author declares no competing interests.

## Funding

This work received no external funding.

## Acknowledgments

The author acknowledges the CELLxGENE Census, GTEx, and Open Targets consortia for making their data and APIs publicly available.

---

## Figure legends

**Figure 1.** PXR target coupling to NR1I2 across ten cell types. Spearman rho over metacells. See `figures/fig1_coupling_heatmap.png`.

**Figure 2.** Top hep-coupled genes survive multiple-testing correction with tight bootstrap CIs. (a) Coupling heatmap with BH-FDR overlay. (b) Forest plot of the top-10 hep-coupled genes with 95% percentile bootstrap CIs. See `figures/fig2a_significance_overlay.png` and `figures/fig2b_forest_hepatocyte.png`.

**Figure 3.** Decoupling is specific to PXR target genes, not a generic hepatocyte signature. See `figures/fig3_negative_control.png`.

**Figure 4.** The hepatic-vs-immune contrast replicates in independent bulk RNA-seq (GTEx v8). See `figures/fig4_gtex_validation.png`.

**Figure 5.** Three PXR agonists induce four of the six top-decoupled panel genes in primary human hepatocytes. See `figures/fig5_rifamycin_perturbation.png`.

**Figure 6.** Rifampicin transcriptional signature strength and replicate consistency by L1000 cell line. See `figures/fig6_lincs_rifampicin.png`.

**Figure 7.** Top hep-selective genes recover textbook pharmacology in an independent disease-association graph. See `figures/fig7_opentargets.png`.

**Supplementary Figure S1.** Decoupling-rank stability across the metacell parameter sweep.

**Supplementary Figure S2.** Subsample stability of metacell coupling under 80% cell-level resampling.

**Supplementary Figure S3.** Per-dataset hepatocyte coupling.

---

## References

1. Kliewer, S. A. et al. An orphan nuclear receptor activated by pregnanes defines a novel steroid signaling pathway. *Cell* **92**, 73-82 (1998).

2. Lehmann, J. M. et al. The human orphan nuclear receptor PXR is activated by compounds that regulate CYP3A4 gene expression and cause drug interactions. *J. Clin. Invest.* **102**, 1016-1023 (1998).

3. Geick, A., Eichelbaum, M. & Burk, O. Nuclear receptor response elements mediate induction of intestinal MDR1 by rifampin. *J. Biol. Chem.* **276**, 14581-14587 (2001).

4. Tirona, R. G. & Kim, R. B. Nuclear receptors and drug disposition gene regulation. *J. Pharm. Sci.* **94**, 1169-1186 (2005).

5. Baran, Y. et al. MetaCell: analysis of single-cell RNA-seq data using K-nn graph partitions. *Genome Biol.* **20**, 206 (2019).

6. Persad, S. et al. SEACells infers transcriptional and epigenomic cellular states from single-cell genomics data. *Nat. Biotechnol.* **41**, 1746-1757 (2023).

7. CZI Single-Cell Biology Program, Abdulla, S., Aevermann, B. et al. CZ CELLxGENE Discover: A single-cell data platform for scalable exploration, analysis and modeling of aggregated data. *bioRxiv* (2023). doi:10.1101/2023.10.30.563174.

8. Dyavar, S. R. et al. Hepatocytic transcriptional signatures predict comparative drug interaction potential of rifamycin antibiotics. *Sci. Rep.* **10**, 12565 (2020). doi:10.1038/s41598-020-69228-z. GEO accession GSE139896.

9. Subramanian, A. et al. A next generation connectivity map: L1000 platform and the first 1,000,000 profiles. *Cell* **171**, 1437-1452 (2017).

10. Ochoa, D. et al. The next-generation Open Targets Platform: reimagined, redesigned, rebuilt. *Nucleic Acids Res.* **51**, D1353-D1359 (2023).

11. Glaeser, H., Drescher, S., Eichelbaum, M. & Fromm, M. F. Influence of rifampicin on the expression and function of human intestinal cytochrome P450 enzymes. *Br. J. Clin. Pharmacol.* **59**, 199-206 (2005).

12. Pavek, P. Pregnane X Receptor (PXR)-mediated gene repression and cross-talk of PXR with other nuclear receptors via coactivator interaction. *Front. Pharmacol.* **7**, 456 (2016).

13. Birdwell, K. A. et al. Clinical Pharmacogenetics Implementation Consortium (CPIC) guidelines for CYP3A5 genotype and tacrolimus dosing. *Clin. Pharmacol. Ther.* **98**, 19-24 (2015).

14. Wang, Y. M., Ong, S. S., Chai, S. C. & Chen, T. Role of CAR and PXR in xenobiotic sensing and metabolism. *Expert Opin. Drug Metab. Toxicol.* **8**, 803-817 (2014).

15. Mencarelli, A. et al. Pregnane-X-receptor mediates the anti-inflammatory activities of rifaximin on detoxification pathways in intestinal epithelial cells. *Biochem. Pharmacol.* **82**, 1675-1685 (2011).

16. Benjamini, Y. & Hochberg, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *J. R. Stat. Soc. B* **57**, 289-300 (1995).
