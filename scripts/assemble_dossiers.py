"""Assemble per-gene markdown dossiers from cached API pulls + the paper's CSVs.

Reads :
    dossiers/_cache/<GENE>_open_targets.json    (built by build_dossier_data.py)
    dossiers/_cache/<GENE>_chembl.json
    data/processed/coupling.csv, coupling_ci_{lower,upper}.csv, coupling_qvalues.csv
    data/processed/decoupling.csv

Writes:
    dossiers/<GENE>.md                          (one self-contained brief per gene)
    dossiers/README.md                          (index)

Adds a "Recent literature" section pulled live from NCBI E-utilities so each
dossier ships with the most recent ~5 PubMed abstracts mentioning the gene
together with PXR / NR1I2 — bounded query, no API key required.
"""

# ruff: noqa: E501  # rendered output strings are intentionally long


from __future__ import annotations

import json
import logging
import textwrap
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import httpx
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "dossiers" / "_cache"
OUT = ROOT / "dossiers"
OUT.mkdir(parents=True, exist_ok=True)

GENES = [
    ("CYP2C9", "ENSG00000138109", "CHEMBL3397", "P11712"),
    ("CYP3A5", "ENSG00000106258", "CHEMBL3019", "P20815"),
    ("ABCC2", "ENSG00000023839", "CHEMBL5748", "Q92887"),
    ("SLCO1B1", "ENSG00000134538", "CHEMBL1697668", "Q9Y6L6"),
    ("CYP2C8", "ENSG00000138115", "CHEMBL3721", "P10632"),
    ("CPT1A", "ENSG00000110090", "CHEMBL1293194", "P50416"),
    ("NR1I2", "ENSG00000144852", "CHEMBL3401", "O75469"),
]

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def load_paper_metrics() -> dict[str, dict]:
    c = pd.read_csv(ROOT / "data" / "processed" / "coupling.csv", index_col=0)
    lo = pd.read_csv(ROOT / "data" / "processed" / "coupling_ci_lower.csv", index_col=0)
    hi = pd.read_csv(ROOT / "data" / "processed" / "coupling_ci_upper.csv", index_col=0)
    q = pd.read_csv(ROOT / "data" / "processed" / "coupling_qvalues.csv", index_col=0)
    ds = pd.read_csv(ROOT / "data" / "processed" / "decoupling.csv", index_col=0)
    out: dict[str, dict] = {}
    for gene, *_ in GENES:
        if gene not in c.columns:
            out[gene] = {}
            continue
        rec = {
            "hep_rho": float(c.loc["hepatocyte", gene]),
            "hep_lo": float(lo.loc["hepatocyte", gene]),
            "hep_hi": float(hi.loc["hepatocyte", gene]),
            "hep_q": float(q.loc["hepatocyte", gene]),
            "per_cell_type": c[gene].to_dict(),
            "ds_mean": float(ds[gene].mean()) if gene in ds.columns else None,
        }
        out[gene] = rec
    return out


