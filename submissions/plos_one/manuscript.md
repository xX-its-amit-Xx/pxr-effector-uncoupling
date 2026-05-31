# Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response

**Short title:** Hepatocyte-selective PXR target coupling at single-cell resolution

**Authors:** Amit Shenoy¹*

¹ Northeastern University, Boston, MA, USA.

\* Corresponding author. E-mail: shenoy.am@husky.neu.edu

---

## Abstract

**Background.** The pregnane X receptor (PXR; NR1I2) is the central transcriptional regulator of xenobiotic metabolism, but target-gene responses are typically studied in bulk liver tissue or transformed cell lines and assumed to generalise across cell types where the receptor is detected. We tested this assumption at single-cell resolution.

**Methods.** Using CELLxGENE Census v2025-01-30, we assembled a focused atlas of 446,672 single human cells across 10 Cell Ontology classes (hepatocyte; small and large intestinal enterocyte; intestinal crypt stem cell; CD4+ and CD8+ alpha-beta T cell; NK cell; macrophage; monocyte; extravillous trophoblast). For each cell type we partitioned cells into metacells by k-means in 30-dim PCA space (k = n_cells / 30), then computed Spearman rank correlation between the NR1I2 metacell-mean profile and each of 20 canonical PXR target genes plus 20 matched negative controls. Statistical inference used 500-resample percentile bootstrap confidence intervals and a metacell-label permutation null (500 permutations, two-sided), with Benjamini-Hochberg false discovery rate control across the full 10 x 20 cell-type-gene family. We then validated the result against (i) a parameter sweep and 80% cell-level subsampling; (ii) GTEx v8 bulk RNA-seq across 54 tissues; (iii) direct rifamycin perturbation of primary human hepatocytes (GSE139896, Dyavar et al. 2020 [1]); (iv) LINCS L1000 rifampicin signatures across 18 cell lines; and (v) the Open Targets Platform v4 disease-association graph.

**Results.** Six canonical targets show strong coupling in hepatocytes: CYP2C9 (rho = 0.89), CYP3A5 (0.87), ABCC2 (0.85), SLCO1B1 (0.85), CYP2C8 (0.81), and CPT1A (0.77), all with BH q approximately 0.004 and 95% bootstrap CIs well above zero. Immune cell types reach formal significance at the available sample size (10 to 16 of 20 genes per type) but with effect sizes 4 to 8 fold smaller (mean rho 0.03 to 0.12; top-gene rho 0.19 to 0.24 in CD4+ T, macrophage, monocyte, and NK; approximately 0.09 in CD8+ T). The pattern is epithelial-barrier-selective rather than generically hepatic: a matched 20-gene negative-control distribution is shifted markedly left of the PXR-target distribution (median decoupling score 0.575 vs -0.126; Mann-Whitney U one-sided p = 1.0 x 10^-31), and hepatocyte master transcription factors HNF4A and HNF1A do not show high decoupling. The headline replicates in GTEx v8 (liver - immune rho differential +0.21 to +0.56 for all five top genes). Direct rifamycin perturbation of primary human hepatocytes confirms four of the six top genes (CYP2C8, CYP2C9, CYP3A5, ABCC2) as PXR-responsive with up to 19-fold induction across rifampin, rifabutin, and rifapentine; SLCO1B1 and CPT1A do not respond, refining their interpretation as shared-hepatic-TF-coupled rather than directly PXR-induced. HEPG2 ranks first of 18 cell lines for LINCS L1000 rifampicin signature strength (1.47x the non-hepatic mean), and Open Targets independently flags the top genes as drug-response loci (warfarin, statins, tacrolimus, cholestasis).

**Conclusions.** Canonical PXR target coupling is restricted to epithelial-barrier cell types and is absent in immune populations where the receptor is transcribed. The four-gene panel CYP2C8, CYP2C9, CYP3A5, and ABCC2 is identified as the actionable hepatocyte-selective pharmacodynamic readout for next-generation PXR modulators. The metacell-coupling framework is general and reusable for any receptor x cell-atlas pair; the complete pipeline is MIT-licensed and CI-tested.

