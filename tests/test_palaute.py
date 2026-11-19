"""Palautekanavan testit (P01–P07).

Palaute-painike avaa lomakkeen, joka rakentaa valmiiksi täytetyn GitHub-issuen linkin repon
lomakepohjille (.github/ISSUE_TEMPLATE). Nämä eivät ole fysiikan validointia vaan varmistavat,
että linkki osuu oikeisiin kenttiin, piiri tulee mukaan ja lomake ei häiritse simulaattoria.
"""
import json
import re
from urllib.parse import urlsplit, parse_qs

API = "HydSim"
REPO = "Jipirtti/Hydrauliikkasimulaattori"
TEMPLATES = {"fysiikka": ("1-fysiikka.yml", ["tunnus", "ilmio", "odotus", "piiri"]),
             "virhe": ("2-virhe.yml", ["kuvaus", "toisto", "selain", "piiri"]),
             "ehdotus": ("3-ehdotus.yml", ["tarve", "ratkaisu", "fysiikka"])}


def _fill(sim, kind, a="Testihavainto", b="", title="", tunnus=""):
    sim.js("document.querySelector('#palauteBtn').click()")
    sim.js(f"""(() => {{const r=document.querySelector('input[name=spl-kind][value={kind}]');r.checked=true;
        r.dispatchEvent(new Event('change',{{bubbles:true}}));
        document.querySelector('#splTitle').value={json.dumps(title)};
        document.querySelector('#splA').value={json.dumps(a)};
        document.querySelector('#splB').value={json.dumps(b)};
        document.querySelector('#splTunnus').value={json.dumps(tunnus)};}})()""")


def _capture_open(sim):
    sim.js("window.__opened=[];window.open=(u)=>{window.__opened.push(u);return null;};true;")


def _params(url):
    u = urlsplit(url)
    return u, {k: v[0] for k, v in parse_qs(u.query, keep_blank_values=True).items()}


def test_P01_painike_ja_kieli(sim):
    """Palaute-painike on yläpalkissa ja vaihtaa kieltä muiden painikkeiden mukana."""
    assert sim.js("document.querySelector('header.bar #palauteBtn').textContent") == "Palaute"
    sim.call("setLang", "en")
    assert sim.js("document.querySelector('#palauteBtn').textContent") == "Feedback"
    sim.call("setLang", "fi")
    assert sim.js("document.querySelector('#palauteBtn').textContent") == "Palaute"


def test_P02_virhe_linkki_ja_piiri(sim):
    """Virheilmoitus: linkki osuu 2-virhe.yml:n kenttiin ja piiri on sama kuin Tallenna / lataa -teksti."""
    sim.call("loadExample", "ex1")
    _capture_open(sim)
    _fill(sim, "virhe", a="Venttiili ei vaihda asentoa", b="1. Lataa esimerkki 1\n2. Klikkaa venttiiliä", title="Venttiili jumissa")
    sim.js("document.querySelector('#splOpen').click()")
    opened = sim.js("window.__opened")
    assert len(opened) == 1
    u, q = _params(opened[0])
    assert u.netloc == "github.com" and u.path == f"/{REPO}/issues/new"
    assert q["template"] == "2-virhe.yml"
    assert q["title"] == "[Virhe] Venttiili jumissa"
    assert q["kuvaus"].startswith("Venttiili ei vaihda asentoa")
    assert "Tekniset tiedot" in q["kuvaus"] and sim.js(f"{API}.version") in q["kuvaus"]
    assert q["toisto"].startswith("1. Lataa esimerkki 1\n2.")
    assert sim.js(f"{API}.version") in q["selain"]
    assert q["piiri"] == sim.call("serialize")
    assert set(q) - {"template", "title"} <= set(TEMPLATES["virhe"][1])
    assert sim.js("document.querySelector('#palauteModal').classList.contains('open')")


