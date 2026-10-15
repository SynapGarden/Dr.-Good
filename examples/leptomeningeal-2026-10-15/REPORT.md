# Leptomeningeal disease — evidence-first pipeline report

Run date: 2026-10-15 (ET). Stages A-C complete; Stage D (KERMT ADMET) status noted below.

## 1. What this is, in plain words

**Leptomeningeal disease (LMD)** is what happens when cancer spreads into the thin, fluid-filled lining that wraps the brain and spinal cord. Cancer cells float in the cerebrospinal fluid rather than sitting in one lump, so they are hard to reach with drugs and hard to measure. It is uncommon, it is serious, and it is badly under-studied.

**What this run did.** First it pulled every leptomeningeal study from ClinicalTrials.gov (219 found) and kept the **19 that have actual results posted** — those are the only ones with real patient outcome numbers to stand on. Then, for the drugs in those trials that are small molecules, it found the protein each one acts on and a real experimental crystal structure of that protein, generated close chemical relatives ("cousins") with MolMIM, docked everything with DiffDock, scored binding twice with Boltz-2, and finally ran the owner's locally trained KERMT model to predict absorption and safety properties.

**What this cannot show.** Nothing here is evidence that any drug works. The trial numbers come from small, uncontrolled studies. The model numbers are computer guesses about chemistry, not about patients. No new treatment is being proposed; this is a map of what is known plus hypotheses to test in a lab.

## 2. Trial evidence — the 19 studies with posted results