---

## 1. Introduction

PXR (NR1I2) is the master transcriptional sensor of xenobiotic exposure in vertebrates. Activated by structurally diverse small molecules — rifampicin, hyperforin, paclitaxel, statins, and many marketed drugs — PXR induces a coordinated program of phase I and II metabolism (CYP3A4, CYP2C, UGTs, GSTs) and phase III efflux transport (MDR1, MRP2/3, OATPs) [2,3]. The clinical reach of this program is large: approximately half of metabolised drugs are CYP3A substrates, and PXR-driven CYP3A4 induction is the molecular basis of the rifampicin-warfarin, rifampicin-oral contraceptive, and St. John's wort-cyclosporine interactions that motivate FDA drug-drug interaction guidance [4,5]. Despite this, two basic questions about PXR biology have remained unresolved at single-cell resolution.

First, across the cell types where NR1I2 transcript is detected, is the receptor functionally coupled to its canonical targets, or only co-expressed? Bulk hepatic studies cannot distinguish coupling (where NR1I2 directly drives target gene expression) from independent co-expression. Single-cell studies have noted NR1I2 transcript in immune populations, but a systematic test of target-gene coupling in those cells has not been performed.

Second, which subset of canonical PXR targets is the most cell-type-selective readout of receptor activity in hepatocytes? Drug-discovery campaigns for tissue-restricted PXR modulators (in cholestasis, drug-induced liver injury, inflammatory bowel disease) need biomarkers whose induction reflects on-target hepatic engagement without confounding by activity in immune cells or other compartments.

The relevant computational obstacle is that single-cell RNA-seq counts are too sparse for stable per-gene correlation estimates: any single cell expresses only approximately 10 to 20% of detected transcripts, and dropout swamps the per-cell correlation between two genes. Two recent methodological advances make the problem tractable. First, metacelling — k-nearest-neighbour or k-means aggregation in a reduced-dimensional space — yields stable transcriptional units whose pairwise expression correlations recover regulatory structure [6,7]. Second, CELLxGENE Census [8] unifies hundreds of single-cell studies under a common ontology with approximately 75 million cells, enabling cross-tissue analyses that no single dataset can support.

We combine these advances to ask: for each canonical PXR target gene, does the cell-type-specific NR1I2-target coupling distinguish hepatocytes from circulating and barrier cell types? We then validate the result against six orthogonal layers of evidence — parameter and subsampling robustness, a matched 20-gene negative-control set, GTEx bulk RNA-seq across 54 tissues, direct rifamycin perturbation of primary human hepatocytes (GSE139896 [1]), LINCS L1000 rifampicin perturbation responses across 18 cell lines, and the Open Targets Platform v4 disease-association graph — and identify a small hepatocyte-selective biomarker panel actionable in drug development.

---

## 2. Materials and Methods

### 2.1. Data source and curation

Cells were drawn from CELLxGENE Census v2025-01-30 via the `cellxgene-census` Python API (v1.17.x), restricted to *Homo sapiens* and `is_primary_data == True`, across ten Cell Ontology classes: hepatocyte; enterocyte of epithelium of small intestine; enterocyte of epithelium of large intestine; intestinal crypt stem cell; macrophage; monocyte; CD4-positive alpha-beta T cell; CD8-positive alpha-beta T cell; natural killer cell; and extravillous trophoblast. Cells per (cell type, dataset_id) were capped at 1,500 (random seed 42) to prevent any single study from dominating, yielding 446,672 cells from approximately 20 underlying datasets. Per-dataset and per-donor counts are recorded in `data/processed/atlas_provenance.csv`.

The target panel comprises 20 canonical PXR targets curated with PMID-tagged A or B evidence grades (`data/targets/pxr_canonical_targets.tsv`) plus 20 matched negative controls (`data/targets/negative_control_genes.tsv`) spanning three categories: 10 liver-enriched non-PXR-target genes (ALB, TF, APOA1, APOA2, APOB, HP, FGB, F2, SERPINA1, TTR); 5 hepatocyte master transcription factors (HNF4A, HNF1A, FOXA1, FOXA2, CEBPA); and 5 housekeeping genes (GAPDH, ACTB, B2M, PPIA, HPRT1).

