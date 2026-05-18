"""Open Targets Platform GraphQL client for disease associations.

Supports any Ensembl gene ID; per-gene responses are cached under
data/cache/opentargets_<symbol>.json. The schema was updated 2026-Q1 to use
the Pagination input on associatedDiseases — this module follows the new
schema.
"""

from __future__ import annotations

import json
import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import DATA_PROCESSED, NR1I2_ENSEMBL, OPENTARGETS_URL

log = logging.getLogger(__name__)

CACHE_DIR = DATA_PROCESSED.parent / "cache"

_QUERY = """
query Diseases($targetId: String!, $size: Int!) {
  target(ensemblId: $targetId) {
    id
    approvedSymbol
    associatedDiseases(page: { index: 0, size: $size }) {
      count
      rows {
        disease {
          id
          name
          therapeuticAreas { id name }
        }
        score
        datatypeScores { id score }
      }
    }
  }
}
"""


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _post(query: str, variables: dict) -> dict:
    resp = httpx.post(
        OPENTARGETS_URL,
        json={"query": query, "variables": variables},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_disease_associations(
    ensembl_id: str = NR1I2_ENSEMBL,
    symbol: str | None = None,
    n: int = 50,
    force: bool = False,
) -> dict:
    """
    Fetch a gene's top-N disease associations from Open Targets Platform.

    Caches per-symbol under data/cache/opentargets_<symbol>.json. Pass
    `force=True` to re-fetch even if the cache exists.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    key = symbol or ensembl_id
    cache = CACHE_DIR / f"opentargets_{key}.json"

    if cache.exists() and not force:
        log.debug("Cached Open Targets response for %s", key)
        return json.loads(cache.read_text())

    log.info("Fetching Open Targets associations for %s (%s)", key, ensembl_id)
    data = _post(_QUERY, {"targetId": ensembl_id, "size": n})
    cache.write_text(json.dumps(data, indent=2))
    return data


def parse_top_diseases(data: dict, top_n: int = 10) -> list[dict]:
    """Return top_n diseases by overall association score with therapeutic areas."""
    target = data["data"]["target"]
    if target is None:
        return []
    rows = target["associatedDiseases"]["rows"]
    parsed: list[dict] = []
    for row in rows[:top_n]:
        parsed.append(
            {
                "disease_id": row["disease"]["id"],
                "disease_name": row["disease"]["name"],
                "score": row["score"],
                "therapeutic_areas": [ta["name"] for ta in row["disease"]["therapeuticAreas"]],
            }
        )
    return parsed


_DRUG_RESPONSE_KEYWORDS = (
    "response to ",
    "drug response",
    "drug metabolism",
    "warfarin",
    "statin",
    "tacrolimus",
    "clopidogrel",
    "antimalarial",
    "anticoagulant",
    "antifungal",
    "antiplatelet",
    "cyclosporine",
    "pharmacogenom",
)


def count_drug_response_phenotypes(data: dict, top_n: int | None = None) -> int:
    """Count diseases whose name matches drug-response / pharmacogenomic phrasing.

    If `top_n` is given, only look at the top-N by score; otherwise scan all
    rows in the cached response.
    """
    target = data["data"]["target"]
    if target is None:
        return 0
    rows = target["associatedDiseases"]["rows"]
    if top_n is not None:
        rows = rows[:top_n]
    n = 0
    for row in rows:
        name = row["disease"]["name"].lower()
        if any(kw in name for kw in _DRUG_RESPONSE_KEYWORDS):
            n += 1
    return n


def fetch_many(
    genes: dict[str, str],
    n: int = 50,
    force: bool = False,
) -> dict[str, dict]:
    """Fetch disease associations for a dict {symbol: ensembl_id}."""
    out: dict[str, dict] = {}
    for sym, eid in genes.items():
        out[sym] = fetch_disease_associations(eid, symbol=sym, n=n, force=force)
    return out
