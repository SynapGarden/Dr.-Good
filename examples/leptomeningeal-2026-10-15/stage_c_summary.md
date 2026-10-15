# Stage C — BioNeMo molecule hypotheses (leptomeningeal disease set)

Date: 2026-10-15 (ET). Generator: **MolMIM** (hosted NVIDIA NIM, CMA-ES, QED objective, min_similarity 0.9, 30 particles, 20 iterations), 5 analogs per drug for 11 eligible small molecules = 55 analogs. Every SMILES is MolMIM output verbatim; none was hand-edited.

Docking: **DiffDock** (hosted NIM), 20 poses per candidate, into the Stage B experimental structure with the co-crystallized ligand and all waters/heteroatoms stripped (single protein chain closest to the reference ligand site). Confidence is DiffDock's own pose confidence for the top pose — higher is better, and it is a pose-plausibility number, not an affinity.

Affinity: **Boltz-2** (hosted NIM) on the real drug and its single best-docked cousin only, run twice each. `affinity_pred_value` is on a log scale where **lower = stronger predicted binding**; `binding_probability` is the model's own 0-1 chance that the pair binds at all.

## How to read the structure column
For 8 drugs the drug itself sits in the crystal structure, so the pocket is known to fit that exact molecule. For sapanisertib, tesevatinib and capecitabine the structure contains a different ligand, so their docking is **weaker evidence** — the pocket is right, but it was never shown to hold this drug.

## DiffDock — real drug vs best cousin

| Drug | Target | PDB (chain) | Drug confidence | Best cousin | Cousin confidence | Structure evidence |
|---|---|---|---|---|---|---|
| telaglenastat | Glutaminase, kidney isoform (GLS) | 5HL1 (B) | -2.338 | cousin_1 | -0.846 | drug co-crystallized |
| adavosertib | WEE1 kinase | 5V5Y (A) | 0.512 | cousin_4 | -0.300 | drug co-crystallized |
| tucatinib | HER2 (ERBB2) | 8VB5 (A) | -0.076 | cousin_3 | -0.086 | drug co-crystallized |
| ceritinib | ALK kinase | 4MKC (A) | 0.183 | cousin_1 | -0.110 | drug co-crystallized |
| sorafenib | Multi-kinase; BRAF/CRAF, VEGFR1-3, PDGFR-β, KIT, FLT3, RET | 1UWH (A) | 0.420 | cousin_5 | 0.304 | drug co-crystallized |
| methotrexate | Dihydrofolate reductase (DHFR) | 1U72 (A) | -0.005 | cousin_4 | -0.445 | drug co-crystallized |
| etoposide | Topoisomerase II alpha | 5GWK (A) | -3.849 | cousin_3 | -1.464 | drug co-crystallized |
| patupilone | Tubulin / microtubules (stabilizer) | 7DAE (D) | -0.153 | cousin_2 | -0.135 | drug co-crystallized |
| sapanisertib | mTOR kinase | 4JSV (B) | 0.375 | cousin_4 | 0.306 | weaker — drug not in structure |
| tesevatinib | EGFR (also HER2, EPHB4) | 1XKK (A) | -0.159 | cousin_4 | 0.231 | weaker — drug not in structure |
| capecitabine | Thymidylate synthase (via its metabolite FdUMP; prodrug) | 6QXG (A) | -0.635 | cousin_4 | -0.538 | weaker — drug not in structure |

All 66 candidates were docked; 64 returned poses. See `diffdock_results.csv` for every candidate.

## Boltz-2 — two repeats each

