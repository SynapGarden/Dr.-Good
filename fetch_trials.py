#!/usr/bin/env python3
"""Fetch clinical trials for ANY indication from ClinicalTrials.gov API v2.

Disease-agnostic: the condition and all search terms are inputs. Nothing about
any particular disease is hardcoded. The exact query and the retrieval date are
written alongside the data so the filtering is reproducible for any indication.

Usage:
  python fetch_trials.py --term "leptomeningeal" --term "neoplastic meningitis" --slug leptomeningeal
  python fetch_trials.py --term "pancreatic cancer" --slug pancreatic --field cond
  python fetch_trials.py --config runs/als.json
"""
import argparse, csv, json, sys, time, datetime, hashlib, collections
from pathlib import Path
import requests

API = "https://clinicaltrials.gov/api/v2/studies"
QUERY_FIELDS = ["cond", "term", "intr", "outc", "titles", "locn", "id", "spons", "patient"]


def fetch(terms, field="cond", status=None, agg=None, page_size=1000, session=None):
    """Return {nctId: study} for every term, de-duplicated by NCT ID."""
    s = session or requests.Session()
    studies, provenance = {}, []
    for term in terms:
        token, pages, n_before = None, 0, len(studies)
        while True:
            params = {f"query.{field}": term, "pageSize": page_size}
            if token:
                params["pageToken"] = token
            if status:
                params["filter.overallStatus"] = "|".join(status)
            if agg:
                params["aggFilters"] = agg
            r = s.get(API, params=params, timeout=90)
            r.raise_for_status()
            j = r.json()
            for st in j.get("studies", []):
                nct = st["protocolSection"]["identificationModule"]["nctId"]
                studies[nct] = st
            pages += 1
            token = j.get("nextPageToken")
            if not token:
                break
            time.sleep(0.2)
        provenance.append({
            "term": term, "query_field": f"query.{field}", "pages": pages,
            "new_unique_studies": len(studies) - n_before,
        })
    return studies, provenance


def flatten(nct, st):
    ps = st["protocolSection"]
    sm = ps.get("statusModule", {})
    dm = ps.get("designModule", {})
    return {
        "nct": nct,
        "title": ps.get("identificationModule", {}).get("briefTitle", ""),
        "status": sm.get("overallStatus", ""),
        "phase": "|".join(dm.get("phases", [])),
        "study_type": dm.get("studyType", ""),
        "allocation": dm.get("designInfo", {}).get("allocation", ""),
        "model": dm.get("designInfo", {}).get("interventionModel", ""),
        "interventions": "; ".join(
            f'{i.get("type","")}: {i.get("name","")}'
            for i in ps.get("armsInterventionsModule", {}).get("interventions", [])),
        "conditions": "; ".join(ps.get("conditionsModule", {}).get("conditions", [])),
        "enrollment": dm.get("enrollmentInfo", {}).get("count", ""),
        "enrollment_type": dm.get("enrollmentInfo", {}).get("type", ""),
        "start": sm.get("startDateStruct", {}).get("date", ""),
        "completion": sm.get("completionDateStruct", {}).get("date", ""),
        "hasResults": st.get("hasResults", ""),
        "sponsor": ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", ""),
        "url": f"https://clinicaltrials.gov/study/{nct}",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fetch trials for any indication.")
    ap.add_argument("--term", action="append", default=[],
                    help="Search term; repeat for synonyms. Results are unioned and de-duplicated.")
    ap.add_argument("--slug", help="Short name for this indication, used in filenames.")
    ap.add_argument("--field", default="cond", choices=QUERY_FIELDS,
                    help="Which ClinicalTrials.gov query field to search (default: cond).")
    ap.add_argument("--status", action="append",
                    help="Optional filter.overallStatus value; repeat to allow several.")
    ap.add_argument("--agg", help="Optional aggFilters string, e.g. results:with")
    ap.add_argument("--outdir", default=".", help="Where to write the run folder.")
    ap.add_argument("--keep-raw", action="store_true",
                    help="Also save each full study record under raw/.")
    ap.add_argument("--config", help="JSON file supplying any of the above keys.")
    a = ap.parse_args(argv)

    if a.config:
        cfg = json.loads(Path(a.config).read_text())
        for k, v in cfg.items():
            if not getattr(a, k, None):
                setattr(a, k, v)
    if not a.term:
        ap.error("at least one --term is required (or supply terms in --config)")
    slug = a.slug or "".join(c if c.isalnum() else "-" for c in a.term[0].lower()).strip("-")

    retrieved = datetime.datetime.now(datetime.timezone.utc)
    studies, provenance = fetch(a.term, a.field, a.status, a.agg)
    rows = [flatten(n, s) for n, s in sorted(studies.items())]

    out = Path(a.outdir) / f"{slug}_{retrieved:%Y-%m-%d}"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / f"trials_{slug}_{retrieved:%Y-%m-%d}.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["nct"])
        w.writeheader()
        w.writerows(rows)

    if a.keep_raw:
        raw = out / "raw"
        raw.mkdir(exist_ok=True)
        for n, s in studies.items():
            (raw / f"{n}.json").write_text(json.dumps(s, indent=1))

    with_results = [r for r in rows if r["hasResults"] is True or str(r["hasResults"]).lower() == "true"]
    manifest = {
        "indication_slug": slug,
        "search_terms": a.term,
        "query_field": f"query.{a.field}",
        "filter_overallStatus": a.status,
        "aggFilters": a.agg,
        "api_base": API,
        "retrieved_utc": retrieved.isoformat(),
        "unique_studies": len(rows),
        "studies_with_posted_results": len(with_results),
        "per_term": provenance,
        "csv": csv_path.name,
        "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "status_counts": dict(collections.Counter(r["status"] for r in rows)),
        "phase_counts": dict(collections.Counter(r["phase"] for r in rows)),
        "tool_versions": {"python": sys.version.split()[0], "requests": requests.__version__},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"{len(rows)} unique studies, {len(with_results)} with posted results")
    print(f"wrote {csv_path}")
    print(f"wrote {out/'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