def fetch_pubmed_abstracts(gene: str, max_results: int = 5) -> list[dict]:
    """Pull the most recent PubMed records matching '<GENE> AND (PXR OR NR1I2)'.

    Cached to dossiers/_cache/<GENE>_pubmed.json — re-runs that hit the
    cache make no network calls. NCBI rate-limits unauthenticated clients
    to ~3 req/s; we sleep 1.2 s between calls to stay comfortably under.
    """
    cache = CACHE / f"{gene}_pubmed.json"
    if cache.exists():
        return json.loads(cache.read_text())
    query = f"{gene} AND (PXR OR NR1I2)"
    search = httpx.get(
        f"{EUTILS}/esearch.fcgi",
        params={"db": "pubmed", "term": query, "retmax": max_results, "sort": "pub_date"},
        timeout=30,
    )
    search.raise_for_status()
    ids = [pid.text for pid in ET.fromstring(search.text).findall(".//Id")]
    if not ids:
        return []
    time.sleep(0.4)
    fetch = httpx.get(
        f"{EUTILS}/efetch.fcgi",
        params={"db": "pubmed", "id": ",".join(ids), "retmode": "xml"},
        timeout=60,
    )
    fetch.raise_for_status()
    root = ET.fromstring(fetch.text)
    out: list[dict] = []
    for article in root.findall(".//PubmedArticle"):
        title_el = article.find(".//ArticleTitle")
        title = "".join(title_el.itertext()).strip() if title_el is not None else "(untitled)"
        year_el = article.find(".//PubDate/Year") or article.find(".//PubDate/MedlineDate")
        year = year_el.text[:4] if year_el is not None and year_el.text else ""
        journal_el = article.find(".//Journal/ISOAbbreviation")
        journal = journal_el.text if journal_el is not None else ""
        pmid_el = article.find(".//PMID")
        pmid = pmid_el.text if pmid_el is not None else ""
        abstract_parts = [
            ("".join(p.itertext()).strip()) for p in article.findall(".//Abstract/AbstractText")
        ]
        abstract = " ".join(abstract_parts)[:600]
        first_author_el = article.find(".//AuthorList/Author[1]/LastName")
        first_author = first_author_el.text if first_author_el is not None else ""
        out.append(
            {
                "pmid": pmid,
                "title": title,
                "first_author": first_author,
                "year": year,
                "journal": journal,
                "abstract": abstract,
            }
        )
    cache.write_text(json.dumps(out, indent=2))
    return out


def fmt_per_cell_type(per: dict[str, float]) -> str:
    order = [
        "hepatocyte",
        "enterocyte of epithelium of small intestine",
        "intestinal crypt stem cell",
        "enterocyte of epithelium of large intestine",
        "macrophage",
        "monocyte",
        "natural killer cell",
        "CD4-positive, alpha-beta T cell",
        "CD8-positive, alpha-beta T cell",
        "extravillous trophoblast",
    ]
    short = {
        "hepatocyte": "Hepatocyte",
        "enterocyte of epithelium of small intestine": "SI enterocyte",
        "intestinal crypt stem cell": "Crypt stem",
        "enterocyte of epithelium of large intestine": "LI enterocyte",
        "macrophage": "Macrophage",
        "monocyte": "Monocyte",
        "natural killer cell": "NK cell",
        "CD4-positive, alpha-beta T cell": "CD4+ T",
        "CD8-positive, alpha-beta T cell": "CD8+ T",
        "extravillous trophoblast": "EVT",
    }
    rows = ["| Cell type | Spearman ρ(NR1I2, gene) |", "|---|---|"]
    for c in order:
        if c not in per:
            continue
        rho = per[c]
        rows.append(f"| {short[c]} | {rho:.3f} |" if pd.notna(rho) else f"| {short[c]} | n/a |")
    return "\n".join(rows)


def fmt_tractability(t: list[dict]) -> str:
    if not t:
        return "_No tractability records returned by Open Targets._"
    by_modality: dict[str, list[str]] = {}
    for row in t:
        if row.get("value") is True:
            by_modality.setdefault(row["modality"], []).append(row["label"])
    if not by_modality:
        return "_All tractability flags returned `false` — the target currently lacks approved drugs, clinical candidates, or high-quality chemical probes recognised by Open Targets._"
    out = []
    name = {"SM": "Small molecule", "AB": "Antibody", "PR": "PROTAC", "OC": "Other clinical"}
    for mod, labels in by_modality.items():
        out.append(f"- **{name.get(mod, mod)}**: {', '.join(labels)}")
    return "\n".join(out)


def fmt_associated_diseases(rows: list[dict], n: int = 8) -> str:
    if not rows:
        return "_No associated diseases returned._"
    lines = ["| Rank | Disease | Score | Therapeutic area |", "|---|---|---|---|"]
    for i, r in enumerate(rows[:n], 1):
        d = r["disease"]
        ta = ", ".join(t["name"] for t in d.get("therapeuticAreas") or []) or "—"
        lines.append(f"| {i} | {d['name']} (`{d['id']}`) | {r['score']:.3f} | {ta} |")
    return "\n".join(lines)


