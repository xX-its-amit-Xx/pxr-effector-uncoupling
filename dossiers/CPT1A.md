# CPT1A dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/CPT1A_open_targets.json`
> ChEMBL: `dossiers/_cache/CPT1A_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{ci_lower,ci_upper,qvalues}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **CPT1A** |
| Approved name | carnitine palmitoyltransferase 1A |
| Ensembl gene | [`ENSG00000110090`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000110090) |
| UniProt | [`P50416`](https://www.uniprot.org/uniprotkb/P50416/entry) |
| ChEMBL target | [`CHEMBL1293194`](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL1293194/) |
| Biotype | protein_coding |

### Function (UniProt curated, via Open Targets)

- Catalyzes the transfer of the acyl group of long-chain fatty acid-CoA conjugates onto carnitine, an essential step for the mitochondrial uptake of long-chain fatty acids and their subsequent beta-oxidation in the mitochondrion (PubMed:11350182, PubMed:14517221, PubMed:16651524, PubMed:9691089). Also possesses a lysine succinyltransferase activity that can regulate enzymatic activity of substrate proteins such as ENO1 and metabolism independent of its classical carnitine O-palmitoyltransferase activity (PubMed:29425493). Plays an important role in hepatic triglyceride metabolism (By similarity). Also plays a role in inducible regulatory T-cell (iTreg) differentiation once activated by butyryl-CoA that antagonizes malonyl- CoA-mediated CPT1A repression (By similarity). Sustains the IFN-I response by recruiting ZDHCC4 to palmitoylate MAVS at the mitochondria leading to MAVS stabilization and activation (PubMed:38016475). Promotes ROS-induced oxidative stress in liver injury via modulation of NFE2L2 and NLRP3-mediated signaling pathways (By similarity). {ECO:0000250|UniProtKB:P32198, ECO:0000269|PubMed:11350182, ECO:0000269|PubMed:14517221, ECO:0000269|PubMed:16651524, ECO:0000269|PubMed:29425493, ECO:0000269|PubMed:38016475, ECO:0000269|PubMed:9691089}.

## Paper finding (this study)

Hepatocyte Spearman ρ(NR1I2, CPT1A) = **0.774** (95 % bootstrap CI 0.727–0.819, BH-FDR q = 0.0041). Mean decoupling score across the nine non-hepatocyte cell types = **0.658**.

### Per-cell-type coupling

| Cell type | Spearman ρ(NR1I2, gene) |
|---|---|
| Hepatocyte | 0.774 |
| SI enterocyte | 0.322 |
| Crypt stem | 0.584 |
| LI enterocyte | 0.195 |
| Macrophage | -0.044 |
| Monocyte | -0.072 |
| NK cell | -0.020 |
| CD4+ T | 0.034 |
| CD8+ T | -0.027 |
| EVT | 0.068 |

## Open Targets — tractability

- **Small molecule**: High-Quality Ligand, Druggable Family
- **Antibody**: UniProt SigP or TMHMM
- **PROTAC**: Database Ubiquitination, Half-life Data, Small Molecule Binder

## Open Targets — top disease associations

| Rank | Disease | Score | Therapeutic area |
|---|---|---|---|
| 1 | carnitine palmitoyl transferase 1A deficiency (`MONDO_0009705`) | 0.836 | genetic, familial or congenital disease, nutritional or metabolic disease |
| 2 | genetic disorder (`EFO_0000508`) | 0.487 | genetic, familial or congenital disease |
| 3 | cataract (`MONDO_0005129`) | 0.398 | genetic, familial or congenital disease, disorder of visual system, phenotype |
| 4 | response to xenobiotic stimulus (`GO_0009410`) | 0.346 | biological_process |
| 5 | hypertension (`EFO_0000537`) | 0.343 | cardiovascular disease, phenotype |
| 6 | aortic stenosis (`EFO_0000266`) | 0.321 | cardiovascular disease |
| 7 | heart valve prosthesis (`EFO_0003906`) | 0.208 | medical procedure |
| 8 | type 2 diabetes mellitus (`MONDO_0005148`) | 0.132 | endocrine system disease, nutritional or metabolic disease, phenotype |

## Open Targets — approved drugs & clinical candidates

_No approved drugs or clinical candidates listed in Open Targets._

This is the expected pattern for metabolising enzymes and transporters: they are pharmacologically important but not therapeutic targets in their own right. See the ChEMBL bioactivity section below for tool compounds and substrates.

## Open Targets — pharmacogenomics

_No pharmacogenomics records returned._

## Open Targets — safety liabilities

| Event | Datasource | Effects (direction / dosing) | Biosample |
|---|---|---|---|
| Increased, Liver Steatosis | AOP-Wiki | Inhibition/Decrease/Downregulation / None | — |

## ChEMBL — mechanism of action records

_No ChEMBL mechanism records for this target._

## ChEMBL — most potent bioactivity records

| Molecule | Type | Value | pChEMBL | Assay | Reference |
|---|---|---|---|---|---|
| `CHEMBL3752910` | Kd | 1.402 nM | 8.85 | Binding affinity to human CPT1A incubated for 45 mins by Kin | `CHEMBL5649169` |
| `CHEMBL3431816` | IC50 | 7.1 nM | 8.15 | SUPPLEMENTARY: Inhibition of Carnitine palmitoyltransferase  | `CHEMBL3431459` |
| `CHEMBL3431624` | IC50 | 11.6 nM | 7.94 | SUPPLEMENTARY: Inhibition of Carnitine palmitoyltransferase  | `CHEMBL3431459` |
| `CHEMBL3431814` | IC50 | 12.8 nM | 7.89 | SUPPLEMENTARY: Inhibition of Carnitine palmitoyltransferase  | `CHEMBL3431459` |
| `CHEMBL3431540` | IC50 | 13.2 nM | 7.88 | SUPPLEMENTARY: Inhibition of Carnitine palmitoyltransferase  | `CHEMBL3431459` |
| `CHEMBL3431837` | IC50 | 14.7 nM | 7.83 | SUPPLEMENTARY: Inhibition of Carnitine palmitoyltransferase  | `CHEMBL3431459` |
| `CHEMBL3431830` | IC50 | 15.15 nM | 7.82 | SUPPLEMENTARY: Inhibition of Carnitine palmitoyltransferase  | `CHEMBL3431459` |
| `CHEMBL2216778` | IC50 | 16.0 nM | 7.80 | Inhibition of human CPT1A | `CHEMBL2216752` |

## Recent literature

(Live PubMed pull: `CPT1A AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

