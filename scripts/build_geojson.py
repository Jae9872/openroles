#!/usr/bin/env python3
"""Build a GeoJSON FeatureCollection of companies (one point per company)
with job counts. Coords resolved via the aggregator's location lookup, with a
fallback that tries each comma-separated token of the location string."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, "/Users/tr-mac-020/Downloads/jba/scripts")
from geolocation import build_lookup, lookup_location

LM = build_lookup("/Users/tr-mac-020/Downloads/jba/data/locations.json")

def resolve_coords(loc):
    if not loc: return None
    for token in str(loc).split(","):
        r = lookup_location(token.strip(), LM)
        if r and r.get("coords"):
            return r["coords"]
    # last resort: try whole string
    r = lookup_location(str(loc).strip(), LM)
    return (r or {}).get("coords")

def main():
    rows = [json.loads(l) for l in (ROOT/"data/enriched_jobs.jsonl").read_text().splitlines() if l.strip()]
    agg = {}
    for r in rows:
        slug = r.get("company_slug") or r.get("company")
        if not slug: continue
        a = agg.setdefault(slug, {"name": slug, "jobs": 0, "coords": None, "source": r.get("source")})
        a["jobs"] += 1
        if a["coords"] is None:
            a["coords"] = resolve_coords(r.get("location"))
    features = []
    for slug, a in agg.items():
        c = a["coords"]
        if not c or len(c) != 2: continue
        lat, lng = c  # aggregator stores [lat, lng]
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {"id": slug, "name": slug, "jobs": a["jobs"], "source": a["source"]},
        })
    out = {"type": "FeatureCollection", "features": features}
    (ROOT/"data/companies.geojson").write_text(json.dumps(out))
    (ROOT/"site/companies.geojson").write_text(json.dumps(out))
    print("GEOJSON_OK companies=%d with_coords=%d (of %d)" % (len(agg), len(features), len(agg)))
    return 0

if __name__ == "__main__":
    import sys; sys.exit(main())
