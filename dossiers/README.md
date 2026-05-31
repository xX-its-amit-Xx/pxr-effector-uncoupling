# Per-gene dossiers

Structured intel for each hepatocyte-selective PXR readout plus the receptor itself.
Each file is a self-contained brief assembled from Open Targets v4, ChEMBL v34, the paper's own coupling CSVs, and a live PubMed pull.

| Gene | Hepatocyte ρ | Decoupling score | Role |
|---|---|---|---|
| [CYP2C9](CYP2C9.md) | 0.89 | 0.70 | Phase I CYP; warfarin / NSAID metabolism |
| [CYP3A5](CYP3A5.md) | 0.87 | 0.63 | Polymorphic CYP; tacrolimus dosing |
| [ABCC2](ABCC2.md) | 0.85 | 0.68 | Apical efflux transporter (MRP2); Dubin-Johnson syndrome |
| [SLCO1B1](SLCO1B1.md) | 0.85 | 0.76 | Basolateral uptake transporter; statin response, Rotor syndrome |
| [CYP2C8](CYP2C8.md) | 0.81 | 0.69 | Phase I CYP; paclitaxel / repaglinide metabolism |
| [CPT1A](CPT1A.md) | 0.77 | 0.66 | Rate-limiting enzyme, mitochondrial fatty-acid β-oxidation |
| [NR1I2](NR1I2.md) | n/a | n/a | The receptor itself (PXR) |

## How to use these

A reviewer or co-author can read one file per gene and walk away with:
- the paper's quantitative finding (coupling ρ, CI, q-value, decoupling magnitude across every cell type)
- the external-pharmacology context (Open Targets disease associations, tractability flags, approved-drug & clinical-candidate inventory, pharmacogenomic variants of clinical interest, known safety liabilities)
- the medicinal-chemistry context (ChEMBL mechanism-of-action records, most potent measured bioactivities, drug-status flags)
- the last few recent PubMed papers tying the gene back to PXR / NR1I2

Nothing in these files is curated by hand — everything is mechanically pulled from public databases and reassembled. To refresh, re-run `scripts/build_dossier_data.py` (drops the cache) then `scripts/assemble_dossiers.py` (rebuilds the markdown).
