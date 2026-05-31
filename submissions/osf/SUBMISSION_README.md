# OSF project — how to create

## Goal

A public Open Science Framework (OSF) project at https://osf.io/ that:
1. Provides a citable DOI for the whole study
2. Organises the work into five browseable components (Manuscript / Code / Data / Figures / Dossiers)
3. Mirrors the GitHub repository's code via the OSF GitHub addon
4. Stands as a one-stop entry point for reviewers, reusers, and citations

## Step-by-step

1. **Sign in.** Create an account at https://osf.io/ if needed; sign in with the email `shenoy.am@husky.neu.edu`.

2. **Create the parent project.**
   - "Create new project" -> Title: *pxr-effector-uncoupling: cell-type-resolved coupling of PXR (NR1I2) target genes across 446,672 single human cells*
   - Description: paste the "Public project description" block from `osf_project_description.md`.
   - Storage location: pick the institutional or default region.

3. **Set tags and subjects.**
   - Tags: PXR, NR1I2, single-cell-RNAseq, metacells, pharmacogenomics, hepatocyte, CELLxGENE, GTEx, LINCS, OpenTargets, reproducible-bioinformatics
   - Subjects (under "Add a subject"): Bioinformatics; Pharmacology; Computational Biology; Hepatology

4. **Set license.** Click "Add a license" -> CC-BY-4.0; the year is 2026; the copyright holder is "Amit Shenoy".

5. **Set up the Wiki home.**
   - Open the project's Wiki tab.
   - Paste the "Wiki home page content" block from `osf_project_description.md` into the `home` page.
   - Save.

6. **Create the five components.** For each component listed in `osf_components.md`:
   - Click "Add Component" inside the parent project.
   - Title, description, tags, and license as specified.
   - Upload the file list specified.

7. **Connect GitHub addon (for the Code component).**
   - Inside the Code component, open Settings -> Add-ons.
   - Enable GitHub.
   - Authorize OSF to read your GitHub account.
   - Connect the repository `xX-its-amit-Xx/pxr-effector-uncoupling`.

8. **Make public.**
   - On each component and the parent project: Settings -> Project Visibility -> Public.
   - OSF will warn that this action is irreversible without contacting support; this is intentional.

9. **Request DOI minting.**
   - Once the parent project is Public and has a description + at least one component with files, the "Create DOI" button becomes available at Settings -> DOI.
   - Click it. OSF mints a DOI via DataCite within minutes.
   - You can repeat the DOI request for each component if you want individually citable DOIs for, e.g., the Data and Code components.

## Before publishing — checklist

- [ ] GitHub repository URL is reconciled (manuscript and README use `xX-its-amit-Xx/pxr-effector-uncoupling`; CITATION.cff currently says `ashenoy00000/pxr-effector-uncoupling` — pick one before publishing).
- [ ] `CITATION.cff` is present in the repository root and references the correct GitHub URL.
- [ ] `manuscript/manuscript.pdf` has been rendered (or the Markdown is uploaded along with figures the OSF previewer can resolve).
- [ ] If you want a single landing page for citing the whole project, mint the DOI on the parent project; if you want per-component citations, mint per component.

## Timeline

- DOI minting: a few minutes after the public + has-files threshold is met.
- DataCite + Google Scholar indexing: 24 to 72 hours.
- No editorial review; OSF is a project-hosting platform, not a journal.

## What this is *not*

- OSF is not a peer-reviewed venue. The submission here exists to provide a stable, browseable home and a citable DOI; it does not substitute for or compete with a journal submission.
- OSF Preprints (osf.io/preprints) is a separate sister product; if you also want a Bioinformatics-flavored preprint posting, consider Research Square or bioRxiv in addition. This project page is the *home*, not a preprint.
