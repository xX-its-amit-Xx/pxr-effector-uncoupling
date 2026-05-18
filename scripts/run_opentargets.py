"""External validation via Open Targets disease associations.

For each top hepatocyte-selective PXR target gene (plus NR1I2 and selected
controls), pull the top-50 disease associations from Open Targets Platform.
Count how many fall into drug-response / pharmacogenomics phenotypes — the
expectation is that PXR targets are enriched relative to housekeeping /
hepatocyte-TF controls.

Reads  : data/targets/pxr_canonical_targets.tsv, negative_control_genes.tsv
Writes : data/processed/opentargets_per_gene.csv
         data/processed/opentargets_top_diseases.csv
         data/cache/opentargets_<symbol>.json (per-gene cached responses)
         figures/supp_opentargets.png
"""

import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from pxr_uncoupling.config import (  # noqa: E402
    COLOR_ACCENT,
    COLOR_CREAM,
    COLOR_SAGE,
    DATA_PROCESSED,
    FIGURES,
    NR1I2_ENSEMBL,
)
from pxr_uncoupling.opentargets import (  # noqa: E402
    count_drug_response_phenotypes,
    fetch_disease_associations,
    parse_top_diseases,
)

# Top 5 hepatocyte-selective PXR targets (from decoupling.csv) — Ensembl IDs from
# data/targets/pxr_canonical_targets.tsv. Hard-coded for reproducibility.
TOP_HEPATOCYTE_SELECTIVE = {
    "CYP2C8": "ENSG00000138115",
    "CYP2C9": "ENSG00000138109",
    "SLCO1B1": "ENSG00000134538",
    "ABCC2": "ENSG00000023839",
    "CYP3A5": "ENSG00000106258",
}

# Representative controls spanning the three categories.
SELECTED_CONTROLS = {
    "ALB": "ENSG00000163631",  # liver-enriched
    "HNF4A": "ENSG00000101076",  # hepatocyte TF
    "GAPDH": "ENSG00000111640",  # housekeeping
}