def fmt_drugs(drug_block: dict) -> str:
    rows = drug_block.get("rows") or []
    if not rows:
        return "_No approved drugs or clinical candidates listed in Open Targets._\n\nThis is the expected pattern for metabolising enzymes and transporters: they are pharmacologically important but not therapeutic targets in their own right. See the ChEMBL bioactivity section below for tool compounds and substrates."
    seen = set()
    lines = ["| Drug | Max stage | Action | Drug type |", "|---|---|---|---|"]
    for r in rows[:15]:
        d = r["drug"]
        if d["id"] in seen:
            continue
        seen.add(d["id"])
        moa_rows = (d.get("mechanismsOfAction") or {}).get("rows") or []
        moa_txt = "; ".join(filter(None, [m.get("mechanismOfAction") for m in moa_rows[:2]])) or "—"
        action = ", ".join(sorted({m.get("actionType") or "—" for m in moa_rows[:2]})) or "—"
        lines.append(
            f"| {d['name']} (`{d['id']}`) | {d.get('maximumClinicalStage', '?')} | {action} ({moa_txt}) | {d.get('drugType', '—')} |"
        )
    return "\n".join(lines)


def fmt_pgx(pgx: list[dict], n: int = 8) -> str:
    if not pgx:
        return "_No pharmacogenomics records returned._"
    lines = ["| Variant | Drug(s) | Category | Phenotype | Evidence |", "|---|---|---|---|---|"]
    for r in pgx[:n]:
        drugs = (
            ", ".join(
                filter(
                    None,
                    [
                        (d.get("drugFromSource") or d.get("drugId") or "")
                        for d in (r.get("drugs") or [])
                    ],
                )
            )
            or "—"
        )
        variant = r.get("variantRsId") or r.get("variantFunctionalConsequenceId") or "—"
        cat = r.get("pgxCategory") or "—"
        pheno = (r.get("phenotypeText") or "")[:80] or "—"
        ev = r.get("evidenceLevel") or "—"
        lines.append(f"| {variant} | {drugs} | {cat} | {pheno} | {ev} |")
    return "\n".join(lines)


def fmt_safety(saf: list[dict], n: int = 6) -> str:
    if not saf:
        return "_No safety liabilities listed in Open Targets._"
    lines = [
        "| Event | Datasource | Effects (direction / dosing) | Biosample |",
        "|---|---|---|---|",
    ]
    for r in saf[:n]:
        ev = r.get("event") or r.get("eventId") or "—"
        ds = r.get("datasource") or "—"
        effects = (r.get("effects") or [{}])[0]
        effect_txt = f"{effects.get('direction', '—')} / {effects.get('dosing', '—')}"
        biosamples = r.get("biosamples") or []
        bs = (
            ", ".join(
                filter(
                    None, [(b.get("tissueLabel") or b.get("cellLabel") or "") for b in biosamples]
                )
            )
            or "—"
        )
        lines.append(f"| {ev} | {ds} | {effect_txt} | {bs} |")
    return "\n".join(lines)


def fmt_chembl_mechanisms(mechs: list[dict], drugs: list[dict], n: int = 8) -> str:
    if not mechs:
        return "_No ChEMBL mechanism records for this target._"
    drugs_by_id = {d["molecule_chembl_id"]: d for d in drugs if d.get("molecule_chembl_id")}
    lines = ["| Molecule | Max phase | Action | Mechanism |", "|---|---|---|---|"]
    seen = set()
    for m in mechs:
        mid = m.get("molecule_chembl_id")
        if not mid or mid in seen:
            continue
        seen.add(mid)
        if len(seen) > n:
            break
        d = drugs_by_id.get(mid, {})
        name = d.get("pref_name") or m.get("parent_molecule_chembl_id") or mid
        phase = d.get("max_phase")
        phase_str = str(phase) if phase is not None else "—"
        flags = []
        if d.get("withdrawn_flag"):
            flags.append("⚠ withdrawn")
        if d.get("black_box_warning"):
            flags.append("⚠ black box")
        name_str = f"{name} (`{mid}`)" + (f" ({', '.join(flags)})" if flags else "")
        lines.append(
            f"| {name_str} | {phase_str} | {m.get('action_type', '—')} | {m.get('mechanism_of_action', '—')} |"
        )
    return "\n".join(lines)


