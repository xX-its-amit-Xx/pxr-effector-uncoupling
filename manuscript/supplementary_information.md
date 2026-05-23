# Supplementary Information

**Cell-type-resolved decoupling of PXR target genes across a 446,672-cell human atlas**

Amit Shenoy

---

## Supplementary Figures

![Supplementary Figure S1](../figures/figS1_parameter_sensitivity.png)

**Fig. S1 | Decoupling-rank stability across the metacell parameter sweep.** (**left**) Spearman ρ of the decoupling-rank vector (20 genes) for each parameter combination vs. the reference combination (cells_per_metacell = 30, min_metacells = 20, seed = 42), plotted against random seed and coloured by cells_per_metacell. 17 of 18 combinations evaluated (one cpm = 60 combo dropped because k-means cannot recover ≥ 10 metacells from the smallest cell types). Median Spearman ρ = 0.95 (range 0.90–1.00). (**right**) Jaccard overlap of the top-5 hep-selective gene set against the reference combination. Jaccard = 1.0 at the reference; median 0.67 elsewhere, reflecting the CPT1A ↔ CYP3A5 5th-slot swap discussed in Results — both are bona-fide PXR targets at the selectivity boundary (DS values within ~0.03).

\newpage

![Supplementary Figure S2](../figures/figS2_subsample_stability.png)

**Fig. S2 | Subsample stability of metacell coupling under 80% cell-level resampling.** Box plot of per-(cell type, gene) ρ standard deviation across 20 independent 80%-subsample replicates, summarised by cell type. Hepatocyte, immune cell types and monocyte/T cells show tight stability (median std ≤ 0.025) due to large cell counts; intestinal epithelia and extravillous trophoblast (much smaller N) show wider spread (median std up to 0.10), with intestinal crypt stem cell as the noisiest (n ≈ 1,900 cells). Overall median per-(cell type, gene) ρ std = 0.022, well below the effect-size differences of interest in Results.

\newpage

![Supplementary Figure S3](../figures/figS3_per_dataset_hepatocyte.png)

**Fig. S3 | Per-dataset hepatocyte coupling shows preserved gene ranking with substantial between-study magnitude variance.** Coupling ρ for each of the nine hepatocyte datasets that contribute ≥ 300 cells in the final atlas, computed independently per dataset (rows) and gene (columns). Top-gene ranking (SLCO1B1, CYP2C9, ABCC2, CYP3A5, CYP2C8 grouped on the right side) is preserved across all datasets, but absolute ρ magnitudes vary considerably (median pairwise Spearman ρ of per-gene coupling vectors = 0.337 across 36 dataset pairs, range −0.19 to +0.74). This median is essentially unchanged from a previous version of the analysis with a more aggressive per-cell-type subsampling cap (where one dataset filled ~60 % of slots), implying that between-dataset variance is study-level heterogeneity — donor age/sex/ancestry, perfusion vs needle biopsy, sequencing platform — not a sample-size limitation that can be resolved by adding cells.
