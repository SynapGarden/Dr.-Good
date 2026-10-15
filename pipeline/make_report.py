import json, os, csv
B='/workspace/leptomeningeal/'
A=json.load(open(B+'stage_a_19_studies.json'))
T=json.load(open(B+'stage_b_targets.json'))
dd=list(csv.DictReader(open(B+'stage_c/diffdock_results.csv')))
bz=list(csv.DictReader(open(B+'stage_c/boltz2_results.csv')))
kp=B+'stage_d/predictions_lmd_v11.csv'
K=list(csv.DictReader(open(kp))) if os.path.exists(kp) else []

# headline outcomes, each quoted from the opened primaryResults above
HEAD={
"NCT00445965":"67/78 alive at 6 months; 31 complete responses, 8 stable, 21 progressed, 18 not evaluable",
"NCT00450866":"CNS progression-free at 3 months: 12 participants (Group A), 2 (Group B)",
"NCT00523939":"Response Rate: no value posted in the results module",
"NCT00801216":"2-year event-free survival: 16 participants (of 40 enrolled, 38 at risk)",
"NCT00924820":"CSF response rate 93% of participants; median time to progression 3 weeks",
"NCT00964743":"Safety-only readout: adverse events in 2 of 2 participants",
"NCT00992602":"Survival free of neurological progression: 6 weeks",
"NCT01325207":"Best response: 6 partial responses, 18 stable, 0 complete; 1 dose-limiting toxicity at 80 mg",
"NCT01596127":"Response rate 0% at 2 weeks",
"NCT02336451":"ORR by arm 35.7 / 30.0 / 50.0 / 59.1%; leptomeningeal arm (Arm 5) 16.7%",
"NCT02616393":"Brain-met ORR 31.3% overall; leptomeningeal cohort (B) ORR 0%",
"NCT02939300":"44% of participants alive at 3 months",
"NCT02948751":"Diagnostic device: 3 participants with LM detected (of 14); no treatment effect measured",
"NCT03091478":"At 12 weeks: 2 complete, 1 partial, 2 stable, 8 progressive",
"NCT03275402":"3-year overall survival rate 0.65",
"NCT03501979":"Survival after starting treatment: 6 participants (of 17)",
"NCT04250545":"MTD/RP2D: NA (not established); overall responses 1 + 0 + 1 participants across dose levels",
"NCT04420598":"Cohort 1 16-week PFS: 1 of 8; ORR cohorts 2/3/4: 7, 5, 3 responders",
"NCT04460937":"Maximum tolerated dose 200 mg adavosertib with radiation",
}

import re as _re
_ROLLUP=_re.compile(r'(^|\b)(all subjects|all participants|all patients|all cohorts|overall|total)(\b|$)', _re.I)

def _pick_rows(rows):
    """Return the rows to aggregate. If CT.gov posted an all-subjects rollup
    group, use ONLY that row; summing it with the per-cohort rows double-counts."""
    roll=[r for r in rows if _ROLLUP.search(r.get('group',''))]
    if len(roll)==1:
        return roll, True
    if len(roll)>1:
        raise ValueError(f"ambiguous: {len(roll)} rollup-like AE groups: {[r.get('group') for r in roll]}")
    return rows, False

def ae(s):
    rows=s.get('adverseEventSummary') or []
    if not rows: return "not posted"
    use, rolled=_pick_rows(rows)
    d=sum(r['deaths'] for r in use if r.get('deaths') is not None)
    dk=any(r.get('deaths') is None for r in use)
    se=sum(r['seriousAffected'] for r in use if r.get('seriousAffected') is not None)
    sk=any(r.get('seriousAffected') is None for r in use)
    if dk and d==0 and sk and se==0: return "not posted"
    at=sum(r.get('deathsAtRisk') or 0 for r in use)
    enr=(s.get('enrollment') or {}).get('count')
    # Guard: deaths can never exceed participants at risk or enrolment.
    if at and d>at:
        raise ValueError(f"{s['nct']}: deaths {d} exceed at-risk {at}")
    if enr and d>enr:
        raise ValueError(f"{s['nct']}: deaths {d} exceed enrolment {enr}")
    den=f" of {at}" if at else ""
    return f"serious AEs {se}{den}{'+ (some groups not posted)' if sk else ''}; deaths {d if not dk else str(d)+'+ (some groups not posted)'}{den}"

