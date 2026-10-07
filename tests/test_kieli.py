"""Kieliversioiden testit (suomi / englanti).

Nämä eivät ole fysiikan validointia vaan varmistavat, että kielen vaihto on täydellinen
eikä vaikuta laskentaan. Tunnukset K01–K03.
"""
import re
from conftest import INDEX

TYPES = ["tank", "pump", "prv", "check", "throttle", "owfc", "dcv43", "dcv42", "cyl", "scyl", "motor", "gauge", "flowm"]


def _all_components(sim):
    comps = [{"id": f"c{i+1}", "type": t, "x": 100 + i * 150, "y": 200, "rot": 0, "label": f"X{i}",
              "p": {"kind": "saato"} if t == "pump" else ({"ori": "pysty"} if t in ("cyl", "scyl") else {})}
             for i, t in enumerate(TYPES)]
    probes = [{"kind": k, "target": tg} for k, tg in
              [("p", "c2:P"), ("q", "c2:P"), ("F", "c9"), ("v", "c9"), ("F", "c11"), ("v", "c11")]]
    sim.call("loadCircuit", {"comps": comps, "wires": [], "probes": probes})
    sim.call("run", 0.2)


def test_K01_englanninkieliset_tekstit_kattavat(sim):
    """Jokaisen komponentin ominaisuuspaneeli, paletti ja anturit renderöidään englanniksi ilman puuttuvia käännöksiä."""
    sim.call("setLang", "en")
    _all_components(sim)
    for i in range(1, len(TYPES) + 1):
        sim.js(f"""(() => {{const g=document.querySelector('.comp[data-id="c{i}"]');const r=g.getBoundingClientRect();
            g.dispatchEvent(new PointerEvent('pointerdown',{{bubbles:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2,pointerId:1,button:0}}));
            document.querySelector('#cv').dispatchEvent(new PointerEvent('pointerup',{{bubbles:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2,pointerId:1}}));}})()""")
    sim.js("document.querySelector('#helpBtn').click()")
    missing = sim.call("i18nMissing")
    assert not missing, f"K01: kääntämättömiä tekstejä: {missing}"
    body = sim.js("document.body.innerText")
    leftovers = [l for l in body.split("\n") if re.search("[äöÄÖ]", l) and "Seinäjoki" not in l]
    assert not leftovers, f"K01: suomenkielistä tekstiä englanninkielisessä näkymässä: {leftovers[:5]}"


def test_K02_kielen_vaihto_ei_vaikuta_laskentaan(sim):
    def ajo(vaihda):
        sim.call("setLang", "fi")
        sim.call("loadExample", "ex1"); sim.call("run", 1.0)
        if vaihda:
            sim.call("setLang", "en")
        sim.call("setValve", "SV1", 1); sim.call("run", 1.0)
        return sim.call("p", "SYL1", "A"), sim.call("state", "SYL1")["x"]
    assert ajo(False) == ajo(True), "K02: kielen vaihto muutti simulointituloksia"


def test_K03_url_parametri_ja_valitsin(browser):
    page = browser.new_page()
    page.goto(INDEX.as_uri() + "?lang=en")
    page.wait_for_function("window.HydSim !== undefined")
    assert page.evaluate("HydSim.lang()") == "en"
    assert page.evaluate("document.documentElement.lang") == "en"
    assert page.inner_text("#helpBtn") == "Help"
    page.click("[data-lang=fi]")
    assert page.evaluate("HydSim.lang()") == "fi"
    assert page.inner_text("#helpBtn") == "Ohje"
    assert page.evaluate("document.querySelector('[data-lang=fi]').getAttribute('aria-pressed')") == "true"
    page.close()
