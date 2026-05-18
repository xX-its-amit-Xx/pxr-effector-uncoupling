"""GTEx Portal v2 API client for bulk tissue-level expression validation.

We use the geneExpression endpoint, which returns per-sample TPM as an array
in fixed sample-ID order within each tissue. With consistent sample order
across genes (same tissue → same donor set → same order), within-tissue
Spearman rho(NR1I2, target) is computed by aligning arrays element-wise.

Responses are cached under data/cache/gtex_<symbol>.json.
"""

from __future__ import annotations

import json
import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import DATA_PROCESSED

log = logging.getLogger(__name__)

GTEX_API = "https://gtexportal.org/api/v2"
CACHE_DIR = DATA_PROCESSED.parent / "cache"
DATASET_ID = "gtex_v8"

# Gene symbol -> versioned GTEx gencode ID (resolved 2026-05-18 via
# /api/v2/reference/gene).
GENCODE_IDS: dict[str, str] = {
    "NR1I2": "ENSG00000144852.17",
    "CYP2C8": "ENSG00000138115.13",
    "CYP2C9": "ENSG00000138109.9",
    "SLCO1B1": "ENSG00000134538.2",
    "ABCC2": "ENSG00000023839.10",
    "CYP3A5": "ENSG00000106258.13",
    "ALB": "ENSG00000163631.16",
    "HNF4A": "ENSG00000101076.16",
    "GAPDH": "ENSG00000111640.14",
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _get(path: str, params: dict) -> dict:
    resp = httpx.get(f"{GTEX_API}/{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_gene_expression(symbol: str, force: bool = False) -> dict:
    """Fetch per-sample TPM for `symbol` across all GTEx v8 tissues.

    Returns the raw API response. Cached under data/cache/gtex_<symbol>.json.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"gtex_{symbol}.json"

    if cache.exists() and not force:
        log.debug("Cached GTEx response for %s", symbol)
        return json.loads(cache.read_text())

    if symbol not in GENCODE_IDS:
        raise KeyError(f"No gencodeId registered for {symbol}")

    log.info("Fetching GTEx expression for %s (%s)", symbol, GENCODE_IDS[symbol])
    data = _get(
        "expression/geneExpression",
        {
            "gencodeId": GENCODE_IDS[symbol],
            "datasetId": DATASET_ID,
            "itemsPerPage": 100,
        },
    )
    cache.write_text(json.dumps(data, indent=2))
    return data


def per_tissue_arrays(data: dict) -> dict[str, list[float]]:
    """Return {tissueSiteDetailId: [tpm_per_sample]}."""
    return {row["tissueSiteDetailId"]: list(row["data"]) for row in data.get("data", [])}


def fetch_many(symbols: list[str], force: bool = False) -> dict[str, dict[str, list[float]]]:
    """Fetch all symbols; return {symbol: {tissue: [tpm]}}."""
    out: dict[str, dict[str, list[float]]] = {}
    for sym in symbols:
        data = fetch_gene_expression(sym, force=force)
        out[sym] = per_tissue_arrays(data)
    return out