def fmt_top_activities(acts: list[dict], n: int = 8) -> str:
    if not acts:
        return "_No bioactivity records returned._"
    lines = [
        "| Molecule | Type | Value | pChEMBL | Assay | Reference |",
        "|---|---|---|---|---|---|",
    ]
    for a in acts[:n]:
        mid = a.get("molecule_chembl_id") or "—"
        st = a.get("standard_type") or "—"
        val = a.get("standard_value")
        unit = a.get("standard_units") or ""
        val_str = f"{val} {unit}".strip() if val is not None else "—"
        pchembl = a.get("pchembl_value") or "—"
        assay = (a.get("assay_description") or "—")[:60]
        ref = a.get("document_chembl_id") or "—"
        lines.append(f"| `{mid}` | {st} | {val_str} | {pchembl} | {assay} | `{ref}` |")
    return "\n".join(lines)


def fmt_literature(papers: list[dict]) -> str:
    if not papers:
        return "_No PubMed records returned for `<GENE> AND (PXR OR NR1I2)`._"
    lines = []
    for p in papers:
        author = p["first_author"] or "Anon."
        year = p["year"] or "n.d."
        journal = p["journal"] or ""
        title = p["title"]
        url = f"https://pubmed.ncbi.nlm.nih.gov/{p['pmid']}/"
        snip = (p["abstract"] or "").strip()
        snip = (snip[:280] + "…") if len(snip) > 280 else snip
        lines.append(f"**{author} et al. ({year})** [{title}]({url}) — *{journal}*. {snip}\n")
    return "\n".join(lines)


def build_one(gene: str, ensembl: str, chembl: str, uniprot: str, metrics: dict) -> str:
    ot_data = json.loads((CACHE / f"{gene}_open_targets.json").read_text())
    ch_data = json.loads((CACHE / f"{gene}_chembl.json").read_text())
    t = (ot_data.get("data") or {}).get("target") or {}

    fn_descs = t.get("functionDescriptions") or []
    fn_block = (
        "\n".join(f"- {d}" for d in fn_descs[:3])
        if fn_descs
        else "_No function description available._"
    )

    log.info("[LIT ] fetching PubMed for %s", gene)
    try:
        lit = fetch_pubmed_abstracts(gene)
    except Exception as exc:  # noqa: BLE001
        log.warning("PubMed fetch failed for %s: %s", gene, exc)
        lit = []
    time.sleep(1.3)  # stay under NCBI's 3 req/s without an API key

    per = metrics.get("per_cell_type") or {}
    hep_rho = metrics.get("hep_rho")
    hep_lo = metrics.get("hep_lo")
    hep_hi = metrics.get("hep_hi")
    hep_q = metrics.get("hep_q")
    ds_mean = metrics.get("ds_mean")

    if hep_rho is not None:
        paper_summary = (
            f"Hepatocyte Spearman ρ(NR1I2, {gene}) = **{hep_rho:.3f}** "
            f"(95 % bootstrap CI {hep_lo:.3f}–{hep_hi:.3f}, BH-FDR q = {hep_q:.4f}). "
            f"Mean decoupling score across the nine non-hepatocyte cell types = **{ds_mean:.3f}**."
        )
    else:
        paper_summary = "_This gene is not in the analysed PXR target set._"

    md = f"""# {gene} dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/{gene}_open_targets.json`
> ChEMBL: `dossiers/_cache/{gene}_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{{ci_lower,ci_upper,qvalues}}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **{t.get("approvedSymbol") or gene}** |
| Approved name | {t.get("approvedName") or "—"} |
| Ensembl gene | [`{ensembl}`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g={ensembl}) |
| UniProt | [`{uniprot}`](https://www.uniprot.org/uniprotkb/{uniprot}/entry) |
| ChEMBL target | [`{chembl}`](https://www.ebi.ac.uk/chembl/target_report_card/{chembl}/) |
| Biotype | {t.get("biotype") or "—"} |

### Function (UniProt curated, via Open Targets)

{fn_block}

## Paper finding (this study)

{paper_summary}

### Per-cell-type coupling

{fmt_per_cell_type(per)}

## Open Targets — tractability

{fmt_tractability(t.get("tractability") or [])}

## Open Targets — top disease associations

{fmt_associated_diseases(((t.get("associatedDiseases") or {}).get("rows") or []))}

## Open Targets — approved drugs & clinical candidates

{fmt_drugs(t.get("drugAndClinicalCandidates") or {})}

## Open Targets — pharmacogenomics

{fmt_pgx(t.get("pharmacogenomics") or [])}

## Open Targets — safety liabilities

{fmt_safety(t.get("safetyLiabilities") or [])}

## ChEMBL — mechanism of action records

{fmt_chembl_mechanisms(ch_data.get("mechanisms") or [], ch_data.get("drugs") or [])}

## ChEMBL — most potent bioactivity records

{fmt_top_activities(ch_data.get("top_activities") or [])}

## Recent literature

(Live PubMed pull: `{gene} AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

{fmt_literature(lit)}

---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
"""
    return md


