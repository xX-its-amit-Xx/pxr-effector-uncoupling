# OSF project — description and wiki

## Project title

**pxr-effector-uncoupling: cell-type-resolved coupling of PXR (NR1I2) target genes across 446,672 single human cells**

## Public project description (for the "Description" field, ~500 words)

This Open Science Framework (OSF) project is the registered, browseable, and citable home for the study "Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response" by Amit Shenoy (Northeastern University, 2026). The work asks a focused biological question — *which subset of canonical PXR target genes is actually transcriptionally coupled to NR1I2 in each cell type where the receptor is detected?* — and answers it with a metacell-aggregated single-cell pipeline across 446,672 cells (10 cell types) from CELLxGENE Census, with six orthogonal validation layers.

Six canonical PXR targets — CYP2C9 (Spearman rho 0.89), CYP3A5 (0.87), ABCC2 (0.85), SLCO1B1 (0.85), CYP2C8 (0.81), and CPT1A (0.77) — are strongly coupled to NR1I2 in hepatocytes (BH q approximately 0.004), but show only weak baseline coupling in immune and placental cells (mean rho 0.03 to 0.12, top-gene rho 0.19 to 0.24 in CD4+ T, macrophage, monocyte, NK; near-zero in placenta), even when sample sizes (50 to 110 k cells per immune cell type) make those weak effects formally significant. The effect-size differential is 4 to 8 fold. The pattern is epithelial-barrier-selective rather than generically hepatic (matched 20-gene negative-control set: PXR-target vs control DS Mann-Whitney U one-sided p = 1.0 x 10^-31; hepatocyte master TFs HNF4A and HNF1A do *not* show high DS).

The headline replicates across five orthogonal external datasets and modalities: (i) GTEx v8 bulk RNA-seq across 54 tissues recovers the same liver-vs-immune contrast for all five top genes (delta = +0.21 to +0.56); (ii) direct rifamycin perturbation of primary human hepatocytes (GSE139896, Dyavar et al. 2020 *Sci Rep*) confirms four of the six top genes (CYP2C8, CYP2C9, CYP3A5, ABCC2) as PXR-responsive with up to 19-fold induction; (iii) LINCS L1000 rifampicin signature strength across 18 cell lines ranks HEPG2 #1 (1.47x the non-hepatic mean); (iv) Open Targets disease associations recover textbook PXR pharmacology (warfarin, statins, cholestasis, tacrolimus); (v) a parameter sweep (17 combinations) and 20 rounds of 80% cell-level subsampling confirm rank stability.

An honest refinement: SLCO1B1 and CPT1A are coupled in baseline scRNA-seq but do *not* respond to rifamycin in primary hepatocytes, implying their hepatocyte coupling reflects shared regulation by HNF4A and FOXA1/2 rather than direct PXR control. The actionable biomarker panel for next-generation PXR-targeted drugs is therefore the four-gene set CYP2C8 / CYP2C9 / CYP3A5 / ABCC2.

The project is single-author, runs end-to-end on a workstation in under five minutes once the H5AD is cached, and is fully reproducible: MIT-licensed code, locked dependencies, 16 passing pytest tests, GitHub Actions CI, a CITATION.cff, and per-gene evidence dossiers. This OSF project is structured as a parent project with five components (Manuscript, Code, Data, Figures, Dossiers) so reviewers and reusers can navigate each artefact directly.

## Wiki home page content

```markdown
# pxr-effector-uncoupling

**A cell-type-resolved, statistically-grounded map of which PXR (NR1I2) target genes stay coupled to receptor expression vs. which decouple.**

- **GitHub:** https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling
- **Author:** Amit Shenoy, Northeastern University (shenoy.am@husky.neu.edu)
- **License:** MIT (code) / CC-BY-4.0 (figures, data, manuscript)

## Components

- **Manuscript** — full manuscript Markdown and PDF
- **Code** — Python source, scripts, notebooks, tests, CI
- **Data** — processed CSVs (coupling, decoupling, CIs, p/q values, external validations), curated gene tables
- **Figures** — all main and supplementary PNG figures
- **Dossiers** — per-gene evidence dossiers (PMID-tagged target curation)

## Key result

| Gene | Hepatocyte rho (95% CI) | BH q-value | Decoupling score | Direct PXR target (rifamycin)? |
|------|-------------------------|------------|------------------|--------------------------------|
| CYP2C9  | 0.89 (0.86 to 0.92) | 0.004 | 0.698 | Yes |
| CYP3A5  | 0.87 (0.84 to 0.90) | 0.004 | 0.631 | Yes |
| ABCC2   | 0.85 (0.82 to 0.87) | 0.004 | 0.677 | Yes |
| SLCO1B1 | 0.85 (0.81 to 0.88) | 0.004 | 0.756 | No (HNF4A coupling) |
| CYP2C8  | 0.81 (0.77 to 0.85) | 0.004 | 0.695 | Yes — strongest, up to 19x |
| CPT1A   | 0.77 (0.73 to 0.82) | 0.004 | 0.658 | No (HNF4A/PPARalpha coupling) |

## Reproducibility

```bash
uv sync
uv run python scripts/run_analysis.py
uv run python scripts/run_robustness.py
uv run pytest -v
```

All processed CSVs are in `data/processed/`; raw H5AD is fetched separately via `gh workflow run fetch_atlas.yml`.

## Citation

See `CITATION.cff` and the Zenodo DOI (linked once minted).
```

## OSF settings

- **Visibility:** Public (the work is intended to be openly browseable).
- **License:** CC-BY-4.0 at the project level.
- **Default storage:** OSF Storage; mirror code to a connected GitHub addon pointed at `xX-its-amit-Xx/pxr-effector-uncoupling`.
- **Tags:** PXR, NR1I2, single-cell-RNAseq, metacells, pharmacogenomics, hepatocyte, CELLxGENE, GTEx, LINCS, OpenTargets, reproducible-bioinformatics.
- **Subjects:** Bioinformatics; Pharmacology; Computational Biology; Hepatology.
