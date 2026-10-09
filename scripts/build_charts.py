#!/usr/bin/env python3
"""Reads the CSVs in data/ and writes self-contained HTML charts into charts/.
CSV files are the source of truth; re-run this after editing data."""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "charts"
OUT.mkdir(exist_ok=True)

def rows(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

SPEC = ["far_right","right","centre_right","centre","centre_left","left","far_left"]
LABEL = {"far_right":"Far right","right":"Right","centre_right":"Centre-right","centre":"Centre",
         "centre_left":"Centre-left","left":"Left","far_left":"Far left"}
COLOR = {"far_right":"#2a78d6","right":"#85b7eb","centre_right":"#b5d4f4","centre":"#b4b2a9",
         "centre_left":"#f7c1c1","left":"#f09595","far_left":"#e24b4a"}

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<script src="../assets/chart.umd.js"></script>
<style>body{{font-family:system-ui,sans-serif;margin:24px;color:#222;background:#fff}}h1{{font-size:20px;font-weight:500}}h2{{font-size:15px;font-weight:500;margin:24px 0 4px}}
.cap{{font-size:12px;color:#777;margin:0 0 8px}}.wrap{{position:relative;width:100%;height:{h}px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px 28px}}
.lg{{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:#555;margin:6px 0 0}}.sw{{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:4px;vertical-align:-2px}}
table{{border-collapse:collapse;font-size:12px}}th,td{{padding:4px 8px;border-bottom:1px solid #e5e5e5;text-align:right}}th:first-child,td:first-child{{text-align:left}}</style></head><body>
<h1>{title}</h1><p class="cap">{sub}</p>"""
FOOT = "</body></html>"

def write(name, html):
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", OUT / name)

# ---------- 1. Chamber by spectrum 1990-2026 ----------
cam = rows(DATA / "historical" / "camara_espectro_1990_2026.csv")
years = [r["election"] for r in cam]
tot = [int(r["total_seats"]) for r in cam]
ds = []
for k in reversed(SPEC):
    ds.append({"label": LABEL[k], "backgroundColor": COLOR[k], "borderColor": COLOR[k],
               "data": [round(int(r[k]) / int(r["total_seats"]) * 100, 1) for r in cam],
               "seats": [int(r[k]) for r in cam]})
legend = "".join(f'<span><span class="sw" style="background:{COLOR[k]}"></span>{LABEL[k]}</span>' for k in reversed(SPEC))
table = "<table><tr><th>Election</th>" + "".join(f"<th>{LABEL[k]}</th>" for k in SPEC) + "</tr>"
for r in cam:
    table += f"<tr><td>{r['election']} ({r['total_seats']})</td>" + "".join(
        f"<td>{r[k]}<br><small>{int(r[k])/int(r['total_seats'])*100:.1f}%</small></td>" for k in SPEC) + "</tr>"
table += "</table>"
html = HEAD.format(title="Chamber of Deputies by ideological spectrum, 1990–2026", sub="Seats elected per election. Source: TSE; party mapping in data/historical/partidos_espectro_mapeamento.csv", h=360)
html += f'<div class="lg">{legend}</div><h2>Seat share per election</h2><div class="wrap"><canvas id="bars"></canvas></div>'
html += '<h2>Trajectory of each spectrum (% of the House)</h2><div class="wrap"><canvas id="lines"></canvas></div><h2>Table</h2>' + table
html += f"""<script>
const years={json.dumps(years)}, ds={json.dumps(ds)};
const tip={{callbacks:{{label:t=>t.dataset.label+': '+t.dataset.seats[t.dataIndex]+' seats ('+t.raw+'%)'}}}};
new Chart(document.getElementById('bars'),{{type:'bar',data:{{labels:years,datasets:ds.map(d=>({{...d,barThickness:22}}))}},
 options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}},tooltip:tip}},
 scales:{{x:{{stacked:true,max:100,ticks:{{callback:v=>v+'%'}}}},y:{{stacked:true}}}}}}}});
new Chart(document.getElementById('lines'),{{type:'line',data:{{labels:years,datasets:ds.map(d=>({{...d,fill:false,tension:.25,pointRadius:3}}))}},
 options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},plugins:{{legend:{{display:false}},tooltip:tip}},
 scales:{{y:{{min:0,max:45,ticks:{{callback:v=>v+'%'}}}}}}}}}});
