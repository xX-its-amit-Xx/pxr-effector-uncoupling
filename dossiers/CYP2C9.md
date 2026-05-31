# CYP2C9 dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/CYP2C9_open_targets.json`
> ChEMBL: `dossiers/_cache/CYP2C9_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{ci_lower,ci_upper,qvalues}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **CYP2C9** |
| Approved name | cytochrome P450 family 2 subfamily C member 9 |
| Ensembl gene | [`ENSG00000138109`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000138109) |
| UniProt | [`P11712`](https://www.uniprot.org/uniprotkb/P11712/entry) |
| ChEMBL target | [`CHEMBL3397`](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3397/) |
| Biotype | protein_coding |

### Function (UniProt curated, via Open Targets)

- A cytochrome P450 monooxygenase involved in the metabolism of various endogenous substrates, including fatty acids and steroids (PubMed:12865317, PubMed:15766564, PubMed:19965576, PubMed:21576599, PubMed:7574697, PubMed:9435160, PubMed:9866708). Mechanistically, uses molecular oxygen inserting one oxygen atom into a substrate, and reducing the second into a water molecule, with two electrons provided by NADPH via cytochrome P450 reductase (NADPH--hemoprotein reductase) (PubMed:12865317, PubMed:15766564, PubMed:19965576, PubMed:21576599, PubMed:7574697, PubMed:9435160, PubMed:9866708). Catalyzes the epoxidation of double bonds of polyunsaturated fatty acids (PUFA) (PubMed:15766564, PubMed:19965576, PubMed:7574697, PubMed:9866708). Catalyzes the hydroxylation of carbon-hydrogen bonds. Metabolizes cholesterol toward 25-hydroxycholesterol, a physiological regulator of cellular cholesterol homeostasis (PubMed:21576599). Exhibits low catalytic activity for the formation of catechol estrogens from 17beta- estradiol (E2) and estrone (E1), namely 2-hydroxy E1 and E2 (PubMed:12865317). Catalyzes bisallylic hydroxylation and hydroxylation with double-bond migration of polyunsaturated fatty acids (PUFA) (PubMed:9435160, PubMed:9866708). Also metabolizes plant monoterpenes such as limonene. Oxygenates (R)- and (S)-limonene to produce carveol and perillyl alcohol (PubMed:11950794). Contributes to the wide pharmacokinetics variability of the metabolism of drugs such as S- warfarin, diclofenac, phenytoin, tolbutamide and losartan (PubMed:25994031). {ECO:0000269|PubMed:11950794, ECO:0000269|PubMed:12865317, ECO:0000269|PubMed:15766564, ECO:0000269|PubMed:19965576, ECO:0000269|PubMed:21576599, ECO:0000269|PubMed:25994031, ECO:0000269|PubMed:7574697, ECO:0000269|PubMed:9435160, ECO:0000269|PubMed:9866708}.

## Paper finding (this study)

Hepatocyte Spearman ρ(NR1I2, CYP2C9) = **0.891** (95 % bootstrap CI 0.859–0.918, BH-FDR q = 0.0041). Mean decoupling score across the nine non-hepatocyte cell types = **0.698**.

### Per-cell-type coupling

| Cell type | Spearman ρ(NR1I2, gene) |
|---|---|
| Hepatocyte | 0.891 |
| SI enterocyte | 0.477 |
| Crypt stem | 0.279 |
| LI enterocyte | 0.251 |
| Macrophage | 0.127 |
| Monocyte | 0.165 |
| NK cell | 0.143 |
| CD4+ T | 0.234 |
| CD8+ T | 0.076 |
| EVT | -0.019 |

## Open Targets — tractability

- **Small molecule**: Structure with Ligand, High-Quality Ligand, High-Quality Pocket, Druggable Family
- **Antibody**: GO CC high conf, UniProt loc med conf
- **PROTAC**: Half-life Data, Small Molecule Binder

## Open Targets — top disease associations

| Rank | Disease | Score | Therapeutic area |
|---|---|---|---|
| 1 | cholesterol embolism (`EFO_0005801`) | 0.487 | cardiovascular disease |
| 2 | response to anticoagulant (`GO_0061476`) | 0.406 | biological_process |
| 3 | Abnormality of the skeletal system (`HP_0000924`) | 0.226 | phenotype |
| 4 | placenta praevia (`EFO_0007442`) | 0.089 | pregnancy or perinatal disease, reproductive system or breast disease |
| 5 | colorectal carcinoma (`EFO_1001951`) | 0.083 | gastrointestinal disease, cancer or benign tumor |
| 6 | head and neck squamous cell carcinoma (`EFO_0000181`) | 0.079 | cancer or benign tumor |
| 7 | hypertension (`EFO_0000537`) | 0.077 | cardiovascular disease, phenotype |
| 8 | Blindness (`HP_0000618`) | 0.076 | phenotype |

## Open Targets — approved drugs & clinical candidates

_No approved drugs or clinical candidates listed in Open Targets._

This is the expected pattern for metabolising enzymes and transporters: they are pharmacologically important but not therapeutic targets in their own right. See the ChEMBL bioactivity section below for tool compounds and substrates.

## Open Targets — pharmacogenomics

| Variant | Drug(s) | Category | Phenotype | Evidence |
|---|---|---|---|---|
| — | sulfonamides, urea derivatives | toxicity | decreased risk of hypoglycemia | 3 |
| — | sulfonamides, urea derivatives | toxicity | increased risk of hypoglycemia | 3 |
| — | olanzapine | toxicity | hypotension | 3 |
| — | olanzapine | toxicity | hypotension | 3 |
| — | phenytoin | metabolism/pk | decreased rate of phenytoin clearance | 3 |
| — | phenytoin | metabolism/pk | increased rate of phenytoin clearance | 3 |
| — | sulfonamides, urea derivatives | efficacy | increased response | 3 |
| — | phenytoin | metabolism/pk | — | 3 |

## Open Targets — safety liabilities

| Event | Datasource | Effects (direction / dosing) | Biosample |
|---|---|---|---|
| maculopapular exanthema | ClinPGx | — / — | — |
| phenytoin toxicity | ClinPGx | — / — | — |
| regulation of transcription factor activity | ToxCast | — / — | HepaRG |
| adverse events | ClinPGx | — / — | — |
| dyspepsia | ClinPGx | — / — | — |
| venous thrombosis | ClinPGx | — / — | — |

## ChEMBL — mechanism of action records

_No ChEMBL mechanism records for this target._

## ChEMBL — most potent bioactivity records

| Molecule | Type | Value | pChEMBL | Assay | Reference |
|---|---|---|---|---|---|
| `CHEMBL16596` | IC50 | 0.5 nM | 9.30 | Inhibition of CYP2C9 | `CHEMBL1153536` |
| `CHEMBL220360` | IC50 | 0.93 nM | 9.03 | Inhibition of CYP2C9 in human liver microsomes after 30 mins | `CHEMBL1221281` |
| `CHEMBL38958` | IC50 | 1.0 nM | 9.00 | Inhibition of CYP2C9 | `CHEMBL1153536` |
| `CHEMBL1825089` | IC50 | 1.0 nM | 9.00 | Inhibition of CYP2C9 using a fluorescent probe 7-methoxy-4-t | `CHEMBL1821661` |
| `CHEMBL1922663` | IC50 | 1.5 nM | 8.82 | Inhibition of human CYP2C9 | `CHEMBL1921749` |
| `CHEMBL1223034` | IC50 | 2.6 nM | 8.59 | Inhibition of CYP2C9 in human liver microsomes after 30 mins | `CHEMBL1221281` |
| `CHEMBL4593464` | IC50 | 2.7 nM | 8.57 | Inhibition of CYP2C9 in human liver microsomes using diclofe | `CHEMBL4371025` |
| `CHEMBL1172346` | IC50 | 3.0 nM | 8.52 | Inhibition of CYP2C9 | `CHEMBL1177769` |

## Recent literature

(Live PubMed pull: `CYP2C9 AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

