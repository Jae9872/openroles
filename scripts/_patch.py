from pathlib import Path
t = Path("site/map.html").read_text()

old_panel = """  <aside class='panel' id='panel'>
    <h1>Companies</h1>
    <div class='meta' id='meta'>Loading…</div>
    <div class='countries' id='countries' style='padding:8px 16px;border-bottom:1px solid var(--border);font-size:11px;color:var(--muted)'>Loading countries…</div>
    <div class='search'><input id='q' type='search' placeholder='Filter companies…' aria-label='Filter companies'></div>
    <div class='list' id='list'></div>"""
new_panel = """  <aside class='panel' id='panel'>
    <h1>openroles atlas</h1>
    <div class='tabs' style='display:flex;border-bottom:1px solid var(--border)'>
      <button class='tab on' data-tab='countries' onclick='switchTab("countries")' style='flex:1;padding:8px;border:none;background:transparent;color:var(--muted);font-size:12px;font-weight:500;cursor:pointer;border-bottom:2px solid transparent'>Countries</button>
      <button class='tab' data-tab='companies' onclick='switchTab("companies")' style='flex:1;padding:8px;border:none;background:transparent;color:var(--muted);font-size:12px;font-weight:500;cursor:pointer;border-bottom:2px solid transparent'>Companies</button>
    </div>
    <div class='meta' id='meta'>Loading…</div>
    <div class='countries' id='countries' style='padding:8px 16px;border-bottom:1px solid var(--border);font-size:11px;color:var(--muted)'>Loading countries…</div>
    <div class='search' id='searchbox' style='display:none'><input id='q' type='search' placeholder='Filter companies…' aria-label='Filter companies'></div>
    <div class='list' id='list'></div>"""
assert old_panel in t, "panel block not found"
t = t.replace(old_panel, new_panel)

t = t.replace("var geo = null, selected = null, currentFilter = 'all';",
              "var geo = null, selected = null, currentFilter = 'all', selectedCountry = null, countriesData = null;")

old_rl = """  let feats = (geo?.features || [])
    .filter(x => !f || (x.properties.name||'').toLowerCase().includes(f))
    .filter(x => currentFilter==='all' || hasFlag(x, currentFilter));
  if (selectedCountry) feats = feats.filter(x => x.properties.country === selectedCountry);
  feats = feats.sort((a,b)=> b.properties.jobs - a.properties.jobs);"""
if old_rl not in t:
    old_rl2 = """  const feats = (geo?.features || [])
    .filter(x => !f || (x.properties.name||'').toLowerCase().includes(f))
    .filter(x => currentFilter==='all' || hasFlag(x, currentFilter))
    .sort((a,b)=> b.properties.jobs - a.properties.jobs);"""
    new_rl2 = """  let feats = (geo?.features || [])
    .filter(x => !f || (x.properties.name||'').toLowerCase().includes(f))
    .filter(x => currentFilter==='all' || hasFlag(x, currentFilter));
  if (selectedCountry) feats = feats.filter(x => x.properties.country === selectedCountry);
  feats = feats.sort((a,b)=> b.properties.jobs - a.properties.jobs);"""
    assert old_rl2 in t
    t = t.replace(old_rl2, new_rl2)

switch_tab = '''function switchTab(tab){
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('on', b.dataset.tab === tab));
  if (tab === 'countries') {
    document.getElementById('searchbox').style.display = 'none';
    renderCountries();
  } else {
    document.getElementById('searchbox').style.display = '';
    renderList(document.getElementById('q').value);
  }
}
function renderCountries(){
  const list = document.getElementById('list');
  list.innerHTML = '';
  if (!countriesData) { list.innerHTML = '<div style="padding:16px;color:var(--muted);font-size:13px">Loading…</div>'; return; }
  const filtered = countriesData.filter(c => c.country !== 'Unknown');
  filtered.forEach(c => {
    const d = document.createElement('div');
    d.className = 'row';
    d.innerHTML = '<div class="name">'+c.country+'<span class="count">'+c.jobs.toLocaleString()+'</span></div>'+
                  '<div class="loc">'+c.companies+' companies</div>';
    d.addEventListener('click', () => selectCountry(c));
    list.appendChild(d);
  });
  document.getElementById('meta').textContent = filtered.length + ' countries · ' + filtered.reduce((s,c)=>s+c.jobs,0).toLocaleString() + ' roles';
}
function selectCountry(c){
  selectedCountry = c.code;
  globe.pointOfView({ lat: c.lat, lng: c.lng, altitude: 1.6 }, prefersReduced ? 0 : 900);
  let back = document.getElementById('back-btn');
  if (!back){ back = document.createElement('button'); back.id='back-btn'; back.style.cssText='margin:8px 16px;padding:6px 12px;border-radius:6px;border:1px solid var(--border);background:var(--surf);color:var(--text);font-size:12px;cursor:pointer;width:calc(100% - 32px)'; back.textContent='← All countries'; back.onclick=clearCountry; document.getElementById('panel').insertBefore(back, document.getElementById('countries')); }
  back.style.display = '';
  switchTab('companies');
}
function clearCountry(){
  selectedCountry = null;
  const back = document.getElementById('back-btn'); if (back) back.style.display = 'none';
  globe.pointOfView({ lat: 20, lng: 0, altitude: 2.2 }, prefersReduced ? 0 : 800);
  switchTab('countries');
}

'''
t = t.replace("function applyFilter(f){", switch_tab + "\nfunction applyFilter(f){", 1)

old_cb = """  geo = data; window.geo = geo;
  applyFilter('all');
"""
new_cb = """  geo = data; window.geo = geo;
  applyFilter('all');
  fetch('countries.json').then(r=>r.json()).then(cs => {
    countriesData = cs;
    renderCountries();
    const el = document.getElementById('countries');
    if (el) el.innerHTML = '<div style="font-weight:600;color:var(--text);margin-bottom:4px;font-size:11px;text-transform:uppercase;letter-spacing:.06em">Top countries</div>' +
      cs.slice(0, 8).map(c => '<div style="display:flex;justify-content:space-between;padding:2px 0"><span>'+c.country+'</span><span style="color:var(--emerald)">'+c.jobs.toLocaleString()+'</span></div>').join('');
  }).catch(()=>{});
  switchTab('countries');
"""
assert old_cb in t
t = t.replace(old_cb, new_cb, 1)

# remove duplicate countries fetch
old_dup = """  fetch('countries.json').then(r=>r.json()).then(cs => {
    const el = document.getElementById('countries');
    el.innerHTML = '<div style="font-weight:600;color:var(--text);margin-bottom:4px;font-size:11px;text-transform:uppercase;letter-spacing:.06em">Top countries</div>' +
      cs.slice(0, 10).map(c => '<div style="display:flex;justify-content:space-between;padding:2px 0"><span>'+c.country+'</span><span style="color:var(--emerald)">'+c.jobs.toLocaleString()+'</span></div>').join('');
  }).catch(()=>{});
  // country borders"""
new_dup = """  // country borders"""
if old_dup in t:
    t = t.replace(old_dup, new_dup, 1)

Path("site/map.html").write_text(t)
print("patched successfully")