</script>""" + FOOT
write("01_camara_espectro_1990_2026.html", html)

# ---------- 2. National indicators ----------
ind = rows(DATA / "national" / "indicadores_nacionais.csv")
series = {}
for r in ind:
    series.setdefault(r["indicator"], []).append({"x": int(r["year"]), "y": float(r["value"])})
PANELS = [
 ("Religion (% population)", [("catholic","Catholic","#7a5c2e"),("evangelical","Evangelical","#0ca30c"),("no_religion","No religion","#b4b2a9")], 0, 100),
 ("Internet (%)", [("internet_individuals","Individuals online","#5a3fd6"),("internet_households","Households connected","#a58cf0")], 0, 100),
 ("Mobile lines /100 · smartphone %", [("mobile_lines","Lines per 100","#d97706"),("smartphone_users","Smartphone users %","#f5c26b")], 0, 150),
 ("Facebook and Instagram (millions)", [("facebook_users","Facebook","#1877f2"),("instagram_users","Instagram","#d6336c")], 0, 150),
 ("GDP per capita (current US$)", [("gdp_per_capita","GDP per capita","#5a3fd6")], 0, 14000),
 ("GDP growth (%)", [("gdp_growth","Growth","#9fc49f")], -6, 9),
 ("HDI", [("hdi","HDI","#0ca30c")], 0.5, 0.85),
 ("Unemployment (%)", [("unemployment","Unemployment","#d97706")], 0, 16),
 ("Years of schooling (adults 25+)", [("years_schooling","Years","#0ca30c")], 0, 10),
 ("Gini index", [("gini","Gini","#7a5c2e")], 0.4, 0.65),
 ("Prisoners per 100,000", [("prisoners_rate","Prisoners /100k","#b91c1c")], 0, 450),
 ("Homicides per 100,000", [("homicide_rate","Homicides /100k","#b91c1c")], 0, 35),
 ("Women and work (%)", [("women_pay_ratio","Pay as % of men's","#d6336c"),("female_participation","Participation rate","#f09595")], 40, 100),
 ("Family (% households)", [("female_headed_households","Female-headed","#5a3fd6"),("one_person_households","One-person","#a58cf0")], 0, 60),
 ("Fertility (children per woman)", [("fertility_rate","Fertility","#7a5c2e")], 0, 4),
 ("Vehicles per 100 inhabitants", [("vehicles_per_100","Vehicles /100","#d97706")], 0, 70),
 ("Vehicle fleet (millions)", [("vehicle_fleet","Total","#d97706"),("motorcycles","Motorcycles","#f5c26b")], 0, 140),
 ("CLT vs informal (% of employed)", [("clt_share","CLT","#0ca30c"),("informal_share","Informal","#ec835a")], 0, 60),
 ("Workers by contract (millions)", [("clt_employees","CLT","#0ca30c"),("employees_no_contract","No contract","#ec835a"),("self_employed","Self-employed","#d97706")], 0, 45),
 ("MEI registrations (millions)", [("mei","MEI","#5a3fd6")], 0, 20),
]
html = HEAD.format(title="Brazil, national indicators 1990–2026", sub="Source and notes per point in data/national/indicadores_nacionais.csv. Values flagged approx there are indicative only.", h=200)
html += '<div class="grid">'
cfg = []
for i, (title, ss, lo, hi) in enumerate(PANELS):
    lg = "".join(f'<span><span class="sw" style="background:{c}"></span>{l}</span>' for _, l, c in ss)
    html += f'<div><h2>{title}</h2><div class="wrap"><canvas id="p{i}"></canvas></div><div class="lg">{lg}</div></div>'
    cfg.append({"id": f"p{i}", "lo": lo, "hi": hi, "bar": ss[0][0] == "gdp_growth",
                "ds": [{"label": l, "borderColor": c, "backgroundColor": c, "data": series.get(k, [])} for k, l, c in ss]})
html += "</div><script>const P=" + json.dumps(cfg) + """;
P.forEach(p=>{new Chart(document.getElementById(p.id),{type:p.bar?'bar':'line',data:{datasets:p.ds.map(d=>({...d,tension:.25,pointRadius:2,borderWidth:2,barThickness:5,
 backgroundColor:p.bar?(c=>c.parsed&&c.parsed.y<0?'#ec835a':'#9fc49f'):d.backgroundColor}))},
 options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'nearest',intersect:false},plugins:{legend:{display:false},
 tooltip:{callbacks:{title:t=>t[0].parsed.x,label:t=>t.dataset.label+': '+t.parsed.y}}},
 scales:{x:{type:'linear',min:1990,max:2026,ticks:{stepSize:6,callback:v=>v}},y:{min:p.lo,max:p.hi}}}})});
