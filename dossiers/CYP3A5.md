# CYP3A5 dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/CYP3A5_open_targets.json`
> ChEMBL: `dossiers/_cache/CYP3A5_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{ci_lower,ci_upper,qvalues}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **CYP3A5** |
| Approved name | cytochrome P450 family 3 subfamily A member 5 |
| Ensembl gene | [`ENSG00000106258`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000106258) |
| UniProt | [`P20815`](https://www.uniprot.org/uniprotkb/P20815/entry) |
| ChEMBL target | [`CHEMBL3019`](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3019/) |
| Biotype | protein_coding |

### Function (UniProt curated, via Open Targets)

- A cytochrome P450 monooxygenase involved in the metabolism of steroid hormones and vitamins (PubMed:10681376, PubMed:11093772, PubMed:12865317, PubMed:2732228). Mechanistically, uses molecular oxygen inserting one oxygen atom into a substrate, and reducing the second into a water molecule, with two electrons provided by NADPH via cytochrome P450 reductase (NADPH--hemoprotein reductase). Catalyzes the hydroxylation of carbon-hydrogen bonds (PubMed:10681376, PubMed:11093772, PubMed:12865317, PubMed:2732228). Exhibits high catalytic activity for the formation of catechol estrogens from 17beta- estradiol (E2) and estrone (E1), namely 2-hydroxy E1 and E2 (PubMed:12865317). Catalyzes 6beta-hydroxylation of the steroid hormones testosterone, progesterone, and androstenedione (PubMed:2732228). Catalyzes the oxidative conversion of all-trans- retinol to all-trans-retinal, a rate-limiting step for the biosynthesis of all-trans-retinoic acid (atRA) (PubMed:10681376). Further metabolizes all trans-retinoic acid (atRA) to 4-hydroxyretinoate and may play a role in hepatic atRA clearance (PubMed:11093772). Also involved in the oxidative metabolism of xenobiotics, including calcium channel blocking drug nifedipine and immunosuppressive drug cyclosporine (PubMed:2732228). {ECO:0000269|PubMed:10681376, ECO:0000269|PubMed:11093772, ECO:0000269|PubMed:12865317, ECO:0000269|PubMed:2732228}.

## Paper finding (this study)

Hepatocyte Spearman ρ(NR1I2, CYP3A5) = **0.875** (95 % bootstrap CI 0.844–0.900, BH-FDR q = 0.0041). Mean decoupling score across the nine non-hepatocyte cell types = **0.631**.

### Per-cell-type coupling

| Cell type | Spearman ρ(NR1I2, gene) |
|---|---|
| Hepatocyte | 0.875 |
| SI enterocyte | 0.668 |
| Crypt stem | 0.623 |
| LI enterocyte | 0.261 |
| Macrophage | 0.126 |
| Monocyte | 0.153 |
| NK cell | 0.124 |
| CD4+ T | 0.210 |
| CD8+ T | 0.095 |
| EVT | -0.067 |

## Open Targets — tractability

- **Small molecule**: Approved Drug, Structure with Ligand, High-Quality Ligand, Druggable Family
- **Antibody**: UniProt loc med conf
- **PROTAC**: Half-life Data, Small Molecule Binder

## Open Targets — top disease associations

| Rank | Disease | Score | Therapeutic area |
|---|---|---|---|
| 1 | HIV infection (`EFO_0000764`) | 0.606 | infectious disease, reproductive system or breast disease |
| 2 | HIV-1 infection (`EFO_0000180`) | 0.592 | infectious disease, reproductive system or breast disease |
| 3 | chronic hepatitis C virus infection (`EFO_0004220`) | 0.567 | infectious disease, gastrointestinal disease, endocrine system disease |
| 4 | hepatitis C virus infection (`EFO_0003047`) | 0.547 | infectious disease, gastrointestinal disease, endocrine system disease |
| 5 | infection (`EFO_0000544`) | 0.516 | biological_process |
| 6 | COVID-19 (`MONDO_0100096`) | 0.413 | infectious disease |
| 7 | AIDS (`EFO_0000765`) | 0.408 | immune system disease, infectious disease, genetic, familial or congenital disease, reproductive system or breast disease |
| 8 | viral disease (`EFO_0000763`) | 0.375 | infectious disease |

## Open Targets — approved drugs & clinical candidates

| Drug | Max stage | Action | Drug type |
|---|---|---|---|
| COBICISTAT (`CHEMBL2095208`) | APPROVAL | INHIBITOR (Cytochrome P450 3A inhibitor) | Small molecule |
| RITONAVIR (`CHEMBL163`) | APPROVAL | INHIBITOR (Cytochrome P450 3A inhibitor; Human immunodeficiency virus type 1 protease inhibitor) | Small molecule |

## Open Targets — pharmacogenomics

| Variant | Drug(s) | Category | Phenotype | Evidence |
|---|---|---|---|---|
| — | atazanavir | metabolism/pk | metabolize atazanavir more rapidly | 3 |
| — | carboplatin | toxicity | increased risk for leukopenia or neutropenia | 3 |
| — | paclitaxel | toxicity | increased risk for leukopenia or neutropenia | 3 |
| — | olanzapine | metabolism/pk | decreased exposure | 4 |
| — | olanzapine | metabolism/pk | increased exposure | 4 |
| — | cyclosporine | metabolism/pk | decreased metabolism of cyclosporine | 3 |
| — | cyclosporine | dosage | increased cyclosporine dose requirements | 3 |
| — | tacrolimus | dosage | increased dose of tacrolimus | 2A |

## Open Targets — safety liabilities

| Event | Datasource | Effects (direction / dosing) | Biosample |
|---|---|---|---|
| myalgia | ClinPGx | — / — | — |
| systolic and diastolic blood pressure | ClinPGx | — / — | — |
| regulation of catalytic activity | ToxCast | — / — | — |
| leukopenia or neutropenia | ClinPGx | — / — | — |
| dose reductions due to toxicity | ClinPGx | — / — | — |
| calcineurin-inhibitor induced hepatic toxicity | ClinPGx | — / — | — |

## ChEMBL — mechanism of action records

_No ChEMBL mechanism records for this target._

## ChEMBL — most potent bioactivity records

| Molecule | Type | Value | pChEMBL | Assay | Reference |
|---|---|---|---|---|---|
| `CHEMBL1159650` | IC50 | 2.0 nM | 8.70 | Inhibition of CYP3A5 (unknown origin) | `CHEMBL6103568` |
| `CHEMBL157101` | IC50 | 16.0 nM | 7.80 | Inhibition of CYP3A5 (unknown origin) incubated for 30 min i | `CHEMBL6071168` |
| `CHEMBL1159650` | IC50 | 21.0 nM | 7.68 | Inhibition of CYP3A5 in doxycycline-induced CYP3A5 overexpre | `CHEMBL4321880` |
| `CHEMBL1159650` | IC50 | 44.0 nM | 7.36 | Inhibition of CYP3A5 in wild type human AsPC1 cells assessed | `CHEMBL4321880` |
| `CHEMBL1159650` | IC50 | 78.0 nM | 7.11 | Inhibition of CYP3A5 in lentiviral pLVX-TRE3G-ZsGreen1-CYP3A | `CHEMBL4321880` |
| `CHEMBL1159650` | Kd | 100.0 nM | 7.00 | Binding affinity to heme in His-tagged CYP3A5 (unknown origi | `CHEMBL4321880` |
| `CHEMBL1159650` | IC50 | 103.0 nM | 6.99 | Inhibition of CYP3A5 in CRISPR/Cas9-mediated CYP3A5 knock-ou | `CHEMBL4321880` |
| `CHEMBL157101` | IC50 | 120.0 nM | 6.92 | Fluorescent High Throughput P450 Assays: The interaction of  | `CHEMBL3886338` |

## Recent literature

(Live PubMed pull: `CYP3A5 AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

