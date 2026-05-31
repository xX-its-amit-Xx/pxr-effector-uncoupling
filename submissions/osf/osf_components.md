# OSF components

The OSF project should be created as a parent project with five sub-components. Each component has its own DOI-citable landing page and can be navigated independently. The recommended structure mirrors the repository's logical division.

## Parent project

**Title:** pxr-effector-uncoupling: cell-type-resolved coupling of PXR (NR1I2) target genes across 446,672 single human cells
**Visibility:** Public
**License:** CC-BY-4.0
**Storage addons:** OSF Storage (default); GitHub addon connected to `xX-its-amit-Xx/pxr-effector-uncoupling`

## Component 1 — Manuscript

- **Title:** Manuscript - "Cell-type-resolved decoupling of PXR target genes identifies hepatocyte-selective readouts for xenobiotic response"
- **Description:** Full manuscript Markdown source and rendered PDF, plus the structured abstract, plain-language summary, and supplementary methods. Mirror of `manuscript/manuscript.md` from the repository.
- **Files to upload:**
  - `manuscript/manuscript.md`
  - `manuscript/manuscript.pdf` (render via `pandoc manuscript.md -o manuscript.pdf --pdf-engine=xelatex` from the repository's `manuscript/` directory)
  - `CITATION.cff`
- **Tags:** manuscript, preprint, PXR
- **License:** CC-BY-4.0

## Component 2 — Code

- **Title:** Code - reproducible pipeline (MIT-licensed Python)
- **Description:** Source modules (`src/pxr_uncoupling/`), entry-point scripts (`scripts/`), Jupyter notebooks (`notebooks/`), pytest unit tests (`tests/`), and pinned environment (`pyproject.toml`, `uv.lock`). 16 tests pass; GitHub Actions CI runs on every push.
- **Addons:** GitHub addon - mirror `xX-its-amit-Xx/pxr-effector-uncoupling` (read-only).
- **Files to upload manually (snapshot):**
  - `pyproject.toml`, `uv.lock`
  - All files under `src/pxr_uncoupling/`
  - All files under `scripts/`
  - All files under `notebooks/`
  - All files under `tests/`
  - `LICENSE` (MIT)
- **Tags:** software, python, reproducibility, scanpy, metacells
- **License:** MIT

## Component 3 — Data

- **Title:** Data - processed CSVs and curated gene tables
- **Description:** All derived data products from the analysis: coupling matrices with bootstrap CIs and BH-FDR q-values, decoupling scores, negative-control comparisons, GTEx replication, GSE139896 rifamycin perturbation summary, LINCS L1000 strength, Open Targets associations, parameter-sweep agreement, subsample stability, per-dataset hepatocyte analysis, and atlas provenance. Also includes the curated PXR target panel and the matched negative-control gene table.
- **Files to upload:**
  - All CSV/JSON files under `data/processed/`
  - All TSV files under `data/targets/`
- **Tags:** dataset, csv, processed-data, PXR-targets, negative-controls
- **License:** CC-BY-4.0
- **Note:** The raw CELLxGENE Census H5AD (`data/raw/nr1i2_atlas.h5ad`, ~600 MB) is *not* included; it is reproducible from CELLxGENE Census v2025-01-30 via the `fetch_atlas.yml` GitHub Actions workflow.

## Component 4 — Figures

- **Title:** Figures - main and supplementary
- **Description:** All publication figures (PNG, 300 DPI) referenced in the manuscript:
  - Fig. 1 - main coupling heatmap (10 cell types x 20 genes)
  - Fig. 2a - BH-FDR significance overlay
  - Fig. 2b - top-10 hepatocyte rho with 95% bootstrap CIs
  - Fig. 3 - PXR targets vs matched negative controls (Mann-Whitney U)
  - Fig. 4 - GTEx v8 bulk-tissue replication across 54 tissues
  - Fig. 5 - direct rifamycin perturbation in primary human hepatocytes (GSE139896)
  - Fig. 6 - LINCS L1000 rifampicin signature strength + replicate consistency
  - Fig. 7 - Open Targets disease-association validation
  - Fig. S1 - parameter sweep agreement
  - Fig. S2 - 80% subsample stability
  - Fig. S3 - per-dataset hepatocyte coupling
- **Files to upload:** all PNGs in `figures/`.
- **Tags:** figures, png, heatmap, scrnaseq
- **License:** CC-BY-4.0

## Component 5 — Dossiers (per-gene evidence)

- **Title:** Dossiers - per-gene PMID-tagged target evidence
- **Description:** Curated, evidence-graded per-gene dossiers for the 20 canonical PXR target panel and the 20 matched negative controls. Each entry includes A/B evidence grade and PMID-tagged source citations underpinning the inclusion in the target panel.
- **Files to upload:**
  - `data/targets/pxr_canonical_targets.tsv`
  - `data/targets/negative_control_genes.tsv`
  - (Optional) any per-gene Markdown dossier files generated for the project; if not present, the TSV files themselves are the canonical machine-readable evidence record.
- **Tags:** target-curation, PMID, evidence-grade, PXR, NR1I2
- **License:** CC-BY-4.0

## Recommended creation order

1. Create the parent project on osf.io (Title from above).
2. Add Wiki home content from `osf_project_description.md` (the "Wiki home page content" block).
3. Create components 1 to 5 as sub-projects (use the "Add Component" UI inside the parent project).
4. For component 2 (Code), connect the GitHub addon to mirror the live repository.
5. Set each component's license and tags as listed above.
6. Mark the parent project Public and request DOI minting (the "Create DOI" button appears once the project has files and a non-empty description).