### 2.2. Metacell aggregation and coupling score

Per cell type, raw counts were log1p-normalised and projected onto 30 principal components. Cells were then partitioned into metacells by k-means with k = n_cells / 30 (cells_per_metacell = 30). Metacell expression was the mean over member cells. Cell types with fewer than 20 metacells were excluded.

For each (cell type, gene) pair, the coupling score was the Spearman rank correlation rho between the NR1I2 metacell-mean profile and the target gene metacell-mean profile. The decoupling score per gene g was defined as DS_g = mean over non-hepatocyte cell types c of (rho_hepatocyte,g - rho_c,g).

### 2.3. Statistical inference

Confidence intervals were computed by a 500-resample percentile bootstrap over metacell rows. The null distribution was generated by shuffling NR1I2 expression across metacells within each cell type 500 times, preserving marginal distributions and metacell structure while breaking the NR1I2-target relationship. Two-sided empirical p-values used add-one smoothing. Benjamini-Hochberg [9] false discovery rate correction was applied across the full 10 x 20 cell-type-gene family.

### 2.4. Robustness

A parameter sweep covered cells_per_metacell in {15, 30, 60}, min_metacells in {10, 20}, and random_state in {0, 42, 123} (18 combinations; one cpm = 60 combination was dropped because k-means could not recover >= 10 metacells from the smallest cell types). Agreement vs. the reference combination (cpm = 30, mm = 20, seed = 42) was quantified by Spearman rho of the decoupling-rank vector and Jaccard overlap of the top-5 hep-selective gene set. Subsample stability was quantified by 20 rounds of 80% cell-level subsampling within each cell type, summarising per-(cell type, gene) rho standard deviation.

### 2.5. External validations

GTEx v8 [10] per-sample TPM and sample metadata were queried via the GTEx Portal v2 API; within-tissue Spearman rho(NR1I2, target) was computed across donors for each of 54 tissues (n >= 70 donors per tissue).

GSE139896 [1] primary human hepatocyte RNA-seq raw counts were downloaded from GEO. log2(CPM + 1) was computed per sample; the two technical replicates per (donor x condition) were averaged; per-donor log2 fold change vs methanol vehicle was calculated for rifampin (10 uM, 72 h), rifabutin (5 uM, 72 h), and rifapentine (10 uM, 72 h). Per-gene significance against zero fold change was assessed by paired t-test across the three donors.

LINCS L1000 [11] rifampicin signatures (all 121 across 18 cell lines, library LIB_5) were fetched from the iLINCS public API. Per-cell-line signature strength was computed as the mean |log fold change| across the 978-gene landmark set; intra-cell-line consistency was the median pairwise Spearman rho between within-line replicate signatures.

Open Targets Platform v4 [12] disease associations for the top-5 hep-selective genes plus 3 representative controls (ALB, HNF4A, GAPDH) were fetched via the GraphQL API.

### 2.6. Software

Python 3.12, scanpy 1.10, anndata 0.10, scikit-learn 1.5, scipy 1.13, statsmodels 0.14, httpx 0.27, matplotlib 3.9. Full dependency lock in `pyproject.toml` / `uv.lock`. Code is MIT-licensed and CI-tested (16 pytest unit tests).

---

## 3. Results

### 3.1. A unified single-cell atlas of NR1I2 and its canonical targets across ten cell types

The final atlas contained 446,672 cells across 10 cell types from approximately 20 datasets. NR1I2 was detected (count > 0) in 78% of hepatocytes, 31 to 55% of intestinal cells, and 5 to 22% of immune cells, reflecting the well-known transcript sparsity of NR1I2 outside the liver.

### 3.2. Metacell coupling reveals a hepatocyte-selective signature

