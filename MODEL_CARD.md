# Model card — Dr. Good KERMT multitask ADMET model (checkpoint v11)

## What this model does

Given a molecule's structure (as a SMILES string), it predicts 25 properties describing how that molecule is likely to behave in a body: how fast it is cleared, how much of it is free in blood plasma, whether it blocks certain liver enzymes, how soluble it is, and whether it interacts with the hERG cardiac ion channel. These are collectively called **ADMET** properties — absorption, distribution, metabolism, excretion and toxicity.

This is a fine-tune of **KERMT**, a chemical pretrained model from NVIDIA Digital Biology, trained on a public multitask ADMET dataset.

## Intended use

Research triage only. It is meant to answer "does this molecule look roughly reasonable on known chemistry?" inside the Dr. Good evidence pipeline, where it serves as a **validation layer** — a check that the pipeline behaves sensibly on drugs whose properties are already understood.

## What this model must not be used for

- **It is not a safety claim.** A favourable hERG or CYP prediction is not evidence that a compound is safe in people. An unfavourable one is not evidence of harm.
- **It does not predict brain or spinal fluid penetration.** No endpoint here measures blood-brain barrier or blood-CSF transport. For central nervous system indications, this model is silent on the property that matters most.
- **It is not a substitute for measurement.** Every output is a prediction, and several endpoints are weakly supported (below).
- **It must not be used to make anything more toxic.** Toxicity endpoints exist here to avoid harm, not to optimise for it.

## Training data