def test_P03_fysiikka_vaatii_perustelun(sim):
    """Fysiikkahavainto: ilman odotettua tulosta linkkiä ei avata; täytettynä kentät osuvat 1-fysiikka.yml:ään."""
    _capture_open(sim)
    _fill(sim, "fysiikka", a="Sylinterin nopeus on liian suuri", b="")
    sim.js("document.querySelector('#splOpen').click()")
    assert sim.js("window.__opened") == []
    assert sim.js("document.querySelector('#splStatus').textContent").startswith("Täytä vähintään")
    sim.js("document.querySelector('#splB').value='v = Q/A = 0,1 m/s'")
    sim.js("document.querySelector('#splTunnus').value='V05'")
    sim.js("document.querySelector('#splOpen').click()")
    _, q = _params(sim.js("window.__opened")[0])
    assert q["template"] == "1-fysiikka.yml" and q["title"].startswith("[Fysiikka] Sylinterin nopeus")
    assert q["odotus"] == "v = Q/A = 0,1 m/s" and q["tunnus"] == "V05"
    assert set(q) - {"template", "title"} <= set(TEMPLATES["fysiikka"][1])


def test_P04_ehdotus_ilman_piiria(sim):
    """Kehitysehdotus: 3-ehdotus.yml, eikä piiriä liitetä (lomakkeessa ei ole piirikenttää)."""
    _capture_open(sim)
    _fill(sim, "ehdotus", a="Tarvitaan paineakku", b="Uusi komponentti")
    assert sim.js("document.querySelector('#splPiiriRow').hidden")
    sim.js("document.querySelector('#splOpen').click()")
    _, q = _params(sim.js("window.__opened")[0])
    assert q["template"] == "3-ehdotus.yml" and q["ratkaisu"] == "Uusi komponentti"
    assert q["tarve"].startswith("Tarvitaan paineakku") and "piiri" not in q


def test_P05_pikanappaimet_eivat_vuoda(sim):
    """Lomakkeen ollessa auki Delete ei poista valittuja komponentteja ja Escape sulkee lomakkeen."""
    sim.call("loadExample", "ex1")
    before = len(json.loads(sim.call("serialize"))["comps"])
    sim.js("document.querySelector('#cv').focus&&document.querySelector('#cv').focus()")
    sim.js("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'a',ctrlKey:true,bubbles:true}))")
    sim.js("document.querySelector('#palauteBtn').click()")
    sim.js("document.querySelector('#splCancel').focus()")
    sim.js("document.querySelector('#splCancel').dispatchEvent(new KeyboardEvent('keydown',{key:'Delete',bubbles:true}))")
    assert len(json.loads(sim.call("serialize"))["comps"]) == before
    sim.js("document.querySelector('#splCancel').dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))")
    assert not sim.js("document.querySelector('#palauteModal').classList.contains('open')")


def test_P06_englanti_ja_ei_suomea(sim):
    """Englanninkielinen lomake: ei suomenkielisiä rivejä; suljettuna lomake ei näy sivun tekstissä."""
    sim.call("setLang", "en")
    body = sim.js("document.body.innerText")
    assert "Simulator feedback" not in body and "Palaute simulaattorista" not in body
    sim.js("document.querySelector('#palauteBtn').click()")
    text = sim.js("document.querySelector('#palauteModal').innerText")
    assert "Simulator feedback" in text and "Open on GitHub" in text
    leftovers = [l for l in text.split("\n") if re.search("[äöÄÖ]", l)]
    assert not leftovers, f"P06: suomenkielistä tekstiä: {leftovers}"


def test_P07_pitka_piiri_leikepoydalle(sim):
    """Liian pitkä piiri ei riko linkkiä: linkki pysyy rajan alla ja piiri ohjataan leikepöydälle."""
    sim.js(f"{API}.__ser={API}.serialize;{API}.serialize=()=>JSON.stringify({{v:1,pad:'x'.repeat(20000)}});")
    _fill(sim, "virhe", a="Iso piiri", b="")
    p = sim.js("SimPalaute._preview()")
    sim.js(f"{API}.serialize={API}.__ser")
    assert len(p["link"]["url"]) <= sim.js("SimPalaute._limits.URL_MAX")
    assert p["link"]["clip"].startswith('{"v":1,"pad":"xxx')
    _, q = _params(p["link"]["url"])
    assert q["piiri"].startswith("(Piiri ei mahtunut linkkiin")
    assert '"pad":"xxx' in p["report"]
