# CYP2C8 dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/CYP2C8_open_targets.json`
> ChEMBL: `dossiers/_cache/CYP2C8_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{ci_lower,ci_upper,qvalues}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **CYP2C8** |
| Approved name | cytochrome P450 family 2 subfamily C member 8 |
| Ensembl gene | [`ENSG00000138115`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000138115) |
| UniProt | [`P10632`](https://www.uniprot.org/uniprotkb/P10632/entry) |
| ChEMBL target | [`CHEMBL3721`](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3721/) |
| Biotype | protein_coding |

### Function (UniProt curated, via Open Targets)

- A cytochrome P450 monooxygenase involved in the metabolism of various endogenous substrates, including fatty acids, steroid hormones and vitamins (PubMed:11093772, PubMed:14559847, PubMed:15766564, PubMed:19965576, PubMed:7574697). Mechanistically, uses molecular oxygen inserting one oxygen atom into a substrate, and reducing the second into a water molecule, with two electrons provided by NADPH via cytochrome P450 reductase (NADPH--hemoprotein reductase) (PubMed:11093772, PubMed:14559847, PubMed:15766564, PubMed:19965576, PubMed:7574697). Primarily catalyzes the epoxidation of double bonds of polyunsaturated fatty acids (PUFA) with a preference for the last double bond (PubMed:15766564, PubMed:19965576, PubMed:7574697). Catalyzes the hydroxylation of carbon-hydrogen bonds. Metabolizes all trans-retinoic acid toward its 4-hydroxylated form (PubMed:11093772). Displays 16-alpha hydroxylase activity toward estrogen steroid hormones, 17beta-estradiol (E2) and estrone (E1) (PubMed:14559847). Plays a role in the oxidative metabolism of xenobiotics. It is the principal enzyme responsible for the metabolism of the anti-cancer drug paclitaxel (taxol) (PubMed:26427316). {ECO:0000269|PubMed:11093772, ECO:0000269|PubMed:14559847, ECO:0000269|PubMed:15766564, ECO:0000269|PubMed:19965576, ECO:0000269|PubMed:26427316, ECO:0000269|PubMed:7574697}.

## Paper finding (this study)

Hepatocyte Spearman ρ(NR1I2, CYP2C8) = **0.814** (95 % bootstrap CI 0.767–0.848, BH-FDR q = 0.0041). Mean decoupling score across the nine non-hepatocyte cell types = **0.695**.

### Per-cell-type coupling

| Cell type | Spearman ρ(NR1I2, gene) |
|---|---|
| Hepatocyte | 0.814 |
| SI enterocyte | 0.151 |
| Crypt stem | 0.147 |
| LI enterocyte | 0.103 |
| Macrophage | 0.125 |
| Monocyte | 0.147 |
| NK cell | 0.135 |
| CD4+ T | 0.193 |
| CD8+ T | 0.084 |
| EVT | -0.014 |

## Open Targets — tractability

- **Small molecule**: Structure with Ligand, High-Quality Pocket, Druggable Family
- **Antibody**: GO CC high conf, UniProt loc med conf
- **PROTAC**: Half-life Data, Small Molecule Binder

## Open Targets — top disease associations

| Rank | Disease | Score | Therapeutic area |
|---|---|---|---|
| 1 | Abnormality of the skeletal system (`HP_0000924`) | 0.321 | phenotype |
| 2 | melanoma (`EFO_0000756`) | 0.223 | cancer or benign tumor |
| 3 | hepatocellular carcinoma (`EFO_0000182`) | 0.213 | gastrointestinal disease, endocrine system disease, cancer or benign tumor |
| 4 | urinary bladder carcinoma (`MONDO_0004986`) | 0.200 | urinary system disease, cancer or benign tumor |
| 5 | lung adenocarcinoma (`EFO_0000571`) | 0.193 | respiratory or thoracic disease, cancer or benign tumor |
| 6 | gastric carcinoma (`EFO_0000178`) | 0.190 | gastrointestinal disease, cancer or benign tumor |
| 7 | multiple myeloma (`EFO_0001378`) | 0.188 | immune system disease, hematologic disease, cancer or benign tumor, genetic, familial or congenital disease |
| 8 | gastrointestinal stromal tumor (`MONDO_0011719`) | 0.188 | genetic, familial or congenital disease, gastrointestinal disease, cancer or benign tumor |

## Open Targets — approved drugs & clinical candidates

_No approved drugs or clinical candidates listed in Open Targets._

This is the expected pattern for metabolising enzymes and transporters: they are pharmacologically important but not therapeutic targets in their own right. See the ChEMBL bioactivity section below for tool compounds and substrates.

## Open Targets — pharmacogenomics

| Variant | Drug(s) | Category | Phenotype | Evidence |
|---|---|---|---|---|
| — | diclofenac | metabolism/pk | increased metabolism of diclofenac | 3 |
| — | rosiglitazone | toxicity | increased weight gain and increased risk of edema | 3 |
| — | rosiglitazone | toxicity | decreased weight gain and decreased risk of edema | 3 |
| — | paclitaxel | toxicity | no significant association | 4 |
| rs1058932 | carboplatin | toxicity | decreased severity of thrombocytopenia | 3 |
| rs1058932 | gemcitabine | toxicity | decreased severity of thrombocytopenia | 3 |
| rs1934951 | bisphosphonates | toxicity | decreased risk for osteonecrosis of the jaw | 4 |
| rs1934951 | pamidronate | toxicity | decreased risk for osteonecrosis of the jaw | 4 |

## Open Targets — safety liabilities

| Event | Datasource | Effects (direction / dosing) | Biosample |
|---|---|---|---|
| anemia | ClinPGx | — / — | — |
| thrombocytopenia | ClinPGx | — / — | — |
| side effects | ClinPGx | — / — | — |
| neurotoxicity | ClinPGx | — / — | — |
| leukopenia | ClinPGx | — / — | — |
| kidney dysfunction | ClinPGx | — / — | — |

## ChEMBL — mechanism of action records

_No ChEMBL mechanism records for this target._

## ChEMBL — most potent bioactivity records

| Molecule | Type | Value | pChEMBL | Assay | Reference |
|---|---|---|---|---|---|
| `CHEMBL4577468` | IC50 | 2.5 nM | 8.60 | Inhibition of CYP2C8 (unknown origin) | `CHEMBL4390688` |
| `CHEMBL4066318` | Ki | 22.0 nM | 7.66 | Reversible inhibition of CYP2C8 in human liver microsomes af | `CHEMBL4017488` |
| `CHEMBL4086080` | IC50 | 26.0 nM | 7.58 | Inhibition of microsomal CYP2C8 (unknown origin) | `CHEMBL4014311` |
| `CHEMBL2036213` | IC50 | 43.0 nM | 7.37 | Inhibition of human recombinant CYP2C8 incubated for 15 mins | `CHEMBL2034935` |
| `CHEMBL2036225` | IC50 | 50.0 nM | 7.30 | Inhibition of human recombinant CYP2C8 incubated for 15 mins | `CHEMBL2034935` |
| `CHEMBL4066318` | Ki | 52.1 nM | 7.28 | Time dependent inhibition of CYP2C8 in human liver microsome | `CHEMBL4017488` |
| `CHEMBL2036220` | IC50 | 54.0 nM | 7.27 | Inhibition of human recombinant CYP2C8 incubated for 15 mins | `CHEMBL2034935` |
| `CHEMBL787` | IC50 | 56.5 nM | 7.25 | Inhibition of CYP2C8 (unknown origin) using amodiaquine as s | `CHEMBL6114965` |

## Recent literature

(Live PubMed pull: `CYP2C8 AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

