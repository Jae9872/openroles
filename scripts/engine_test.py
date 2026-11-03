#!/usr/bin/env python3
"""C2 — freshness engine, self-test on synthetic fixtures (no network):
dedupe by URL-hash, purge rows older than 30 days, provenance required."""
import json, datetime, pathlib, sys

ROW = dict(title="Eng", company_slug="demo", source="greenhouse",
           location="NYC", url="https://x/y", posted_at="2026-11-01")

def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        k = r["url"]
        if k not in seen:
            seen.add(k); out.append(r)
    return out

def posted_dt(r):
    for field in ("updated_at", "posted_at"):
        v = r.get(field) or ""
        if v:
            try:
                d = v.replace("Z", "").split("T")[0]
                return datetime.date.fromisoformat(d)
            except Exception:
                pass
    return None

def purge_stale(rows, days=30, today=None):
    today = today or datetime.date.today()
    keep = []
    for r in rows:
        d = posted_dt(r)
        if d is None or (today - d).days > days or not provenance_ok(r):
            continue  # unstamped rows are dropped, not guessed
        keep.append(r)
    return keep

def provenance_ok(r):
    return bool(r.get("source_url")) and bool(r.get("fetched_at"))

def main():
    today = datetime.date(2026, 11, 3)
    fresh = dict(ROW, source_url="https://boards.example/" , fetched_at="2026-11-03T00:00:00Z")
    stale = dict(ROW, url="https://x/stale", source_url="https://boards.example/",
                 fetched_at="2026-11-03T00:00:00Z")
    stale.update(posted_at="2026-08-01")
    dup = dict(fresh)  # same url -> must collapse
    nosource = dict(ROW, url="https://x/nosrc", fetched_at="2026-11-03T00:00:00Z")
    rows = [fresh, dup, stale, nosource]
    r1 = dedupe(rows)
    assert len(r1) == 3, "dedupe collapsed same-URL rows"
    r2 = purge_stale(r1, today=today)
    assert len(r2) == 1, "30-day purge removed stale row"
    assert all(provenance_ok(r) for r in r2), "every surviving row has provenance"
    assert purge_stale([nosource], today=today) == [], "rows without provenance never survive"
    print("ENGINE_OK dedupe=%d purge_kept=%d provenance=full" % (len(rows), len(r2)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
