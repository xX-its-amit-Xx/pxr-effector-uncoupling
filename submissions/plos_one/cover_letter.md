# Cover Letter — PLOS ONE

Amit Shenoy
Northeastern University
Boston, MA, USA
shenoy.am@husky.neu.edu

Dear Editor,

I am pleased to submit the manuscript "Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response" for consideration at PLOS ONE.

The work delivers, to my knowledge, the first cell-type-resolved transcriptional coupling map of the pregnane X receptor (PXR; NR1I2) and its 20 canonical target genes across 446,672 single human cells from ten Cell Ontology classes (hepatocyte, three intestinal epithelial types, five immune types, and extravillous trophoblast) drawn from CELLxGENE Census v2025-01-30. Six canonical PXR targets — CYP2C9, CYP3A5, ABCC2, SLCO1B1, CYP2C8, and CPT1A — show strong coupling in hepatocytes (Spearman rho 0.77 to 0.89, BH q approximately 0.004), while immune cells reach formal significance at the available sample size but with 4 to 8 fold smaller effect sizes (mean rho 0.03 to 0.12). The pattern is epithelial-barrier-selective, not generically hepatic: a matched 20-gene negative-control set is decisively decoupled (Mann-Whitney U one-sided p = 1.0 x 10^-31), and hepatocyte master transcription factors HNF4A and HNF1A do not show high decoupling.

I have chosen PLOS ONE because the work is, above all, a rigorous and technically sound piece of bioinformatics whose value is its replicability and its actionable biological output for drug development. PLOS ONE's stated mission — to publish methodologically rigorous studies regardless of perceived "broad interest" — is the right home for a single-author computational paper whose headline is supported across six orthogonal validation layers: (i) parameter sweep across 17 combinations (median Spearman rho of decoupling rankings vs reference = 0.95) plus 20-round 80% cell-level subsampling (median per-(cell type, gene) rho std = 0.022); (ii) the matched negative-control comparison cited above; (iii) GTEx v8 bulk RNA-seq across 54 tissues, recovering the same liver-vs-immune contrast for all five top genes (delta +0.21 to +0.56); (iv) direct rifamycin perturbation of primary human hepatocytes (GSE139896, Dyavar et al. 2020) confirming four of the six top genes (CYP2C8, CYP2C9, CYP3A5, ABCC2) as PXR-responsive with up to 19-fold induction; (v) LINCS L1000 rifampicin signature strength across 18 cell lines ranking HEPG2 first; and (vi) the Open Targets disease-association graph recovering textbook PXR pharmacology (warfarin, statins, tacrolimus, cholestasis). The honest refinement that SLCO1B1 and CPT1A are coupled by shared hepatic-TF regulation rather than direct PXR control — surfaced by the perturbation overlay — is exactly the kind of careful interpretation that PLOS ONE's reproducibility-first standard rewards.

I want to be transparent about the work's profile. This is a single-author submission with no PI sponsorship and no external funding. The strength offered in lieu of institutional weight is the reproducible bundle: MIT-licensed code, locked Python 3.12 dependencies (uv.lock), 16 passing pytest unit tests, GitHub Actions CI, a CITATION.cff, all processed CSVs committed under `data/processed/`, and a GitHub Actions workflow that re-derives the CELLxGENE atlas on Ubuntu in approximately one hour. The complete repository is at https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling and will receive a Zenodo DOI upon acceptance.

The work has not been published elsewhere and is not under consideration at any other journal. All figures meet PLOS ONE's 300-DPI requirement and are MIT/CC-BY-4.0 licensed and original to this work. No human subjects, animal, or biosafety approvals are applicable as the study re-analyses publicly accessible datasets.

I confirm I am the sole author and have read and approved the manuscript for submission. I look forward to the editor's response.

Sincerely,
Amit Shenoy
