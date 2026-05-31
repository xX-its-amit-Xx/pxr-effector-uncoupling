# ABCC2 dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/ABCC2_open_targets.json`
> ChEMBL: `dossiers/_cache/ABCC2_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{ci_lower,ci_upper,qvalues}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **ABCC2** |
| Approved name | ATP binding cassette subfamily C member 2 |
| Ensembl gene | [`ENSG00000023839`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000023839) |
| UniProt | [`Q92887`](https://www.uniprot.org/uniprotkb/Q92887/entry) |
| ChEMBL target | [`CHEMBL5748`](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5748/) |
| Biotype | protein_coding |

### Function (UniProt curated, via Open Targets)

- ATP-dependent transporter of the ATP-binding cassette (ABC) family that binds and hydrolyzes ATP to enable active transport of various substrates including many drugs, toxicants and endogenous compound across cell membranes. Transports a wide variety of conjugated organic anions such as sulfate-, glucuronide- and glutathione (GSH)- conjugates of endo- and xenobiotics substrates (PubMed:10220572, PubMed:10421658, PubMed:11500505, PubMed:16332456). Mediates hepatobiliary excretion of mono- and bis-glucuronidated bilirubin molecules and therefore play an important role in bilirubin detoxification (PubMed:10421658). Also mediates hepatobiliary excretion of others glucuronide conjugates such as 17beta-estradiol 17- glucosiduronic acid and leukotriene C4 (PubMed:11500505). Transports sulfated bile salt such as taurolithocholate sulfate (PubMed:16332456). Transports various anticancer drugs, such as anthracycline, vinca alkaloid and methotrexate and HIV-drugs such as protease inhibitors (PubMed:10220572, PubMed:11500505, PubMed:12441801). Confers resistance to several anti-cancer drugs including cisplatin, doxorubicin, epirubicin, methotrexate, etoposide and vincristine (PubMed:10220572, PubMed:11500505). {ECO:0000269|PubMed:10220572, ECO:0000269|PubMed:10421658, ECO:0000269|PubMed:11500505, ECO:0000269|PubMed:12441801, ECO:0000269|PubMed:16332456}.

## Paper finding (this study)

Hepatocyte Spearman ρ(NR1I2, ABCC2) = **0.848** (95 % bootstrap CI 0.817–0.870, BH-FDR q = 0.0041). Mean decoupling score across the nine non-hepatocyte cell types = **0.677**.

### Per-cell-type coupling

| Cell type | Spearman ρ(NR1I2, gene) |
|---|---|
| Hepatocyte | 0.848 |
| SI enterocyte | 0.636 |
| Crypt stem | 0.042 |
| LI enterocyte | 0.099 |
| Macrophage | 0.112 |
| Monocyte | 0.230 |
| NK cell | 0.179 |
| CD4+ T | 0.173 |
| CD8+ T | 0.049 |
| EVT | 0.021 |

## Open Targets — tractability

- **Small molecule**: Structure with Ligand, High-Quality Ligand, Druggable Family
- **Antibody**: UniProt loc high conf, GO CC high conf, UniProt SigP or TMHMM
- **PROTAC**: Database Ubiquitination, Half-life Data, Small Molecule Binder

## Open Targets — top disease associations

| Rank | Disease | Score | Therapeutic area |
|---|---|---|---|
| 1 | Dubin-Johnson syndrome (`MONDO_0009380`) | 0.817 | nutritional or metabolic disease, genetic, familial or congenital disease |
| 2 | Intrahepatic cholestasis of pregnancy (`EFO_0009048`) | 0.481 | gastrointestinal disease, genetic, familial or congenital disease |
| 3 | genetic disorder (`EFO_0000508`) | 0.472 | genetic, familial or congenital disease |
| 4 | cholestasis (`MONDO_0001751`) | 0.471 | gastrointestinal disease, phenotype |
| 5 | hypothyroidism (`EFO_0004705`) | 0.322 | endocrine system disease |
| 6 | Abnormality of the liver (`HP_0001392`) | 0.289 | phenotype |
| 7 | prostatitis (`EFO_0003830`) | 0.275 | infectious disease, reproductive system or breast disease |
| 8 | autosomal recessive inherited pseudoxanthoma elasticum (`MONDO_0009925`) | 0.259 | integumentary system disease, musculoskeletal or connective tissue disease, genetic, familial or congenital disease |

## Open Targets — approved drugs & clinical candidates

_No approved drugs or clinical candidates listed in Open Targets._

This is the expected pattern for metabolising enzymes and transporters: they are pharmacologically important but not therapeutic targets in their own right. See the ChEMBL bioactivity section below for tool compounds and substrates.

## Open Targets — pharmacogenomics

| Variant | Drug(s) | Category | Phenotype | Evidence |
|---|---|---|---|---|
| rs717620 | efavirenz | metabolism/pk | decreased concentrations of efavirenz | 3 |
| rs717620 | erythromycin | other | decreased metabolism of erythromycin | 3 |
| rs717620 | tenofovir | toxicity | decreased risk of kidney tubular dysfunction | 3 |
| rs717620 | tamoxifen | efficacy | increased disease-free survival | 3 |
| rs717620 | mycophenolic acid | metabolism/pk | decreased exposure to mycophenolic acid | 3 |
| rs717620 | tacrolimus | metabolism/pk | decreased exposure to mycophenolic acid | 3 |
| rs717620 | cisplatin | efficacy | decreased response | 3 |
| rs717620 | doxorubicin | efficacy | decreased response | 3 |

## Open Targets — safety liabilities

| Event | Datasource | Effects (direction / dosing) | Biosample |
|---|---|---|---|
| neurotoxicity syndromes | ClinPGx | — / — | — |
| cardiotoxicity | ClinPGx | — / — | — |
| adverse reactions | ClinPGx | — / — | — |
| resistance to treatment | ClinPGx | — / — | — |
| anemia | ClinPGx | — / — | — |
| neutropenia | ClinPGx | — / — | — |

## ChEMBL — mechanism of action records

_No ChEMBL mechanism records for this target._

## ChEMBL — most potent bioactivity records

| Molecule | Type | Value | pChEMBL | Assay | Reference |
|---|---|---|---|---|---|
| `CHEMBL2074720` | IC50 | 280.0 nM | 6.55 | TP_TRANSPORTER: inhibition of LTC4 uptake (LTC4: 0.05 uM) in | `CHEMBL2074539` |
| `CHEMBL3038248` | IC50 | 400.0 nM | 6.40 | TP_TRANSPORTER: inhibition of LTC4 uptake (LTC4: 0.05 uM) in | `CHEMBL2074539` |
| `CHEMBL1829174` | IC50 | 2410.0 nM | 5.62 | Inhibition of human MRP2 | `CHEMBL4261634` |
| `CHEMBL160` | IC50 | 3100.0 nM | 5.51 | Inhibition Assay: To assess the inhibition of the MRP2, MRP3 | `CHEMBL3639237` |
| `CHEMBL495936` | IC50 | 3300.0 nM | 5.48 | TP_TRANSPORTER: inhibition of PAH uptake (PAH: 0.1uM) in mem | `CHEMBL2074311` |
| `CHEMBL2074650` | Ki | 3700.0 nM | 5.43 | TP_TRANSPORTER: inhibition of LTC4 uptake in membrane vesicl | `CHEMBL2073997` |
| `CHEMBL456` | IC50 | 3850.0 nM | 5.42 | Inhibition of human MRP2 overexpressed in Sf9 cell membrane  | `CHEMBL4028801` |
| `CHEMBL15177` | IC50 | 4000.0 nM | 5.40 | TP_TRANSPORTER: inhibition of PAH uptake (PAH: 0.1uM) in mem | `CHEMBL2074311` |

## Recent literature

(Live PubMed pull: `ABCC2 AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

