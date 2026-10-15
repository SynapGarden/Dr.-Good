# Licensing

Three different things in this project carry three different licenses. This page says what applies where, and is honest about what is unresolved.

## 1. The code in this repository — Apache License 2.0

See [LICENSE](LICENSE). Use it, modify it, redistribute it, commercially or not, with attribution.

## 2. Upstream code we build on

- **KERMT** (NVIDIA Digital Biology) — Apache License 2.0, Copyright 2025 NVIDIA Corporation. The KERMT license file also carries MIT notices for:
  - Copyright (c) 2021 Tencent AI Lab
  - Copyright (c) 2020 Wengong Jin, Kyle Swanson *et al.* (chemprop)
- **cuik-molmaker** 0.2 — Apache License 2.0.
- **RDKit** — BSD 3-Clause.

## 3. The training data — a GPL umbrella over mixed subsets

The multitask ADMET dataset ([Figshare DOI 10.6084/m9.figshare.30350548.v2](https://doi.org/10.6084/m9.figshare.30350548.v2)) states its overall license as **GPL**, and its own `LICENSE.txt` adds: *"This dataset is released under the GPL license. Data subsets are subject to their original license as specified below."*

Those subsets are not uniform:

| Subset | License | Endpoints affected |
|---|---|---|
| Iwata 2022 | **CC-BY-NC** | all `CL_total_*`, all `VDss_*`, dog/monkey/rat plasma protein binding, part of human |
| Sources 1, 4, 6, 7, 8 | **CC-BY-SA** | microsomal clearance, Caco-2 permeability, Pgp, hERG, LogD |
| Source 3 (PubChem) | **ODbL** | the CYP inhibition endpoints |
| Source 9 | ODbL and CC-BY-SA | — |
| Sources 10, 11 | **CC-BY** | solubility |
| Source 12 | MIT | — |
| Source 5 (Falcon-Cano, Caco-2) | **none listed** | part of Caco-2 permeability |

## 4. The model weights — non-commercial research use

Because a substantial part of the training data is **CC-BY-NC**, commercial use of the resulting weights is ruled out. Several other parts are share-alike, and a GPL umbrella sits over the whole dataset.

**What is unresolved:** whether dataset license terms propagate to a model trained on that data is an open legal question. The sources do not answer it, and neither do we. Releasing the weights for non-commercial research use is a **conservative choice made in good faith, not legal advice.** It is deliberately the most permissive label we were confident was safe.

Academic, nonprofit and individual research use is exactly what this is intended to allow. If you want to use the weights commercially, do your own diligence on the upstream terms first.

## 5. The clinical trial data

Records retrieved from [ClinicalTrials.gov](https://clinicaltrials.gov/) are U.S. government public data. This repository ships the retrieval code and a manifest, not a redistributed copy of the registry — anyone can regenerate the data from the recorded query.
