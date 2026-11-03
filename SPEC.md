# SPEC — openroles

## R1 — Free forever for seekers
No paywall, no account, no application fee at any stage. Applying goes straight to
the company's own ATS endpoint.

## R2 — Public, provenance-stamped data
Every published row carries `source_url` and `fetched_at`. Rows without provenance
never reach the public list.

## R3 — Freshness
Jobs older than 30 days are purged automatically. Refresh is deterministic and
stamp-driven (two runs with the same stamp produce identical output).

## R4 — Dedupe
Identical URLs collapse to one row.

## R5 — Human trail
Rows enter `pending`. Publishing requires an `approved_by` identity. Rejecting
requires a `reason`. No automated outreach ever leaves the queue.

## R6 — Enrichment flags
Each row carries `flags: { has_visa, remote_type, has_equity, salary_low, salary_high }`
derived from real description text (never fabricated — null when unknown).

## R7 — Public site
Zero login wall. Filter bar (All / Visa / Remote / Equity) with live counts.
Keyboard navigation (J/K/Enter). Empty/loading/error states designed.

## R8 — Verifier gate
Every card advances only on a clean receipt + artifact digest + re-execution.
Chain integrity must hold (`verify_chain` empty list).

## Numbered tests (Node/Python)
- T1: ingest produces ≥N live roles with provenance on every row
- T2: mode/filter combos return stable, deterministic results
- T3: counts equal row counts (never marketing numbers)
- T4: refresh determinism (same stamp → same hash)
- T5: auth/privacy boundary (public = counts only)
- T6: curation loop (pending → approve/reject+reason)
- T7: map + server endpoints
- T8: published rows are complete cards (no null garnish)
- T9: verifier rejects junk social links; verified rows self-verify
- T10: enrichment flags present and non-fabricated (null allowed, never guessed)

## Done condition
`architect verify` → `PASS :: chain_intact=True` and `ci_all.py` → `FULL_OK`.