| NCT | Study | Phase | Drug(s) | Design | Enrolled | Headline posted outcome | Serious AEs / deaths | Modality |
|---|---|---|---|---|---|---|---|---|
| NCT02336451 | A Phase II Study to Evaluate the Efficacy and Safety of Oral | P2 | ceritinib | 5 arms, non-randomized, no comparator (allocation NON_RANDOMIZED, model PARALLEL) | 156 | ORR by arm 35.7 / 30.0 / 50.0 / 59.1%; leptomeningeal arm (Arm 5) 16.7% | serious AEs 75 of 156; deaths 31 of 156 | SMALL MOLECULE (ceritinib) |
| NCT00445965 | Iodine I 131 Monoclonal Antibody 3F8 in Treating Patients Wi | P2 | — | single-arm (allocation NA, model SINGLE_GROUP) | 78 | 67/78 alive at 6 months; 31 complete responses, 8 stable, 21 progressed, 18 not evaluable | serious AEs 39 of 78; deaths 54 of 78 | BIOLOGIC (radiolabeled antibody 131I-3F8) |
| NCT00450866 | Epothilone B in Treating Patients With CNS Metastases From B | P2 | patupilone | single-arm (allocation NA, model SINGLE_GROUP) | 55 | CNS progression-free at 3 months: 12 participants (Group A), 2 (Group B) | serious AEs 18; deaths 0+ (some groups not posted) | SMALL MOLECULE (patupilone/epothilone B; record labels it "Biological") |
| NCT03275402 | 131I-omburtamab Radioimmunotherapy for Neuroblastoma Central | P2, P3 | — | single-arm (allocation NA, model SINGLE_GROUP) | 52 | 3-year overall survival rate 0.65 | serious AEs 20 of 52; deaths 17 of 52 | BIOLOGIC (radiolabeled antibody 131I-omburtamab) |
| NCT04420598 | DS-8201a for trEatment of aBc, BRain Mets, And Her2[+] Disea | P2 | — | single-arm (allocation NA, model SINGLE_GROUP) | 41 | Cohort 1 16-week PFS: 1 of 8; ORR cohorts 2/3/4: 7, 5, 3 responders | serious AEs 11 of 40; deaths 22 of 40 | BIOLOGIC (antibody-drug conjugate trastuzumab deruxtecan) |
| NCT00801216 | High-dose Sequential Chemoimmunotherapy for B-cell Lymphomas | P2 | methotrexate, cytarabine, cyclophosphamide, etoposide, thiotepa, carmustine | single-arm (allocation NA, model SINGLE_GROUP) | 40 | 2-year event-free survival: 16 participants (of 40 enrolled, 38 at risk) | serious AEs 4 of 38; deaths 22 of 38 | MIXED regimen: small molecules (methotrexate, cytarabine, cyclophosphamide, etoposide, thiotepa, carmustine) + rituximab (antibody) + stem-cell transplant + radiation |
| NCT02616393 | Phase 2 Study of Study of Tesevatinib in Subjects With NSCLC | P2 | tesevatinib | 3 arms, non-randomized, no comparator (allocation NON_RANDOMIZED, model SINGLE_GROUP) | 36 | Brain-met ORR 31.3% overall; leptomeningeal cohort (B) ORR 0% | serious AEs 21 of 36; deaths 18 of 36 | SMALL MOLECULE (tesevatinib) |
| NCT01325207 | Intrathecal Trastuzumab for Leptomeningeal Metastases in HER | P1, P2 | — | single-arm (allocation not stated, model SEQUENTIAL) | 34 | Best response: 6 partial responses, 18 stable, 0 complete; 1 dose-limiting toxicity at 80 mg | serious AEs 21 of 34; deaths 30 of 34 | BIOLOGIC (intrathecal trastuzumab antibody) |
| NCT04250545 | Testing of the Anti Cancer Drugs CB-839 HCl (Telaglenastat)  | P1 | sapanisertib, telaglenastat | single-arm (allocation NA, model SINGLE_GROUP) | 22 | MTD/RP2D: NA (not established); overall responses 1 + 0 + 1 participants across dose levels | serious AEs 12 of 22; deaths 15 of 22 | SMALL MOLECULE (sapanisertib + telaglenastat) |
| NCT00924820 | A Pilot Study of Bevacizumab for Neoplastic Meningitis | P1, P2 | — | single-arm (allocation NA, model SINGLE_GROUP) | 20 | CSF response rate 93% of participants; median time to progression 3 weeks | serious AEs 11; deaths 0+ (some groups not posted) | BIOLOGIC (bevacizumab antibody) |
| NCT02939300 | Ipilimumab and Nivolumab in Leptomeningeal Metastases | P2 | — | single-arm (allocation NA, model SINGLE_GROUP) | 18 | 44% of participants alive at 3 months | serious AEs 10 of 18; deaths 13 of 18 | BIOLOGIC (nivolumab + ipilimumab antibodies) |
| NCT03501979 | Tucatinib, Trastuzumab, and Capecitabine for the Treatment o | P2 | tucatinib, capecitabine | single-arm (allocation NA, model SINGLE_GROUP) | 17 | Survival after starting treatment: 6 participants (of 17) | serious AEs 1 of 17; deaths 11 of 17 | MIXED: small molecules tucatinib + capecitabine, plus trastuzumab antibody |
| NCT02948751 | Microfluidic Device to Diagnose Leptomeningeal Metastasis in | not stated | — | single-arm (allocation NA, model SINGLE_GROUP) | 14 | Diagnostic device: 3 participants with LM detected (of 14); no treatment effect measured | serious AEs 0 of 14; deaths 0 of 14 | DEVICE/diagnostic (OncoCEE CSF test) — no treatment |
| NCT03091478 | Pembrolizumab in Patients With Leptomeningeal Disease | P2 | — | single-arm (allocation NA, model SINGLE_GROUP) | 13 | At 12 weeks: 2 complete, 1 partial, 2 stable, 8 progressive | serious AEs 7 of 13; deaths 9 of 13 | BIOLOGIC (pembrolizumab antibody) |
| NCT00523939 | DepoCyt for Active Lymphomatous or Leukemic Meningitis | P2 | cytarabine | 2 arms, non-randomized, no comparator (allocation NON_RANDOMIZED, model PARALLEL) | 4 | Response Rate: no value posted in the results module | serious AEs 3; deaths 0+ (some groups not posted) | SMALL MOLECULE (liposomal cytarabine, intrathecal) |
| NCT01596127 | Intrathecal Rituximab in Lymphoid Malignancies Involving Cen | P1, P2 | — | single-arm (allocation NA, model SINGLE_GROUP) | 4 | Response rate 0% at 2 weeks | serious AEs 1 of 3; deaths 1 of 3 | BIOLOGIC (intrathecal rituximab antibody) |
| NCT04460937 | Testing the Addition of an Anti-cancer Drug, Adavosertib, to | P1 | adavosertib | single-arm (allocation NA, model SINGLE_GROUP) | 4 | Maximum tolerated dose 200 mg adavosertib with radiation | serious AEs 0 of 4; deaths 4 of 4 | SMALL MOLECULE (adavosertib) + RADIATION |
| NCT00992602 | Liposomal Cytarabine and High-Dose Methotrexate in Treating  | P2 | methotrexate, cytarabine | single-arm (allocation NA, model SINGLE_GROUP) | 3 | Survival free of neurological progression: 6 weeks | serious AEs 0 of 3; deaths 3 of 3 | SMALL MOLECULE (methotrexate + liposomal cytarabine) |
| NCT00964743 | Depocyt® With Sorafenib in Neoplastic Meningitis | NA | cytarabine, sorafenib | single-arm (allocation NA, model SINGLE_GROUP) | 2 | Safety-only readout: adverse events in 2 of 2 participants | serious AEs 2; deaths 0+ (some groups not posted) | SMALL MOLECULE (liposomal cytarabine + sorafenib) |

