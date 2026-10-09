"""Render assets/og-image.png (1200x630), the link preview image used by WhatsApp and other apps.
Needs Playwright with Chromium. Reads the national Chamber shares straight from the built index.html."""
import asyncio, json, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent

CARD = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:630px;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;background:#fbfbf9;color:#1e1e1c;display:flex}
.l{width:520px;padding:56px 0 48px 64px;display:flex;flex-direction:column}
h1{font-size:50px;line-height:1.08;margin:0 0 18px;letter-spacing:-.5px}
p{font-size:24px;color:#666;margin:0}
.k{margin-top:auto;font-size:18px;color:#888;line-height:1.5}
.r{flex:1;padding:52px 60px 40px 30px;display:flex;flex-direction:column;justify-content:center}
.row{display:flex;align-items:center;gap:12px;margin:4px 0}.y{width:48px;font-size:16px;color:#777;text-align:right}
.b{flex:1;display:flex;height:34px;border-radius:4px;overflow:hidden}
.lg{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:16px;font-size:14px;color:#555;padding-left:60px}.lg i{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:5px;vertical-align:-1px}
</style></head><body><div class="l"><h1>Brazilian General Elections after Redemocratization</h1><p>1990 to 2026 · a data driven look at what shapes our choices</p>
<div class="k">Chamber, Senate, governors and presidents by ideological spectrum, for Brazil and every state</div></div>
<div class="r" id="r"></div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.goto((ROOT / "index.html").as_uri())
        await pg.wait_for_timeout(400)
        data = await pg.evaluate("({br:COMP.camara.BR,spec:SPEC,color:COLOR,names:STR.en.spec})")
        await pg.set_content(CARD)
        await pg.evaluate("""d=>{const order=[...d.spec].reverse();let h='';Object.keys(d.br).sort().forEach(y=>{const r=d.br[y];if(!r||!r.total)return;
          h+='<div class="row"><span class="y">'+y+'</span><div class="b">'+order.map(s=>'<span style="width:'+((r[s]||0)/r.total*100)+'%;background:'+d.color[s]+'"></span>').join('')+'</div></div>'});
          h+='<div class="lg">'+order.map(s=>'<span><i style="background:'+d.color[s]+'"></i>'+d.names[s]+'</span>').join('')+'</div>';document.getElementById('r').innerHTML=h}""", data)
        await pg.screenshot(path=str(ROOT / "assets" / "og-image.png"))
        await b.close()

asyncio.run(main())