L=[]
w=L.append
w("# Leptomeningeal disease — evidence-first pipeline report")
w("")
w("Run date: 2026-10-15 (ET). Stages A-C complete; Stage D (KERMT ADMET) status noted below.")
w("")
w("## 1. What this is, in plain words")
w("")
w("**Leptomeningeal disease (LMD)** is what happens when cancer spreads into the thin, fluid-filled lining that wraps the brain and spinal cord. Cancer cells float in the cerebrospinal fluid rather than sitting in one lump, so they are hard to reach with drugs and hard to measure. It is uncommon, it is serious, and it is badly under-studied.")
w("")
w("**What this run did.** First it pulled every leptomeningeal study from ClinicalTrials.gov (219 found) and kept the **19 that have actual results posted** — those are the only ones with real patient outcome numbers to stand on. Then, for the drugs in those trials that are small molecules, it found the protein each one acts on and a real experimental crystal structure of that protein, generated close chemical relatives (\"cousins\") with MolMIM, docked everything with DiffDock, scored binding twice with Boltz-2, and finally ran the owner's locally trained KERMT model to predict absorption and safety properties.")
w("")
w("**What this cannot show.** Nothing here is evidence that any drug works. The trial numbers come from small, uncontrolled studies. The model numbers are computer guesses about chemistry, not about patients. No new treatment is being proposed; this is a map of what is known plus hypotheses to test in a lab.")
w("")
w("## 2. Trial evidence — the 19 studies with posted results")
w("")
w("| NCT | Study | Phase | Drug(s) | Design | Enrolled | Headline posted outcome | Serious AEs / deaths | Modality |")
w("|---|---|---|---|---|---|---|---|---|")
for s in sorted(A,key=lambda x:-(x['enrollment'].get('count') or 0)):
    ph=', '.join(p.replace('PHASE','P') for p in (s.get('phase') or [])) or 'not stated'
    drugs=', '.join(s.get('smallMoleculeDrugs') or []) or '—'
    w(f"| {s['nct']} | {s['briefTitle'][:60]} | {ph} | {drugs} | {s.get('designSummary')} | {s['enrollment'].get('count')} | {HEAD[s['nct']]} | {ae(s)} | {s.get('modality')} |")
w("")
w("## 3. Read this before the table above")
w("")
w("> **None of the 19 studies had a control arm.** Every one is single-arm or several non-randomised cohorts of the same drug. That means the posted outcomes describe how these particular patients did — they do **not** show that any drug beat another option, or beat no treatment at all.")
w(">")
w("> **Most studies were tiny.** Enrollments include 2, 3, 4, 4, 4, 13, 14, 17, 18, 20 and 22 participants. At those sizes a single patient moves the headline number by tens of percent. Only NCT02336451 (ceritinib, n=156) is large enough for its response rates to mean much, and even there the leptomeningeal arm was 16.7%.")
w(">")
w("> Deaths in these tables are mostly from the cancer itself, not from the drug; these are late-stage patients. Do not read a death count as a drug safety signal without the full record.")
w("")
w("## 4. Molecule hypotheses — structure, docking, affinity, ADMET")
w("")
TB={t['drug']:t for t in T}
ddall={(r['drug'],r['candidate']):r for r in dd if r.get('status')=='success'}
sel={(r['drug'],r['role']):r['candidate'] for r in bz}
ddm={}
for (drg,role),cand in sel.items():
    k=(drg,cand)
    if k in ddall: ddm[(drg,role)]=ddall[k]