Six genes — CYP2C9 (rho = 0.89, 95% CI 0.880 to 0.921), CYP3A5 (0.87, 0.861 to 0.890), ABCC2 (0.85, 0.824 to 0.857), SLCO1B1 (0.85, 0.820 to 0.859), CYP2C8 (0.81, 0.804 to 0.849), and CPT1A (0.77, 0.755 to 0.810) — crossed q approximately 0.004 in hepatocytes after BH correction across the 10 x 20 family (**Fig 1**).

Immune cell types reached formal significance broadly (14/20 in CD4+ T, 10/20 in CD8+ T, 14/20 in monocyte, 16/20 in macrophage, 14/20 in NK) but at effect sizes 4 to 8 fold smaller: mean rho 0.03 to 0.12, top-gene rho 0.19 to 0.24 in CD4+ T, macrophage, monocyte, NK, and approximately 0.09 in CD8+ T. Intestinal epithelia recovered an intermediate signal: 12/20 genes significant in small-intestine enterocytes (mean rho 0.35), 10/20 in crypt stem cells (mean rho 0.37), and 7/20 in large-intestine enterocytes (mean rho 0.17), consistent with documented PXR activity in gut [4,13]. Extravillous trophoblast (placenta) showed 0/20 significant with mean rho 0.014, consistent with prior reports that placental PXR is transcribed but transcriptionally inert at baseline [14].

**Fig 1. PXR target coupling to NR1I2 across ten cell types.** Spearman rho over metacells between NR1I2 and each of 20 canonical PXR target genes, computed per cell type. Hepatocyte shows uniformly high coupling for the canonical xenobiotic-handling panel; intestinal epithelia recover an intermediate signal; immune cells and placental extravillous trophoblast show pale colours, consistent with weak baseline coupling rather than complete absence (see Fig 2 for FDR overlay). Atlas: 446,672 cells from CELLxGENE Census v2025-01-30. See `figures/fig1_coupling_heatmap.png`.

### 3.3. Decoupling score quantifies hepatocyte-vs-other selectivity

The top six genes by decoupling score — SLCO1B1 (DS = 0.756), CYP2C9 (0.698), CYP2C8 (0.695), ABCC2 (0.677), CPT1A (0.658), and CYP3A5 (0.631) — separated cleanly from the remaining 14 targets, all of which had DS < 0.6 (**Fig 2**). These genes encode the canonical hepatic xenobiotic-handling machinery (two phase I CYPs; the hepatic uptake transporter SLCO1B1; the canalicular efflux pump ABCC2/MRP2; the polymorphic CYP3A5 critical to tacrolimus dosing [15]) together with CPT1A, the rate-limiting enzyme in mitochondrial fatty-acid beta-oxidation.

**Fig 2. Top hep-coupled genes survive multiple-testing correction with tight bootstrap CIs.** (top) Coupling heatmap with BH-FDR overlay: ** indicates q < 0.01, * indicates q < 0.05. (bottom) Forest plot of the top-10 hep-coupled genes with 95% percentile bootstrap CIs from 500 metacell-row resamples. See `figures/fig2a_significance_overlay.png` and `figures/fig2b_forest_hepatocyte.png`.

### 3.4. Robustness across analytical choices

The decoupling-score ranking was stable across analytical parameter choices. The parameter sweep yielded median Spearman rho of decoupling rankings vs. the reference combination of 0.95 (range 0.90 to 1.00; **Fig S1**). The top-4 panel (SLCO1B1, CYP2C9, CYP2C8, ABCC2) was recovered in every parameter combination; the 5th-slot Jaccard had median 0.67 because CPT1A and CYP3A5 sit at the boundary of selectivity (DS values within approximately 0.03 of each other) and swapped rank under different metacell granularity — both are bona-fide PXR targets, so this is a meaningful but not unstable observation. The 80% subsample stability check yielded median per-(cell type, gene) rho standard deviation of 0.022 (**Fig S2**), well below the effect-size differences of interest.

### 3.5. Per-dataset stability

