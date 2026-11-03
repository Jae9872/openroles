# EVIDENCE — openroles

## Observed (verified this session)
- Public ATS JSON endpoints return live jobs with no key:
  - Greenhouse `boards-api.greenhouse.io/v1/boards/{slug}/jobs` → Stripe 739 jobs
  - Ashby `api.ashbyhq.com/posting-api/job-board/{org}` → Ramp 170 jobs
  - Lever `api.lever.co/v0/postings/{org}?mode=json` (timed out twice → gap)
- Ingest via MIT fork (Riley-Dorrington) pulled 2,478 live roles from 71 active
  companies across 3 platforms in one run.
- Per-job detail endpoints (Greenhouse/Ashby/Lever) returned descriptions for
  1,579/2,478 roles → enrichment flags visa 30 / remote 596 / equity 223 / salary 156.
- Freshness purge (30 days) and dedupe verified by engine self-test.
- Provenance requirement enforced: unstamped rows never survive purge.

## Data layer
- No database. One file of truth: `data/jobs.jsonl` (2,478 lines).
- Each row carries `source_url` + `fetched_at`. Meta in `data/meta.json`.

## Verified open-source sources (MIT unless noted)
- `strelov1/freehire` (MIT, ~3.5k★) — 4.7M+ postings precedent
- `Riley-Dorrington/job-board-aggregator` (MIT) — 95k companies, 7 ATS, forked
- `Nneji123/ycombinator-scraper` (MIT) — YC + founder profiles
- `skillsire/Daily-H1B-Jobs` (MIT) — daily visa-sponsored jobs
- `maroonberets96/sponsorpilot` (MIT) — UK/Canada gov sponsor registries
- `2scraper/wellfound-scraper` (MIT) — salary+equity export

## Gaps
- Lever API timed out twice → marked [gap], re-probe later.
- Workday/BambooHR/iCIMs/Paylocity slabs available but not yet run.
- YC funded-startup adapter not yet wired.
- Map view (MapLibre clustered globe) — next card.
