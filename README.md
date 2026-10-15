# Dr. Good — a disease-agnostic clinical evidence pipeline

**Dr. Good** turns a disease name into a grounded, citable evidence package: it pulls every registered clinical trial for that indication from ClinicalTrials.gov, deep-reads the ones with posted results, identifies the molecular targets those trials actually named, and then runs a molecular-modelling layer over the drugs involved to check that the pipeline behaves sensibly on chemistry we already understand. The indication is always an input parameter, never hardcoded. The run included here as a **worked example** covers *leptomeningeal disease* (LMD) and is dated 2026-10-15 — it is a demonstration of the pipeline, not the product.

The **trial curation is the primary output.** The molecular modelling exists to validate that the pipeline is wired up correctly and produces plausible results on known drugs. It is not a drug discovery engine.

## What this is not

- It does **not** prove that any treatment works. Every model score is a hypothesis.
- It does **not** replace reading the trial record. Every number it reports is traced back to a record that was actually retrieved; where a record does not contain something, the pipeline says so rather than filling the gap.
- It does **not** predict whether a drug crosses into the brain or spinal fluid. No endpoint in the model measures that. For a disease like LMD, that is the decisive property, and this pipeline cannot speak to it.
- It is **not** a safety assessment. See [MODEL_CARD.md](MODEL_CARD.md).

## The five stages

| Stage | What happens | Needs |
|---|---|---|
| **A** | Pull and deep-read trials from ClinicalTrials.gov API v2 | nothing — free and keyless |
| **B** | Find experimental protein structures in the RCSB Protein Data Bank for each target the trials named | nothing |
| **C** | Generate close chemical analogs (MolMIM or GenMol), dock them against the structure (DiffDock), and score binding twice (Boltz-2) | `NGC_API_KEY` |
| **D** | Predict 25 absorption/distribution/metabolism/excretion/toxicity properties with the locally fine-tuned KERMT model | a local NVIDIA GPU |
| **E** | Combine everything into one report with citations | nothing |

Stages A, B and E are free. Stage C needs a free NVIDIA key. **Stage D needs a local GPU** — there is no hosted option, so most users will run A through C and stop. That is still a complete evidence package.

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env    # then fill in your NVIDIA key
python fetch_trials.py --term "leptomeningeal" --term "neoplastic meningitis" --slug leptomeningeal
```

This writes `runs/<slug>_<date>/trials_<slug>_<date>.csv` plus a `manifest.json` recording the exact search terms, query field, filters, retrieval timestamp, study counts and a SHA-256 of the CSV, so anyone can reproduce or audit the filtering.

## Changing the indication

The disease is a parameter. Nothing else changes:

```bash
# A different cancer
python fetch_trials.py --term "glioblastoma" --slug glioblastoma

# Several terms, unioned and de-duplicated by NCT ID
python fetch_trials.py --term "amyotrophic lateral sclerosis" --term "motor neuron disease" --slug als

# Search intervention names instead of conditions
python fetch_trials.py --term "pembrolizumab" --field intr --slug pembrolizumab

