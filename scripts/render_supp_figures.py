"""Render Figs 2a/2b + Figs S1/S2 from robustness outputs.

Inputs : data/processed/coupling*.csv, sensitivity_agreement.csv, subsample_summary.csv
Outputs: figures/fig2a_significance_overlay.png
         figures/fig2b_forest_hepatocyte.png
         figures/figS1_parameter_sensitivity.png
         figures/figS2_subsample_stability.png
"""

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

import pandas as pd  # noqa: E402

from pxr_uncoupling.config import DATA_PROCESSED, FIGURES  # noqa: E402
from pxr_uncoupling.supplementary_plots import (  # noqa: E402
    decoupling_with_ci_forest,
    heatmap_with_significance,
    sensitivity_plot,
    subsample_stability_plot,
)


def _read(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED / name, index_col=0)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)

    coupling = _read("coupling.csv")
    qvalues = _read("coupling_qvalues.csv")
    ci_lo = _read("coupling_ci_lower.csv")
    ci_hi = _read("coupling_ci_upper.csv")
    agreement = pd.read_csv(DATA_PROCESSED / "sensitivity_agreement.csv")
    summary = pd.read_csv(DATA_PROCESSED / "subsample_summary.csv")

    log.info("Rendering fig2a_significance_overlay ...")
    heatmap_with_significance(coupling, qvalues)

    log.info("Rendering fig2b_forest_hepatocyte ...")
    decoupling_with_ci_forest(coupling, ci_lo, ci_hi, qvalues)

    log.info("Rendering figS1_parameter_sensitivity ...")
    sensitivity_plot(agreement)

    log.info("Rendering figS2_subsample_stability ...")
    subsample_stability_plot(summary)

    log.info("Saved 4 figures to %s", FIGURES)


if __name__ == "__main__":
    main()