**Molnár et al. (n.d.)** [From Genotype to Functional Risk: A Multi-Omic Approach to Predicting Thiopurine and Methotrexate Co-Therapy-Induced Liver Injury.](https://pubmed.ncbi.nlm.nih.gov/42198405/) — *Pharmaceuticals (Basel)*. The combination of thiopurine and methotrexate (MTX) is a standard co-therapy regimen for acute lymphoblastic leukemia (ALL). Despite its efficacy, this regimen is constrained by a narrow therapeutic window and considerable inter-individual variability, which heightens the risk o…

**Takahashi et al. (n.d.)** [Influence of pharmacokinetics-related polymorphisms on asciminib exposure in patients with Japanese chronic myeloid leukemia.](https://pubmed.ncbi.nlm.nih.gov/41553485/) — *Eur J Clin Pharmacol*. The effects of polymorphisms in CYP3A4, UGT2B7, ABCB1, ABCG2, ABCC2, NR1I2, and AHR genes on asciminib exposure were evaluated in Japanese patients with chronic myeloid leukemia. Plasma concentrations of asciminib (40 mg twice daily [BID] or 80 mg once daily [QD]) were measured b…

**Rzeczycki et al. (n.d.)** [Gut Microbiota in the Regulation of Intestinal Drug Transporters: Molecular Mechanisms and Pharmacokinetic Implications.](https://pubmed.ncbi.nlm.nih.gov/41465322/) — *Int J Mol Sci*. Gut microbiota, through both its species composition and its metabolites, impacts expression and activity of intestinal drug transporters. This phenomenon directly affects absorption process of orally administered drugs and contributes to the observed inter-individual variability…

**Pan et al. (n.d.)** [Activation of pregnane X receptor-organic anion transporting polypeptide 1a/b /P-glycoprotein/multidrug resistance protein 2 axis mediates the accelerated blood and liver clearance of PEGylated liposomes.](https://pubmed.ncbi.nlm.nih.gov/41106060/) — *Drug Metab Dispos*. Previous studies revealed that pregnane X receptor (PXR) was involved in the "accelerated blood clearance (ABC)" phenomenon induced by repeated injections of PEGylated liposomes, and observed the quickly reduced hepatic accumulation of the second dose in rats at 12 hours after th…

**Pawłowska et al. (n.d.)** [Unsymmetrical Bisacridines' Interactions with ABC Transporters and Their Cellular Impact on Colon LS 174T and Prostate DU 145 Cancer Cells.](https://pubmed.ncbi.nlm.nih.gov/39683740/) — *Molecules*. Multidrug resistance (MDR) is a process that constitutes a significant obstacle to effective anticancer therapy. Here, we examined whether unsymmetrical bisacridines (UAs) are substrates for ABC transporters and can influence their expression in human colon LS 174T and prostate D…


---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
