#!/usr/bin/env python3
"""C3 — free public portal. Reads ENRICHED rows; renders neon filter badges
for visa/remote/equity and a client-side J/K-free filter bar."""
import json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (ROOT/"data/enriched_jobs.jsonl").read_text().splitlines() if l.strip()]
by_c = {}
for r in rows:
    by_c.setdefault((r.get("company_slug"), r.get("source")), []).append(r)

def badge(fl):
    b = []
    if fl.get("has_visa"):
        b.append("<span class='badge visa'>🛂 Visa Sponsor</span>")
    rt = fl.get("remote_type")
    if rt and rt != "Onsite":
        b.append("<span class='badge remote'>🌐 %s</span>" % html.escape(rt))
    if fl.get("has_equity"):
        b.append("<span class='badge equity'>📈 Equity</span>")
    if fl.get("salary_low"):
        b.append("<span class='badge sal'>%s–%s</span>" % (html.escape(fl["salary_low"]), html.escape(fl["salary_high"] or "")))
    return " ".join(b)

limit = 400
trs, i = [], 0
for (slug, source), jobs in sorted(by_c.items()):
    for j in jobs:
        i += 1
        if i > limit: break
        fl = j.get("flags") or {}
        data_flags = " ".join([
            "visa" if fl.get("has_visa") else "",
            "remote" if fl.get("remote_type") != "Onsite" else "",
            "equity" if fl.get("has_equity") else "",
        ]).strip()
        trs.append(("<tr data-flags='%s'><td>%s</td><td>%s</td><td>%s</td>"
                    "<td><a href='%s' target='_blank' rel='noopener'>apply ↗</a> %s"
                    "<br><span class='stamp'>via %s @ %s</span></td></tr>") % (
            html.escape(data_flags),
            html.escape(str(slug)), html.escape(j["title"][:70]),
            html.escape(str(j.get("location") or "")[:40]),
            html.escape(j["url"], quote=True), badge(fl),
            html.escape(source), html.escape(str(j.get("fetched_at", ""))[:10])))

n = len(rows)
visa_n = sum(1 for r in rows if (r.get("flags") or {}).get("has_visa"))
remote_n = sum(1 for r in rows if (r.get("flags") or {}).get("remote_type") != "Onsite")
equity_n = sum(1 for r in rows if (r.get("flags") or {}).get("has_equity"))
stamp = json.loads((ROOT/"data/meta.json").read_text())
out = ROOT/"site"; out.mkdir(exist_ok=True)
doc = ("""<!doctype html><html><head><meta charset='utf-8'><title>openroles — free forever</title>
<style>
body{font:15px/1.5 system-ui;margin:28px auto;max-width:1080px;color:#111;background:#09090b;color:#f4f4f5}
h1{font-size:20px;letter-spacing:-.02em}
.banner{background:#18181b;border:1px solid #27272a;padding:10px 14px;border-radius:8px;display:inline-block;margin:10px 0 14px}
table{border-collapse:collapse;width:100%%} td,th{border-bottom:1px solid #18181b;padding:7px 8px;vertical-align:top}
a{color:#60a5fa;text-decoration:none} a:hover{text-decoration:underline}
.stamp{color:#71717a;font-size:11px}
.badge{display:inline-block;margin:2px 2px 0 0;padding:1px 7px;border-radius:999px;font-size:10px;font-weight:600;border:1px solid #27272a}
.badge.visa{color:#34d399;border-color:#34d39940;background:#34d39910}
.badge.remote{color:#60a5fa;border-color:#60a5fa40;background:#60a5fa10}
.badge.equity{color:#a78bfa;border-color:#a78bfa40;background:#a78bfa10}
.badge.sal{color:#fbbf24;border-color:#fbbf2440;background:#fbbf2410}
.filters button{margin:0 6px 8px 0;padding:5px 11px;border-radius:999px;border:1px solid #27272a;background:#18181b;color:#a1a1aa;font-size:12px;cursor:pointer}
.filters button.on{border-color:#f4f4f5;color:#f4f4f5;background:#27272a}
.filters .count{color:#71717a;font-size:11px;margin-left:4px}
</style></head><body>
<h1>openroles — free forever</h1>
<div class='banner'>No paywall. No account. <b>%(n)d live roles from %(cs)d companies.</b>
 Filtered: <b>%(visa)d visa</b> · <b>%(remote)d remote</b> · <b>%(equity)d equity</b>. Updated %(t)s.</div>
<div class='filters'>
  <button data-f='all' class='on' onclick='filt("all")'>All <span class='count'>%(n)d</span></button>
  <button data-f='visa' onclick='filt("visa")'>🛂 Visa <span class='count'>%(visa)d</span></button>
  <button data-f='remote' onclick='filt("remote")'>🌐 Remote <span class='count'>%(remote)d</span></button>
  <button data-f='equity' onclick='filt("equity")'>📈 Equity <span class='count'>%(equity)d</span></button>
</div>
<table><tr><th>company</th><th>role</th><th>location</th><th>link + signals</th></tr>
%(trs)s
</table>
<p style='color:#71717a;font-size:12px;margin-top:14px'>Rows enter the public list only with valid provenance; anything older than 30 days is purged automatically. Applying stays free, always.</p>
<script>
function filt(f){
  document.querySelectorAll('.filters button').forEach(b=>b.classList.toggle('on', b.dataset.f===f));
  document.querySelectorAll('tr[data-flags]').forEach(r=>{
    const fl = r.dataset.flags || '';
    r.style.display = (f==='all' || fl.split(' ').indexOf(f)!==-1) ? '' : 'none';
  });
}
</script>
</body></html>""") % {"n": n, "cs": len(by_c), "visa": visa_n, "remote": remote_n,
                       "equity": equity_n, "trs": "".join(trs), "t": stamp["generated_at"]}
(out/"index.html").write_text(doc)
assert doc.count("<tr") > 100 and "free forever" in doc and n >= 900 and visa_n >= 1
print("SITE_OK rows=%d companies=%d visa=%d remote=%d equity=%d" % (n, len(by_c), visa_n, remote_n, equity_n))
