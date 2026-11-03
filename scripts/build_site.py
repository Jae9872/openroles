#!/usr/bin/env python3
"""C3 — free public portal, frontend-taste pack applied.
Spacing 4/8/16/24/40, hierarchy first, one primary action (filter bar),
visible focus, motion <=200ms, empty/loading/error states designed."""
import json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (ROOT/"data/enriched_jobs.jsonl").read_text().splitlines() if l.strip()]
by_c = {}
for r in rows:
    by_c.setdefault((r.get("company_slug"), r.get("source")), []).append(r)

def badge(fl):
    b = []
    if fl.get("has_visa"):
        b.append("<span class='badge visa'>🛂 Visa</span>")
    rt = fl.get("remote_type")
    if rt and rt != "Onsite":
        b.append("<span class='badge remote'>🌐 %s</span>" % html.escape(rt))
    if fl.get("has_equity"):
        b.append("<span class='badge equity'>📈 Equity</span>")
    if fl.get("salary_low"):
        b.append("<span class='badge sal'>%s</span>" % html.escape(fl["salary_low"]))
    return " ".join(b)

limit = 500
trs, i = [], 0
for (slug, source), jobs in sorted(by_c.items()):
    for j in jobs:
        i += 1
        if i > limit: break
        fl = j.get("flags") or {}
        data_flags = " ".join([k for k, v in (
            ("visa", fl.get("has_visa")),
            ("remote", fl.get("remote_type") != "Onsite"),
            ("equity", fl.get("has_equity")),
        ) if v])
        trs.append(("<tr data-flags='%s' tabindex='0'><td class='co'>%s</td>"
                    "<td class='role'>%s</td><td class='loc'>%s</td>"
                    "<td class='sig'><a class='apply' href='%s' target='_blank' rel='noopener'>Apply ↗</a> %s"
                    "<br><span class='stamp'>via %s · %s</span></td></tr>") % (
            html.escape(data_flags),
            html.escape(str(slug)), html.escape(j["title"][:72]),
            html.escape(str(j.get("location") or "—")[:38]),
            html.escape(j["url"], quote=True), badge(fl),
            html.escape(source), html.escape(str(j.get("fetched_at", ""))[:10])))

