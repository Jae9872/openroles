#!/usr/bin/env python3
"""C1 — public board ingestion. Every job row carries source_url + fetched_at.
Only public ATS JSON APIs (Greenhouse/Ashby). No paywalled/scraped data."""
import json, sys, time, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

ADAPTERS = {
    "greenhouse": lambda s: ("https://boards-api.greenhouse.io/v1/boards/%s/jobs" % s,
        lambda d: [ (j, j.get("updated_at") or "") for j in d.get("jobs", []) ]),
    "ashby": lambda s: ("https://api.ashbyhq.com/posting-api/job-board/%s" % s,
        lambda d: [ (j, j.get("publishedAt") or "") for j in d.get("jobs", []) ]),
}

def fetch(slug, source):
    url, extract = ADAPTERS[source](slug)
    req = urllib.request.Request(url, headers={"User-Agent": "openroles-ingest/0.1 (+public-boards; contact: repo)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        d = json.load(r)
    raw = extract(d)
    out = []
    for j, posted in raw:
        title = (j.get("title") or "").strip()
        link = j.get("absolute_url") or j.get("jobUrl") or ""
        loc = j.get("location") if isinstance(j.get("location"), str) else (j.get("location") or {}).get("name", "")
        if not title or not link:
            continue
        out.append({"title": title, "company_slug": slug, "source": source,
                    "location": loc, "url": link, "posted_at": posted,
                    "source_url": "https://%s" % ("/".join(url.split("/")[2:4])),
                    "fetched_at": NOW})
    return out

def main():
    smoke = "--smoke" in sys.argv
    seed = json.loads((ROOT / "data/companies.json").read_text())
    rows, ok = [], 0
    for c in seed:
        try:
            jobs = fetch(c["slug"], c["source"])
            rows += jobs
            ok += 1
        except Exception as e:
            print("FETCH_FAIL %s: %s" % (c["slug"], str(e)[:80])) 
            if smoke: return 1
    stamp = {"generated_at": NOW, "companies_ok": ok, "jobs": len(rows)}
    (ROOT / "data").mkdir(exist_ok=True)
    target_jobs = (ROOT / "data/smoke_jobs.jsonl") if smoke else (ROOT / "data/jobs.jsonl")
    target_jobs.write_text("".join(json.dumps(r) + "\n" for r in rows))
    if not smoke:
        (ROOT / "data/meta.json").write_text(json.dumps(stamp, indent=1))
    ok_all = ok >= 2 and len(rows) > 0
    print("SMOKE_OK n_jobs=%d companies=%d fetched_at=%s probe=%s" % (len(rows), ok, NOW, target_jobs.name) if ok_all else "SMOKE_FAIL")
    return 0 if ok_all else 1

if __name__ == "__main__":
    sys.exit(main())