bzm={}
for r in bz:
    bzm.setdefault((r['drug'],r['role']),{})[r['run']]=r
w("Boltz-2 `affinity_pred_value` is log-scale: **lower = stronger predicted binding**. `binding_probability` is the model's own 0-1 chance the pair binds at all. DiffDock confidence is pose plausibility, not affinity.")
w("")
w("| Drug | Target | PDB (res. Å) | Bound ligand | DiffDock drug | DiffDock best cousin | Boltz-2 drug aff r1/r2 | drug prob r1/r2 | cousin aff r1/r2 | cousin prob r1/r2 | Rank stable | Evidence note |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|")
weak={'sapanisertib','tesevatinib','capecitabine'}
for t in T:
    d=t['drug']
    dr=ddm.get((d,'drug')); co=ddm.get((d,'cousin'))
    bd=bzm.get((d,'drug'),{}); bc=bzm.get((d,'cousin'),{})
    f=lambda x: f"{float(x):.4f}" if x not in (None,'') else 'missing'
    if not dr:
        note='not eligible for the molecule models — '+str(t.get('bound_ligand') or t.get('target'))
    elif d in weak:
        note='weaker — drug not present in the structure'
    else:
        note='drug co-crystallized'
    if d=='etoposide': note+='; **rank flipped between repeats — no ordering claimed**; real target is protein+DNA, only protein modelled'
    stab=(bd.get('1',{}).get('rank_stable') or 'missing')
    w(f"| {d} | {t['target']} | {t['pdb']} ({t.get('resolution_A')}) | {t.get('bound_ligand')} | {f(dr['diffdock_confidence']) if dr else 'missing'} | {f(co['diffdock_confidence']) if co else 'missing'} ({co['candidate'].split('_')[-1] if co else '—'}) | {f(bd.get('1',{}).get('affinity_pred_value'))} / {f(bd.get('2',{}).get('affinity_pred_value'))} | {f(bd.get('1',{}).get('binding_probability'))} / {f(bd.get('2',{}).get('binding_probability'))} | {f(bc.get('1',{}).get('affinity_pred_value'))} / {f(bc.get('2',{}).get('affinity_pred_value'))} | {f(bc.get('1',{}).get('binding_probability'))} / {f(bc.get('2',{}).get('binding_probability'))} | {stab} | {note} |")
w("")
w("Two candidates failed DiffDock outright and are reported as failed, not substituted: `telaglenastat_cousin_2` and `tesevatinib_cousin_2` (service error: \"Fail to read ligand molecule description\").")
w("")
w("### KERMT ADMET (Stage D)")
w("")
if K:
    cols=[c for c in K[0].keys() if c not in ('name','role','target','smiles')]
    w("Checkpoint: v11 epoch-31, val MAE 0.39627. Values are in the model's own units (several are log-scale), rounded to 3 decimals.")
    w("")
    w("| Molecule | role | "+" | ".join(cols)+" |")
    w("|---|---|"+"---|"*len(cols))
    for r in K:
        def fmt(v):
            try: return f"{float(v):.3f}"
            except: return v if v else 'missing'
        w(f"| {r['name']} | {r.get('role','')} | "+" | ".join(fmt(r[c]) for c in cols)+" |")
else:
    w("> **Stage D did not run.** The KERMT model has no hosted API — it needs the owner's local GPU machine **Mothership2** and the v11 checkpoint on its `Z:` drive. Mothership2 was offline (not connected to the Grok Bot desktop app) for the whole of this run, so no ADMET numbers exist for this set. Per the pipeline's own rules, nothing was substituted or estimated. The run can be completed in minutes once Mothership2 is online.")