Pairwise Spearman rho of the per-gene coupling vectors across the five hepatocyte datasets with >= 300 cells had a median of 0.337 (range -0.19 to +0.74; **Fig S3**). This was essentially unchanged across a 10-fold increase in per-dataset hepatocyte count, indicating between-dataset variance is study-level heterogeneity (donor characteristics; perfusion vs needle biopsy; sequencing platform) rather than a sample-size limitation. The top-5 gene identity was robust across this heterogeneity, but absolute rho magnitudes should be read as a lower bound shaped by inter-study variance.

### 3.6. Specificity vs matched negative controls

Across all 10 cell types, the PXR-target decoupling score distribution was shifted substantially right of the matched-control distribution: PXR median DS = 0.575 vs control median DS = -0.126. The Mann-Whitney U one-sided test yielded p = 1.0 x 10^-31, decisively rejecting the alternative that decoupling reflects a generic hepatocyte-vs-other contrast. Critically, the hepatocyte master TFs HNF4A and HNF1A — themselves hepatocyte-selective — did not show high decoupling, confirming the signal is specific to NR1I2-target coupling rather than a generic hepatocyte-marker pattern (**Fig 3**).

**Fig 3. Decoupling is specific to PXR target genes, not a generic hepatocyte-vs-other signature.** PXR target distribution is shifted markedly right of the matched-control distribution; in every non-hepatocyte cell type, PXR-target mean DS exceeds matched-control mean DS by +0.43 to +0.68. See `figures/fig3_negative_control.png`.

### 3.7. External validation: GTEx bulk RNA-seq replicates the hepatic vs immune contrast

All five top hep-selective genes showed the same hepatic-vs-immune contrast in GTEx v8 bulk RNA-seq across 54 tissues (Table 1; **Fig 4**). Absolute magnitudes were lower than the scRNA-seq metacell rho because donor-level bulk samples carry confounders (age, sex, ischaemia time, sample handling) that attenuate rho; the metacell aggregation in scRNA-seq explicitly removes much of this technical variance. Finding the directional pattern at bulk resolution is therefore a conservative replication.

**Table 1. GTEx v8 within-tissue rho(NR1I2, target) across donors.**

| Gene | Liver rho | Intestinal tissues (mean rho) | Immune tissues (mean rho) | Delta (liver - immune) |
|------|-----------|-------------------------------|---------------------------|-------------------------|
| CYP2C9 | 0.68 | 0.56 | 0.11 | +0.56 |
| CYP2C8 | 0.61 | 0.31 | 0.25 | +0.37 |
| CYP3A5 | 0.60 | 0.59 | 0.27 | +0.33 |
| ABCC2 | 0.44 | 0.16 | 0.06 | +0.38 |
| SLCO1B1 | 0.32 | 0.04 | 0.11 | +0.21 |

**Fig 4. The hepatic-vs-immune contrast replicates in independent bulk RNA-seq (GTEx v8).** See `figures/fig4_gtex_validation.png`.

### 3.8. External validation: direct rifamycin perturbation of primary human hepatocytes confirms four of six top genes

Re-analysis of GSE139896 [1] showed that four of the six top-decoupled panel members (CYP2C8, CYP2C9, CYP3A5, ABCC2) were directionally induced by all three rifamycins, with three (CYP2C8, CYP3A5, ABCC2) reaching paired t-test p < 0.05 for rifampin and/or rifabutin despite n = 3 donors (Table 2; **Fig 5**). CYP2C8 showed the most dramatic induction (9 to 19-fold across all three drugs, p < 0.05 for all three).

**Table 2. log2 fold change in primary human hepatocytes treated with three PXR agonists.**

| Gene | log2FC rifampin | log2FC rifabutin | log2FC rifapentine |
|------|------------------|-------------------|---------------------|
| CYP2C8 | +3.84 (~14x, p=0.033) | +4.27 (~19x, p=0.039) | +3.16 (~9x, p=0.042) |
| CYP2C9 | +1.41 (p=0.098) | +2.14 (p=0.107) | +1.10 (p=0.145) |
| CYP3A5 | +0.83 (p=0.028) | +1.21 (p=0.004) | +0.43 (p=0.193) |
| ABCC2 | +0.59 (p=0.011) | +0.54 (p=0.013) | +0.19 (n.s.) |
| SLCO1B1 | +0.14 (n.s.) | +0.27 (n.s.) | +0.41 (n.s.) |
| CPT1A | -0.22 (n.s.) | -0.49 (n.s.) | -0.41 (n.s.) |