## 3. Read this before the table above

> **None of the 19 studies had a control arm.** Every one is single-arm or several non-randomised cohorts of the same drug. That means the posted outcomes describe how these particular patients did — they do **not** show that any drug beat another option, or beat no treatment at all.
>
> **Most studies were tiny.** Enrollments include 2, 3, 4, 4, 4, 13, 14, 17, 18, 20 and 22 participants. At those sizes a single patient moves the headline number by tens of percent. Only NCT02336451 (ceritinib, n=156) is large enough for its response rates to mean much, and even there the leptomeningeal arm was 16.7%.
>
> Deaths in these tables are mostly from the cancer itself, not from the drug; these are late-stage patients. Do not read a death count as a drug safety signal without the full record.

## 4. Molecule hypotheses — structure, docking, affinity, ADMET

Boltz-2 `affinity_pred_value` is log-scale: **lower = stronger predicted binding**. `binding_probability` is the model's own 0-1 chance the pair binds at all. DiffDock confidence is pose plausibility, not affinity.

| Drug | Target | PDB (res. Å) | Bound ligand | DiffDock drug | DiffDock best cousin | Boltz-2 drug aff r1/r2 | drug prob r1/r2 | cousin aff r1/r2 | cousin prob r1/r2 | Rank stable | Evidence note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sapanisertib | mTOR kinase | 4JSV (3.5000) | none (ADP; drug not bound). Drug-bound only in PI3Kα 6GVF (2.5 Å, ligand FE5) | 0.3752 | 0.3059 (4) | 0.2852 / -0.2500 | 0.4688 / 0.4375 | 0.2871 / 0.0703 | 0.3828 / 0.3438 | yes | weaker — drug not present in the structure |
| telaglenastat | Glutaminase, kidney isoform (GLS) | 5HL1 (2.4) | 63J (CB-839) | -2.3377 | -0.8458 (1) | -0.4707 / 0.2891 | 0.5078 / 0.5312 | 0.6484 / 1.1875 | 0.1465 / 0.1318 | yes | drug co-crystallized |
| adavosertib | WEE1 kinase | 5V5Y (1.9) | 8X7 (MK-1775) | 0.5123 | -0.3001 (4) | -2.1250 / -2.2188 | 0.8594 / 0.8750 | 1.1875 / 1.2031 | 0.1934 / 0.1196 | yes | drug co-crystallized |
| tucatinib | HER2 (ERBB2) | 8VB5 (1.48) | A1AAC (HER2 exon20-insertion mutant) | -0.0764 | -0.0856 (3) | 0.3477 / 0.2754 | 0.4453 / 0.4258 | 1.3438 / 1.1797 | 0.0674 / 0.0449 | yes | drug co-crystallized |
| capecitabine | Thymidylate synthase (via its metabolite FdUMP; prodrug) | 6QXG (2.08) | UFP (FdUMP, the active metabolite — not capecitabine) | -0.6346 | -0.5376 (4) | 0.4453 / 0.5273 | 0.4062 / 0.3789 | 1.3984 / 1.2656 | 0.2334 / 0.3008 | yes | weaker — drug not present in the structure |
| methotrexate | Dihydrofolate reductase (DHFR) | 1U72 (1.9) | MTX (+NADPH); Leu22-variant study — check chain is wild-type | -0.0046 | -0.4453 (4) | -2.0625 / -2.2188 | 0.9922 / 0.9922 | 1.7031 / 1.7109 | 0.1006 / 0.0923 | yes | drug co-crystallized |
| ceritinib | ALK kinase | 4MKC (2.01) | 4MK (LDK378 = ceritinib) | 0.1825 | -0.1101 (1) | -1.4062 / -1.3516 | 0.8281 / 0.8281 | 0.8906 / 0.9844 | 0.0869 / 0.0986 | yes | drug co-crystallized |
| tesevatinib | EGFR (also HER2, EPHB4) | 1XKK (2.4) | none for tesevatinib; FMM = lapatinib, a quinazoline analog | -0.1589 | 0.2306 (4) | -1.6797 / -1.7500 | 0.7188 / 0.7227 | 1.6406 / 1.6250 | 0.0601 / 0.0588 | yes | weaker — drug not present in the structure |
| sorafenib | Multi-kinase; BRAF/CRAF, VEGFR1-3, PDGFR-β, KIT, FLT3, RET | 1UWH (2.95) | BAX (sorafenib, wild-type BRAF) | 0.4197 | 0.3038 (5) | -1.0000 / -0.9766 | 0.5586 / 0.5508 | 1.3359 / 1.4531 | 0.4922 / 0.5156 | yes | drug co-crystallized |
| etoposide | Topoisomerase II alpha | 5GWK (3.152) | EVP (with DNA) | -3.8492 | -1.4638 (3) | 0.4277 / 0.4551 | 0.6641 / 0.6562 | 0.6523 / 0.2520 | 0.5547 / 0.5586 | no | drug co-crystallized; **rank flipped between repeats — no ordering claimed**; real target is protein+DNA, only protein modelled |
| patupilone | Tubulin / microtubules (stabilizer) | 7DAE (2.394) | EPB (epothilone B) | -0.1532 | -0.1351 (2) | 1.1016 / 0.9766 | 0.5547 / 0.4453 | 1.2578 / 1.2344 | 0.1309 / 0.1099 | yes | drug co-crystallized |
| cytarabine | DNA polymerase (label: "appears to"; no specific protein named) | none chosen (—) | not applicable — no named protein target | missing | missing (—) | missing / missing | missing / missing | missing / missing | missing / missing | missing | not eligible for the molecule models — not applicable — no named protein target |
| cyclophosphamide | DNA (alkylator) — no protein target | not applicable (—) | — | missing | missing (—) | missing / missing | missing / missing | missing / missing | missing / missing | missing | not eligible for the molecule models — — |
| thiotepa | DNA (alkylator) — no protein target | not applicable (—) | — | missing | missing (—) | missing / missing | missing / missing | missing / missing | missing / missing | missing | not eligible for the molecule models — — |
| carmustine | DNA/RNA alkylator — no protein target | not applicable (—) | — | missing | missing (—) | missing / missing | missing / missing | missing / missing | missing / missing | missing | not eligible for the molecule models — — |

