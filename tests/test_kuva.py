"""Kaavion kopiointi kuvana (SimKuva) – testit KV01–KV04.

Sama testi kaikissa simulaattoreissa; NAKYMAT kertoo, mitkä kaaviot kussakin näkymässä on.
"""
import pytest
from conftest import INDEX

API = "HydSim"
NAKYMAT = [('', ['piiri', 'mittaukset'])]


@pytest.fixture
def page(browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, locale="fi-FI")
    ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(INDEX.as_uri() + "?lang=fi")
    pg.wait_for_function(f"window.{API} !== undefined && window.SimKuva !== undefined")
    pg.wait_for_timeout(600)
    yield pg
    assert not errs, f"JavaScript-virheet: {errs}"
    ctx.close()


def nayta(pg, js):
    if js:
        pg.evaluate(js)
        pg.wait_for_timeout(300)


def nakyvat(pg):
    return pg.evaluate("[...document.querySelectorAll('.skv-btn')].filter(b=>b.offsetParent).map(b=>b.dataset.skv).sort()")


def test_KV01_painike_jokaisessa_kaaviossa(page):
    """Jokaisen näkyvän kaavion kulmassa on Kopioi kuva -painike, ja teksti vaihtuu kielen mukana."""
    for js, ids in NAKYMAT:
        nayta(page, js)
        assert nakyvat(page) == sorted(ids), f"KV01: näkymä {js or 'alku'}: {nakyvat(page)} ≠ {sorted(ids)}"
        assert set(page.evaluate("[...document.querySelectorAll('.skv-btn')].filter(b=>b.offsetParent).map(b=>b.textContent)")) == {"Kopioi kuva"}
    page.evaluate(f"window.{API}.setLang('en')")
    page.wait_for_timeout(100)
    assert set(page.evaluate("[...document.querySelectorAll('.skv-btn')].map(b=>b.textContent)")) == {"Copy image"}


def test_KV02_kuva_vaalea_ja_tarkka(page):
    """Kuva on valkopohjainen ja vähintään kaksinkertaisella tarkkuudella; näytön teema ja tarkkuus palautuvat."""
    page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
    dpr0 = page.evaluate("devicePixelRatio")
    for js, ids in NAKYMAT:
        nayta(page, js)
        for k in ids:
            r = page.evaluate(f"""SimKuva.render('{k}').then(c=>{{const g=c.getContext('2d');const px=[...g.getImageData(1,1,1,1).data];
                let tumma=0;const d=g.getImageData(0,0,c.width,c.height).data;for(let i=0;i<d.length;i+=4*97)if(d[i]<200)tumma++;
                return {{w:c.width,h:c.height,px,tumma}};}})""")
            assert r["px"] == [255, 255, 255, 255], f"KV02 {k}: tausta {r['px']}"
            assert r["w"] >= 2 * 360 and r["h"] >= 2 * 100, f"KV02 {k}: koko {r['w']}×{r['h']}"
            assert r["tumma"] > 50, f"KV02 {k}: kuvassa ei ole sisältöä"
            assert page.evaluate("document.documentElement.getAttribute('data-theme')") == "dark", f"KV02 {k}: teema ei palautunut"
            assert page.evaluate("devicePixelRatio") == dpr0, f"KV02 {k}: tarkkuus ei palautunut"


def test_KV03_kopiointi_leikepoydalle(page):
    """Kopioi kuva -painike vie PNG-kuvan leikepöydälle ja näyttää ilmoituksen."""
    js, ids = NAKYMAT[0]
    nayta(page, js)
    page.click(f'.skv-btn[data-skv="{ids[0]}"]')
    page.wait_for_selector(".skv-toast")
    assert page.inner_text(".skv-toast") == "Kuva kopioitu leikepöydälle"
    tyypit = page.evaluate("navigator.clipboard.read().then(it=>it[0].types)")
    assert tyypit == ["image/png"], f"KV03: {tyypit}"


def test_KV04_varaikkuna_kun_kopiointi_estetty(page):
    """Jos selain estää kopioinnin, kuva näytetään ikkunassa, josta sen voi kopioida tai tallentaa."""
    js, ids = NAKYMAT[0]
    nayta(page, js)
    page.evaluate("()=>{navigator.clipboard.write=()=>Promise.reject(new Error('estetty'));}")
    assert page.evaluate(f"SimKuva.copy('{ids[0]}')") is False
    assert page.is_visible("#skvModal img")
    assert page.get_attribute("#skvModal img", "src").startswith("data:image/png")
    assert page.get_attribute("#skvModal a", "download").endswith(".png")
    page.keyboard.press("Escape")
    assert page.locator("#skvModal").count() == 0
