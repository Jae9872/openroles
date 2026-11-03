#!/usr/bin/env python3
"""Build GeoJSON of companies (one point per company) with job counts + country.
Also writes data/countries.json (top countries by job count) for the globe legend."""
import json, sys, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, "/Users/tr-mac-020/Downloads/jba/scripts")
from geolocation import build_lookup, lookup_location

LM = build_lookup("/Users/tr-mac-020/Downloads/jba/data/locations.json")
CITY2COUNTRY = {e[0].lower(): e[2] for e in json.load(open("/Users/tr-mac-020/Downloads/jba/data/locations.json"))["data"]}
COUNTRY_NAMES = {
 "US":"United States","GB":"United Kingdom","IN":"India","DE":"Germany","CA":"Canada",
 "FR":"France","AU":"Australia","SG":"Singapore","NL":"Netherlands","BR":"Brazil",
 "ES":"Spain","IT":"Italy","JP":"Japan","KR":"South Korea","CN":"China","MX":"Mexico",
 "IE":"Ireland","SE":"Sweden","CH":"Switzerland","IL":"Israel","AE":"UAE",
 "PL":"Poland","PT":"Portugal","NZ":"New Zealand","BE":"Belgium","DK":"Denmark",
 "NO":"Norway","FI":"Finland","AT":"Austria","CZ":"Czechia","RO":"Romania",
 "UA":"Ukraine","TR":"Turkey","ZA":"South Africa","AR":"Argentina","CL":"Chile",
 "CO":"Colombia","VE":"Venezuela","PH":"Philippines","ID":"Indonesia","TH":"Thailand",
 "VN":"Vietnam","MY":"Malaysia","PK":"Pakistan","EG":"Egypt","NG":"Nigeria",
 "KE":"Kenya","GH":"Ghana","MA":"Morocco","TN":"Tunisia","Unknown":"Unknown",
}


def resolve_coords(loc):
    if not loc: return None
    for token in str(loc).split(","):
        r = lookup_location(token.strip(), LM)
        if r and r.get("coords"):
            return r["coords"]
    r = lookup_location(str(loc).strip(), LM)
    return (r or {}).get("coords")

def resolve_country(loc):
    if not loc: return None
    for token in str(loc).split(","):
        c = CITY2COUNTRY.get(token.strip().lower())
        if c: return c
    return CITY2COUNTRY.get(str(loc).strip().lower())

def main():
    rows = [json.loads(l) for l in (ROOT/"data/enriched_jobs.jsonl").read_text().splitlines() if l.strip()]
    agg = {}
    for r in rows:
        slug = r.get("company_slug") or r.get("company")
        if not slug: continue
        a = agg.setdefault(slug, {"name": slug, "jobs": 0, "coords": None, "source": r.get("source"),
                                  "visa": 0, "remote": 0, "equity": 0, "country": None})
        a["jobs"] += 1
        fl = r.get("flags") or {}
        if fl.get("has_visa"): a["visa"] += 1
        if fl.get("remote_type") not in (None, "Onsite"): a["remote"] += 1
        if fl.get("has_equity"): a["equity"] += 1
        if a["coords"] is None:
            a["coords"] = resolve_coords(r.get("location"))
        if a["country"] is None:
            a["country"] = resolve_country(r.get("location"))

    features = []
    for slug, a in agg.items():
        c = a["coords"]
        if not c or len(c) != 2: continue
        lat, lng = c
        flag_tokens = []
        if a["visa"]: flag_tokens.append("visa")
        if a["remote"]: flag_tokens.append("remote")
        if a["equity"]: flag_tokens.append("equity")
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {"id": slug, "name": slug, "jobs": a["jobs"], "source": a["source"],
                           "flags": " ".join(flag_tokens), "visa": a["visa"], "remote": a["remote"],
                           "equity": a["equity"], "country": a["country"] or "Unknown", "country_name": COUNTRY_NAMES.get(a["country"] or "Unknown", a["country"] or "Unknown")},
        })

    out = {"type": "FeatureCollection", "features": features}
    (ROOT/"data/companies.geojson").write_text(json.dumps(out))
    (ROOT/"site/companies.geojson").write_text(json.dumps(out))

    # country breakdown
    by_country = collections.Counter()
    for f in features:
        by_country[f["properties"]["country"]] += f["properties"]["jobs"]
    country_list = [{"country": COUNTRY_NAMES.get(c, c), "code": c, "jobs": n, "companies": sum(1 for f in features if f["properties"]["country"] == c)}
                    for c, n in by_country.most_common(30)]
    (ROOT/"data/countries.json").write_text(json.dumps(country_list, indent=1))
    (ROOT/"site/countries.json").write_text(json.dumps(country_list))

    # jobs sample for selected-company panel
    sample = []
    for r in rows[:3000]:
        sample.append({"company_slug": r.get("company_slug") or r.get("company"),
                      "title": r.get("title"), "url": r.get("url"),
                      "location": r.get("location")})
    (ROOT/"site/jobs_sample.json").write_text(json.dumps(sample))

    print("GEOJSON_OK companies=%d with_coords=%d (of %d) | top country: %s (%d jobs)" %
          (len(agg), len(features), len(agg), country_list[0]["country"], country_list[0]["jobs"]))
    return 0

if __name__ == "__main__":
    import sys; sys.exit(main())