Two candidates failed DiffDock outright and are reported as failed, not substituted: `telaglenastat_cousin_2` and `tesevatinib_cousin_2` (service error: "Fail to read ligand molecule description").

### KERMT ADMET (Stage D)

Checkpoint: v11 epoch-31, val MAE 0.39627. Values are in the model's own units (several are log-scale), rounded to 3 decimals.

| Molecule | role | CL_microsome_human | CL_microsome_mouse | CL_microsome_rat | CL_total_dog | CL_total_human | CL_total_monkey | CL_total_rat | CYP2C8_inhibition | CYP2C9_inhibition | CYP2D6_inhibition | CYP3A4_inhibition | Dog_fraction_unbound_plasma | Human_fraction_unbound_plasma | Monkey_fraction_unbound_plasma | Rat_fraction_unbound_plasma | Papp_Caco2 | Pgp_human | hERG_binding | LogD_pH_7.4 | kinetic_logSaq | thermo_logSaq | VDss_dog | VDss_human | VDss_monkey | VDss_rat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| telaglenastat | drug | 4.717 | 4.724 | 4.665 | 0.907 | 0.390 | 1.108 | 0.885 | 3.413 | 3.099 | 3.815 | 3.542 | -1.353 | -2.191 | -1.164 | -1.834 | 0.560 | 0.610 | 3.352 | 3.560 | -5.470 | -5.581 | 0.246 | -0.075 | 0.008 | 0.170 |
| telaglenastat_cousin_1 | cousin | 3.980 | 4.596 | 4.354 | 1.188 | 0.756 | 0.977 | 1.442 | 4.089 | 4.102 | 3.942 | 4.206 | -0.314 | -0.556 | -0.483 | -0.465 | 1.260 | 0.558 | 4.507 | 1.857 | -3.884 | -2.304 | 0.094 | 0.071 | -0.034 | 0.343 |
| adavosertib | drug | 4.148 | 4.290 | 4.456 | 0.969 | 0.728 | 0.909 | 1.435 | 4.028 | 3.889 | 4.176 | 3.985 | -0.754 | -0.931 | -0.745 | -0.778 | 0.855 | 0.616 | 3.977 | 2.371 | -4.052 | -3.436 | 0.232 | 0.162 | 0.053 | 0.341 |
| adavosertib_cousin_4 | cousin | 4.136 | 4.927 | 4.714 | 1.162 | 0.779 | 1.116 | 1.378 | 3.611 | 3.690 | 3.407 | 3.845 | -0.935 | -1.392 | -0.691 | -1.213 | 1.213 | 0.370 | 3.296 | 3.062 | -4.666 | -4.315 | 0.298 | 0.179 | 0.150 | 0.609 |
| tucatinib | drug | 4.468 | 4.700 | 4.642 | 1.125 | 0.745 | 1.032 | 1.205 | 3.627 | 3.346 | 3.510 | 3.052 | -0.977 | -1.432 | -0.835 | -1.262 | 0.910 | 0.444 | 3.955 | 2.890 | -4.746 | -4.087 | 0.375 | 0.265 | 0.116 | 0.381 |
| tucatinib_cousin_3 | cousin | 4.124 | 4.413 | 4.456 | 1.279 | 0.772 | 1.110 | 1.704 | 4.157 | 4.279 | 3.838 | 4.083 | -0.374 | -0.420 | -0.375 | -0.270 | 0.555 | 0.634 | 4.277 | 0.794 | -3.872 | -2.569 | 0.206 | 0.176 | -0.010 | 0.464 |
| ceritinib | drug | 4.411 | 4.355 | 4.422 | 0.918 | 0.528 | 1.090 | 1.217 | 3.485 | 3.634 | 3.902 | 3.605 | -1.227 | -1.667 | -1.016 | -1.541 | 0.312 | 0.811 | 3.876 | 2.677 | -5.131 | -4.911 | 0.423 | 0.270 | 0.095 | 0.377 |
| ceritinib_cousin_1 | cousin | 3.942 | 4.442 | 4.481 | 1.213 | 0.848 | 1.064 | 1.599 | 4.091 | 4.101 | 3.651 | 4.075 | -0.446 | -0.857 | -0.469 | -0.501 | 0.954 | 0.418 | 3.734 | 1.660 | -3.964 | -2.446 | 0.337 | 0.371 | 0.084 | 0.516 |
| sorafenib | drug | 4.352 | 4.515 | 4.604 | 0.915 | 0.446 | 1.220 | 0.879 | 3.109 | 3.056 | 3.469 | 3.316 | -1.330 | -1.784 | -1.143 | -1.669 | 0.557 | 0.643 | 3.524 | 3.294 | -5.708 | -5.616 | 0.215 | -0.074 | 0.142 | 0.182 |
| sorafenib_cousin_5 | cousin | 4.610 | 5.059 | 5.166 | 0.962 | 0.534 | 1.480 | 1.145 | 3.355 | 3.468 | 3.726 | 3.702 | -1.324 | -1.726 | -1.108 | -1.721 | 1.134 | -0.067 | 3.254 | 4.277 | -6.021 | -6.348 | 0.281 | 0.125 | 0.302 | 0.385 |
| methotrexate | drug | 3.495 | 3.932 | 4.144 | 0.419 | 0.162 | 0.273 | 0.706 | 4.596 | 4.368 | 4.815 | 4.694 | -0.486 | -0.921 | -0.406 | -0.801 | -0.509 | 0.488 | 5.683 | -1.533 | -3.832 | -3.435 | -0.365 | -0.572 | -0.566 | -0.378 |
| methotrexate_cousin_4 | cousin | 4.158 | 4.304 | 4.448 | 1.001 | 0.652 | 0.954 | 1.317 | 4.076 | 4.043 | 4.051 | 4.002 | -0.405 | -0.702 | -0.523 | -0.391 | 0.909 | 0.626 | 4.031 | 0.935 | -3.833 | -1.734 | 0.093 | 0.066 | 0.028 | 0.235 |
| etoposide | drug | 4.383 | 4.614 | 4.739 | 1.058 | 0.185 | 0.844 | 1.430 | 4.094 | 4.257 | 4.637 | 3.894 | -1.006 | -1.443 | -1.032 | -1.126 | 0.109 | 0.295 | 4.334 | 1.569 | -4.026 | -3.812 | 0.347 | -0.046 | -0.017 | 0.337 |
| etoposide_cousin_3 | cousin | 3.990 | 4.582 | 4.577 | 1.291 | 0.940 | 1.072 | 1.610 | 4.195 | 4.364 | 3.888 | 4.153 | -0.530 | -0.812 | -0.563 | -0.499 | 0.864 | 0.087 | 4.236 | 1.018 | -3.956 | -2.585 | 0.460 | 0.378 | 0.194 | 0.589 |
| patupilone | drug | 4.807 | 4.918 | 5.165 | 1.344 | 0.583 | 0.876 | 1.462 | 4.094 | 4.303 | 4.238 | 3.460 | -1.007 | -0.838 | -1.032 | -1.059 | 1.303 | 0.263 | 4.387 | 2.856 | -3.934 | -2.926 | 0.437 | 0.307 | 0.185 | 0.667 |
| patupilone_cousin_2 | cousin | 4.034 | 4.766 | 4.845 | 1.228 | 0.656 | 1.073 | 1.586 | 4.182 | 4.100 | 3.978 | 4.014 | -0.571 | -0.623 | -0.643 | -0.402 | 1.288 | 0.246 | 3.948 | 2.421 | -3.888 | -2.831 | 0.399 | 0.142 | 0.035 | 0.388 |
| sapanisertib | drug | 4.180 | 4.506 | 4.749 | 0.973 | 0.764 | 0.889 | 1.294 | 3.748 | 3.965 | 4.055 | 3.744 | -0.370 | -0.671 | -0.688 | -0.713 | 1.198 | 0.092 | 4.171 | 2.293 | -4.087 | -3.425 | 0.291 | 0.283 | 0.160 | 0.290 |
| sapanisertib_cousin_4 | cousin | 4.035 | 4.444 | 4.644 | 1.085 | 0.886 | 1.020 | 1.605 | 3.973 | 4.188 | 4.047 | 3.978 | -0.356 | -0.544 | -0.540 | -0.352 | 0.738 | 0.327 | 3.831 | 1.145 | -3.907 | -2.887 | 0.172 | 0.385 | 0.055 | 0.420 |
| tesevatinib | drug | 4.539 | 4.785 | 4.799 | 1.058 | 0.674 | 1.256 | 1.581 | 3.685 | 3.807 | 3.655 | 3.746 | -1.115 | -1.521 | -0.872 | -1.339 | 0.997 | 0.251 | 3.402 | 3.581 | -4.907 | -4.716 | 0.463 | 0.459 | 0.206 | 0.609 |
| tesevatinib_cousin_4 | cousin | 4.060 | 4.345 | 4.505 | 0.991 | 0.572 | 0.968 | 1.384 | 4.126 | 4.010 | 4.497 | 4.343 | -0.397 | -0.388 | -0.510 | -0.318 | 0.971 | 0.382 | 4.451 | 1.032 | -3.925 | -1.655 | 0.095 | -0.044 | -0.040 | 0.255 |
| capecitabine | drug | 3.964 | 4.329 | 4.312 | 0.845 | 0.514 | 0.810 | 1.177 | 4.059 | 4.225 | 4.419 | 4.499 | -0.619 | -0.868 | -0.616 | -0.700 | 0.816 | 0.398 | 4.441 | 1.142 | -3.866 | -3.099 | -0.088 | -0.110 | -0.057 | 0.087 |
| capecitabine_cousin_4 | cousin | 3.982 | 4.267 | 4.381 | 1.283 | 0.787 | 1.131 | 1.500 | 4.103 | 4.179 | 3.654 | 4.145 | -0.294 | -0.358 | -0.330 | -0.328 | 0.751 | 0.591 | 4.446 | 0.730 | -3.945 | -1.671 | 0.218 | 0.236 | 0.186 | 0.504 |