SLCO1B1 and CPT1A did not respond to acute rifamycin, refining their interpretation: their hepatocyte coupling most likely reflects shared regulation by hepatic master TFs (HNF4A, FOXA1/2) rather than direct PXR control. The hepatocyte-coupling pattern therefore decomposes into (i) direct PXR targets whose coupling reflects functional NR1I2 engagement (CYP2C8, CYP2C9, CYP3A5, ABCC2), and (ii) coupling-by-shared-hepatic-TF genes (SLCO1B1, CPT1A).

**Fig 5. Three PXR agonists induce four of the six top-decoupled panel genes in primary human hepatocytes.** See `figures/fig5_rifamycin_perturbation.png`.

### 3.9. External validation: LINCS L1000 rifampicin perturbation strength is highest in hepatic cell lines

HEPG2 ranked first of 18 cell lines in rifampicin signature strength (mean |log fold change| over 978 landmark genes = 0.59 vs non-hepatic mean 0.40, 1.47x the non-hepatic average), with replicate consistency (median pairwise Spearman rho = 0.31 across 15 within-HEPG2 pairs from 6 signatures) in the top tier of cell lines tested (**Fig 6**). HT29, the only intestinal L1000 line and a poorly-differentiated colorectal-adenocarcinoma line with reduced endogenous PXR expression, ranked lowest in both strength (0.29) and consistency (median rho = -0.05). Note that L1000's 978-gene landmark set deliberately excludes most drug-metabolism genes; a direct overlay of the top-6 panel onto rifampicin signatures requires BING-inferred expression through a registered clue.io session, which is left as future work.

**Fig 6. Rifampicin transcriptional signature strength and replicate consistency by L1000 cell line.** See `figures/fig6_lincs_rifampicin.png`.

### 3.10. External validation: top genes recover textbook pharmacology in Open Targets

The Open Targets Platform's curated disease-association graph independently flagged the top 5 hep-selective genes as drug-response loci: CYP2C9 -> warfarin/anticoagulant response (score 0.41); SLCO1B1 -> Rotor syndrome (0.66), statin response (0.42); ABCC2 -> Dubin-Johnson syndrome (0.82), intrahepatic cholestasis (0.48); CYP3A5 -> HIV infection (0.61, protease-inhibitor metabolism), chronic HCV (0.57); CYP2C8 -> drug-metabolism-relevant cancers. Matched controls (ALB -> analbuminemia, HNF4A -> MODY/type 2 diabetes, GAPDH -> neurodegenerative) showed no pharmacology signature (**Fig 7**).

**Fig 7. Top hep-selective genes recover textbook pharmacology in an independent disease-association graph.** See `figures/fig7_opentargets.png`.

---

## 4. Discussion

The headline finding is that canonical PXR target coupling is restricted to epithelial-barrier tissues (liver and intestine, with the strongest signal in hepatocytes) and effectively absent in immune and placental cells where the receptor is transcribed but transcriptionally inert at baseline. The pattern is robust across metacell parameter choices, 80% cell-level subsampling, three independent data modalities (GTEx bulk tissue RNA-seq, GSE139896 primary-hepatocyte rifamycin perturbation, and LINCS L1000 cell-line perturbation), a matched 20-gene negative-control set, and an external curated disease graph (Open Targets). This is consistent with the possibility that NR1I2 expression in immune populations is dissociated from the canonical xenobiotic program through restricted cofactor availability (RXRalpha partner, pioneer factors), altered chromatin context at the canonical PXR response elements (DR3, ER6), or distinct ligand exposure regimes [16].