</script>""" + FOOT
write("02_indicadores_nacionais.html", html)

# ---------- 3. States 2026 ----------
st = rows(DATA / "states" / "estados_2026.csv")
cols = list(st[0].keys())
html = HEAD.format(title="Brazilian states: indicators vs 2026 first-round presidential vote", sub="Vote: TSE 4 Oct 2026. Other columns: latest available, see docs/SOURCES.md. Pick an indicator to plot against the Flávio Bolsonaro vote.", h=360)
html += '<label>Indicator: <select id="sel"></select></label> <span id="corr"></span><div class="wrap"><canvas id="sc"></canvas></div><h2>Table</h2><div id="tb"></div>'
html += "<script>const D=" + json.dumps(st) + ";const cols=" + json.dumps(cols) + """;
const sel=document.getElementById('sel');cols.slice(3).forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;sel.appendChild(o)});
function corr(x,y){const n=x.length,mx=x.reduce((a,b)=>a+b)/n,my=y.reduce((a,b)=>a+b)/n;let sxy=0,sx=0,sy=0;for(let i=0;i<n;i++){sxy+=(x[i]-mx)*(y[i]-my);sx+=(x[i]-mx)**2;sy+=(y[i]-my)**2}return sxy/Math.sqrt(sx*sy)}
let ch;function draw(){const k=sel.value;const pts=D.map(r=>({x:+r[k],y:+r.flavio_pct_1st_round,uf:r.uf}));
document.getElementById('corr').textContent='Pearson r = '+corr(pts.map(p=>p.x),pts.map(p=>p.y)).toFixed(2);if(ch)ch.destroy();
ch=new Chart(document.getElementById('sc'),{type:'scatter',data:{datasets:[{data:pts,pointRadius:5,pointBackgroundColor:pts.map(p=>p.y>=50?'#2a78d6':'#e24b4a')}]},
 options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:t=>t.raw.uf+': '+k+' '+t.raw.x+' · Flávio '+t.raw.y+'%'}}},
 scales:{x:{title:{display:true,text:k}},y:{min:20,max:75,title:{display:true,text:'Flávio Bolsonaro % (1st round)'}}}},
 plugins:[{id:'lbl',afterDatasetsDraw:c=>{const ctx=c.ctx;ctx.font='10px sans-serif';ctx.fillStyle='#222';c.getDatasetMeta(0).data.forEach((p,i)=>ctx.fillText(pts[i].uf,p.x+6,p.y+3))}}]})}
sel.addEventListener('change',draw);draw();
let h='<table><tr>'+cols.map(c=>'<th>'+c+'</th>').join('')+'</tr>';D.forEach(r=>{h+='<tr>'+cols.map(c=>'<td>'+r[c]+'</td>').join('')+'</tr>'});document.getElementById('tb').innerHTML=h+'</table>';
</script>""" + FOOT
write("03_estados_2026.html", html)