**Ganamurali et al. (n.d.)** [Guggulsterone-Mediated Selective Modulation of Nuclear Receptors: Implications for FXR-PXR Signaling and Hepatic Metabolic Homeostasis.](https://pubmed.ncbi.nlm.nih.gov/42140551/) — *Prostaglandins Other Lipid Mediat*. Guggulsterone (GSS), a plant-derived steroid from Commiphora mukul, exhibits complex pharmacological behavior through modulation of nuclear receptors and detoxification enzymes. Acting as an antagonist of the Farnesoid X receptor (FXR) and an agonist of the Pregnane X receptor (P…

**Yu et al. (n.d.)** [Dexamethasone-Mediated Regulation of CYP3A4 and UGTs in Human Hepatoma HuH-7 Cells.](https://pubmed.ncbi.nlm.nih.gov/42014325/) — *Fundam Clin Pharmacol*. The application of human hepatic cell lines to early drug discovery and development instead of human primary hepatocytes (HPHs) has been limited because of the low level of drug-metabolizing enzymes (DMEs). The study aimed to evaluate the effects of dexamethasone (DEX) treatment …

**Davey et al. (n.d.)** [Use of a cytochrome P450 humanized mouse model to refine schistosomiasis drug discovery.](https://pubmed.ncbi.nlm.nih.gov/41961851/) — *Proc Natl Acad Sci U S A*. Control of schistosomiasis, a neglected tropical disease caused by infection with Schistosoma spp., remains reliant on a single chemotherapy, praziquantel (PZQ). This strategy presents a risk to global health should PZQ-resistant schistosomes establish in endemic areas and justif…

**Kahiya et al. (n.d.)** [In Silico Comparison of Rifampicin and 25-desacetyl Rifampicin-Induced PXR-Mediated CYP450 Transcriptional Response in 3D Primary Human Hepatocytes.](https://pubmed.ncbi.nlm.nih.gov/41787130/) — *Bull Math Biol*. The pregnane X receptor (PXR) regulates the expression of cytochrome P450 (CYP) enzymes and plays a crucial role in the metabolism of various drugs. Rifampicin (RIF) is a PXR ligand that forms the primary metabolite, 25-desacetyl rifampicin (25-DRIF), which retains the antimicrob…

**Xiao et al. (n.d.)** [Deep Learning Models for Predicting Human Cytochrome P450 Inhibition and Induction.](https://pubmed.ncbi.nlm.nih.gov/40966069/) — *J Chem Inf Model*. Given the critical roles played by human cytochrome P450 enzymes (CYPs) in drug metabolism, accurately predicting their potential inhibition and induction by drugs and drug candidates is a key objective for improving drug development and safety assessment. Traditional experimenta…


---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
