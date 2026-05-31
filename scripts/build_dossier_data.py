"""Pull Open Targets + ChEMBL data for each top-coupled gene, cache as JSON.

Output : dossiers/_cache/<GENE>_open_targets.json
         dossiers/_cache/<GENE>_chembl.json

The dossiers/<GENE>.md files are assembled separately from these caches,
so the slow API pulls and the markdown writing stay decoupled.
"""

# ruff: noqa: E501  # rendered output strings are intentionally long

from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "dossiers" / "_cache"
CACHE.mkdir(parents=True, exist_ok=True)

# Ensembl IDs for the top-6 hep-selective panel plus the receptor.
GENES = {
    "CYP2C9": {"ensembl": "ENSG00000138109", "chembl": "CHEMBL3397", "uniprot": "P11712"},
    "CYP3A5": {"ensembl": "ENSG00000106258", "chembl": "CHEMBL3019", "uniprot": "P20815"},
    "ABCC2": {"ensembl": "ENSG00000023839", "chembl": "CHEMBL5748", "uniprot": "Q92887"},
    "SLCO1B1": {"ensembl": "ENSG00000134538", "chembl": "CHEMBL1697668", "uniprot": "Q9Y6L6"},
    "CYP2C8": {"ensembl": "ENSG00000138115", "chembl": "CHEMBL3721", "uniprot": "P10632"},
    "CPT1A": {"ensembl": "ENSG00000110090", "chembl": "CHEMBL1293194", "uniprot": "P50416"},
    "NR1I2": {"ensembl": "ENSG00000144852", "chembl": "CHEMBL3401", "uniprot": "O75469"},
}

OT_ENDPOINT = "https://api.platform.opentargets.org/api/v4/graphql"
CHEMBL_API = "https://www.ebi.ac.uk/chembl/api/data"

OT_QUERY = """
query target($id: String!) {
  target(ensemblId: $id) {
    id
    approvedSymbol
    approvedName
    biotype
    functionDescriptions
    nameSynonyms { label source }
    tractability { modality value label }
    drugAndClinicalCandidates {
      count
      rows {
        drug {
          id
          name
          maximumClinicalStage
          tradeNames
          mechanismsOfAction { rows { mechanismOfAction actionType targets { approvedSymbol } } }
          drugType
        }
      }
    }
    associatedDiseases(page: { index: 0, size: 10 }) {
      count
      rows {
        disease { id name therapeuticAreas { id name } }
        score
        datatypeScores { id score }
      }
    }
    safetyLiabilities { event eventId effects { direction dosing } biosamples { tissueLabel cellLabel } datasource literature }
    pharmacogenomics {
      drugs { drugFromSource drugId }
      genotypeAnnotationText
      pgxCategory
      phenotypeText
      phenotypeFromSourceId
      variantRsId
      variantFunctionalConsequenceId
      evidenceLevel
      studyId
    }
    chemicalProbes { id control drugId mechanismOfAction isHighQuality origin probesDrugsScore probeMinerScore scoreInCells scoreInOrganisms targetFromSourceId urls { url } }
    pathways { pathwayId pathway topLevelTerm }
  }
}
"""


def fetch_open_targets(gene: str, ensembl: str) -> dict:
    out = CACHE / f"{gene}_open_targets.json"
    if out.exists():
        log.info("[OT  ] cache hit for %s", gene)
        return json.loads(out.read_text())
    log.info("[OT  ] fetching %s (%s)", gene, ensembl)
    r = httpx.post(
        OT_ENDPOINT,
        json={"query": OT_QUERY, "variables": {"id": ensembl}},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    out.write_text(json.dumps(data, indent=2))
    return data


def fetch_chembl(gene: str, chembl_target_id: str) -> dict:
    out = CACHE / f"{gene}_chembl.json"
    if out.exists():
        log.info("[CHEM] cache hit for %s", gene)
        return json.loads(out.read_text())
    log.info("[CHEM] fetching %s (%s)", gene, chembl_target_id)
    bundle = {"target_id": chembl_target_id}

    # Mechanism of action records for this target.
    r = httpx.get(
        f"{CHEMBL_API}/mechanism.json",
        params={"target_chembl_id": chembl_target_id, "limit": 20},
        timeout=60,
    )
    r.raise_for_status()
    bundle["mechanisms"] = r.json().get("mechanisms", [])

    # Top bioactivities sorted by pChEMBL (most potent first).
    r = httpx.get(
        f"{CHEMBL_API}/activity.json",
        params={
            "target_chembl_id": chembl_target_id,
            "pchembl_value__isnull": "false",
            "standard_type__in": "IC50,Ki,Kd,EC50",
            "limit": 10,
            "order_by": "-pchembl_value",
        },
        timeout=60,
    )
    r.raise_for_status()
    bundle["top_activities"] = r.json().get("activities", [])

    # Pull drug names for the top mechanism hits.
    mol_ids = sorted(
        {m.get("molecule_chembl_id") for m in bundle["mechanisms"] if m.get("molecule_chembl_id")}
    )
    drugs: list[dict] = []
    for mid in mol_ids[:20]:
        rr = httpx.get(f"{CHEMBL_API}/molecule/{mid}.json", timeout=60)
        if rr.status_code != 200:
            continue
        m = rr.json()
        drugs.append(
            {
                "molecule_chembl_id": m.get("molecule_chembl_id"),
                "pref_name": m.get("pref_name"),
                "max_phase": m.get("max_phase"),
                "first_approval": m.get("first_approval"),
                "withdrawn_flag": m.get("withdrawn_flag"),
                "black_box_warning": m.get("black_box_warning"),
                "molecule_type": m.get("molecule_type"),
            }
        )
        time.sleep(0.1)
    bundle["drugs"] = drugs

    out.write_text(json.dumps(bundle, indent=2))
    return bundle


def main() -> None:
    for gene, ids in GENES.items():
        try:
            fetch_open_targets(gene, ids["ensembl"])
        except Exception as exc:  # noqa: BLE001
            log.error("Open Targets failed for %s: %s", gene, exc)
        try:
            fetch_chembl(gene, ids["chembl"])
        except Exception as exc:  # noqa: BLE001
            log.error("ChEMBL failed for %s: %s", gene, exc)
        time.sleep(1.0)  # be polite to both APIs


if __name__ == "__main__":
    sys.exit(main())