# Only trials with posted results
python fetch_trials.py --term "sickle cell disease" --slug sickle --agg "results:with"
```

`--field` accepts `cond`, `term`, `intr`, `outc`, `titles`, `locn`, `id`, `spons` or `patient`. Downstream stages read the manifest, so once Stage A runs for a new indication the rest of the pipeline follows the same path.

## Where to get keys

- **ClinicalTrials.gov** — no key needed. The [API v2](https://clinicaltrials.gov/data-api/api) is free and open.
- **NVIDIA `NGC_API_KEY`** — required for Stage C. Get one free at [build.nvidia.com](https://build.nvidia.com/).
- **Model weights** — the fine-tuned KERMT checkpoint is hosted on Hugging Face; see [MODEL_CARD.md](MODEL_CARD.md) for the link and license.

Keys go in `.env` or your environment. **Never commit them.** `.env` is gitignored.

## Run it as a Grok Bot

The easiest way to use this is the shareable Grok Bot template. It wraps the whole pipeline in a chat interface: you ask for a disease, and it runs the stages and reports back. Keys are entered through a masked secret window in the chat — they are never pasted into a message, a file, or this repo.

TEMPLATE_LINK_HERE

## Limitations, honestly

- **Stage D needs a local NVIDIA GPU.** Most users cannot run it.
- **No CSF or blood-brain penetration is modelled.** For central nervous system diseases this is the property that matters most, and the pipeline is silent on it.
- **The model is undertrained.** The shipped checkpoint was fine-tuned for about a day or two on a single consumer GPU (RTX 4070 Ti Super). It is a working baseline, not a well-trained model — with real compute and a proper learning-rate schedule it should go meaningfully further. See [MODEL_CARD.md](MODEL_CARD.md).
- **Two model endpoints are unreliable.** CYP2C8 inhibition and total clearance in monkey perform *worse* than simply guessing the dataset average. Do not use them. Details in [MODEL_CARD.md](MODEL_CARD.md).
- **Several endpoints rest on tiny validation sets** — monkey plasma protein binding has three molecules. Their error estimates mean very little.
- **Docking and binding scores are not clinical evidence.** In the LMD worked example, one drug scored well on every model and had a posted 0% response rate in its leptomeningeal cohort. That contrast is kept in the report on purpose.
- **Trial registries are incomplete.** Posted results are the exception, not the rule, and small single-arm studies dominate rare indications.

## Purpose and guardrails

This project exists to help heal people and reduce suffering. The operating policy is in [POLICY.md](POLICY.md): never design or improve toxins, bioweapons or pathogens; study toxicity only in order to avoid it; prefer unmet, neglected and rare diseases; and treat honesty as part of safety — never invent a number or overstate what a model shows. A score is a hypothesis, not clinical proof.

## Acknowledgements

This pipeline is assembled almost entirely from other people's work, generously made public. With thanks to:

- **[ClinicalTrials.gov](https://clinicaltrials.gov/)** and the U.S. National Library of Medicine, for the trial registry and the free, keyless API v2 that Stage A depends on entirely.
- **[NVIDIA BioNeMo](https://www.nvidia.com/en-us/clara/bionemo/)** and the hosted NIM microservices at [build.nvidia.com](https://build.nvidia.com/), for the whole of Stage C:
  - **MolMIM** — controlled molecular generation, used to produce close analogs under a similarity constraint.
  - **GenMol** — the alternative generator for the same step.
  - **DiffDock** — diffusion-based molecular docking of each candidate into the experimental structure.
  - **Boltz-2** — structure and binding-affinity prediction, run twice per candidate so that unstable rankings are visible rather than hidden.
- **[KERMT](https://github.com/NVIDIA-Digital-Bio/kermt)** (NVIDIA Digital Biology), the chemical pretrained model and multitask fine-tuning code behind Stage D, which also builds on **chemprop** (Jin, Swanson *et al.*) and **cuik-molmaker**.
- The authors of the multitask ADMET dataset, *"Datasets for 'Multitask finetuning and acceleration of chemical pretrained models for small molecule drug property prediction'"*, [Figshare DOI 10.6084/m9.figshare.30350548.v2](https://doi.org/10.6084/m9.figshare.30350548.v2), and every upstream group whose measurements it aggregates.
- **[RCSB Protein Data Bank](https://www.rcsb.org/)** and the wwPDB, for the experimental structures used in Stage B — real crystallography, not predictions.
- **[PubChem](https://pubchem.ncbi.nlm.nih.gov/)**, for canonical structures and identifiers.
- **[ChEMBL](https://www.ebi.ac.uk/chembl/)** (EMBL-EBI), for target annotation.
- **[DailyMed](https://dailymed.nlm.nih.gov/)** and **[openFDA](https://open.fda.gov/)**, for approved drug labels, which is how targets are confirmed rather than guessed.
- **[RDKit](https://www.rdkit.org/)**, for cheminformatics throughout.

Above all, thanks to the patients who enrolled in these trials, and the investigators who posted their results. Posted results are what make an evidence pipeline possible at all.

## License

Code is Apache 2.0. Model weights are released for **non-commercial research use** because the training data contains a non-commercial subset. Full detail and reasoning in [LICENSES.md](LICENSES.md).

---

*In honor of Cynthia Miller* 🩷💙
