# Docs index — openroles

| File | Path | What it is |
|---|---|---|
| README | `README.md` | Project overview, quickstart, commands, license |
| SPEC | `SPEC.md` | Requirements R1–R8, numbered tests, done condition |
| SOUL | `SOUL.md` | Identity, tone, non-negotiables, audience |
| EVIDENCE | `EVIDENCE.md` | Verified facts, data layer, sources, gaps |
| DESIGN | `DESIGN.md` | UI/UX design system + living-atlas art direction |
| RESEARCH | `RESEARCH.md` | Free job-source ledger, niche sweep, license ruling |
| BRIEF | `BRIEF.md` | Architect mission brief (NOW/PLAN/DONE) |
| SESSION | `SESSION.md` | Architect session state |
| AGENTS | `AGENTS.md` | Agent instructions for this repo |

## Key paths
- Engine: `scripts/scrape.py`, `scripts/enrich.py`, `scripts/fetch_descriptions.py`, `scripts/build_site.py`, `scripts/build_geojson.py`, `scripts/ci_all.py`, `scripts/curate.py`, `scripts/engine_test.py`
- Data: `data/jobs.jsonl` (41,615 rows), `data/enriched_jobs.jsonl`, `data/companies.geojson`, `data/countries.json`, `data/meta.json`, `data/companies.json`
- Site: `site/index.html`, `site/map.html`, `site/companies.geojson`, `site/jobs_sample.json`
- Mission: `mission.json`, `reports/` (receipt chain)
- CI: `.github/workflows/deploy.yml`, `.github/workflows/refresh.yml`
