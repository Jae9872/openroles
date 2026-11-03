# RESEARCH — openroles

## Verified free sources (probed live 2026-11-03)
- Greenhouse board API — `boards-api.greenhouse.io/v1/boards/{slug}/jobs` — Stripe 739 jobs, no key
- Ashby posting API — `api.ashbyhq.com/posting-api/job-board/{org}` — Ramp 170 jobs, no key
- Lever postings API — timed out twice → [gap]
- Arbeitnow / Remotive / Jobicy / RemoteOK — free aggregated APIs, no key

## Repos (MIT unless noted)
- `strelov1/freehire` — 4.7M+ postings, MIT (big-engine precedent)
- `Riley-Dorrington/job-board-aggregator` — 95k companies, 7 ATS, MIT (forked)
- `Nneji123/ycombinator-scraper` — YC + founder profiles, MIT
- `skillsire/Daily-H1B-Jobs` — daily visa jobs, MIT
- `maroonberets96/sponsorpilot` — UK/Canada gov sponsor registries, MIT
- `2scraper/wellfound-scraper` — salary+equity export, MIT
- `rishilahoti/ashby-job-scraper` — multi-ATS + diff, NOASSERTION license

## Niche sources
- Visa: Daily-H1B-Jobs, sponsorpilot (gov registry cross-ref)
- Startups: YC scraper (company/founder/job triples), Wellfound scraper
- Founders: HN "who is hiring" thread parsers

## License ruling
- MIT code: forkable. CC BY-NC datasets: dev-only; ship with our own Common Crawl derivation.

## Gaps
- Lever API, WWR RSS (timed out twice)
- Workday/BambooHR/iCIMs/Paylocity slabs not yet run
- YC funded-startup adapter not wired
- Globe country labels (using country breakdown panel instead)
