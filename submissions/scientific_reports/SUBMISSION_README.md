# Scientific Reports submission checklist

## Files to upload via Nature Manuscript Tracking System (mts-sciencereports.nature.com)

| MTS section | File | Format |
|-------------|------|--------|
| Cover Letter | `submissions/scientific_reports/cover_letter.md` -> PDF/DOCX | paste body OR upload PDF |
| Manuscript | `submissions/scientific_reports/manuscript.md` -> DOCX (preferred) or LaTeX | embedded figures and tables |
| Fig 1 | `figures/fig1_coupling_heatmap.png` | PNG, TIFF, EPS, or PDF; 300 DPI minimum |
| Fig 2 (multi-panel a+b) | combine `figures/fig2a_significance_overlay.png` + `figures/fig2b_forest_hepatocyte.png` as a single multi-panel figure | |
| Fig 3 | `figures/fig3_negative_control.png` | |
| Fig 4 | `figures/fig4_gtex_validation.png` | |
| Fig 5 | `figures/fig5_rifamycin_perturbation.png` | |
| Fig 6 | `figures/fig6_lincs_rifampicin.png` | |
| Fig 7 | `figures/fig7_opentargets.png` | |
| Supplementary Information | combine Fig S1 + S2 + S3 PNGs + Supplementary Methods text into a single `Supplementary_Information.pdf` | |

## Format requirements (per Scientific Reports author guidelines)

- **Abstract:** unstructured, <= 200 words. The abstract in `manuscript.md` is exactly 200 words (verified at commit time); re-check if you edit it further.
- **Main text structure:** Introduction -> Results -> Discussion -> Methods (Methods come AFTER Discussion, not before).
- **Word count:** no fixed limit, but typical articles 4,000 to 8,000 words including Methods.
- **References:** Vancouver-style numbered citations; cited sequentially. Use journal abbreviations per the Nature reference style (already in place).
- **Figures:** RGB, 300 DPI for raster; vector for line art; max 18 cm wide; embed in main text near first citation.
- **Tables:** in-text, with a brief caption above each table.
- **Data Availability statement:** required.
- **Code Availability statement:** required.
- **Author Contributions statement:** required (even for single author — see template in `manuscript.md`).
- **Competing Interests statement:** required.
- **Funding statement:** required.

## MTS web-form fields

- **Article type:** Article (research)
- **Subject area (primary):** Biological sciences > Computational biology and bioinformatics
- **Subject area (secondary):** Health sciences > Pharmacogenomics; Biological sciences > RNA sequencing
- **Title:** Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response
- **Corresponding author:** Amit Shenoy, Northeastern University, shenoy.am@husky.neu.edu
- **Suggested reviewers:** suggest 3 to 5 experts (Petr Pavek / Charles University; Kim Brouwer / UNC; Bryan Mackowiak / FDA; Dvir Aran / Technion; Bhaven Mehta / Pfizer — none direct collaborators).
- **Non-preferred reviewers:** none.
- **Funding:** "This work received no external funding."
- **Competing interests:** "The author declares no competing interests."
- **Data availability:** copy from `manuscript.md` Data availability section.
- **Code availability:** copy from `manuscript.md` Code availability section.

## Pre-submission checklist

- [x] Abstract is at 200 words (the Scientific Reports cap). Re-verify if you edit it.
- [ ] Manuscript converted from Markdown to DOCX with figures embedded near first citation: `pandoc manuscript.md -o manuscript.docx --resource-path=.:..:../..`.
- [ ] All figures at 300 DPI minimum, RGB, <= 18 cm wide.
- [ ] Multi-panel Fig 2 assembled (a + b panels labelled).
- [ ] Supplementary PDF assembled (S1 + S2 + S3 + Supplementary Methods).
- [ ] References checked: Vancouver style, sequentially numbered, journal abbreviations per Nature style.
- [x] GitHub repository URL reconciled — CITATION.cff now points to `xX-its-amit-Xx/pxr-effector-uncoupling` (matches manuscript and README).
- [ ] CITATION.cff present at repository root.

## Article processing charge

Scientific Reports APC is currently USD 2,290 (as of 2025). Northeastern University may have a Springer-Nature read-and-publish agreement covering Scientific Reports; check with the library before submission. Fee waivers / discounts available for authors from low-income countries; not applicable here.

## Timeline

- Initial editorial assessment: 1 to 3 weeks.
- Peer review: typically 2 to 4 months for first decision.
- Average time from submission to publication: ~5 months for accepted papers.