**Chen et al. (n.d.)** [Role of pregnane X receptor in the upregulation of human aldehyde oxidase gene expression.](https://pubmed.ncbi.nlm.nih.gov/42178049/) — *Biochem Pharmacol*. The present study was designed to test the hypothesis that pregnane X receptor (PXR) regulates human aldehyde oxidase (AOX1) gene expression. Treatment of LS180 human colon adenocarcinoma cells, a commonly used human PXR (hPXR) experimental model, with a hPXR agonist (rifampicin,…

**Liem et al. (n.d.)** [Impact of the gut microbiome on hepatic cytochrome P450 3A4 (CYP3A4) in humanized pregnane X receptor-constitutive androstane receptor-CYP3A4/3A7 mice.](https://pubmed.ncbi.nlm.nih.gov/42025145/) — *Drug Metab Dispos*. The interaction between the gut microbiome and drug metabolism is bidirectional and can influence the pharmacokinetics of certain drugs. In mice, the gut microbiome has been shown to influence Cyp3a11. However, evidence for microbial regulation of human cytochrome P450 3A4 (CYP3A…

**Yu et al. (n.d.)** [Dexamethasone-Mediated Regulation of CYP3A4 and UGTs in Human Hepatoma HuH-7 Cells.](https://pubmed.ncbi.nlm.nih.gov/42014325/) — *Fundam Clin Pharmacol*. The application of human hepatic cell lines to early drug discovery and development instead of human primary hepatocytes (HPHs) has been limited because of the low level of drug-metabolizing enzymes (DMEs). The study aimed to evaluate the effects of dexamethasone (DEX) treatment …

**Abdel-Rasol et al. (n.d.)** [Coenzyme Q10 protects against atorvastatin-induced hepatotoxicity via attenuation of oxidative stress and functional modulation of CYP3A1.](https://pubmed.ncbi.nlm.nih.gov/41957824/) — *BMC Pharmacol Toxicol*. Atorvastatin (ATO) is a widely prescribed lipid-lowering drug, but its use can be limited by hepatotoxicity, potentially linked to metabolism-related mechanisms. The cellular pathways connecting ATO metabolism to oxidative imbalance and apoptotic alterations remain incompletely d…

**Dohnalová et al. (n.d.)** [Pregnane X receptor antagonist MI-891 reduces hepatic triglycerides in PXR-CAR-CYP3A4/3A7-humanized mice.](https://pubmed.ncbi.nlm.nih.gov/41795330/) — *Biomed Pharmacother*. Hepatic steatosis is a major metabolic concern associated with activation of the pregnane X receptor (PXR), a nuclear receptor known to promote lipogenesis and lipid accumulation in the liver. While the lipogenic effects of PXR agonists are well documented, there is no comprehens…


---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
