# PLOS ONE submission checklist

## Files to upload via Editorial Manager (editorialmanager.com/pone/)

| Editorial Manager item | File | Format |
|------------------------|------|--------|
| Cover Letter | `submissions/plos_one/cover_letter.md` | paste body into the cover-letter field; PDF also acceptable |
| Manuscript | `submissions/plos_one/manuscript.md` -> render to DOCX | DOCX preferred for editorial; LaTeX also accepted |
| Fig 1 (file `Fig1.tif`) | `figures/fig1_coupling_heatmap.png` -> convert to TIFF | TIFF, RGB, LZW, 300 DPI |
| Fig 2a | `figures/fig2a_significance_overlay.png` -> TIFF | (consider combining 2a + 2b as a single multi-panel Fig 2) |
| Fig 2b | `figures/fig2b_forest_hepatocyte.png` -> TIFF | |
| Fig 3 | `figures/fig3_negative_control.png` -> TIFF | |
| Fig 4 | `figures/fig4_gtex_validation.png` -> TIFF | |
| Fig 5 | `figures/fig5_rifamycin_perturbation.png` -> TIFF | |
| Fig 6 | `figures/fig6_lincs_rifampicin.png` -> TIFF | |
| Fig 7 | `figures/fig7_opentargets.png` -> TIFF | |
| Fig S1 | `figures/figS1_parameter_sensitivity.png` -> TIFF | uploaded as Supporting Information |
| Fig S2 | `figures/figS2_subsample_stability.png` -> TIFF | uploaded as Supporting Information |
| Fig S3 | `figures/figS3_per_dataset_hepatocyte.png` -> TIFF | uploaded as Supporting Information |
| Supporting Information S1 Table | curated PXR target panel | upload `data/targets/pxr_canonical_targets.tsv` |
| Supporting Information S2 Table | matched negative controls | upload `data/targets/negative_control_genes.tsv` |
| Supporting Information S3 Table | atlas provenance | upload `data/processed/atlas_provenance.csv` |

## Figure conversion — PLOS-specific requirements

PLOS uses the PACE tool (https://pacev2.apexcovantage.com) for figure-format validation. Each figure should be:

- TIFF, EPS, or PDF (TIFF preferred for raster figures like ours)
- RGB or CMYK colour space (RGB is fine)
- Compression: LZW
- Resolution: 300 to 600 DPI
- Size: <= 19.05 cm wide for double-column figures; <= 8.30 cm for single-column
- Embedded fonts (no font references)
- No transparency layers
- File name in the form `Fig1.tif`, `Fig2.tif`, ... (no spaces, no underscores in the figure-number portion)

A one-line ImageMagick conversion (assuming the source PNG is 300 DPI):

```bash
for f in figures/fig*.png; do
  out=$(basename "$f" .png).tif
  magick "$f" -compress LZW -density 300 -units PixelsPerInch "$out"
done
```

Then rename to PLOS convention: `mv fig1_coupling_heatmap.tif Fig1.tif`, etc.

Once converted, upload each TIFF to PACE for validation before submitting through Editorial Manager.

## Editorial Manager web-form fields

- **Article type:** Research Article
- **Section/category:** Bioinformatics; Pharmacology (secondary).
- **Title:** Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response
- **Short title:** Hepatocyte-selective PXR target coupling at single-cell resolution
- **Author:** Amit Shenoy (corresponding), Northeastern University, shenoy.am@husky.neu.edu
- **Abstract:** copy the structured abstract from `manuscript.md` (Background / Methods / Results / Conclusions).
- **Keywords:** PXR, NR1I2, single-cell RNA-seq, metacells, drug-drug interaction, cell-type specificity, hepatocyte, pharmacogenomics, CELLxGENE.
- **Financial Disclosure:** "This work received no external funding."
- **Competing Interests:** "The author declares no competing interests."
- **Data Availability:** copy the Data Availability statement from `manuscript.md` verbatim.
- **Reviewer suggestions:** suggest 3 to 5 reviewers with PXR / single-cell / pharmacogenomics expertise (not collaborators within the past 4 years). Examples to consider: Kim Brouwer (UNC, hepatic transporter pharmacology), Petr Pavek (Charles University, PXR/CAR pharmacology), Maria Anisimova (computational replication), Dvir Aran (Technion, single-cell methods).
- **Reviewer exclusions:** none required.

## Submission timeline

- Initial editorial assessment: 1 to 2 weeks for technical-soundness screening.
- Peer review: typically 2 to 4 months for an initial decision.
- Average time to publication for accepted PLOS ONE papers: approximately 5 months.

## Pre-submission checklist

- [ ] Manuscript Markdown rendered to DOCX (with figures embedded *in* the text, not at the end, per PLOS's "embedded figures with separate file upload" policy).
- [ ] All figures converted to TIFF and validated through PACE.
- [ ] Supporting Information tables uploaded with descriptive captions in the manuscript.
- [ ] References checked: Vancouver style, sequentially numbered, no broken DOIs.
- [ ] CITATION.cff and `LICENSE` files visible at the GitHub repository root.
- [ ] GitHub repository URL reconciled across manuscript and CITATION.cff (currently has a discrepancy: manuscript uses `xX-its-amit-Xx/pxr-effector-uncoupling`; CITATION.cff uses `ashenoy00000/pxr-effector-uncoupling`).
- [ ] Zenodo DOI minted and added to "Data availability" before final submission, OR explicitly noted as "will be deposited at Zenodo on acceptance".

## Article processing charge

PLOS ONE APC is currently USD 1,931 (Aug 2024). PLOS offers a Global Equity programme and publication-fee assistance for authors who cannot meet the full APC; given the no-funding single-author status, apply early via the Global Participation Initiative or fee-waiver request before final acceptance.
