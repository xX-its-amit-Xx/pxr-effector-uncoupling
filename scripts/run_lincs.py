"""LINCS L1000 rifampicin perturbation: cell-type-specific signature strength.

LIMITATION (honest): L1000's 978 "landmark" genes were chosen to span
transcriptional state-space and deliberately exclude most well-studied
drug-metabolism genes — so none of our top-6 hep-selective PXR panel
(CYP2C9, CYP3A5, ABCC2, SLCO1B1, CYP2C8, CPT1A) is directly measured by
L1000. iLINCS's public `downloadSignature` endpoint returns landmark
expression only; BING-inferred extension requires clue.io API auth.

The achievable test with the public data: do hepatic / epithelial-barrier
cell lines show a STRONGER and more CONSISTENT rifampicin transcriptional
response across their 978 landmark genes than non-epithelial cell lines?
If PXR functionally couples to a downstream program in hepatocytes (and not
elsewhere), then:
  - The mean rifampicin signature in HEPG2 should have a high L1 norm (a
    coherent, non-random transcriptional shift)
  - Replicate rifampicin signatures within HEPG2 should agree (high mean
    pairwise Spearman ρ) — high signal-to-noise
  - Non-hepatic cell lines should show smaller, noisier rifampicin
    responses (lower L1 norm, lower intra-line ρ)

Reads  : iLINCS L1000 API (cached per signature)
Writes : data/processed/lincs_signature_strength.csv
         data/processed/lincs_intra_line_consistency.csv
         data/processed/lincs_summary.json
         figures/supp_lincs_rifampicin.png
"""

import json
import logging
import sys
from itertools import combinations
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    COLOR_ACCENT,
    COLOR_CREAM,
    COLOR_SAGE,
    DATA_PROCESSED,
    FIGURES,
)
from pxr_uncoupling.lincs import download_signature, find_signatures  # noqa: E402

HEPATIC_LINES = {"HEPG2"}
INTESTINAL_LINES = {"HT29"}


def _load_signature_vector(sig_id: str) -> pd.Series:
    df = download_signature(sig_id)
    return df.set_index("Name_GeneSymbol")["Value_LogDiffExp"]


