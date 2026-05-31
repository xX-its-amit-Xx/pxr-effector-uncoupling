# NR1I2 dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/NR1I2_open_targets.json`
> ChEMBL: `dossiers/_cache/NR1I2_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{ci_lower,ci_upper,qvalues}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **NR1I2** |
| Approved name | nuclear receptor subfamily 1 group I member 2 |
| Ensembl gene | [`ENSG00000144852`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000144852) |
| UniProt | [`O75469`](https://www.uniprot.org/uniprotkb/O75469/entry) |
| ChEMBL target | [`CHEMBL3401`](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3401/) |
| Biotype | protein_coding |

### Function (UniProt curated, via Open Targets)

- Nuclear receptor that acts as a transcription factor regulating genes involved in the metabolism and excretion of xenobiotics, drugs, and endogenous compounds. Activated by a broad range of endogenous steroids (e.g. pregnenolone, progesterone) and xenobiotics, including the antibiotic rifampicin and certain plant- derived metabolites. Upon ligand binding, translocates to the nucleus, forms a heterodimer with the retinoid X receptor/RXR, and binds to response elements in target promoters, leading to transcriptional activation. Target genes include cytochrome P450 enzymes such as CYP3A4 and ATP-binding cassette transporters including ABCB1/MDR1. {ECO:0000269|PubMed:11297522, ECO:0000269|PubMed:11668216, ECO:0000269|PubMed:12578355, ECO:0000269|PubMed:18768384, ECO:0000269|PubMed:19297428, ECO:0000269|PubMed:26534988, ECO:0000269|PubMed:9727070}.

## Paper finding (this study)

_This gene is not in the analysed PXR target set._

### Per-cell-type coupling

| Cell type | Spearman ρ(NR1I2, gene) |
|---|---|

## Open Targets — tractability

- **Small molecule**: Structure with Ligand, High-Quality Ligand, High-Quality Pocket, Druggable Family
- **PROTAC**: Database Ubiquitination, Small Molecule Binder

## Open Targets — top disease associations

| Rank | Disease | Score | Therapeutic area |
|---|---|---|---|
| 1 | skin disease (`EFO_0000701`) | 0.323 | integumentary system disease |
| 2 | adolescent idiopathic scoliosis (`EFO_0005423`) | 0.321 | musculoskeletal or connective tissue disease |
| 3 | ulcerative colitis (`EFO_0000729`) | 0.302 | gastrointestinal disease, immune system disease, genetic, familial or congenital disease |
| 4 | neurodegenerative disease (`EFO_0005772`) | 0.203 | nervous system disease |
| 5 | Abnormality of the skeletal system (`HP_0000924`) | 0.179 | phenotype |
| 6 | obesity (`EFO_0001073`) | 0.157 | nutritional or metabolic disease, phenotype |
| 7 | neoplasm (`EFO_0000616`) | 0.119 | cancer or benign tumor |
| 8 | hepatocellular carcinoma (`EFO_0000182`) | 0.115 | gastrointestinal disease, endocrine system disease, cancer or benign tumor |

## Open Targets — approved drugs & clinical candidates

_No approved drugs or clinical candidates listed in Open Targets._

This is the expected pattern for metabolising enzymes and transporters: they are pharmacologically important but not therapeutic targets in their own right. See the ChEMBL bioactivity section below for tool compounds and substrates.

## Open Targets — pharmacogenomics

| Variant | Drug(s) | Category | Phenotype | Evidence |
|---|---|---|---|---|
| rs1523130 | risperidone | metabolism/pk | increased clearance of risperidone | 3 |
| rs3814055 | sirolimus | metabolism/pk | increased likelihood of adverse events including bone marrow, gastro-intestinal  | 3 |
| rs3814055 | sirolimus | metabolism/pk | increased metabolism of temsirolimus | 3 |
| rs3814055 | sirolimus | toxicity | increased likelihood of adverse events including bone marrow, gastro-intestinal  | 3 |
| rs3814055 | sirolimus | toxicity | increased metabolism of temsirolimus | 3 |
| rs3814055 | temsirolimus | metabolism/pk | increased likelihood of adverse events including bone marrow, gastro-intestinal  | 3 |
| rs3814055 | temsirolimus | metabolism/pk | increased metabolism of temsirolimus | 3 |
| rs3814055 | temsirolimus | toxicity | increased likelihood of adverse events including bone marrow, gastro-intestinal  | 3 |

## Open Targets — safety liabilities

| Event | Datasource | Effects (direction / dosing) | Biosample |
|---|---|---|---|
| regulation of steroid hormone biosynthetic process | ToxCast | — / — | H295R |
| bone marrow and gastrointestinal toxicities | ClinPGx | — / — | — |
| anemia | ClinPGx | — / — | — |
| bone marrow and gastrointestinal toxicities or other adverse events | ClinPGx | — / — | — |
| exposure | ClinPGx | — / — | — |
| discontinuation due to neuropsychiatric adverse events | ClinPGx | — / — | — |

## ChEMBL — mechanism of action records

_No ChEMBL mechanism records for this target._

## ChEMBL — most potent bioactivity records

| Molecule | Type | Value | pChEMBL | Assay | Reference |
|---|---|---|---|---|---|
| `CHEMBL463678` | EC50 | 0.7 nM | 9.15 | Agonist activity at human pregnane X receptor expressed in H | `CHEMBL1157161` |
| `CHEMBL5284539` | IC50 | 1.0 nM | 9.00 | Inverse agonist activity at human PXR in human HepG2 cells c | `CHEMBL5236619` |
| `CHEMBL464497` | EC50 | 1.5 nM | 8.82 | Agonist activity at human pregnane X receptor expressed in H | `CHEMBL1157161` |
| `CHEMBL5286515` | IC50 | 1.6 nM | 8.80 | Inverse agonist activity at human PXR in human HepG2 cells c | `CHEMBL5236619` |
| `CHEMBL8739` | EC50 | 2.0 nM | 8.70 | Activation of human PXR expressed in human HepG2 (DPX-2) cel | `CHEMBL3525965` |
| `CHEMBL410683` | IC50 | 2.4 nM | 8.62 | Inhibitory concentration against Pregnane X receptor | `CHEMBL1140376` |
| `CHEMBL402063` | IC50 | 2.4 nM | 8.62 | Inhibitory concentration against Pregnane X receptor | `CHEMBL1140376` |
| `CHEMBL396952` | EC50 | 3.162 nM | 8.50 | Antagonist activity at human PXR by transient transfection a | `CHEMBL1146359` |

## Recent literature

(Live PubMed pull: `NR1I2 AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

