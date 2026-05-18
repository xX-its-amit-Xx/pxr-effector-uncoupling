"""iLINCS L1000 API client for compound perturbation signatures.

Two-step download:
  1) POST /api/ilincsR/downloadSignature with sigID -> returns a session-file token
  2) GET  /tmp/<token>.xls -> TSV with per-gene logDiffExp and p-value

Per-signature TSVs cached under data/cache/lincs_<sigid>.tsv.
"""

from __future__ import annotations

import io
import logging
import time

import httpx
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import DATA_PROCESSED

log = logging.getLogger(__name__)

ILINCS_BASE = "https://www.ilincs.org"
CACHE_DIR = DATA_PROCESSED.parent / "cache"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def find_signatures(term: str) -> list[dict]:
    """Search iLINCS for all signatures matching a compound name (with synonyms)."""
    url = f"{ILINCS_BASE}/api/SignatureMeta/findTermWithSynonyms"
    resp = httpx.get(url, params={"term": term}, timeout=30, follow_redirects=True)
    resp.raise_for_status()
    return resp.json().get("data", [])


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _request_session_token(sig_id: str) -> str:
    url = f"{ILINCS_BASE}/api/ilincsR/downloadSignature"
    resp = httpx.post(
        url,
        json={"sigID": sig_id, "display": False},
        timeout=60,
        follow_redirects=True,
    )
    resp.raise_for_status()
    tokens = resp.json().get("data", [])
    if not tokens:
        raise RuntimeError(f"No session token for {sig_id}")
    return tokens[0]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _fetch_session_tsv(token: str) -> str:
    url = f"{ILINCS_BASE}/tmp/{token}.xls"
    resp = httpx.get(url, timeout=60, follow_redirects=True)
    resp.raise_for_status()
    return resp.text


def download_signature(sig_id: str, force: bool = False) -> pd.DataFrame:
    """Download per-gene log-diff-expression for one signature; cached locally."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"lincs_{sig_id}.tsv"
    if cache.exists() and not force:
        return pd.read_csv(cache, sep="\t")

    log.info("Downloading iLINCS signature %s", sig_id)
    token = _request_session_token(sig_id)
    # iLINCS writes the file server-side after POST; brief pause helps avoid 404.
    time.sleep(0.5)
    text = _fetch_session_tsv(token)
    df = pd.read_csv(io.StringIO(text), sep="\t")
    df.to_csv(cache, sep="\t", index=False)
    return df


def fetch_many(sig_ids: list[str]) -> dict[str, pd.DataFrame]:
    """Download many signatures; returns {sig_id: DataFrame}."""
    out: dict[str, pd.DataFrame] = {}
    for sid in sig_ids:
        try:
            out[sid] = download_signature(sid)
        except Exception as exc:  # noqa: BLE001
            log.warning("Failed to download %s: %s", sid, exc)
    return out
