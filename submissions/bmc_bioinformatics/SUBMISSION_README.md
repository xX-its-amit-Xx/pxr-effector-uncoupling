# BMC Bioinformatics submission checklist

## Article type

**Software** (BMC Bioinformatics article type for reusable tools and pipelines with a worked example). The alternative is "Methodology" — if you prefer not to highlight the software framing, switch the article type during submission; the structure of `manuscript.md` works for either.

## Files to upload via the BMC manuscript-tracking portal (snapp.embnet.org / bmcbioinformatics.biomedcentral.com)

| Field | File | Format |
|-------|------|--------|
| Cover letter | `submissions/bmc_bioinformatics/cover_letter.md` -> PDF/DOCX | paste body OR upload |
| Manuscript | `submissions/bmc_bioinformatics/manuscript.md` -> DOCX or PDF | DOCX preferred |
| Fig 1 | `figures/fig1_coupling_heatmap.png` | PNG, TIFF, or EPS; 300 DPI; <= 85 mm width single-column or <= 170 mm double-column |
| Fig 2 (multi-panel) | combine `figures/fig2a_significance_overlay.png` + `figures/fig2b_forest_hepatocyte.png` | label panels (a), (b) |
| Fig 3 | `figures/fig3_negative_control.png` | |
| Fig 4 | `figures/fig4_gtex_validation.png` | |
| Fig 5 | `figures/fig5_rifamycin_perturbation.png` | |
| Fig 6 | `figures/fig6_lincs_rifampicin.png` | |
| Fig 7 | `figures/fig7_opentargets.png` | |
| Additional file 1 (S1) | `figures/figS1_parameter_sensitivity.png` | |
| Additional file 2 (S2) | `figures/figS2_subsample_stability.png` | |
| Additional file 3 (S3) | `figures/figS3_per_dataset_hepatocyte.png` | |
| Additional file 4 | curated target gene table | `data/targets/pxr_canonical_targets.tsv` |
| Additional file 5 | matched negative-control gene table | `data/targets/negative_control_genes.tsv` |
| Additional file 6 | atlas provenance | `data/processed/atlas_provenance.csv` |

## BMC Bioinformatics format checklist

- **Title:** descriptive; the current title emphasises the methods contribution.
- **Abstract:** structured (Background / Results / Conclusions). The version in `manuscript.md` follows this structure.
- **Main text structure:** Background -> Implementation -> Results -> Discussion -> Conclusions -> Availability and requirements -> Competing interests -> Funding -> Authors' contributions -> Acknowledgements -> References.
- **References:** Vancouver-style numbered; sequentially cited; abbreviated journal titles per Index Medicus.
- **Availability and requirements section:** must include operating system, programming language, license, any restrictions, dependencies. The version in `manuscript.md` follows the required template.
- **Figures:** TIFF, EPS, PNG, or JPEG; vector (PDF/EPS) for line art; 300 DPI minimum for raster; labelled "(a)", "(b)", etc. for multi-panel.
- **Additional files:** numbered Additional file 1, Additional file 2, ...; each with a 1 to 2 sentence description in the main text.
- **No author photos.**
- **Word count:** no strict limit; typical Software articles ~5,000 to 8,000 words including methods.

## Web-form fields

- **Article type:** Software
- **Section/subject:** Methods; Tools; Pharmacogenomics; Single-cell methods.
- **Title:** A reusable metacell-coupling pipeline for cell-type-resolved nuclear-receptor target analysis at single-cell atlas scale, applied to PXR (NR1I2) across 446,672 human cells
- **Corresponding author:** Amit Shenoy, Northeastern University, shenoy.am@husky.neu.edu
- **Abstract:** copy structured Background / Results / Conclusions from `manuscript.md`.
- **Keywords:** metacells, single-cell RNA-seq, coupling analysis, nuclear receptor, PXR, NR1I2, CELLxGENE, reproducible bioinformatics, pharmacogenomics.
- **Suggested reviewers:** suggest 3 to 5 with single-cell methods, reproducible-pipelines, or nuclear-receptor expertise. Avoid direct collaborators within the past 4 years.
- **Conflict of interest:** "The author declares no competing interests."
- **Funding:** "This work received no external funding."

## Pre-submission checklist

- [ ] Manuscript rendered from Markdown to DOCX: `pandoc manuscript.md -o manuscript.docx --resource-path=.:..:../..`.
- [ ] All figures at 300 DPI, with panel labels (a), (b), ...
- [ ] Multi-panel Fig 2 assembled.
- [ ] All Additional files numbered and described in main text.
- [ ] References checked: Vancouver style, Index Medicus journal abbreviations, sequential citations.
- [ ] GitHub repository URL reconciled (discrepancy: manuscript uses `xX-its-amit-Xx/pxr-effector-uncoupling`; CITATION.cff says `ashenoy00000/...` — pick one before submission).
- [ ] CITATION.cff present at repository root.
- [ ] `uv.lock` committed.
- [ ] 16 pytest tests pass on a fresh checkout (`uv sync && uv run pytest -v`).
- [ ] CI workflow visible at https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling/actions.

## Article processing charge

BMC Bioinformatics APC is currently USD 2,790 (Springer Nature, 2025). Northeastern University may have a transformative agreement covering BMC titles; check with the library before submission. Fee waivers are available for low-income countries (not applicable here) and on hardship grounds (apply before submission rather than at acceptance).

## Timeline

- Initial technical pre-screen: ~1 week.
- Peer review: 2 to 4 months typically.
- Average time to publication for accepted papers: ~4 months from submission.