**Liu et al. (n.d.)** [Pregnane X receptor mitigates aristolochic acid-induced acute kidney injury via p53 ubiquitination.](https://pubmed.ncbi.nlm.nih.gov/41812323/) — *Ren Fail*. Aristolochic acid (AA), commonly used in Chinese herbal medicine to treat various diseases, can cause acute kidney injury (AKI). The pregnane X receptor (PXR), a nuclear receptor, is involved in drug metabolism, carcinogenesis, inflammation, apoptosis, oxidative stress and energy…

**Zheng et al. (n.d.)** [Differences in hepatic metabolism of Liandan Xiaoyan Formula between control and ulcerative colitis mice associated with FXR/PXR-CYP450 changes.](https://pubmed.ncbi.nlm.nih.gov/42105596/) — *J Pharm Biomed Anal*. Understanding the metabolic process of traditional Chinese prescription (TCP) during disease states and its underlying mechanisms is crucial for evaluating therapeutic efficacy and safety. Cytochrome P450 (CYP450)-mediated hepatic metabolism plays a key role in this process. Lian…

**Lu et al. (n.d.)** [Health hazards of per- and polyfluoroalkyl substances via nuclear receptors.](https://pubmed.ncbi.nlm.nih.gov/41934778/) — *Environ Pollut*. Per- and polyfluoroalkyl substances (PFAS) are highly persistent environmental contaminants that lead to continuous human exposure, posing a major global public health concern. However, the multisystem effects at the molecular level remain insufficiently understood. This review p…

**Wortman et al. (n.d.)** [Pharmacokinetic drug-drug interactions with flucloxacillin and other isoxazolyl penicillins: A systematic literature review and practical guide.](https://pubmed.ncbi.nlm.nih.gov/41789926/) — *Br J Clin Pharmacol*. Recent years have seen a notable increase in the number of publications concerning pharmacokinetic drug-drug interactions involving the isoxazolyl penicillins cloxacillin, dicloxacillin, flucloxacillin and oxacillin. Given that the findings predominantly rely on clinical observat…

**Elgharbaoui et al. (n.d.)** [In silico identification of peptidomimetic inhibitors targeting PXR and RXR interaction to overcome the inactivation of vitamin D in asthma.](https://pubmed.ncbi.nlm.nih.gov/40908379/) — *Mol Divers*. Asthma is a chronic inflammatory disorder of the airways. Standard treatments, such as inhaled corticosteroids like fluticasone, beclomethasone, and budesonide, are effective in managing asthma symptoms by reducing inflammation through immune suppression. However, prolonged corti…


---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
