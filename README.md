# openroles — free forever job portal

> **Every live role at funded startups. Freshness-stamped. Human-trail. Seekers never pay.**

A free, open-source job portal that aggregates live roles from public company career pages
(Greenhouse, Ashby, Lever, …), enriches them with high-signal flags (visa · remote · equity ·
salary), and publishes them with per-row provenance. No paywall, no account, no AI spam.

**Live (local):** `http://localhost:8090/` · **License:** MIT (code) · **Data:** public ATS boards only

---

## Why this exists

Applying for jobs should never cost money. The raw listings are free everywhere; what's *not*
free is curation, freshness, and a human trail. This portal ships those three for $0/mo:
- **Freshness as proof** — every job carries `source_url` + `fetched_at`; anything older than
  30 days is purged automatically.
- **Human trail** — rows enter `pending` and only publish after a human approves with an
  identity attached; reasonless rejects are impossible by construction.
- **Anti-AI-spam identity** — no automated outreach ever; the portal only links to the
  company's own ATS apply endpoint.

## What's in the box (today)

| Layer | Status | Proof |
|---|---|---|
| Ingest (MIT fork of Riley-Dorrington's engine) | ✅ 2,478 live roles · 71 active companies · 3 ATS platforms | `SMOKE_OK` |
| Freshness engine (dedupe · 30-day purge · provenance) | ✅ | `ENGINE_OK` |
| Enrichment (visa / remote / equity / salary) | ✅ visa 30 · remote 596 · equity 223 · salary 156 | `ENRICH_OK` |
| Free public site (filter bar + neon badges + keyboard nav) | ✅ | `SITE_OK` |
| Human-trail curation | ✅ | `CURATION_OK` |
| Readiness gate | ✅ full pipeline re-verified | `FULL_OK` |
| Verifier chain | ✅ `PASS :: chain_intact=True receipts=12` | `architect verify` |

## Quickstart

```bash
cd openroles
python3 scripts/scrape.py --smoke            # live ingest proof (2 verified boards)
python3 scripts/fetch_descriptions.py       # pull per-job descriptions for enrichment
python3 scripts/enrich.py                   # visa/remote/equity/salary flags
python3 scripts/build_site.py               # regenerate site/
python3 -m http.server 8090 --directory site   # open http://localhost:8090
```

## Architecture (4 boxes, ~200 lines of Python)

```
INGEST  (scrape.py)        FRESHNESS (engine_test.py)   SITE (build_site.py)   TRAIL (curate.py)
public ATS JSON  ───────▶  dedupe + 30-day purge  ────▶  static HTML + badges  ────▶  human approve
(source_url+stamp)          (provenance required)        (filter bar, J/K nav)      (no auto-mail)
```

One file of truth: `data/jobs.jsonl` (2,478 lines, each carrying its own receipt).

## Commands

| Command | What it does |
|---|---|
| `python3 scripts/scrape.py` | Full ingest from `data/companies.json` |
| `python3 scripts/scrape.py --smoke` | Ingest proof (2 verified boards, sidecar output) |
| `python3 scripts/fetch_descriptions.py` | Fetch per-job descriptions for enrichment |
| `python3 scripts/enrich.py` | Visa/remote/equity/salary flags → `enriched_jobs.jsonl` |
| `python3 scripts/build_site.py` | Regenerate `site/index.html` |
| `python3 scripts/ci_all.py` | Full pipeline re-verify (`FULL_OK`) |
| `architect run / next / verify` | Gate receipts + chain integrity |
| `architect board` | Visual kanban (`board.html`) |

## Verified open-source sources

- `strelov1/freehire` — 4.7M+ postings, MIT (big-engine precedent)
- `Riley-Dorrington/job-board-aggregator` — 95k companies, 7 ATS, MIT (forked)
- `Nneji123/ycombinator-scraper` — YC companies + founder profiles, MIT
- `skillsire/Daily-H1B-Jobs` — daily visa-sponsored jobs, MIT
- `maroonberets96/sponsorpilot` — UK/Canada vacancies × gov sponsor registries, MIT
- `2scraper/wellfound-scraper` — Wellfound roles with salary+equity, MIT

## Roadmap

1. **GitHub Actions 12h cron + Pages deploy** — live public URL, $0/mo
2. **Enrichment flags** ✅ (visa 30 / remote 596 / equity 223)
3. **YC adapter** — funded-startup discovery, auto-fills company list
4. **Scale company slabs** — 20 → 200 → thousands (same code)
5. **Map view** — MapLibre clustered globe of companies (in progress)

## License

MIT (code). Data is derived from public ATS JSON endpoints; company datasets from
third-party repos are used under their own licenses (see `RESEARCH.md`).

## Credits

Built on top of `Riley-Dorrington/job-board-aggregator` (MIT) and the verified
open-source ecosystem listed in `RESEARCH.md`. Frontend taste per the `frontend-taste`
pack (spacing 4/8/16/24/40, hierarchy, contrast, motion ≤200ms).