| Drug / target | Role | Run 1 affinity | Run 1 bind prob | Run 2 affinity | Run 2 bind prob | Rank stable? |
|---|---|---|---|---|---|---|
| telaglenastat (Glutaminase, kidney isoform) | drug | -0.4707 | 0.5078 | 0.2891 | 0.5312 | yes |
| telaglenastat (Glutaminase, kidney isoform) | cousin | 0.6484 | 0.1465 | 1.1875 | 0.1318 | yes |
| adavosertib (WEE1 kinase) | drug | -2.1250 | 0.8594 | -2.2188 | 0.8750 | yes |
| adavosertib (WEE1 kinase) | cousin | 1.1875 | 0.1934 | 1.2031 | 0.1196 | yes |
| tucatinib (HER2) | drug | 0.3477 | 0.4453 | 0.2754 | 0.4258 | yes |
| tucatinib (HER2) | cousin | 1.3438 | 0.0674 | 1.1797 | 0.0449 | yes |
| ceritinib (ALK kinase) | drug | -1.4062 | 0.8281 | -1.3516 | 0.8281 | yes |
| ceritinib (ALK kinase) | cousin | 0.8906 | 0.0869 | 0.9844 | 0.0986 | yes |
| sorafenib (Multi-kinase) | drug | -1.0000 | 0.5586 | -0.9766 | 0.5508 | yes |
| sorafenib (Multi-kinase) | cousin | 1.3359 | 0.4922 | 1.4531 | 0.5156 | yes |
| methotrexate (Dihydrofolate reductase) | drug | -2.0625 | 0.9922 | -2.2188 | 0.9922 | yes |
| methotrexate (Dihydrofolate reductase) | cousin | 1.7031 | 0.1006 | 1.7109 | 0.0923 | yes |
| etoposide (Topoisomerase II alpha) | drug | 0.4277 | 0.6641 | 0.4551 | 0.6562 | no |
| etoposide (Topoisomerase II alpha) | cousin | 0.6523 | 0.5547 | 0.2520 | 0.5586 | no |
| patupilone (Tubulin / microtubules) | drug | 1.1016 | 0.5547 | 0.9766 | 0.4453 | yes |
| patupilone (Tubulin / microtubules) | cousin | 1.2578 | 0.1309 | 1.2344 | 0.1099 | yes |
| sapanisertib (mTOR kinase) | drug | 0.2852 | 0.4688 | -0.2500 | 0.4375 | yes |
| sapanisertib (mTOR kinase) | cousin | 0.2871 | 0.3828 | 0.0703 | 0.3438 | yes |
| tesevatinib (EGFR) | drug | -1.6797 | 0.7188 | -1.7500 | 0.7227 | yes |
| tesevatinib (EGFR) | cousin | 1.6406 | 0.0601 | 1.6250 | 0.0588 | yes |
| capecitabine (Thymidylate synthase) | drug | 0.4453 | 0.4062 | 0.5273 | 0.3789 | yes |
| capecitabine (Thymidylate synthase) | cousin | 1.3984 | 0.2334 | 1.2656 | 0.3008 | yes |

**Unstable target: etoposide / topoisomerase II alpha.** Between the two repeats the drug and its cousin swapped places, so no ordering is claimed for that pair. Note too that etoposide in reality wedges into a protein-plus-DNA complex; only the protein chain was modelled here, so this pair is the least trustworthy in the set.

For the other ten, the real drug scored stronger than its cousin in both repeats — expected, since these are optimised approved drugs and the cousins are untested machine edits.

## Failures

| Candidate | Stage | Reason |
|---|---|---|
| telaglenastat_cousin_2 | DiffDock | service returned no numeric pose confidence; details=Fail to read ligand molecule description |
| tesevatinib_cousin_2 | DiffDock | service returned no numeric pose confidence; details=Fail to read ligand molecule description |

No Boltz-2 run failed in the end; several hit rate limits (HTTP 429) on the first pass and completed on retry.

## Files

- `molmim_analogs.json` — parent SMILES and 5 MolMIM analogs per drug
- `diffdock_results.csv` — all 66 candidates with pose confidence
- `boltz2_results.csv` — 44 Boltz-2 runs (11 drugs x drug+cousin x 2 repeats)
- `kermt_input_smiles.csv` — 22 molecules (11 real drugs + 11 best cousins) for Stage D
- `receptors/` — stripped receptor PDBs actually sent to DiffDock
- `raw/` — per-call service responses

**Model scores are hypotheses only — not clinical proof of efficacy or safety.**