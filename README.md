# pxr-effector-uncoupling

A cell-type-resolved map of which PXR target genes stay coupled to NR1I2 expression vs. which decouple — nominating tissue-specific readouts for the next generation of selective PXR modulators.

> Full writeup added after analysis. See Checkpoint 3.

## Reproducing

```bash
uv sync
uv run jupyter lab
# Run notebooks 01–04 in order
```

## Layout

```
data/targets/   curated PXR target gene set (checked in)
notebooks/      01 atlas → 02 coupling → 03 disease overlay → 04 figure
src/            reusable Python package
figures/        output plots
tests/          coupling math unit tests
```

## License

MIT. Copyright 2026 Amit Shenoy.
