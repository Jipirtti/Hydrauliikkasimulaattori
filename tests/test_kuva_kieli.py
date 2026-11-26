"""Kopioitavan kuvan kieli (KV10): jokaisen kaavion kuvaan piirretyt tekstit (otsikko, selite, lähdemerkintä,
kaavion omat tekstit) ovat valitun kielen tekstejä. Saksankielisessä kuvassa ei saa olla tekstiä, joka on
suomenkielisessä kuvassa mutta ei englanninkielisessä, eikä päinvastoin."""
import re

API_NAME = "HydSim"
# Sanat, jotka ovat samat saksaksi ja englanniksi
SALLITUT = set()
VAIHEET = [
    "",
    "HydSim.loadExample('ex1');HydSim.setValve('SV1',1);HydSim.run(2)",
    "HydSim.loadExample('ex3');HydSim.setValve('SV1',1);HydSim.run(2)",
]

HOOK = """(()=>{if(window.__ft)return;window.__ft=[];
for(const f of ['fillText','strokeText']){const o=CanvasRenderingContext2D.prototype[f];
 CanvasRenderingContext2D.prototype[f]=function(s,...a){if(window.__rec)window.__ft.push(String(s));return o.call(this,s,...a);};}
const xs=XMLSerializer.prototype.serializeToString;XMLSerializer.prototype.serializeToString=function(n){const r=xs.call(this,n);
 if(window.__rec){const d=new DOMParser().parseFromString(r,'image/svg+xml');
  d.querySelectorAll('text,tspan,div,span').forEach(t=>{if(!t.children.length&&t.textContent.trim())window.__ft.push(t.textContent.trim());});}
 return r;};})()"""

KERAA = """async ()=>{const out={};for(const k of SimKuva.ids()){window.__ft=[];window.__rec=true;let ok=true;
 try{await SimKuva.render(k);}catch(e){ok=false;}window.__rec=false;if(ok)out[k]=window.__ft.slice();}return out;}"""


def _sana(x):
    # numerot ja yksiköt eivät kerro kieltä (desimaalipilkku vaihtelee kielittäin)
    return not re.search(r"\d", x) and len(x.strip()) > 2


def test_KV10_kuvan_tekstit_valitulla_kielella(sim):
    page = sim.page
    page.evaluate(HOOK)
    virheet = {}
    for js in VAIHEET:
        T = {}
        for l in ("fi", "en", "de"):
            sim.call("setLang", l)
            if js:
                page.evaluate(js)
            page.wait_for_timeout(150)
            T[l] = page.evaluate(KERAA)
        for k, de in T["de"].items():
            fi, en = set(T["fi"].get(k, [])), set(T["en"].get(k, []))
            for x in de:
                if _sana(x) and x not in SALLITUT and ((x in fi and x not in en) or (x in en and x not in fi)):
                    virheet.setdefault((k, x), js or "alku")
    assert T["de"], "KV10: yhtään kaaviota ei muodostunut"
    assert not virheet, f"KV10: kuvassa vieraskielisiä tekstejä: {list(virheet.items())[:8]}"
