# Research Square submission checklist

## Files to upload

| Field | File |
|-------|------|
| Manuscript (PDF or DOCX) | Convert `submissions/research_square/manuscript.md` to PDF or DOCX before upload. |
| Cover letter | `submissions/research_square/cover_letter.md` (paste body into the cover-letter field) |
| Figures | All PNGs in `figures/` (fig1 to fig7 main, figS1 to figS3 supplementary). Embed in the manuscript file. |
| Supplementary code/data link | GitHub URL (entered in the "Supplementary Materials" field): https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling |

## Web-form fields

- **Title:** Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response
- **Authors:** Amit Shenoy (corresponding) — Northeastern University, Boston MA, USA — shenoy.am@husky.neu.edu
- **Subject category:** Bioinformatics (primary); Pharmacology and Pharmacy (secondary); Hepatology (tertiary).
- **Keywords:** PXR, NR1I2, single-cell RNA-seq, metacells, drug-drug interaction, cell-type specificity, hepatocyte, pharmacogenomics, CELLxGENE.
- **Statement of significance:** Copy from the "Research Square Front Matter" block at the top of `manuscript.md`.
- **Plain language summary:** Copy from the "Plain Language Summary" block at the top of `manuscript.md` (approximately 470 words).
- **Funding statement:** This work received no external funding.
- **Conflict of interest statement:** The author declares no competing interests.
- **Data availability:** All data sources are publicly accessible (CELLxGENE Census v2025-01-30; GTEx v8; GEO GSE139896; iLINCS LIB_5; Open Targets v4). Processed data files in https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling/tree/main/data/processed.
- **Code availability:** MIT-licensed at https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling with CITATION.cff and pinned dependencies in `uv.lock`.

## Conversion to PDF

```bash
# Markdown to PDF, embedding figures from the relative path:
cd submissions/research_square
pandoc manuscript.md -o manuscript.pdf --pdf-engine=xelatex --resource-path=.:..:../..
```

If pandoc + xelatex aren't available, convert via VS Code's "Markdown PDF" extension or render to DOCX with `pandoc manuscript.md -o manuscript.docx --resource-path=.:..:../..`.

## Expected timeline

- Editorial pre-screen for plagiarism / scope / completeness: 1 to 3 business days.
- DOI assignment and posting: typically within 5 to 7 business days of submission.
- Optional in-review badge appears once a journal links to it.

## Notes

- This is a preprint deposit, not peer review. No reviewer-response cycle.
- Updates / new versions can be posted later (e.g., after peer review elsewhere); each version gets a new DOI suffix.
- Research Square mirrors content to NCBI's preprint index where eligible.