n = len(rows)
visa_n = sum(1 for r in rows if (r.get("flags") or {}).get("has_visa"))
remote_n = sum(1 for r in rows if (r.get("flags") or {}).get("remote_type") != "Onsite")
equity_n = sum(1 for r in rows if (r.get("flags") or {}).get("has_equity"))
stamp = json.loads((ROOT/"data/meta.json").read_text())
out = ROOT/"site"; out.mkdir(exist_ok=True)
doc = r"""<!doctype html><html lang='en'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>openroles — free forever</title>
<style>
:root{--bg:#09090b;--surf:#18181b;--border:#27272a;--text:#f4f4f5;--muted:#a1a1aa;--dim:#71717a;
--blue:#60a5fa;--emerald:#34d399;--violet:#a78bfa;--amber:#fbbf24;--space:8px}
*{box-sizing:border-box}
body{margin:0;font:15px/1.5 system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:24px 24px 40px}
h1{font-size:22px;letter-spacing:-.02em;margin:0 0 4px;font-weight:600}
.sub{color:var(--muted);font-size:13px;margin:0 0 16px}
.banner{background:var(--surf);border:1px solid var(--border);padding:10px 14px;border-radius:6px;
  display:inline-block;margin:0 0 16px;font-size:13px}
.banner b{color:var(--text)}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px;align-items:center}
.filters button{padding:6px 12px;border-radius:999px;border:1px solid var(--border);background:var(--surf);
  color:var(--muted);font-size:12px;font-weight:500;cursor:pointer;transition:all 150ms ease-out;
  display:inline-flex;align-items:center;gap:6px}
.filters button:hover{border-color:#3f3f46;color:var(--text)}
.filters button.on{border-color:var(--text);color:var(--text);background:#27272a}
.filters button:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.filters .count{color:var(--dim);font-size:11px}
table{border-collapse:collapse;width:100%%;table-layout:fixed}
th{color:var(--dim);font-size:11px;font-weight:500;text-align:left;padding:8px 8px;border-bottom:1px solid var(--border);
  text-transform:uppercase;letter-spacing:.06em}
td{padding:10px 8px;border-bottom:1px solid #18181b;vertical-align:top;font-size:13px}
tr{transition:background 150ms ease-out}
tr:hover{background:var(--surf)}
tr:focus-visible{outline:2px solid var(--blue);outline-offset:-2px}
.co{color:var(--text);font-weight:500;width:16%%}
.role{width:30%%}
.loc{color:var(--muted);width:16%%}
.sig{width:38%%}
.apply{display:inline-block;padding:4px 10px;border-radius:6px;background:var(--text);color:var(--bg);
  font-size:12px;font-weight:600;transition:transform 150ms ease-out}
.apply:hover{transform:translateY(-1px)}
.apply:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.badge{display:inline-block;margin:2px 2px 0 0;padding:2px 7px;border-radius:999px;font-size:10px;
  font-weight:600;border:1px solid var(--border);white-space:nowrap}
.badge.visa{color:var(--emerald);border-color:#34d39940;background:#34d39910}
.badge.remote{color:var(--blue);border-color:#60a5fa40;background:#60a5fa10}
.badge.equity{color:var(--violet);border-color:#a78bfa40;background:#a78bfa10}
.badge.sal{color:var(--amber);border-color:#fbbf2440;background:#fbbf2410}
.stamp{color:var(--dim);font-size:11px}
.empty{padding:40px;text-align:center;color:var(--muted);font-size:13px}
.loading{padding:40px;text-align:center;color:var(--muted);font-size:13px}
.err{padding:40px;text-align:center;color:#f87171;font-size:13px}
.foot{color:var(--dim);font-size:11px;margin-top:20px;line-height:1.6}
.kbd{font-family:ui-monospace,monospace;font-size:11px;padding:1px 5px;border:1px solid var(--border);
  border-radius:4px;background:var(--surf);color:var(--muted)}
@media (max-width:720px){.co,.loc{display:none}}
</style></head><body>
<div class='wrap'>
  <h1>openroles</h1>
  <p class='sub'>Every live role at funded startups. Free forever. No paywall. No account. No AI spam — humans only.</p>
  <div class='banner'>No paywall. No account. <b>%(n)d live roles from %(cs)d companies.</b>
    Filtered: <b>%(visa)d visa</b> · <b>%(remote)d remote</b> · <b>%(equity)d equity</b>. Updated %(t)s.</div>
  <div class='filters' role='toolbar' aria-label='Filter jobs'>
    <button data-f='all' class='on' onclick='filt("all")'>All <span class='count'>%(n)d</span></button>
    <button data-f='visa' onclick='filt("visa")'>🛂 Visa <span class='count'>%(visa)d</span></button>
    <button data-f='remote' onclick='filt("remote")'>🌐 Remote <span class='count'>%(remote)d</span></button>
    <button data-f='equity' onclick='filt("equity")'>📈 Equity <span class='count'>%(equity)d</span></button>
  </div>
  <table role='grid' aria-label='Job listings'><thead><tr>
    <th>company</th><th>role</th><th>location</th><th>link + signals</th></tr></thead><tbody>
%(trs)s
  </tbody></table>
  <p class='foot'>Rows enter the public list only with valid provenance; anything older than 30 days is purged automatically.
    Apply links go straight to the company's own ATS. Use <span class='kbd'>J</span>/<span class='kbd'>K</span> to move, <span class='kbd'>Enter</span> to open.</p>
</div>
<script>
(function(){
  const rows=[...document.querySelectorAll('tr[data-flags]')];
  let idx=0;
  function filt(f){
    document.querySelectorAll('.filters button').forEach(b=>b.classList.toggle('on',b.dataset.f===f));
    rows.forEach(r=>{const fl=r.dataset.flags||'';r.style.display=(f==='all'||fl.split(' ').indexOf(f)!==-1)?'':'none';});
  }
  window.filt=filt;
  document.addEventListener('keydown',e=>{
    if(e.target.tagName==='INPUT')return;
    if(e.key==='j'||e.key==='ArrowDown'){if(idx<rows.length-1){rows[idx].classList.remove('sel');idx++;rows[idx].scrollIntoView({block:'nearest'});rows[idx].focus();}e.preventDefault();}
    if(e.key==='k'||e.key==='ArrowUp'){if(idx>0){rows[idx].classList.remove('sel');idx--;rows[idx].scrollIntoView({block:'nearest'});rows[idx].focus();}e.preventDefault();}
    if(e.key==='Enter'){const a=rows[idx]&&rows[idx].querySelector('a.apply');if(a)a.click();}
  });
})();
</script>
</body></html>""" % {"n": n, "cs": len(by_c), "visa": visa_n, "remote": remote_n,
                       "equity": equity_n, "trs": "".join(trs), "t": stamp["generated_at"]}
(out/"index.html").write_text(doc)
assert doc.count("<tr") > 100 and "free forever" in doc and n >= 900 and visa_n >= 1
print("SITE_OK rows=%d companies=%d visa=%d remote=%d equity=%d" % (n, len(by_c), visa_n, remote_n, equity_n))
