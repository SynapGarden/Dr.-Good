# ADMET output legend (KERMT, 25 endpoints)

Unit/transform source: `Z:\Dr. Good\train_local\data\export_public_cluster_split\README.md` (dataset README shipped with the Figshare export, DOI 10.6084/m9.figshare.30350548.v2), table header line 3, endpoint rows lines 4–28 in the order below; column order matches the header of `all_val_fold_0_cluster_morgan.csv`. The KERMT repo has no per-task unit definitions (task names come from the CSV header). The source writes `log(...)` without stating the base; log10 is likely but **not established in source**.

Direction: neither the KERMT repo nor the dataset README states whether higher or lower is preferable. Where a general field convention exists it is given as such, labelled; it is not from the source.

| Endpoint | Plain-language meaning | Unit / transform (citation) | Direction |
|---|---|---|---|
| `CL_microsome_human` | How fast human liver microsomes (liver-cell enzyme preparations) break the compound down in a test tube. | log(mL/min/kg) per source; label mean 4.41 in val fold_0 is hard to reconcile with that unit — unit should be re-checked against the original source (Wenzel 2019) — `export_public_cluster_split/README.md` line 4 | Lower = slower metabolism (usually preferred for exposure); depends on goal. Not established in source |
| `CL_microsome_mouse` | Same as above, mouse liver microsomes. | log(mL/min/kg) per source (same caveat as human; val mean 4.62) — `export_public_cluster_split/README.md` line 5 | Depends. Not established in source |
| `CL_microsome_rat` | Same as above, rat liver microsomes. | log(mL/min/kg) per source (same caveat; val mean 4.74) — `export_public_cluster_split/README.md` line 6 | Depends. Not established in source |
| `CL_total_dog` | Total body clearance in dogs: how fast the whole body removes the drug from blood. | log(mL/min/kg) — `export_public_cluster_split/README.md` line 7 | Depends (lower usually means longer exposure). Not established in source |
| `CL_total_human` | Total body clearance in humans. | log(mL/min/kg) — `export_public_cluster_split/README.md` line 8 | Depends. Not established in source |
| `CL_total_monkey` | Total body clearance in monkeys. | log(mL/min/kg) — `export_public_cluster_split/README.md` line 9 | Depends. Not established in source |
| `CL_total_rat` | Total body clearance in rats. | log(mL/min/kg) — `export_public_cluster_split/README.md` line 10 | Depends. Not established in source |
| `CYP2C8_inhibition` | Concentration needed to block half the activity of liver enzyme CYP2C8 (IC50). Blocking CYP enzymes causes drug–drug interactions. | log(nM) IC50 — `export_public_cluster_split/README.md` line 11 | Higher IC50 = weaker inhibition = generally preferable (field convention). Not established in source |
| `CYP2C9_inhibition` | IC50 against liver enzyme CYP2C9. | log(nM) IC50 — `export_public_cluster_split/README.md` line 12 | Higher generally preferable (field convention). Not established in source |
| `CYP2D6_inhibition` | IC50 against liver enzyme CYP2D6. | log(nM) IC50 — `export_public_cluster_split/README.md` line 13 | Higher generally preferable (field convention). Not established in source |
| `CYP3A4_inhibition` | IC50 against CYP3A4, the enzyme that metabolises most drugs. | log(nM) IC50 — `export_public_cluster_split/README.md` line 14 | Higher generally preferable (field convention). Not established in source |
| `Dog_fraction_unbound_plasma` | Fraction of drug in dog blood plasma that is free (not stuck to proteins); only free drug can act. | log(fraction unbound) — `export_public_cluster_split/README.md` line 15 | Depends. Not established in source |
| `Human_fraction_unbound_plasma` | Free fraction in human plasma. | log(fraction unbound) — `export_public_cluster_split/README.md` line 16 | Depends. Not established in source |
| `Monkey_fraction_unbound_plasma` | Free fraction in monkey plasma. | log(fraction unbound) — `export_public_cluster_split/README.md` line 17 | Depends. Not established in source |
| `Rat_fraction_unbound_plasma` | Free fraction in rat plasma. | log(fraction unbound) — `export_public_cluster_split/README.md` line 18 | Depends. Not established in source |
| `Papp_Caco2` | How fast the compound crosses a layer of human gut-lining cells (Caco-2); a proxy for oral absorption. | log(10^-6 cm/s) apparent permeability — `export_public_cluster_split/README.md` line 19 | Higher generally preferable for oral absorption (field convention). Not established in source |
| `Pgp_human` | Efflux ratio for P-glycoprotein, a pump that pushes drugs back out of cells. | log(ratio) — `export_public_cluster_split/README.md` line 20 | Lower generally preferable (less pumped out; field convention). Not established in source |
| `hERG_binding` | IC50 for binding the hERG heart potassium channel; blocking it can cause dangerous heart rhythms. | log(nM) IC50 — `export_public_cluster_split/README.md` line 21 | Higher IC50 = weaker binding = generally preferable (field convention). Not established in source |
| `LogD_pH_7.4` | How the compound splits between oil (octanol) and water at body pH: a measure of greasiness. | Unitless ("(-)" in source); log scale not stated in source — `export_public_cluster_split/README.md` line 22 | Depends (moderate usually preferred). Not established in source |
| `kinetic_logSaq` | Kinetic solubility in water (how much dissolves quickly from a DMSO stock). | log(M) — `export_public_cluster_split/README.md` line 23 | Higher generally preferable (field convention). Not established in source |
| `thermo_logSaq` | Thermodynamic (equilibrium) solubility in water. | log(M) — `export_public_cluster_split/README.md` line 24 | Higher generally preferable (field convention). Not established in source |
| `VDss_dog` | Volume of distribution at steady state in dogs: how widely the drug spreads into tissues vs staying in blood. | log(L/kg) — `export_public_cluster_split/README.md` line 25 | Depends. Not established in source |
| `VDss_human` | Volume of distribution, humans. | log(L/kg) — `export_public_cluster_split/README.md` line 26 | Depends. Not established in source |
| `VDss_monkey` | Volume of distribution, monkeys. | log(L/kg) — `export_public_cluster_split/README.md` line 27 | Depends. Not established in source |
| `VDss_rat` | Volume of distribution, rats. | log(L/kg) — `export_public_cluster_split/README.md` line 28 | Depends. Not established in source |

**Endpoints needing attention:** `CL_microsome_*` label values (~4.4–4.7) look inconsistent with the stated unit; `LogD_pH_7.4` unit is "(-)"; direction is not established in source for any endpoint.

**None of these endpoints predicts blood–brain barrier or blood–cerebrospinal-fluid penetration.** All values are model predictions from a machine-learning model, not measurements and not safety claims.