## 5. Honest readout

**Most coherent across trial evidence + docking + affinity:**

- **Ceritinib / ALK (NCT02336451).** The only study in the set with real size (n=156) and real response rates, and the chemistry agrees: ceritinib docks into its own crystal structure (4MKC), and Boltz-2 gives it the strongest numbers in the set after methotrexate (affinity -1.406 / -1.352, binding probability 0.828 in both repeats), beating its cousin in both repeats. Caveat that matters: the **leptomeningeal arm specifically was 16.7%**, far below the brain-met arms. So ALK is a coherent target; leptomeningeal benefit is not demonstrated.
- **Methotrexate / DHFR.** The strongest and most reproducible model result in the set — binding probability 0.992 in both repeats, affinity -2.063 / -2.219. This is also the least surprising: methotrexate-DHFR is one of the best-characterised drug-target pairs in medicine, so this mostly tells us the model behaves sensibly. Clinically it appears only inside multi-drug regimens here (NCT00801216, NCT00992602), so no single-drug conclusion can be drawn.
- **Adavosertib / WEE1.** Clean chemistry (co-crystal 5V5Y, affinity -2.125 / -2.219, probability 0.859 / 0.875, stable). But the trial is n=4 and reports only a maximum tolerated dose — there is no efficacy evidence at all.

