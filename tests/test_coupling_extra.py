"""Additional coupling tests — sparse input, determinism, edge cases."""

import numpy as np
import pandas as pd
import pytest
import scipy.sparse as sp
from anndata import AnnData

from pxr_uncoupling.config import NR1I2_SYMBOL
from pxr_uncoupling.coupling import build_metacells, coupling_per_cell_type, decoupling_score


def _adata(n_cells: int, n_extra: int, rng_seed: int = 0, sparse: bool = False) -> AnnData:
    rng = np.random.default_rng(rng_seed)
    nr = np.abs(rng.normal(size=n_cells)) + 0.1
    cols = {NR1I2_SYMBOL: nr, "G_perfect": nr.copy()}
    for i in range(n_extra):
        cols[f"BG_{i}"] = np.abs(rng.normal(size=n_cells)) + 0.1
    X = np.column_stack(list(cols.values())).astype(np.float32)
    if sparse:
        X = sp.csr_matrix(X)
    obs = pd.DataFrame({"cell_type": ["c"] * n_cells})
    var = pd.DataFrame(index=list(cols.keys()))
    var.index.name = "gene_symbol"
    return AnnData(X=X, obs=obs, var=var)


def test_sparse_input_handled():
    """Pipeline must densify sparse matrices internally without crashing."""
    adata = _adata(300, n_extra=10, sparse=True)
    result = coupling_per_cell_type(
        adata,
        ["G_perfect"],
        cells_per_metacell=10,
        min_metacells=5,
    )
    assert "c" in result.index
    assert abs(result.loc["c", "G_perfect"] - 1.0) < 0.05


def test_determinism_same_seed():
    """Same random_state must yield identical metacells (and thus identical ρ)."""
    adata = _adata(200, n_extra=10, rng_seed=7)
    m1 = build_metacells(adata, cells_per_metacell=10, random_state=42)
    m2 = build_metacells(adata, cells_per_metacell=10, random_state=42)
    pd.testing.assert_frame_equal(m1, m2)


def test_below_min_metacells_skipped():
    """Cell types yielding fewer metacells than threshold are absent from output."""
    adata = _adata(50, n_extra=10)  # 50 cells / 10 per metacell = 5 metacells
    result = coupling_per_cell_type(
        adata,
        ["G_perfect"],
        cells_per_metacell=10,
        min_metacells=20,
    )
    assert result.empty or "c" not in result.index


def test_missing_target_gene_returns_nan():
    """Targets absent from var_names should drop from the output silently."""
    adata = _adata(300, n_extra=10)
    result = coupling_per_cell_type(
        adata,
        ["G_perfect", "G_missing"],
        cells_per_metacell=10,
        min_metacells=5,
    )
    # missing genes are filtered before the loop, so they don't appear at all
    assert "G_missing" not in result.columns
    assert "G_perfect" in result.columns


def test_decoupling_score_shape_and_direction():
    """Decoupling matrix excludes the reference row; sign matches ρ_hep − ρ_other."""
    coupling = pd.DataFrame(
        {"gene1": [0.8, 0.1, -0.2], "gene2": [-0.3, 0.5, 0.6]},
        index=["hepatocyte", "ct1", "ct2"],
    )
    ds = decoupling_score(coupling, reference_cell_type="hepatocyte")
    assert "hepatocyte" not in ds.index
    assert ds.loc["ct1", "gene1"] == pytest.approx(0.7)
    assert ds.loc["ct2", "gene2"] == pytest.approx(-0.9)