- **Source:** *"Datasets for 'Multitask finetuning and acceleration of chemical pretrained models for small molecule drug property prediction'"*, [Figshare DOI 10.6084/m9.figshare.30350548.v2](https://doi.org/10.6084/m9.figshare.30350548.v2), published 2025-10-13.
- **Split:** the dataset's own public cluster split, `fold_0`. Clustered splitting means structurally similar molecules stay on the same side of the split, so the validation score is not inflated by near-duplicates.
- **Size:** 80,900 training molecules, 9,999 validation, 23,213 test.
- The dataset aggregates measurements from a dozen upstream sources; their individual licenses differ and are itemised in [LICENSES.md](LICENSES.md).

## Performance

**Headline validation MAE: 0.39627** at epoch 31. MAE is mean absolute error — the typical size of the miss, in each endpoint's own units. Lower is better.

Two things to understand about that headline number:

1. It is a **plain unweighted average across the 25 endpoints**, not weighted by how many molecules each endpoint has. Weighted by molecule count instead, the error is **0.3419**, which looks better only because the one very large endpoint (kinetic solubility, 6,916 molecules) happens to be an easy one. The unweighted figure is the more honest summary.
2. It is computed over **11,104 finite molecule-endpoint pairs** — most molecules have measurements for only a few of the 25 properties, so the matrix is sparse.

An independent prediction-only pass over the same validation split reproduced the aggregate as 0.39651 against the 0.39627 recorded during training. The 0.00024 difference is most likely GPU or featurisation nondeterminism; that has not been verified.

### Per-endpoint validation error

| endpoint | validation MAE | molecules scored | label mean | label std |
|---|---|---|---|---|
| `CL_microsome_human` | 0.319 | 453 | 4.41 | 0.60 |
| `CL_microsome_mouse` | 0.405 | 58 | 4.62 | 0.72 |
| `CL_microsome_rat` | 0.323 | 193 | 4.74 | 0.57 |
| `CL_total_dog` | 0.349 | 20 | 0.82 | 0.55 |
| `CL_total_human` | 0.509 | 51 | 0.54 | 0.89 |
| `CL_total_monkey` | 0.478 | 10 | 1.11 | 0.51 |
| `CL_total_rat` | 0.348 | 25 | 1.47 | 0.57 |
| `CYP2C8_inhibition` | 0.530 | 34 | 3.94 | 0.60 |
| `CYP2C9_inhibition` | 0.457 | 203 | 3.74 | 0.74 |
| `CYP2D6_inhibition` | 0.515 | 227 | 3.65 | 0.82 |
| `CYP3A4_inhibition` | 0.476 | 384 | 3.56 | 0.87 |
| `Dog_fraction_unbound_plasma` | 0.286 | 10 | -0.80 | 0.75 |
| `Human_fraction_unbound_plasma` | 0.322 | 225 | -1.03 | 0.69 |
| `Monkey_fraction_unbound_plasma` | 0.338 | 3 | -0.66 | 0.57 |
| `Rat_fraction_unbound_plasma` | 0.266 | 13 | -0.72 | 0.66 |
| `Papp_Caco2` | 0.390 | 563 | 0.62 | 0.76 |
| `Pgp_human` | 0.417 | 185 | 0.46 | 0.67 |
| `hERG_binding` | 0.477 | 479 | 3.63 | 0.95 |
| `LogD_pH_7.4` | 0.432 | 355 | 2.13 | 1.22 |
| `kinetic_logSaq` | 0.282 | 6916 | -4.39 | 0.73 |
| `thermo_logSaq` | 0.612 | 589 | -3.09 | 1.87 |
| `VDss_dog` | 0.299 | 20 | -0.02 | 0.52 |
| `VDss_human` | 0.351 | 53 | 0.02 | 0.69 |
| `VDss_monkey` | 0.400 | 10 | 0.23 | 0.54 |
| `VDss_rat` | 0.333 | 25 | 0.28 | 0.63 |

Total: 11104 finite molecule-endpoint pairs across 25 endpoints.

### How to read this table, and where it fails

The column that matters is not the MAE on its own — it is the MAE compared against **what you would get by ignoring the molecule entirely and always answering with the dataset average.** That lazy guess is the bar any model has to clear.

- **Clears the bar comfortably:** kinetic solubility (0.282 against a 0.613 lazy guess, over 6,916 molecules — by far the best-supported endpoint here), thermodynamic solubility, LogD, hERG binding, CYP3A4 and CYP2D6 inhibition, and the microsomal clearance endpoints.
- **Fails the bar — do not use these two:**
  - **`CYP2C8_inhibition`** — MAE 0.530 against a 0.459 lazy guess.
  - **`CL_total_monkey`** — MAE 0.478 against a 0.368 lazy guess.
  
  On these the model has learned nothing useful and performs worse than a constant. They are reported for completeness and should be ignored.
- **Statistically too thin to judge:** `Monkey_fraction_unbound_plasma` rests on **three** molecules. `Dog_fraction_unbound_plasma`, `CL_total_dog`, `CL_total_monkey`, `VDss_dog`, `VDss_monkey`, `Rat_fraction_unbound_plasma`, `CL_total_rat` and `VDss_rat` each rest on 10 to 25. Treat their MAEs as indicative at best.

In short: the solubility, lipophilicity and in-vitro endpoints are usable for triage. The in-vivo animal pharmacokinetic endpoints are not well enough supported to lean on.

## Units and direction

Per-endpoint units are documented in [docs/ADMET_LEGEND.md](docs/ADMET_LEGEND.md), taken row by row from the dataset's own README. Two caveats carried forward honestly:

- **Log base is not established in the source.** The dataset writes `log(...)` without specifying base 10 or natural log. The legend marks it as unestablished rather than guessing.
- **The `CL_microsome_*` unit is doubtful.** It is stated as `log(mL/min/kg)`, but label means of 4.41 to 4.74 do not sit plausibly in that unit. This should be resolved against the source publication before anyone relies on the absolute scale. Relative comparisons between molecules are unaffected.
- **Direction is not stated for any endpoint.** Neither the dataset nor the KERMT repo says whether higher or lower is better. The legend notes the usual field convention where one exists, clearly labelled as convention rather than source.

## How it was trained

Continued fine-tuning from the preceding checkpoint at a learning rate of 1e-6, on a single local NVIDIA GPU. The validation error by this point is nearly flat — the improvement from the previous checkpoint was 0.00045 — so further training at this rate is unlikely to help.

Inference settings must match training: features `rdkit_2d_normalized_cuik_molmaker`, with `--use_cuikmolmaker_featurization` and `--no_features_scaling`.


### A note on how little compute went into this

This checkpoint is **undertrained, deliberately and honestly.** It was fine-tuned over roughly a day or two on a single consumer GPU (an NVIDIA RTX 4070 Ti Super) in short local sessions, not on a cluster. The validation error had flattened at a learning rate of 1e-6 by the final epoch, which means this particular schedule had stopped paying off — it does not mean the model has reached the limit of what the data supports.

**If you have real compute, this is the obvious place to improve.** A longer run with a better learning-rate schedule, more epochs, and proper hyperparameter search would very likely beat 0.39627, and would especially help the endpoints that currently fail to beat the dataset mean. Treat these weights as a working baseline and a demonstration that the pipeline runs end to end, not as a well-trained model.

## License

The weights are released for **non-commercial research use.**

The reasoning, stated plainly: the training data is published under a GPL umbrella, and its subsets carry their own terms — one substantial block (covering all total-clearance, all volume-of-distribution, and most plasma protein binding endpoints) is **CC-BY-NC**, several others are **CC-BY-SA**, the CYP endpoints are **ODbL**, and one Caco-2 source lists no license at all. Whether dataset license terms propagate to a model trained on that data is genuinely unsettled, and nothing in the sources answers it.

So this is a **conservative choice, not legal advice.** Non-commercial research — academic, nonprofit, and individual study — is exactly what it is meant to permit. If you want to use this commercially, do your own diligence on the upstream data terms first.

Code in this repository is Apache 2.0. Full breakdown in [LICENSES.md](LICENSES.md).

## Acknowledgements

KERMT and its fine-tuning code are from NVIDIA Digital Biology, building on chemprop and cuik-molmaker. The dataset is the work of the Figshare authors cited above and the dozen upstream groups whose measurements it aggregates. See the [README acknowledgements](README.md#acknowledgements) for the full list.

---

*In honor of Cynthia Miller* 🩷💙
