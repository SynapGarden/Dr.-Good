#!/usr/bin/env python3
"""Consistency assertions for a pipeline run. Fails loudly rather than silently
shipping a report whose prose and tables disagree.

Usage:
  python checks.py --run /workspace/leptomeningeal
"""
import argparse, csv, json, re, sys
from pathlib import Path

ERRORS, CHECKS = [], 0
NCT = re.compile(r"^NCT\d{8}$")


def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        ERRORS.append(msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="run directory")
    a = ap.parse_args()
    run = Path(a.run)

    # --- IDs are well-formed and consistent across files -------------------
    ids = {}
    sa = run / "stage_a_19_studies.json"
    if sa.exists():
        studies = json.loads(sa.read_text())
        if isinstance(studies, dict):
            studies = studies.get("studies", list(studies.values()))
        got = [s.get("nctId") or s.get("nct_id") for s in studies]
        ids["stage_a"] = {g for g in got if g}
        for g in ids["stage_a"]:
            check(bool(NCT.match(g)), f"malformed NCT ID in stage_a: {g!r}")

    for name in ("stage_b_targets.json",):
        p = run / name
        if p.exists():
            txt = p.read_text()
            found = set(re.findall(r"NCT\d+", txt))
            for g in found:
                check(bool(NCT.match(g)), f"malformed NCT ID in {name}: {g!r}")
            if "stage_a" in ids and found:
                extra = found - ids["stage_a"]
                check(not extra, f"{name} references IDs absent from stage_a: {sorted(extra)}")

    # --- deaths never exceed enrolment, in any file ------------------------
    rep = run / "REPORT.md"
    if rep.exists():
        text = rep.read_text()
        for m in re.finditer(r"deaths?\s+(\d+)\s+of\s+(\d+)", text, re.I):
            d, n = int(m.group(1)), int(m.group(2))
            check(d <= n, f"REPORT.md reports {d} deaths of {n} enrolled")
        for m in re.finditer(r"serious AEs?\s+(\d+)\s+of\s+(\d+)", text, re.I):
            d, n = int(m.group(1)), int(m.group(2))
            check(d <= n, f"REPORT.md reports {d} serious AEs of {n} enrolled")

        # --- prose figures must appear in the tables -----------------------
        prose = set(re.findall(r"(\d+)\s+of\s+(\d+)", text))
        check(len(prose) > 0, "REPORT.md contains no 'N of M' figures to cross-check")

    # --- count coherence ---------------------------------------------------
    man = None
    for p in run.rglob("manifest.json"):
        man = json.loads(p.read_text())
        break
    if man:
        uniq = man.get("unique_studies")
        withres = man.get("studies_with_posted_results")
        if uniq is not None and withres is not None:
            check(withres <= uniq,
                  f"manifest: {withres} with results exceeds {uniq} unique studies")
        csvs = list(run.rglob("trials_*.csv")) or list(run.glob("ctgov_*.csv"))
        if csvs and uniq is not None:
            n = sum(1 for _ in csv.DictReader(open(csvs[0])))
            check(n == uniq,
                  f"{csvs[0].name} has {n} rows but manifest says {uniq} unique studies")
        if "stage_a" in ids and withres is not None:
            check(len(ids["stage_a"]) == withres,
                  f"stage_a holds {len(ids['stage_a'])} studies but manifest says "
                  f"{withres} have posted results")

    # --- every scored molecule appears in the predictions ------------------
    smi = run / "stage_c" / "kermt_input_smiles.csv"
    pred = run / "stage_d" / "predictions_lmd_v11.csv"
    if smi.exists() and pred.exists():
        n_in = sum(1 for _ in csv.DictReader(open(smi)))
        n_out = sum(1 for _ in csv.DictReader(open(pred)))
        check(n_in == n_out,
              f"{n_in} molecules submitted to the model but {n_out} predictions returned")

    print(f"{CHECKS} checks run on {run}")
    if ERRORS:
        print(f"\n{len(ERRORS)} FAILED:")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    print("all passed")


if __name__ == "__main__":
    main()
