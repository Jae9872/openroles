#!/usr/bin/env python3
"""Fetch per-job descriptions from public ATS detail endpoints so the
enrichment engine has real text to mine (visa/remote/equity/salary)."""
import json, re, time, urllib.request, pathlib, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOBS = ROOT / "data/jobs.jsonl"

def strip_html(s):
    if not s: return ""
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def detail_url(j):
    slug = j.get("company_slug") or j.get("company")
    jid = j.get("id")
    src = (j.get("source") or j.get("ats") or "").lower()
    if not jid:
        # recover posting id from the public URL tail (ashby/lever embed it)
        url = j.get("url") or ""
        tail = url.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
        if tail and tail != slug: jid = tail
    if not slug or not jid: return None, src
    if src == "greenhouse":
        return "https://boards-api.greenhouse.io/v1/boards/%s/jobs/%s" % (slug, jid), src
    if src == "ashby":
        return "https://api.ashbyhq.com/posting-api/job-board/%s/posting/%s" % (slug, jid), src
    if src == "lever":
        return "https://api.lever.co/v0/postings/%s/%s?mode=json" % (slug, jid), src
    return None, src

def fetch_one(j):
    url, src = detail_url(j)
    if not url: return j
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "openroles-enrich/0.1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
    except Exception:
        return j
    desc = ""
    if src == "greenhouse":
        desc = strip_html(d.get("content") or d.get("description") or "")
    elif src == "ashby":
        desc = strip_html(d.get("descriptionHtml") or d.get("descriptionPlain") or "")
    elif src == "lever":
        if isinstance(d, dict):
            desc = strip_html(d.get("descriptionPlain") or d.get("description") or "")
        elif isinstance(d, list) and d:
            desc = strip_html(d[0].get("descriptionPlain") or d[0].get("description") or "")
    if desc:
        j["description"] = desc
    return j

def main():
    jobs = [json.loads(l) for l in JOBS.read_text().splitlines() if l.strip()]
    todo = [j for j in jobs if not j.get("description")]
    print("DESCRIPTION_FETCH: total=%d need=%d" % (len(jobs), len(todo)))
    if not todo:
        print("DESCRIPTION_FETCH_OK already_complete"); return 0
    with ThreadPoolExecutor(max_workers=30) as ex:
        futs = {ex.submit(fetch_one, j): j for j in todo}
        done = 0
        for f in as_completed(futs):
            done += 1
            if done % 200 == 0:
                print("  progress %d/%d" % (done, len(todo)), flush=True)
    filled = sum(1 for j in jobs if j.get("description"))
    JOBS.write_text("\n".join(json.dumps(j) for j in jobs) + "\n")
    print("DESCRIPTION_FETCH_OK filled=%d/%d" % (filled, len(jobs)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
