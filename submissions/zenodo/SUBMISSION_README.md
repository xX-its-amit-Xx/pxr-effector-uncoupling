# Zenodo deposit — how to create

## What you are creating

A Zenodo software deposit that mints a citable DOI for the entire `pxr-effector-uncoupling` repository at the v0.2.0 tag. This complements the GitHub repository (which is the live development home) by providing a persistent, citable archive.

## Two paths

### Path A (recommended): GitHub <-> Zenodo automatic deposit

This is the standard and lowest-friction route for software with a GitHub home.

1. Log into https://zenodo.org with the same email used on GitHub, then go to https://zenodo.org/account/settings/github/.
2. Find `xX-its-amit-Xx/pxr-effector-uncoupling` in the repository list and flip the toggle to ON.
3. In the local repository, copy `submissions/zenodo/.zenodo.json` to the repository root: `cp submissions/zenodo/.zenodo.json .zenodo.json`. Commit and push to `main`.
   - This metadata file is what Zenodo reads when minting the deposit; the existing `CITATION.cff` is also picked up.
4. Open https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling/releases/new and create a release tagged `v0.2.0` with title "v0.2.0 - submission archive" (paste the abstract from `manuscript/manuscript.md` as the release body).
5. Publishing the GitHub release triggers a Zenodo webhook that:
   - Downloads the release tarball
   - Reads `.zenodo.json` for metadata
   - Mints a DOI (concept DOI + version DOI)
   - Returns the DOI within ~1 minute

6. Add the DOI badge to README.md and CITATION.cff (Zenodo provides the Markdown badge snippet on the deposit landing page).

### Path B: Manual web upload

If you prefer not to wire up the GitHub integration:

1. From the repository root, create a zip excluding the venv, raw H5AD, and caches:
   ```bash
   git archive --format=zip --prefix=pxr-effector-uncoupling-v0.2.0/ HEAD > pxr-effector-uncoupling-v0.2.0.zip
   ```
2. Go to https://zenodo.org/uploads/new.
3. Drag `pxr-effector-uncoupling-v0.2.0.zip` to the upload area.
4. Open `submissions/zenodo/.zenodo.json` in another tab; copy each field into the corresponding Zenodo form input:
   - **Upload type:** Software
   - **Title:** (copy from JSON)
   - **Authors:** Amit Shenoy, Northeastern University, ORCID 0000-0000-0000-0000 (replace placeholder with your real ORCID before publishing)
   - **Description:** paste the HTML from the JSON
   - **Keywords:** paste each keyword from the JSON
   - **License:** MIT (and note CC-BY-4.0 for non-code in the description)
   - **Related/alternate identifiers:** paste each entry from `related_identifiers` in the JSON
   - **Version:** 0.2.0
5. Click "Publish". DOI is minted immediately.

## Before publishing — checklist

- [ ] Replace the ORCID placeholder `0000-0000-0000-0000` in `.zenodo.json` with the real ORCID (or remove the field).
- [ ] Confirm the GitHub repository URL is correct (the manuscript and README both currently reference `https://github.com/xX-its-amit-Xx/pxr-effector-uncoupling` while CITATION.cff says `https://github.com/ashenoy00000/pxr-effector-uncoupling` — pick one and reconcile before publishing).
- [ ] Add a `v0.2.0` git tag locally and push it: `git tag v0.2.0 && git push origin v0.2.0`.
- [ ] Confirm `CITATION.cff` is present in the repository root.
- [ ] Optional: add Zenodo as a registered community (`biotools`, `biohackathon` are pre-seeded in `.zenodo.json`).

## After publishing

- Add the DOI badge to README.md, e.g.:
  ```markdown
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
  ```
- Update CITATION.cff with the new DOI under `identifiers:`.
- Reference the concept DOI (not the version DOI) in the journal manuscript's "Code Availability" section so that the citation remains valid across future versions.

## Timeline

- DOI minting: ~1 minute after publish.
- Zenodo metadata indexing in DataCite + Google Scholar: 24 to 72 hours.
- No editorial review; Zenodo is an archive, not a journal.
