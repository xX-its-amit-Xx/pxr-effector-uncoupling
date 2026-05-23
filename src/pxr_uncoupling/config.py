from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_TARGETS = ROOT / "data" / "targets"
FIGURES = ROOT / "figures"

# ── CELLxGENE Census ──────────────────────────────────────────────────────────
CENSUS_VERSION = "2025-01-30"  # latest stable as of 2026-05-10
NR1I2_ENSEMBL = "ENSG00000144852"
NR1I2_SYMBOL = "NR1I2"

# ── analysis thresholds ───────────────────────────────────────────────────────
MIN_CELLS_PER_TYPE = 50  # drop cell types below this
MIN_DETECTION_FRACTION = 0.05  # NR1I2 > 0 in at least this fraction
TARGET_CELLS_PER_METACELL = 30  # k-means target
MIN_METACELLS = 20  # drop cell type if fewer metacells than this

# ── curated cell types to query ───────────────────────────────────────────────
# Cell Ontology labels as they appear in CELLxGENE Census obs.cell_type.
# Verified against actual Census obs labels in Notebook 01; mappings documented there.
# Grouped by tissue for downstream figure layout.
CELL_TYPE_TISSUE_MAP: dict[str, str] = {
    # liver
    "hepatocyte": "liver",
    # small intestine / colon
    "enterocyte of epithelium of small intestine": "intestine",
    "enterocyte of epithelium of large intestine": "intestine",
    "Paneth cell": "intestine",
    "intestinal crypt stem cell": "intestine",
    # kidney
    "kidney proximal convoluted tubule epithelial cell": "kidney",
    "kidney proximal straight tubule epithelial cell": "kidney",
    # immune
    "macrophage": "immune",
    "monocyte": "immune",
    "CD4-positive, alpha-beta T cell": "immune",
    "CD8-positive, alpha-beta T cell": "immune",
    "natural killer cell": "immune",
    # placenta / trophoblast
    "trophoblast cell": "placenta",
    "extravillous trophoblast": "placenta",
    # adrenal / endocrine
    "adrenocortical cell": "adrenal",
}

TISSUES_OF_INTEREST = [
    "liver",
    "small intestine",
    "large intestine",
    "kidney",
    "blood",
    "placenta",
    "adrenal gland",
]

# ── Open Targets ──────────────────────────────────────────────────────────────
OPENTARGETS_URL = "https://api.platform.opentargets.org/api/v4/graphql"
OPENTARGETS_CACHE = DATA_RAW / "opentargets_nr1i2.json"

# ── plotting ──────────────────────────────────────────────────────────────────
# Terracotta palette matching amit.sh
# Publication palette (Nature-tier defaults). The canonical definitions live
# in pxr_uncoupling.figure_style; these aliases preserve backward compatibility
# for scripts that import directly from config.
COLOR_ACCENT = "#c0533a"  # hepatic terracotta
COLOR_SAGE = "#7d8c6a"  # control olive
COLOR_CREAM = "#ffffff"  # white background (previously cream — kept name for compat)