w("")
w("## 5. Honest readout")
w("")
w("**Most coherent across trial evidence + docking + affinity:**")
w("")
w("- **Ceritinib / ALK (NCT02336451).** The only study in the set with real size (n=156) and real response rates, and the chemistry agrees: ceritinib docks into its own crystal structure (4MKC), and Boltz-2 gives it the strongest numbers in the set after methotrexate (affinity -1.406 / -1.352, binding probability 0.828 in both repeats), beating its cousin in both repeats. Caveat that matters: the **leptomeningeal arm specifically was 16.7%**, far below the brain-met arms. So ALK is a coherent target; leptomeningeal benefit is not demonstrated.")
w("- **Methotrexate / DHFR.** The strongest and most reproducible model result in the set — binding probability 0.992 in both repeats, affinity -2.063 / -2.219. This is also the least surprising: methotrexate-DHFR is one of the best-characterised drug-target pairs in medicine, so this mostly tells us the model behaves sensibly. Clinically it appears only inside multi-drug regimens here (NCT00801216, NCT00992602), so no single-drug conclusion can be drawn.")
w("- **Adavosertib / WEE1.** Clean chemistry (co-crystal 5V5Y, affinity -2.125 / -2.219, probability 0.859 / 0.875, stable). But the trial is n=4 and reports only a maximum tolerated dose — there is no efficacy evidence at all.")
w("")
w("**Weak or discordant:**")
w("")
w("- **Tesevatinib / EGFR.** Strong model numbers (affinity -1.680 / -1.750, probability ~0.72) against a **0% response rate** in the leptomeningeal cohort of NCT02616393, with 12 of 20 patients dying. This is the clearest reminder in the whole report that good binding predictions do not translate into patient benefit. The structure evidence is also weaker — 1XKK does not contain tesevatinib.")
w("- **Etoposide / topoisomerase II alpha.** Rank flipped between the two Boltz-2 repeats, so by the pipeline's own rule **no ordering is claimed**. Physically it is the worst-modelled case too: etoposide really acts on a protein-plus-DNA complex, and only the protein was modelled.")
w("- **Sapanisertib / mTOR and capecitabine / thymidylate synthase.** Both dock into structures that do not contain the drug, and both score weakly (sapanisertib probability 0.47 / 0.44; capecitabine 0.41 / 0.38). Capecitabine is additionally a prodrug — the active species is its metabolite, so docking the parent molecule is the wrong question.")
w("- **Telaglenastat, tucatinib, sorafenib, patupilone.** Middling binding probabilities (0.13-0.56) and trials of 2-22 patients. Nothing here supports a conclusion either way.")
w("")
w("In every case the cousins MolMIM invented scored worse than the real drug (except the etoposide pair, where no ordering is claimed). That is the expected, reassuring result: these are optimised approved drugs and the cousins are untested machine edits. **No cousin in this run is a lead.**")
w("")
w("## 6. Limitations and the real next step")
w("")
w("- No control arms anywhere in the 19 trials; most enrolled single digits. Posted outcomes are descriptive only.")
w("- Docking and affinity models score a static protein pocket. They do not model the blood-brain or blood-CSF barrier, which is the single biggest obstacle in leptomeningeal disease — a drug can bind perfectly and never reach the cerebrospinal fluid.")
w("- Three drugs were docked into structures that do not contain them (sapanisertib, tesevatinib, capecitabine); one target (topoisomerase II alpha) was modelled without its DNA.")
w("- Antibodies, radiolabelled antibodies, antibody-drug conjugates, cell therapy, radiation and the diagnostic device cannot be scored by these molecule models at all, and several of the 19 trials are exactly those.")
w("- **The next step is not more compute.** It is a wet-lab assay: a binding or cell-viability measurement on the drug-target pairs flagged as coherent, and crucially a CSF-penetration measurement. No amount of additional modelling can substitute for that.")
w("")
w("---")
w("")
w("**Model scores are hypotheses only — not clinical proof of efficacy or safety.**")
open(B+'REPORT.md','w').write("\n".join(L)+"\n")
print("wrote", B+'REPORT.md', len(L), "lines; KERMT rows:", len(K))