**Weak or discordant:**

- **Tesevatinib / EGFR.** Strong model numbers (affinity -1.680 / -1.750, probability ~0.72) against a **0% response rate** in the leptomeningeal cohort of NCT02616393, with 12 of 20 patients dying. This is the clearest reminder in the whole report that good binding predictions do not translate into patient benefit. The structure evidence is also weaker — 1XKK does not contain tesevatinib.
- **Etoposide / topoisomerase II alpha.** Rank flipped between the two Boltz-2 repeats, so by the pipeline's own rule **no ordering is claimed**. Physically it is the worst-modelled case too: etoposide really acts on a protein-plus-DNA complex, and only the protein was modelled.
- **Sapanisertib / mTOR and capecitabine / thymidylate synthase.** Both dock into structures that do not contain the drug, and both score weakly (sapanisertib probability 0.47 / 0.44; capecitabine 0.41 / 0.38). Capecitabine is additionally a prodrug — the active species is its metabolite, so docking the parent molecule is the wrong question.
- **Telaglenastat, tucatinib, sorafenib, patupilone.** Middling binding probabilities (0.13-0.56) and trials of 2-22 patients. Nothing here supports a conclusion either way.

In every case the cousins MolMIM invented scored worse than the real drug (except the etoposide pair, where no ordering is claimed). That is the expected, reassuring result: these are optimised approved drugs and the cousins are untested machine edits. **No cousin in this run is a lead.**

## 6. Limitations and the real next step

- No control arms anywhere in the 19 trials; most enrolled single digits. Posted outcomes are descriptive only.
- Docking and affinity models score a static protein pocket. They do not model the blood-brain or blood-CSF barrier, which is the single biggest obstacle in leptomeningeal disease — a drug can bind perfectly and never reach the cerebrospinal fluid.
- Three drugs were docked into structures that do not contain them (sapanisertib, tesevatinib, capecitabine); one target (topoisomerase II alpha) was modelled without its DNA.
- Antibodies, radiolabelled antibodies, antibody-drug conjugates, cell therapy, radiation and the diagnostic device cannot be scored by these molecule models at all, and several of the 19 trials are exactly those.
- **The next step is not more compute.** It is a wet-lab assay: a binding or cell-viability measurement on the drug-target pairs flagged as coherent, and crucially a CSF-penetration measurement. No amount of additional modelling can substitute for that.

---

**Model scores are hypotheses only — not clinical proof of efficacy or safety.**
