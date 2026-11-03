#!/usr/bin/env python3
"""C6 — enrichment: turn raw scraped text into high-signal filter flags
(visa / remote / equity / salary). Reads data/jobs.jsonl, writes
data/enriched_jobs.jsonl. Enrichment never deletes a row — it only tags."""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

def enrich_job(job):
    description = (job.get("description") or "").lower()
    title = (job.get("title") or "").lower()
    location = (job.get("location") or "").lower()

    # 1. Visa sponsorship engine (avoids the "NO sponsorship" trap)
    has_visa = False
    visa_keywords = ["sponsorship available", "visa sponsorship", "h-1b", "h1b",
                     "opt/cpt", "will sponsor", "tier 2", "sponsor visa"]
    if any(x in description for x in visa_keywords):
        if not any(t in description for t in ["no visa sponsorship", "cannot sponsor",
                                             "not able to sponsor", "without sponsorship",
                                             "no sponsorship"]):
            has_visa = True

    # 2. Remote integrity engine
    remote_type = "Onsite"
    if "remote" in title or "remote" in description or "remote" in location:
        remote_type = "Global Remote"
        if any(t in description for t in ["must reside in", "us citizens only",
                                         "uk residents only", "us only", "reside in"]):
            remote_type = "Geo-Fenced Remote"

    # 3. Equity + salary extractor
    equity_found = any(x in description for x in ["equity", "stock options", "shares", "rsus", "rsu"])
    salary_range = re.findall(r'\$\d{2,3},?\d{3}', description)

    job["flags"] = {
        "has_visa": has_visa,
        "remote_type": remote_type,
        "has_equity": equity_found,
        "salary_low": salary_range[0] if len(salary_range) > 0 else None,
        "salary_high": salary_range[1] if len(salary_range) > 1 else None,
    }
    return job

def main():
    inp = ROOT / "data/jobs.jsonl"
    outp = ROOT / "data/enriched_jobs.jsonl"
    n = visa = remote = geo = equity = sal = 0
    with inp.open() as f, outp.open("w") as g:
        for line in f:
            if not line.strip(): continue
            job = json.loads(line)
            enrich_job(job)
            g.write(json.dumps(job) + "\n")
            n += 1
            fl = job["flags"]
            visa += int(fl["has_visa"]); remote += int(fl["remote_type"] != "Onsite")
            geo += int(fl["remote_type"] == "Geo-Fenced Remote")
            equity += int(fl["has_equity"]); sal += int(fl["salary_low"] is not None)
    print("ENRICH_OK rows=%d visa=%d remote=%d geo_fenced=%d equity=%d salary=%d" %
          (n, visa, remote, geo, equity, sal))
    return 0

if __name__ == "__main__":
    sys.exit(main())