**Chen et al. (n.d.)** [Interactions of neocryptotanshinone and human cytochrome P450 in silico and in vitro.](https://pubmed.ncbi.nlm.nih.gov/41419033/) — *Toxicol In Vitro*. Neocryptotanshinone (NCTS), an ingredient of Salviae Miltiorrhizae Radix et Rhizoma, is a promising compound for development since it exhibits various pharmacological effects including hypoglycemic and anti-inflammatory activities. In this study, we aimed to elucidate the interac…

**Zhu et al. (n.d.)** [CYP2C8-Mediated Drug-Drug Interactions and the Factors Influencing the Interaction Magnitude.](https://pubmed.ncbi.nlm.nih.gov/40980418/) — *Drug Des Devel Ther*. Older adults often have multiple morbidities that may lead to polypharmacy. Cytochrome P450 (CYP) 2C8 has shown significant contributions in the metabolism of various medications; however, its related drug-drug interactions (DDIs) appear to be underrecognized in clinical practice…

**Isono et al. (n.d.)** [Adenosine N6-methylation upregulates the expression of human CYP2B6 by altering the chromatin status.](https://pubmed.ncbi.nlm.nih.gov/36113565/) — *Biochem Pharmacol*. N6-Methyladenosine (m6A) modification is the most prevalent RNA modification in mammals. We have recently demonstrated that inhibition of m6A modification by 3-deazaadenosine results in an increase in the expression of the cytochrome P450 (CYP) isoforms CYP1A2, CYP2B6, and CYP2C8…

**Fricke-Galindo et al. (n.d.)** [Pharmacogenetics Approach for the Improvement of COVID-19 Treatment.](https://pubmed.ncbi.nlm.nih.gov/33807592/) — *Viruses*. The treatment of coronavirus disease 2019 (COVID-19) has been a challenge. The efficacy of several drugs has been evaluated and variability in drug response has been observed. Pharmacogenetics could explain this variation and improve patients' outcomes with this complex disease; …

**Liu et al. (n.d.)** [Expression of cytochrome P450 isozyme transcripts and activities in human livers.](https://pubmed.ncbi.nlm.nih.gov/33350342/) — *Xenobiotica*. Individual differences in cytochrome P450 (CYP) enzymes contribute to responses to drugs and environmental chemicals. The expression of CYPs is influenced by sex, age, and ethnicity. Human CYP studies are often conducted with human liver microsomes and liver cells to evaluate che…


---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
