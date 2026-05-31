# SLCO1B1 dossier

> **Source-of-truth caches**
> Open Targets: `dossiers/_cache/SLCO1B1_open_targets.json`
> ChEMBL: `dossiers/_cache/SLCO1B1_chembl.json`
> PubMed pull: live at assembly time (see `scripts/assemble_dossiers.py::fetch_pubmed_abstracts`)
> Paper metrics: `data/processed/coupling.csv`, `decoupling.csv`, `coupling_{ci_lower,ci_upper,qvalues}.csv`

## Identity

| Field | Value |
|---|---|
| Approved symbol | **SLCO1B1** |
| Approved name | solute carrier organic anion transporter family member 1B1 |
| Ensembl gene | [`ENSG00000134538`](https://www.ensembl.org/Homo_sapiens/Gene/Summary?g=ENSG00000134538) |
| UniProt | [`Q9Y6L6`](https://www.uniprot.org/uniprotkb/Q9Y6L6/entry) |
| ChEMBL target | [`CHEMBL1697668`](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL1697668/) |
| Biotype | protein_coding |

### Function (UniProt curated, via Open Targets)

- Mediates the Na(+)-independent uptake of organic anions (PubMed:10358072, PubMed:15159445, PubMed:17412826). Shows broad substrate specificity, can transport both organic anions such as bile acid taurocholate (cholyltaurine) and conjugated steroids (dehydroepiandrosterone 3-sulfate, 17-beta-glucuronosyl estradiol, and estrone 3-sulfate), as well as eicosanoids (prostaglandin E2, thromboxane B2, leukotriene C4, and leukotriene E4), and thyroid hormones (T4/L-thyroxine, and T3/3,3',5'-triiodo-L-thyronine) (PubMed:10358072, PubMed:10601278, PubMed:10873595, PubMed:11159893, PubMed:12196548, PubMed:12568656, PubMed:15159445, PubMed:15970799, PubMed:16627748, PubMed:17412826, PubMed:19129463, PubMed:26979622). Can take up bilirubin glucuronides from plasma into the liver, contributing to the detoxification-enhancing liver-blood shuttling loop (PubMed:22232210). Involved in the clearance of endogenous and exogenous substrates from the liver (PubMed:10358072, PubMed:10601278). Transports coproporphyrin I and III, by-products of heme synthesis, and may be involved in their hepatic disposition (PubMed:26383540). May contribute to regulate the transport of organic compounds in testes across the blood-testis-barrier (Probable). Can transport HMG-CoA reductase inhibitors (also known as statins), such as pravastatin and pitavastatin, a clinically important class of hypolipidemic drugs (PubMed:10601278, PubMed:15159445, PubMed:15970799). May play an important role in plasma and tissue distribution of the structurally diverse chemotherapeutic drug methotrexate (PubMed:23243220). May also transport antihypertension agents, such as the angiotensin-converting enzyme (ACE) inhibitor prodrug enalapril, and the highly selective angiotensin II AT1-receptor antagonist valsartan, in the liver (PubMed:16624871, PubMed:16627748). Shows a pH-sensitive substrate specificity towards prostaglandin E2 and T4 which may be ascribed to the protonation state of the binding site and leads to a stimulation of substrate transport in an acidic microenvironment (PubMed:19129463). Hydrogencarbonate/HCO3(-) acts as the probable counteranion that exchanges for organic anions (PubMed:19129463). {ECO:0000269|PubMed:10358072, ECO:0000269|PubMed:10601278, ECO:0000269|PubMed:10873595, ECO:0000269|PubMed:11159893, ECO:0000269|PubMed:12196548, ECO:0000269|PubMed:12568656, ECO:0000269|PubMed:15159445, ECO:0000269|PubMed:15970799, ECO:0000269|PubMed:16624871, ECO:0000269|PubMed:16627748, ECO:0000269|PubMed:17412826, ECO:0000269|PubMed:19129463, ECO:0000269|PubMed:22232210, ECO:0000269|PubMed:23243220, ECO:0000269|PubMed:26383540, ECO:0000269|PubMed:26979622, ECO:0000305|PubMed:35307651}.

## Paper finding (this study)

Hepatocyte Spearman ρ(NR1I2, SLCO1B1) = **0.848** (95 % bootstrap CI 0.813–0.876, BH-FDR q = 0.0041). Mean decoupling score across the nine non-hepatocyte cell types = **0.756**.

### Per-cell-type coupling

| Cell type | Spearman ρ(NR1I2, gene) |
|---|---|
| Hepatocyte | 0.848 |
| SI enterocyte | n/a |
| Crypt stem | n/a |
| LI enterocyte | -0.053 |
| Macrophage | 0.103 |
| Monocyte | 0.124 |
| NK cell | 0.193 |
| CD4+ T | 0.200 |
| CD8+ T | 0.094 |
| EVT | -0.017 |

## Open Targets — tractability

- **Small molecule**: Structure with Ligand, High-Quality Ligand, Druggable Family
- **Antibody**: UniProt loc high conf, GO CC high conf, UniProt SigP or TMHMM, Human Protein Atlas loc
- **PROTAC**: Half-life Data, Small Molecule Binder

## Open Targets — top disease associations

| Rank | Disease | Score | Therapeutic area |
|---|---|---|---|
| 1 | Rotor syndrome (`MONDO_0009379`) | 0.657 | nutritional or metabolic disease, genetic, familial or congenital disease |
| 2 | response to statin (`GO_0036273`) | 0.420 | biological_process |
| 3 | gout (`EFO_0004274`) | 0.408 | nutritional or metabolic disease, musculoskeletal or connective tissue disease, phenotype |
| 4 | Disorder of bilirubin metabolism and excretion (`Orphanet_309816`) | 0.370 | genetic, familial or congenital disease, nutritional or metabolic disease |
| 5 | Jaundice (`HP_0000952`) | 0.368 | gastrointestinal disease, phenotype |
| 6 | bilirubin metabolism disease (`MONDO_0024431`) | 0.354 | nutritional or metabolic disease |
| 7 | Gilbert syndrome (`EFO_0005556`) | 0.344 | nutritional or metabolic disease, genetic, familial or congenital disease |
| 8 | response to simvastatin (`GO_1903491`) | 0.310 | biological_process |

## Open Targets — approved drugs & clinical candidates

_No approved drugs or clinical candidates listed in Open Targets._

This is the expected pattern for metabolising enzymes and transporters: they are pharmacologically important but not therapeutic targets in their own right. See the ChEMBL bioactivity section below for tool compounds and substrates.

## Open Targets — pharmacogenomics

| Variant | Drug(s) | Category | Phenotype | Evidence |
|---|---|---|---|---|
| — | atrasentan | metabolism/pk | increased transport and decreased concentration of atrasentan | 3 |
| — | atrasentan | metabolism/pk | decreased transport and increased concentration of atrasentan | 3 |
| — | repaglinide | metabolism/pk | increased exposure of repaglinide | 3 |
| — | simvastatin | metabolism/pk | decreased simvastatin acid concentration | 1A |
| — | simvastatin acid | metabolism/pk | decreased simvastatin acid concentration | 1A |
| — | rosuvastatin | metabolism/pk | decreased exposure to rosuvastatin | 1A |
| — | atorvastatin | metabolism/pk | decreased atorvastatin concentrations | 1A |
| — | fluvastatin | toxicity | higher risk of fluvastatin-related myopathy | 1A |

## Open Targets — safety liabilities

| Event | Datasource | Effects (direction / dosing) | Biosample |
|---|---|---|---|
| statin-related myopathy or myalgia | ClinPGx | — / — | — |
| toxic liver disease | ClinPGx | — / — | — |
| creatine kinase levels and adverse events in response to treatment | ClinPGx | — / — | — |
| lovastatin-related myopathy | ClinPGx | — / — | — |
| cough | ClinPGx | — / — | — |
| creatine kinase levels | ClinPGx | — / — | — |

## ChEMBL — mechanism of action records

_No ChEMBL mechanism records for this target._

## ChEMBL — most potent bioactivity records

| Molecule | Type | Value | pChEMBL | Assay | Reference |
|---|---|---|---|---|---|
| `CHEMBL4637446` | EC50 | 1.1 nM | 8.96 | Substrate activity at OATP1B1 (unknown origin) expressed in  | `CHEMBL4619767` |
| `CHEMBL4636474` | EC50 | 1.7 nM | 8.77 | Substrate activity at OATP1B1 (unknown origin) expressed in  | `CHEMBL4619767` |
| `CHEMBL4633668` | EC50 | 4.5 nM | 8.35 | Substrate activity at OATP1B1 (unknown origin) expressed in  | `CHEMBL4619767` |
| `CHEMBL453904` | Ki | 44.0 nM | 7.36 | TP_TRANSPORTER: inhibition of E217betaG uptake in OATP-C-exp | `CHEMBL2074210` |
| `CHEMBL494753` | Ki | 45.8 nM | 7.34 | TP_TRANSPORTER: inhibition of E217betaG uptake in OATP-C-exp | `CHEMBL2074019` |
| `CHEMBL453904` | IC50 | 50.0 nM | 7.30 | TP_TRANSPORTER: inhibition of Phalloidin uptake (Phalloidin: | `CHEMBL2074164` |
| `CHEMBL1491099` | Ki | 60.0 nM | 7.22 | Ki values for sodium fluorescein (10 uM) uptake in OATP1B1-t | `CHEMBL3039007` |
| `CHEMBL4209316` | IC50 | 66.0 nM | 7.18 | Inhibition of OATP1B1 (unknown origin) | `CHEMBL4699441` |

## Recent literature

(Live PubMed pull: `SLCO1B1 AND (PXR OR NR1I2)`, sorted by publication date, top 5.)

**Molnár et al. (n.d.)** [From Genotype to Functional Risk: A Multi-Omic Approach to Predicting Thiopurine and Methotrexate Co-Therapy-Induced Liver Injury.](https://pubmed.ncbi.nlm.nih.gov/42198405/) — *Pharmaceuticals (Basel)*. The combination of thiopurine and methotrexate (MTX) is a standard co-therapy regimen for acute lymphoblastic leukemia (ALL). Despite its efficacy, this regimen is constrained by a narrow therapeutic window and considerable inter-individual variability, which heightens the risk o…

**Manca et al. (n.d.)** [Pharmacogenetics of First-Line Antitubercular Drugs: An Update.](https://pubmed.ncbi.nlm.nih.gov/40903183/) — *Ther Drug Monit*. Tuberculosis (TB) treatment relies on a prolonged first-line antibiotic regimen, including isoniazid, rifampicin (RF), ethambutol (EMB), and pyrazinamide.Pharmacogenetics plays a crucial role in optimizing TB treatment by addressing individual variability in drug metabolism and r…

**Pham et al. (n.d.)** [Structural equation modelling of nucleotide polymorphisms and pharmacokinetics in direct oral anticoagulant use for stroke and embolism prevention in atrial fibrillation.](https://pubmed.ncbi.nlm.nih.gov/40783160/) — *Eur J Pharmacol*. Genetic factors affect DOAC pharmacokinetics and efficacy in atrial fibrillation (AF) patients, yet no pharmacogenomic guidelines exist. This study aims to assess their impact on supporting personalized therapy. Following PRISMA-2020 (PROSPERO: CRD42024592412), a systematic revie…

**Zhu et al. (n.d.)** [CYP2C8-Mediated Drug-Drug Interactions and the Factors Influencing the Interaction Magnitude.](https://pubmed.ncbi.nlm.nih.gov/40980418/) — *Drug Des Devel Ther*. Older adults often have multiple morbidities that may lead to polypharmacy. Cytochrome P450 (CYP) 2C8 has shown significant contributions in the metabolism of various medications; however, its related drug-drug interactions (DDIs) appear to be underrecognized in clinical practice…

**Amorim et al. (n.d.)** [Pharmacogenetics of tuberculosis treatment toxicity and effectiveness in a large Brazilian cohort.](https://pubmed.ncbi.nlm.nih.gov/39470346/) — *Pharmacogenet Genomics*. Genetic polymorphisms have been associated with risk of antituberculosis treatment toxicity. We characterized associations with adverse events and treatment failure/recurrence among adults treated for tuberculosis in Brazil. Participants were followed in Regional Prospective Obse…


---

_Regenerate with:_
```bash
python scripts/build_dossier_data.py   # refresh JSON caches
python scripts/assemble_dossiers.py    # rebuild this markdown
```