def build_index() -> str:
    lines = [
        "# Per-gene dossiers",
        "",
        "Structured intel for each hepatocyte-selective PXR readout plus the receptor itself.",
        "Each file is a self-contained brief assembled from Open Targets v4, ChEMBL v34, the paper's own coupling CSVs, and a live PubMed pull.",
        "",
        "| Gene | Hepatocyte ρ | Decoupling score | Role |",
        "|---|---|---|---|",
    ]
    metrics = load_paper_metrics()
    roles = {
        "CYP2C9": "Phase I CYP; warfarin / NSAID metabolism",
        "CYP3A5": "Polymorphic CYP; tacrolimus dosing",
        "ABCC2": "Apical efflux transporter (MRP2); Dubin-Johnson syndrome",
        "SLCO1B1": "Basolateral uptake transporter; statin response, Rotor syndrome",
        "CYP2C8": "Phase I CYP; paclitaxel / repaglinide metabolism",
        "CPT1A": "Rate-limiting enzyme, mitochondrial fatty-acid β-oxidation",
        "NR1I2": "The receptor itself (PXR)",
    }
    for gene, *_ in GENES:
        m = metrics.get(gene, {})
        rho = f"{m['hep_rho']:.2f}" if m else "n/a"
        ds = f"{m['ds_mean']:.2f}" if (m and m.get("ds_mean") is not None) else "n/a"
        lines.append(f"| [{gene}]({gene}.md) | {rho} | {ds} | {roles.get(gene, '—')} |")
    lines += [
        "",
        "## How to use these",
        "",
        textwrap.dedent("""\
            A reviewer or co-author can read one file per gene and walk away with:
            - the paper's quantitative finding (coupling ρ, CI, q-value, decoupling magnitude across every cell type)
            - the external-pharmacology context (Open Targets disease associations, tractability flags, approved-drug & clinical-candidate inventory, pharmacogenomic variants of clinical interest, known safety liabilities)
            - the medicinal-chemistry context (ChEMBL mechanism-of-action records, most potent measured bioactivities, drug-status flags)
            - the last few recent PubMed papers tying the gene back to PXR / NR1I2

            Nothing in these files is curated by hand — everything is mechanically pulled from public databases and reassembled. To refresh, re-run `scripts/build_dossier_data.py` (drops the cache) then `scripts/assemble_dossiers.py` (rebuilds the markdown).
        """),
    ]
    return "\n".join(lines)


def main() -> None:
    metrics = load_paper_metrics()
    for gene, ensembl, chembl, uniprot in GENES:
        md = build_one(gene, ensembl, chembl, uniprot, metrics.get(gene, {}))
        out = OUT / f"{gene}.md"
        out.write_text(md, encoding="utf-8")
        log.info("Wrote %s (%d chars)", out, len(md))
    (OUT / "README.md").write_text(build_index(), encoding="utf-8")
    log.info("Wrote dossiers/README.md")


if __name__ == "__main__":
    main()