**Kumar et al. (n.d.)** [High fat diet induced obesity is mitigated in Cyp3a-null female mice.](https://pubmed.ncbi.nlm.nih.gov/29738703/) — *Chem Biol Interact*. Recent studies indicate a role for the constitutive androstane receptor (CAR), pregnane X-receptor (PXR), and hepatic xenobiotic detoxifying CYPs in fatty liver disease or obesity. Therefore, we examined whether Cyp3a-null mice show increased obesity and fatty liver disease follo…

**Wahlang et al. (n.d.)** [Polychlorinated biphenyl 153 is a diet-dependent obesogen that worsens nonalcoholic fatty liver disease in male C57BL6/J mice.](https://pubmed.ncbi.nlm.nih.gov/23618531/) — *J Nutr Biochem*. Polychlorinated biphenyls (PCBs) are persistent environmental pollutants that are detectable in the serum of all American adults. Amongst PCB congeners, PCB 153 has the highest serum level. PCBs have been dose-dependently associated with obesity, metabolic syndrome and nonalcohol…

**Nakamura et al. (n.d.)** [Nuclear pregnane X receptor cross-talk with FoxA2 to mediate drug-induced regulation of lipid metabolism in fasting mouse liver.](https://pubmed.ncbi.nlm.nih.gov/17267396/) — *J Biol Chem*. Upon drug activation, the nuclear pregnane X receptor (PXR) regulates not only hepatic drug but also energy metabolism. Using Pxr(-/-) mice, we have now investigated the PXR-mediated repression of lipid metabolism in the fasting livers. Treatment with PXR activator pregnenolone 1…


---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
