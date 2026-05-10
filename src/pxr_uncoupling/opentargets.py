"""Open Targets Platform GraphQL client for NR1I2 disease associations."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import NR1I2_ENSEMBL, OPENTARGETS_CACHE, OPENTARGETS_URL

log = logging.getLogger(__name__)

_QUERY = """
query NR1I2Diseases($targetId: String!, $size: Int!) {
  target(ensemblId: $targetId) {
    id
    approvedSymbol
    associatedDiseases(size: $size, orderByScore: "score") {
      rows {
        disease {
          id
          name
          therapeuticAreas {
            name
          }
        }
        score
        datatypeScores {
          componentId
          score
        }
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


def fetch_disease_associations(n: int = 50, force: bool = False) -> dict:
    """
    Fetch NR1I2 associated diseases from Open Targets Platform.

    Caches result to data/raw/opentargets_nr1i2.json. Set force=True to re-fetch.
    """
    cache: Path = OPENTARGETS_CACHE
    cache.parent.mkdir(parents=True, exist_ok=True)

    if cache.exists() and not force:
        log.info("Loading cached Open Targets response from %s", cache)
        return json.loads(cache.read_text())

    log.info("Fetching NR1I2 disease associations from Open Targets")
    data = _post(_QUERY, {"targetId": NR1I2_ENSEMBL, "size": n})
    cache.write_text(json.dumps(data, indent=2))
    log.info("Cached to %s", cache)
    return data


def parse_top_diseases(data: dict, top_n: int = 10) -> list[dict]:
    """Return top_n diseases by overall association score with category labels."""
    rows = data["data"]["target"]["associatedDiseases"]["rows"]

    CATEGORY_MAP = {
        "inflammatory bowel disease": "IBD/GI",
        "crohn": "IBD/GI",
        "ulcerative colitis": "IBD/GI",
        "colorectal": "cancer",
        "hepatocellular": "cancer",
        "cholangiocarcinoma": "cancer",
        "breast": "cancer",
        "lung": "cancer",
        "metabolic": "metabolic",
        "diabetes": "metabolic",
        "obesity": "metabolic",
        "fatty liver": "metabolic",
        "cholestasis": "metabolic",
        "nafld": "metabolic",
        "nash": "metabolic",
    }

    parsed = []
    for row in rows[:top_n]:
        disease_name = row["disease"]["name"].lower()
        category = "other"
        for kw, cat in CATEGORY_MAP.items():
            if kw in disease_name:
                category = cat
                break
        parsed.append(
            {
                "disease_id": row["disease"]["id"],
                "disease_name": row["disease"]["name"],
                "score": row["score"],
                "category": category,
            }
        )
    return parsed
