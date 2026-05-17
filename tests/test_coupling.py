"""Unit tests for coupling.py — synthetic AnnData with known ρ values."""

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData

from pxr_uncoupling.config import NR1I2_SYMBOL
from pxr_uncoupling.coupling import coupling_per_cell_type, decoupling_score


def _make_adata(n_cells: int, gene_vals: dict[str, np.ndarray], cell_type: str) -> AnnData:
    genes = [NR1I2_SYMBOL] + [g for g in gene_vals if g != NR1I2_SYMBOL]
    X = np.column_stack([gene_vals[g] for g in genes]).astype(np.float32)
    obs = pd.DataFrame({"cell_type": [cell_type] * n_cells})
    var = pd.DataFrame(index=genes)
    var.index.name = "gene_symbol"
    return AnnData(X=X, obs=obs, var=var)


def test_perfectly_correlated():
    """NR1I2 and PERFECT_GENE are identical → ρ ≈ 1."""
    rng = np.random.default_rng(0)
    nr = np.abs(rng.normal(size=300)) + 0.1
    adata = _make_adata(300, {NR1I2_SYMBOL: nr, "PERFECT_GENE": nr}, "cell_type_A")
    result = coupling_per_cell_type(adata, ["PERFECT_GENE"], cells_per_metacell=10, min_metacells=5)
    assert "cell_type_A" in result.index
    rho = result.loc["cell_type_A", "PERFECT_GENE"]
    assert abs(rho - 1.0) < 0.05, f"Expected ρ ≈ 1, got {rho}"


def test_uncorrelated():
    """NR1I2 and RANDOM_GENE are independent → |ρ| small."""
    rng = np.random.default_rng(1)
    nr = np.abs(rng.normal(size=300)) + 0.1
    rand = np.abs(rng.normal(size=300)) + 0.1
    # Extra noise genes give PCA genuine structure so k-means avoids spurious correlation
    noise = {f"NOISE_{i}": np.abs(rng.normal(size=300)) + 0.1 for i in range(10)}
    gene_vals = {NR1I2_SYMBOL: nr, "RANDOM_GENE": rand, **noise}
    adata = _make_adata(300, gene_vals, "cell_type_B")
    result = coupling_per_cell_type(adata, ["RANDOM_GENE"], cells_per_metacell=10, min_metacells=5)
    assert "cell_type_B" in result.index
    rho = result.loc["cell_type_B", "RANDOM_GENE"]
    assert abs(rho) < 0.4, f"Expected |ρ| < 0.4 for uncorrelated genes, got {rho}"


def test_decoupling_score():
    """Decoupling score = ρ_hepatocyte − ρ_other."""
    rng = np.random.default_rng(2)
    nr_hep = np.abs(rng.normal(size=300)) + 0.1
    nr_other = np.abs(rng.normal(size=300)) + 0.1

    target_other = np.abs(rng.normal(size=300)) + 0.1
    adata_hep = _make_adata(300, {NR1I2_SYMBOL: nr_hep, "TARGET": nr_hep}, "hepatocyte")
    adata_other = _make_adata(
        300,
        {NR1I2_SYMBOL: nr_other, "TARGET": target_other},
        "other_ct",
    )

    import anndata

    combined = anndata.concat([adata_hep, adata_other])

    coupling = coupling_per_cell_type(combined, ["TARGET"], cells_per_metacell=10, min_metacells=5)
    ds = decoupling_score(coupling, reference_cell_type="hepatocyte")
    # hepatocyte-TARGET ρ should be high; other should be low → decoupling_score > 0
    assert ds.loc["other_ct", "TARGET"] > 0, (
        f"Expected positive decoupling score, got {ds.loc['other_ct', 'TARGET']}"
    )


def test_decoupling_score_missing_reference():
    """Raises ValueError when reference cell type absent."""
    df = pd.DataFrame({"gene_A": [0.8, 0.1]}, index=["ct1", "ct2"])
    with pytest.raises(ValueError, match="not in coupling matrix"):
        decoupling_score(df, reference_cell_type="hepatocyte")