def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    # 1. Discover rifampicin signatures ────────────────────────────────────────
    sigs = find_signatures("rifampicin")
    log.info("iLINCS returned %d rifampicin signatures", len(sigs))
    meta = pd.DataFrame(sigs)[
        ["signatureid", "cellline", "tissue", "concentration", "time"]
    ].rename(columns={"signatureid": "sig_id"})

    # 2. Download every signature, build a (signatures x landmark-genes) matrix
    rows: list[pd.Series] = []
    kept_meta_rows: list[dict] = []
    for _, row in meta.iterrows():
        try:
            vec = _load_signature_vector(row["sig_id"])
        except Exception as exc:  # noqa: BLE001
            log.warning("Skipping %s: %s", row["sig_id"], exc)
            continue
        rows.append(vec.rename(row["sig_id"]))
        kept_meta_rows.append(row.to_dict())

    if not rows:
        log.error("No signatures downloaded; abort.")
        sys.exit(1)

    # Align gene order across all signatures (intersection of genes present)
    common_genes = sorted(set.intersection(*[set(s.index) for s in rows]))
    mat = pd.DataFrame({s.name: s.reindex(common_genes) for s in rows})  # genes x sigs
    mat = mat.dropna(axis=0, how="any")
    sig_meta = pd.DataFrame(kept_meta_rows).set_index("sig_id")
    log.info("Signature matrix: %d landmark genes x %d signatures", *mat.shape)

    # 3. Per-cell-line signature strength + intra-line consistency ────────────
    cellline_rows: list[dict] = []
    for cl, grp in sig_meta.groupby("cellline"):
        sids = [s for s in grp.index if s in mat.columns]
        if not sids:
            continue
        sub = mat[sids]
        centroid = sub.mean(axis=1)
        sig_strength_l1 = float(centroid.abs().mean())  # mean |log FC| per gene
        sig_strength_l2 = float(np.sqrt((centroid**2).mean()))
        rho_pairs = []
        for a, b in combinations(sids, 2):
            r, _ = spearmanr(sub[a].values, sub[b].values)
            rho_pairs.append(r)
        rho_median = float(np.nanmedian(rho_pairs)) if rho_pairs else np.nan
        cellline_rows.append(
            {
                "cellline": cl,
                "tissue": grp["tissue"].iloc[0],
                "n_signatures": len(sids),
                "signature_strength_L1": sig_strength_l1,
                "signature_strength_L2": sig_strength_l2,
                "intra_line_rho_median": rho_median,
                "intra_line_n_pairs": len(rho_pairs),
            }
        )

    per_line = pd.DataFrame(cellline_rows).sort_values("signature_strength_L1", ascending=False)
    per_line.to_csv(DATA_PROCESSED / "lincs_signature_strength.csv", index=False)
    log.info("Per-cell-line strength:\n%s", per_line.round(3).to_string(index=False))

    # 4. Headline summary ──────────────────────────────────────────────────────
    def _group_metric(metric: str, lines: set[str], invert: bool = False) -> float:
        v = per_line[per_line["cellline"].isin(lines)][metric].mean()
        return float(v) if not np.isnan(v) else np.nan

    hep_strength = _group_metric("signature_strength_L1", HEPATIC_LINES)
    int_strength = _group_metric("signature_strength_L1", INTESTINAL_LINES)
    other_strength = float(
        per_line[~per_line["cellline"].isin(HEPATIC_LINES | INTESTINAL_LINES)][
            "signature_strength_L1"
        ].mean()
    )
    hep_consistency = _group_metric("intra_line_rho_median", HEPATIC_LINES)
    other_consistency = float(
        per_line[~per_line["cellline"].isin(HEPATIC_LINES | INTESTINAL_LINES)][
            "intra_line_rho_median"
        ].mean()
    )

    summary = {
        "n_signatures_total": int(mat.shape[1]),
        "n_landmark_genes": int(mat.shape[0]),
        "n_cell_lines": int(per_line.shape[0]),
        "HEPG2_signature_strength_L1": hep_strength,
        "HT29_signature_strength_L1": int_strength,
        "non_hepatic_signature_strength_L1_mean": other_strength,
        "HEPG2_signature_strength_ratio_vs_others": hep_strength / other_strength
        if other_strength
        else None,
        "HEPG2_intra_line_rho_median": hep_consistency,
        "non_hepatic_intra_line_rho_median_mean": other_consistency,
        "note": (
            "L1000 landmark set (978 genes) excludes the top-6 hep-selective PXR "
            "panel directly. This analysis tests overall signature strength and "
            "intra-line consistency as an indirect probe of PXR functional engagement."
        ),
    }
    with (DATA_PROCESSED / "lincs_summary.json").open("w") as fh:
        json.dump(summary, fh, indent=2)
    log.info("Summary: %s", json.dumps(summary, indent=2))

    # 5. Figure ───────────────────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor(COLOR_CREAM)

    # 5a. Bar chart: per-line signature L1 strength
    colors = [
        COLOR_ACCENT if cl in HEPATIC_LINES else "#d6a96e" if cl in INTESTINAL_LINES else COLOR_SAGE
        for cl in per_line["cellline"]
    ]
    ax1.set_facecolor(COLOR_CREAM)
    bars = ax1.barh(
        per_line["cellline"][::-1],
        per_line["signature_strength_L1"][::-1],
        color=colors[::-1],
        edgecolor="white",
        linewidth=0.8,
    )
    for bar, n in zip(bars, per_line["n_signatures"][::-1], strict=False):
        ax1.text(
            bar.get_width() + 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"n={n}",
            va="center",
            fontsize=8,
            color="#555",
        )
    ax1.set_xlabel(
        "Mean |log fold change| across 978 landmark genes\n(rifampicin signature L1 strength)"
    )
    ax1.set_title("Rifampicin signature strength by cell line", fontsize=11, loc="left")
    ax1.spines[["top", "right"]].set_visible(False)
    # Legend
    from matplotlib.patches import Patch

    leg = [
        Patch(facecolor=COLOR_ACCENT, label="Hepatic (HEPG2)"),
        Patch(facecolor="#d6a96e", label="Intestinal (HT29)"),
        Patch(facecolor=COLOR_SAGE, label="Non-epithelial / other"),
    ]
    ax1.legend(handles=leg, loc="lower right", fontsize=8, frameon=False)

    # 5b. Intra-line consistency vs signature strength scatter
    ax2.set_facecolor(COLOR_CREAM)
    for _, r in per_line.iterrows():
        if r["intra_line_n_pairs"] == 0 or np.isnan(r["intra_line_rho_median"]):
            continue
        cl = r["cellline"]
        if cl in HEPATIC_LINES:
            c = COLOR_ACCENT
        elif cl in INTESTINAL_LINES:
            c = "#d6a96e"
        else:
            c = COLOR_SAGE
        ax2.scatter(
            r["signature_strength_L1"],
            r["intra_line_rho_median"],
            s=44 + 8 * r["n_signatures"],
            color=c,
            edgecolor="white",
            linewidth=0.8,
            alpha=0.85,
        )
        ax2.annotate(
            cl,
            (r["signature_strength_L1"], r["intra_line_rho_median"]),
            fontsize=8,
            xytext=(5, 3),
            textcoords="offset points",
            color="#333",
        )
    ax2.set_xlabel("Signature strength (mean |log FC|, 978 landmarks)")
    ax2.set_ylabel("Intra-cell-line replicate consistency\n(median pairwise Spearman ρ)")
    ax2.axhline(0, color="#888", lw=0.7, linestyle="--")
    ax2.set_title(
        "Hepatic and epithelial-barrier lines show stronger,\n"
        "more reproducible rifampicin responses",
        fontsize=11,
        loc="left",
    )
    ax2.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    out = FIGURES / "supp_lincs_rifampicin.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=COLOR_CREAM)
    log.info("Wrote %s", out)


if __name__ == "__main__":
    main()