def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    # 1. Fetch (cached per-gene) ───────────────────────────────────────────────
    all_genes: dict[str, tuple[str, str]] = {
        "NR1I2": (NR1I2_ENSEMBL, "receptor"),
    }
    for sym, eid in TOP_HEPATOCYTE_SELECTIVE.items():
        all_genes[sym] = (eid, "PXR target (top hepatocyte-selective)")
    for sym, eid in SELECTED_CONTROLS.items():
        all_genes[sym] = (eid, "negative control")

    per_gene_rows: list[dict] = []
    top_disease_rows: list[dict] = []
    for sym, (eid, group) in all_genes.items():
        data = fetch_disease_associations(eid, symbol=sym, n=50)
        target = data.get("data", {}).get("target")
        if target is None:
            log.warning("%s (%s): no Open Targets record", sym, eid)
            continue
        ad = target["associatedDiseases"]
        n_total = ad["count"]
        n_drug = count_drug_response_phenotypes(data, top_n=50)
        per_gene_rows.append(
            {
                "gene_symbol": sym,
                "ensembl_id": eid,
                "group": group,
                "n_disease_associations": n_total,
                "n_drug_response_top50": n_drug,
                "drug_response_fraction": n_drug / 50 if n_drug else 0.0,
            }
        )
        for d in parse_top_diseases(data, top_n=5):
            top_disease_rows.append(
                {
                    "gene_symbol": sym,
                    "group": group,
                    "disease_name": d["disease_name"],
                    "score": d["score"],
                    "therapeutic_areas": "; ".join(d["therapeutic_areas"]),
                }
            )

    per_gene = pd.DataFrame(per_gene_rows)
    top_diseases = pd.DataFrame(top_disease_rows)
    per_gene.to_csv(DATA_PROCESSED / "opentargets_per_gene.csv", index=False)
    top_diseases.to_csv(DATA_PROCESSED / "opentargets_top_diseases.csv", index=False)
    log.info(
        "Wrote opentargets_per_gene.csv (%d rows) and opentargets_top_diseases.csv (%d rows)",
        len(per_gene),
        len(top_diseases),
    )

    # 2. Compact JSON summary ──────────────────────────────────────────────────
    summary = {
        "per_gene": per_gene.set_index("gene_symbol").to_dict(orient="index"),
        "top_diseases_pxr_targets": (
            top_diseases[top_diseases["group"].str.contains("PXR target")]
            .groupby("gene_symbol")
            .apply(
                lambda df: df[["disease_name", "score"]].to_dict(orient="records"),
                include_groups=False,
            )
            .to_dict()
        ),
    }
    with (DATA_PROCESSED / "opentargets_summary.json").open("w") as fh:
        json.dump(summary, fh, indent=2, default=str)

    # 3. Plot: side-by-side disease tables, PXR targets vs controls ───────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor(COLOR_CREAM)

    def _render_table(ax, group_filter: str, title: str, accent: str) -> None:
        ax.set_facecolor(COLOR_CREAM)
        ax.axis("off")
        subset = top_diseases[top_diseases["group"].str.contains(group_filter)]
        subset_order = [
            sym
            for sym in (
                list(TOP_HEPATOCYTE_SELECTIVE.keys())
                if "PXR" in group_filter
                else list(SELECTED_CONTROLS.keys())
            )
            if sym in subset["gene_symbol"].values
        ]
        # header
        ax.text(
            0.0,
            0.98,
            "Gene",
            fontsize=11,
            weight="bold",
            color="#222",
            transform=ax.transAxes,
            va="top",
        )
        ax.text(
            0.18,
            0.98,
            "Top 3 Open Targets diseases (score)",
            fontsize=11,
            weight="bold",
            color="#222",
            transform=ax.transAxes,
            va="top",
        )
        ax.add_patch(
            plt.Rectangle(
                (-0.02, 0.93), 1.04, 0.01, transform=ax.transAxes, color=accent, alpha=0.6
            )
        )
        y = 0.87
        for sym in subset_order:
            gene_rows = subset[subset["gene_symbol"] == sym].head(3)
            ax.text(
                0.0,
                y,
                sym,
                fontsize=10,
                weight="bold",
                color=accent,
                transform=ax.transAxes,
                va="top",
            )
            disease_block = "\n".join(
                f"• {r['disease_name'][:55]}  ({r['score']:.2f})" for _, r in gene_rows.iterrows()
            )
            ax.text(
                0.18,
                y,
                disease_block,
                fontsize=9,
                weight="normal",
                color="#333",
                transform=ax.transAxes,
                va="top",
                family="monospace",
            )
            y -= 0.165
        ax.set_title(title, fontsize=11, loc="left", pad=14)

    _render_table(axes[0], "PXR target", "Top 5 hepatocyte-selective PXR targets", COLOR_ACCENT)
    _render_table(
        axes[1], "negative control", "Matched negative controls (1 per category)", COLOR_SAGE
    )

    plt.tight_layout()
    fig.savefig(
        FIGURES / "supp_opentargets.png", dpi=300, bbox_inches="tight", facecolor=COLOR_CREAM
    )
    log.info("Wrote %s", FIGURES / "supp_opentargets.png")

    print("\n=== OPEN TARGETS EXTERNAL VALIDATION ===")
    pxr_subset = per_gene[per_gene["group"].str.contains("PXR target")]
    ctrl_subset = per_gene[per_gene["group"] == "negative control"]
    print("PXR targets (top hep-selective, n=5):")
    print(
        f"  mean drug-response phenotypes in top-50: "
        f"{pxr_subset['n_drug_response_top50'].mean():.2f}"
    )
    print(f"  per-gene: {pxr_subset.set_index('gene_symbol')['n_drug_response_top50'].to_dict()}")
    print(f"Negative controls (n={len(ctrl_subset)}):")
    print(
        f"  mean drug-response phenotypes in top-50: "
        f"{ctrl_subset['n_drug_response_top50'].mean():.2f}"
    )
    print(f"  per-gene: {ctrl_subset.set_index('gene_symbol')['n_drug_response_top50'].to_dict()}")


if __name__ == "__main__":
    main()
