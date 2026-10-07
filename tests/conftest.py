"""Pytest-asetukset hydrauliikkasimulaattorin validointitesteille.

Testit avaavat index.html-tiedoston headless-Chromiumissa ja ohjaavat simulaattoria
sen testirajapinnan window.HydSim kautta. Jokainen tarkistus kirjataan raporttiin
validointiraportti.md, joka liitetään GitHub Actions -ajon yhteenvetoon.
"""
import os
import pathlib
import datetime
import pytest
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
REPORT = ROOT / "validointiraportti.md"
_rows = []


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def sim(browser):
    """Tuore simulaattori-sivu jokaiselle testille."""
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(INDEX.as_uri())
    page.wait_for_function("window.HydSim !== undefined")
    page.evaluate("localStorage.clear()")
    page.evaluate("HydSim.setLang('fi')")   # testiselaimen oletuskieli on englanti

    class Sim:
        def js(self, expr):
            return page.evaluate(expr)

        def call(self, fn, *args):
            return page.evaluate(f"(a) => HydSim.{fn}(...a)", list(args))

    s = Sim()
    s.errors = errors
    yield s
    assert not errors, f"JavaScript-virheitä: {errors}"
    assert not s.call("numericError"), "Simulaattori ilmoitti numeerisesta virheestä"
    page.close()


@pytest.fixture
def check(request):
    """check(id, kuvaus, mitattu, odotettu, toleranssi_suht) kirjaa ja tarkistaa arvon."""
    def _check(vid, desc, measured, expected, rel_tol, unit=""):
        ok = abs(measured - expected) <= rel_tol * abs(expected)
        _rows.append((vid, desc, measured, expected, rel_tol, unit, ok))
        assert ok, (f"{vid} {desc}: mitattu {measured:.4g} {unit}, odotettu {expected:.4g} {unit} "
                    f"(toleranssi ±{rel_tol*100:.1f} %)")
    return _check


def pytest_sessionfinish(session, exitstatus):
    if not _rows:
        return
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sha = os.environ.get("GITHUB_SHA", "paikallinen")[:7]
    lines = [f"# Validointiraportti", "",
             f"Ajettu {now}, versio `{sha}`. Tarkistuksia {len(_rows)}, "
             f"hyväksytty {sum(r[6] for r in _rows)}.", "",
             "| ID | Ilmiö | Mitattu | Odotettu (käsinlasku) | Toleranssi | Tulos |",
             "| --- | --- | --- | --- | --- | --- |"]
    for vid, desc, m, e, tol, unit, ok in _rows:
        lines.append(f"| {vid} | {desc} | {m:.4g} {unit} | {e:.4g} {unit} | ±{tol*100:.1f} % | {'✅' if ok else '❌'} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