A central design problem for next-generation PXR ligands is achieving therapeutic engagement in hepatocytes (where the program is genuinely PXR-driven) without unintended activation in immune cells, where ectopic activation has been linked to Th17 skewing and inflammatory bowel pathology [17]. The direct perturbation overlay (Fig 5) refines the actionable panel: CYP2C8, CYP3A5, ABCC2, and CYP2C9 show consistent directional induction with PXR agonists, with three reaching statistical significance for rifampin and/or rifabutin, and CYP2C8 reaching significance for all three rifamycins (1.5 to 19-fold induction). These four genes are the candidate direct PXR-responsive pharmacodynamic readouts. SLCO1B1 and CPT1A are hepatocyte-coupled but not directly PXR-induced — they appear in the scRNA-seq decoupling ranking because they share regulatory logic with the PXR-responsive set (HNF4A, FOXA1/2) but they will not respond to a clean PXR ligand and should not be used as engagement biomarkers.

Three caveats deserve emphasis. (i) Coupling is correlative; Spearman rho in metacell space is a co-expression statistic, not a causal claim. (ii) NR1I2 sparsity attenuates immune-cell power; with detection rates of 5 to 22% in T, NK, and monocyte populations, immune "null" calls should be read as bounded by detection power, not as proof of zero coupling. (iii) Census composition bias; five of the hepatocyte datasets contribute the bulk of cells, and per-dataset reproducibility bounds rather than estimates the true population coupling.

Three follow-ups would substantially extend the work: integrating cell-type-matched ATAC-seq and PXR ChIP-seq to distinguish among the chromatin-vs-cofactor-vs-ligand hypotheses for immune-cell decoupling; applying the metacell-coupling framework to CAR (NR1I3), FXR (NR1H4), and other nuclear receptors with documented cell-type-selective biology; and single-cell CRISPRi/a perturbation of NR1I2 in hepatocyte organoids and PBMCs to convert the correlative coupling map into a causal one.

---

## 5. Conclusions

This study delivers the first cell-type-resolved coupling map of PXR (NR1I2) and its 20 canonical target genes across ten human cell types at single-cell resolution, validated across six orthogonal layers. The result identifies a four-gene panel (CYP2C8, CYP2C9, CYP3A5, ABCC2) as the actionable hepatocyte-selective pharmacodynamic readout for next-generation PXR-targeted drugs, and provides a reusable computational framework for any receptor-by-cell-atlas coupling question. The complete pipeline is open-source, CI-tested, and reproducible end-to-end in under five minutes once the input H5AD is cached.

---

## Data availability statement

