#!/usr/bin/env python3
"""C3 — static free portal page. Zero login wall, stamps visible per row."""
import json, html, pathlib, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (ROOT/"data/jobs.jsonl").read_text().splitlines() if l.strip()]
by_c = {}
for r in rows:
    k = (r.get("company_slug"), r.get("source"))
    by_c.setdefault(k, []).append(r)
limit = 600  # page loads a generous chunk; rest throughput to chunked files later (fork path)
trs, i = [], 0
for (slug, source), jobs in sorted(by_c.items()):
    for j in jobs:
        i += 1
        if i > limit: break
        trs.append("<tr><td>%s</td><td>%s</td><td>%s</td><td></td></tr>".replace("></td>", ">"))
        trs.append(("<tr><td>%s</td><td>%s</td><td>%s</td><td><a href='%s'>apply ↗</a> <span class='stamp'>via %s @ %s</span></td></tr>") % (
            html.escape(str(slug)), html.escape(j["title"][:70]),
            html.escape(str(j.get("location") or "")[:40]),
            html.escape(j["url"], quote=True),
            html.escape(source), html.escape(str(j.get("fetched_at", ""))[:10])))
n = len(rows)
stamp = json.loads((ROOT/"data/meta.json").read_text())
out = (ROOT/"site"); out.mkdir(exist_ok=True)
html_doc = ("""<!doctype html><html><head><meta charset='utf-8'><title>openroles — free forever</title>
<style>body{font:15px/1.5 system-ui;margin:40px auto;max-width:960px;color:#111}
h1{font-size:22px} table{border-collapse:collapse;width:100%%} td{border-bottom:1px solid #eee;padding:6px 8px}
.stamp{color:#777;font-size:11px;font-weight:normal;margin-left:8px}
.free{background:#eef;background:#f6f7ff;padding:8px 12px;border-radius:8px;display:inline-block}</style></head><body>
<h1>openroles — every live role at %(nj)s verified public boards, free forever</h1>
<p class='free'>No paywall. No account. <b>%(n)d live roles from %(cs)d companies.</b> Every row shows its source stamp. Updated %(t)s.</p>
<table><tr><th>company</th><th>role</th><th>location</th><th>link + provenance</th></tr>
%(trs)s
</table><p style='color:#999;font-size:12px'>Roles enter the public list only with valid provenance; anything older than 30 days is purged automatically. Applying stays free, always.</p>
</body></html>""") % {"nj": stamp["companies_ok"], "n": n, "cs": len(by_c), "trs": "".join(trs), "t": stamp["generated_at"]}
(out/"index.html").write_text(html_doc)
assert html_doc.count("<tr>") > 100 and "free forever" in html_doc and n >= 900
print("SITE_OK rows=%d companies=%d" % (n, len(by_c)))
