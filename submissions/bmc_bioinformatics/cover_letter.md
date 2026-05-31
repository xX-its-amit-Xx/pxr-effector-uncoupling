# Cover Letter — BMC Bioinformatics

Amit Shenoy
Northeastern University
Boston, MA, USA
shenoy.am@husky.neu.edu

Dear Editor,

I am submitting the manuscript "A reusable metacell-coupling pipeline for cell-type-resolved nuclear-receptor target analysis at single-cell atlas scale, applied to PXR (NR1I2) across 446,672 human cells" for consideration at BMC Bioinformatics.

This is, primarily, a methods contribution that happens to recover an actionable biological story. The pipeline I present takes three user inputs — a list of Cell Ontology terms, a regulator gene, and a candidate target panel (plus an optional matched negative-control panel) — and produces a complete cell-type-resolved coupling and decoupling analysis with five integrated layers of validation: a 500-resample bootstrap of metacell rows, a metacell-label permutation null with Benjamini-Hochberg FDR over the full cell-type x gene family, a parameter sweep (cells_per_metacell, min_metacells, seed) with rank-stability and Jaccard diagnostics, a 20-round 80% cell-level subsample-stability check, and a per-dataset reproducibility analysis. Four additional orchestration scripts attach external validations to the candidate top genes: GTEx v8 bulk RNA-seq across 54 tissues, GEO direct perturbation overlay, LINCS L1000 cell-line signature analysis, and Open Targets disease-association overlay. The pipeline is therefore self-contained and decision-relevant: it produces a ranked candidate gene set together with the evidence needed to defend the ranking.

I believe this fits BMC Bioinformatics for three concrete reasons:

**1. It is a method, not a one-off application.** The implementation is parameterised over (regulator, target panel, cell-atlas, negative-control panel) and is structured so a user can swap any of those four inputs and re-run end-to-end. The same code that produced the PXR worked example will, with three configuration changes, produce an equivalent analysis for CAR (NR1I3), FXR (NR1H4), GR (NR3C1), or any other nuclear receptor with a curated target panel and adequate cell-type coverage in CELLxGENE Census or another supported atlas.

**2. It addresses an explicit reproducibility bar.** BMC Bioinformatics' standards for software submissions — pinned dependencies, automated tests, continuous integration, persistent identifier, clear installation and usage docs — are met: Python 3.12 with `uv.lock`, 16 passing pytest unit tests, GitHub Actions CI, a CITATION.cff, and an MIT license. A Zenodo DOI will be minted upon acceptance. The pipeline runs end-to-end on a workstation in under five minutes once the input H5AD is cached.

**3. The validation story is methodologically informative.** The pipeline correctly distinguishes between (a) genes whose coupling reflects direct receptor engagement (confirmed for CYP2C8, CYP2C9, CYP3A5, ABCC2 by the rifamycin perturbation module) and (b) genes that share a regulatory backbone with receptor targets without being directly induced (SLCO1B1 and CPT1A, both hepatocyte-coupled but not rifamycin-responsive — likely HNF4A / FOXA1/2 driven). This decomposition is surfaced automatically by the GEO-perturbation module and is the kind of methodological feature that distinguishes a thoughtfully validated pipeline from a one-shot correlation analysis. The matched 20-gene negative-control comparison — which crucially includes hepatocyte master TFs (HNF4A, HNF1A) that correctly do *not* show high decoupling — provides a tissue-matched specificity check (Mann-Whitney U one-sided p = 1.0 x 10^-31) that is also reusable for any future application of the pipeline.

The PXR worked example uses 446,672 single cells across ten Cell Ontology classes from CELLxGENE Census v2025-01-30 and is the largest cell-type-resolved coupling analysis of a nuclear receptor I am aware of. The biological by-product is itself useful for drug developers (the four-gene panel for hepatocyte-selective PXR pharmacodynamics), but the manuscript is framed primarily around the methodology and its reusability, which I believe matches BMC Bioinformatics' scope more closely than a pure application paper.

This is a single-author submission with no external funding. The complete codebase, processed CSVs, figures, manuscript, and reproducibility infrastructure are at https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling. The work is original, not under consideration elsewhere, and has not been previously published.

I look forward to the editor's response and to peer review.

Sincerely,
Amit Shenoy