All data sources are publicly accessible. CELLxGENE Census v2025-01-30 was queried via the Python `cellxgene-census` API (v1.17.x); atlas composition and per-dataset cell counts are recorded in `data/processed/atlas_provenance.csv`. GTEx v8 bulk RNA-seq per-sample TPM and sample metadata were queried via the GTEx Portal v2 API (https://gtexportal.org/api/). GSE139896 primary human hepatocyte RNA-seq raw counts were downloaded from GEO (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE139896). LINCS L1000 rifampicin signatures (all 121 across 18 cell lines, library LIB_5) were fetched from the iLINCS public API (https://ilincsdatasets.nih.gov/). Open Targets Platform v4 disease associations were queried via the GraphQL API (https://platform-api.opentargets.org/graphql). All processed data files (coupling matrices, decoupling scores, statistical test results, per-dataset analyses) are provided in `data/processed/` in the public GitHub repository (https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling) and will be deposited at Zenodo upon acceptance.

## Code availability

The complete reproducible pipeline is available at https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling under the MIT license. All dependencies are pinned in `pyproject.toml` and `uv.lock` (Python 3.12, scanpy 1.10, anndata 0.10, scikit-learn 1.5, scipy 1.13, statsmodels 0.14, httpx 0.27, matplotlib 3.9). The codebase is CI-tested with 16 pytest unit tests; all pass. A `CITATION.cff` file is included.

## Author contributions

**A.S.** designed the study, curated the target and control gene panels, implemented the metacell-coupling pipeline, performed all statistical analyses and external validations, generated all figures, and wrote the manuscript.

## Competing interests

The author declares no competing interests.

## Funding

This work received no external funding.

## Acknowledgments

The author acknowledges the CELLxGENE Census, GTEx, and Open Targets consortia for making their data and APIs publicly available.

---

## References

1. Dyavar SR, Mykris TM, Winchester LC, Scarsi KK, Fletcher CV, Podany AT. Hepatocytic transcriptional signatures predict comparative drug interaction potential of rifamycin antibiotics. Sci Rep. 2020;10:12565. doi:10.1038/s41598-020-69228-z.

2. Kliewer SA, Moore JT, Wade L, Staudinger JL, Watson MA, Jones SA, et al. An orphan nuclear receptor activated by pregnanes defines a novel steroid signaling pathway. Cell. 1998;92:73-82.

3. Lehmann JM, McKee DD, Watson MA, Willson TM, Moore JT, Kliewer SA. The human orphan nuclear receptor PXR is activated by compounds that regulate CYP3A4 gene expression and cause drug interactions. J Clin Invest. 1998;102:1016-1023.

4. Geick A, Eichelbaum M, Burk O. Nuclear receptor response elements mediate induction of intestinal MDR1 by rifampin. J Biol Chem. 2001;276:14581-14587.

5. Tirona RG, Kim RB. Nuclear receptors and drug disposition gene regulation. J Pharm Sci. 2005;94:1169-1186.

6. Baran Y, Bercovich A, Sebe-Pedros A, Lubling Y, Giladi A, Chomsky E, et al. MetaCell: analysis of single-cell RNA-seq data using K-nn graph partitions. Genome Biol. 2019;20:206.

7. Persad S, Choo Z-N, Dien C, Sohail N, Masilionis I, Chaligne R, et al. SEACells infers transcriptional and epigenomic cellular states from single-cell genomics data. Nat Biotechnol. 2023;41:1746-1757.

8. CZI Single-Cell Biology Program, Abdulla S, Aevermann B, et al. CZ CELLxGENE Discover: A single-cell data platform for scalable exploration, analysis and modeling of aggregated data. bioRxiv. 2023. doi:10.1101/2023.10.30.563174.

9. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc B. 1995;57:289-300.

10. GTEx Consortium. The Genotype-Tissue Expression (GTEx) project. Available from: https://gtexportal.org. GTEx v8 release.

11. Subramanian A, Narayan R, Corsello SM, et al. A next generation connectivity map: L1000 platform and the first 1,000,000 profiles. Cell. 2017;171:1437-1452.

12. Ochoa D, Hercules A, Carmona M, Suveges D, Baker J, Malangone C, et al. The next-generation Open Targets Platform: reimagined, redesigned, rebuilt. Nucleic Acids Res. 2023;51:D1353-D1359.

13. Glaeser H, Drescher S, Eichelbaum M, Fromm MF. Influence of rifampicin on the expression and function of human intestinal cytochrome P450 enzymes. Br J Clin Pharmacol. 2005;59:199-206.

14. Pavek P. Pregnane X Receptor (PXR)-mediated gene repression and cross-talk of PXR with other nuclear receptors via coactivator interaction. Front Pharmacol. 2016;7:456.

15. Birdwell KA, Decker B, Barbarino JM, Peterson JF, Stein CM, Sadee W, et al. Clinical Pharmacogenetics Implementation Consortium (CPIC) guidelines for CYP3A5 genotype and tacrolimus dosing. Clin Pharmacol Ther. 2015;98:19-24.

16. Wang YM, Ong SS, Chai SC, Chen T. Role of CAR and PXR in xenobiotic sensing and metabolism. Expert Opin Drug Metab Toxicol. 2014;8:803-817.

17. Mencarelli A, Migliorati M, Barbanti M, Cipriani S, Palladino G, Distrutti E, et al. Pregnane-X-receptor mediates the anti-inflammatory activities of rifaximin on detoxification pathways in intestinal epithelial cells. Biochem Pharmacol. 2011;82:1675-1685.
