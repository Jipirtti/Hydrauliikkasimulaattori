"""Letkujen mitoituksen ja painehäviön testit (V23–V26, M08, U06, K05).

Odotusarvot lasketaan tässä tiedostossa itsenäisesti öljyn arvoista ν = 46 mm²/s ja ρ = 870 kg/m³
(ISO VG 46, 40 °C), samoista kuin simulaattorissa.
"""
import json
import math
import re
from test_validointi import areas

NU = 46e-6
RHO = 870.0
MU = RHO * NU


def _adv(sim, example):
    sim.call("setMode", "advanced")
    sim.call("loadExample", example)


def test_V23_laminaari_painehavio(sim, check):
    """Hagen–Poiseuille: Δp = 128·μ·L·Q / (π·d⁴), kun Re < 2300."""
    _adv(sim, "ex1")
    sim.call("setHose", "SV1.A", "SYL1.A", {"di": 6.3, "L": 10})
    sim.call("run", 1); sim.call("setValve", "SV1", 1); sim.call("run", 0.8)
    h = sim.call("hose", "SV1.A", "SYL1.A")
    d, L, Q = 6.3e-3, 10.0, abs(h["Q"]) / 60000
    Re = 4 * Q / (math.pi * d * NU)
    assert Re < 2000, f"V23: virtaus ei ole laminaarinen (Re {Re:.0f})"
    dp_meas = sim.call("p", "SV1", "A") - sim.call("p", "SYL1", "A")
    check("V23", "Laminaari letkuhäviö Δp = 128·μ·L·Q / (π·d⁴)", dp_meas,
          128 * MU * L * Q / (math.pi * d ** 4) / 1e5, 0.02, "bar")


def test_V24_turbulentti_painehavio(sim, check):
    """Blasius: λ = 0,316·Re^−0,25 ja Δp = λ·(L/d)·ρ·v²/2, kun Re > 4000."""
    _adv(sim, "ex5"); sim.call("setParam", "SYL1", "L", 2000); sim.call("reset")
    sim.call("setHose", "SV2.A", "SYL1.B", {"di": 12.5, "L": 1})
    sim.call("run", 1); sim.call("setValve", "SV1", 1); sim.call("run", 1.5)
    h = sim.call("hose", "SV2.A", "SYL1.B")
    d, L, Q = 12.5e-3, 1.0, abs(h["Q"]) / 60000
    v = Q / (math.pi / 4 * d ** 2); Re = v * d / NU
    assert Re > 4500, f"V24: virtaus ei ole turbulentti (Re {Re:.0f})"
    lam = 0.316 * Re ** -0.25
    dp_meas = abs(sim.call("p", "SYL1", "B") - sim.call("p", "SV2", "A"))
    check("V24", "Turbulentti letkuhäviö Δp = 0,316·Re^−0,25·(L/d)·ρv²/2", dp_meas,
          lam * L / d * RHO * v ** 2 / 2 / 1e5, 0.02, "bar")


def test_V25_virtausnopeus_ja_varoitus(sim, check):
    _adv(sim, "ex1"); sim.call("run", 1); sim.call("setValve", "SV1", 1); sim.call("run", 0.8)
    assert "letkunopeus" not in sim.call("warningCodes"), "V25: esimerkin letkukoot ylittävät suosituksen"
    h = sim.call("hose", "SV1.A", "SYL1.A"); a = areas(sim, "SYL1")
    v_cyl = sim.call("state", "SYL1")["v"]
    check("V25a", "Letkun virtausnopeus v = v_syl·A / (π/4·di²)", h["v"],
          v_cyl * a["A_mm2"] / (math.pi / 4 * h["di"] ** 2), 0.01, "m/s")
    sim.call("setHose", "SV1.A", "SYL1.A", {"di": 6.3}); sim.call("run", 0.3)
    assert "letkunopeus" in sim.call("warningCodes"), "V25: varoitus puuttuu, vaikka nopeus ylittää painelinjan suosituksen"


def test_V26_linjatyypit_ja_tilavuus(sim, check):
    _adv(sim, "ex1")
    types = {(w["a"], w["b"]): t for w, t in zip(json.loads(sim.call("serialize"))["wires"], sim.call("hoseTypes"))}
    assert types[("c2:S", "c1:T")] == "imu", "V26: pumpun imulinjaa ei tunnistettu"
    assert types[("c6:T", "c7:T")] == "paluu", "V26: paluulinjaa ei tunnistettu"
    assert types[("c6:A", "c8:A")] == "paine", "V26: sylinterilinjaa ei tunnistettu painelinjaksi"
    h = sim.call("hose", "SV1.A", "SYL1.A")
    check("V26", "Letkun öljytilavuus V = π/4·di²·L", h["V"], math.pi / 4 * (h["di"] / 1000) ** 2 * h["L"] * 1000, 0.001, "L")


def test_M08_yksinkertainen_ei_letkuhavioita(sim):
    sim.call("setMode", "simple"); sim.call("loadExample", "ex1")
    sim.call("setHose", "SV1.A", "SYL1.A", {"di": 6.3, "L": 10})
    sim.call("run", 1); sim.call("setValve", "SV1", 1); sim.call("run", 0.8)
    assert abs(sim.call("p", "SV1", "A") - sim.call("p", "SYL1", "A")) < 1e-9, "M08: yksinkertaisessa mallissa letkussa on painehäviö"
    assert sim.call("hose", "SV1.A", "SYL1.A")["dpCalc"] > 1, "M08: laskennallista painehäviötä ei näytetä vertailuksi"


def _click_hose(sim, a, b):
    sim.js(f"""(() => {{const g=[...document.querySelectorAll('#lWires .wire')].find(g=>{{const w=HydSim._wire(g.dataset.w);return w&&((w.a==='{a}'&&w.b==='{b}')||(w.a==='{b}'&&w.b==='{a}'));}});
      const path=g.querySelector('.wb');const L=path.getTotalLength();const pt=path.getPointAtLength(L/2);const sp=new DOMPoint(pt.x,pt.y).matrixTransform(path.getScreenCTM());
      const o={{bubbles:true,pointerId:1,button:0,pointerType:'mouse',clientX:sp.x,clientY:sp.y}};
      document.elementFromPoint(sp.x,sp.y).dispatchEvent(new PointerEvent('pointerdown',o));document.querySelector('#cv').dispatchEvent(new PointerEvent('pointerup',o));}})()""")


def test_U06_mitoitusapu_ja_tallennus(sim):
    _adv(sim, "ex1"); sim.call("pause")
    _click_hose(sim, "c6:A", "c8:A")
    assert sim.js("!!document.querySelector('#hhres')"), "U06: letkun mitoitusapu ei avautunut"
    sim.js("(()=>{const q=document.querySelector('[data-hh=Q]');q.value='40';q.dispatchEvent(new Event('input',{bubbles:true}));const p=document.querySelector('[data-hh=p]');p.value='100';p.dispatchEvent(new Event('input',{bubbles:true}));})()")
    sim.js("document.querySelector('#hApply').click()")
    di = sim.call("hose", "SV1.A", "SYL1.A")["di"]
    v = 40 / 60000 / (math.pi / 4 * (di / 1000) ** 2)
    assert v <= 5.0 and di in (5, 6.3, 8, 10, 12.5, 16, 19, 25, 31.5, 38, 51), f"U06: mitoitusapu antoi {di} mm (v {v:.2f} m/s)"
    smaller = [d for d in (5, 6.3, 8, 10, 12.5, 16, 19, 25) if d < di]
    assert not smaller or 40 / 60000 / (math.pi / 4 * (smaller[-1] / 1000) ** 2) > 5.0, "U06: mitoitusapu ei valinnut pienintä riittävää kokoa"
    saved = json.loads(sim.call("serialize"))
    w = next(w for w in saved["wires"] if {w["a"], w["b"]} == {"c6:A", "c8:A"})
    assert w.get("h", {}).get("di") == di, "U06: letkun koko ei tallentunut piiriin"


def test_K05_letkupaneeli_englanniksi(sim):
    sim.call("setLang", "en"); _adv(sim, "ex1"); sim.call("run", 0.5)
    _click_hose(sim, "c6:A", "c8:A")
    text = sim.js("document.querySelector('#insp').innerText")
    assert not sim.call("i18nMissing"), f"K05: kääntämättömiä tekstejä: {sim.call('i18nMissing')}"
    left = [l for l in text.split("\n") if re.search("[äöÄÖ]", l)]
    assert not left, f"K05: suomenkielistä tekstiä letkupaneelissa: {left[:5]}"
    assert "Inner diameter" in text and "Reynolds number" in text, "K05: letkun mitoituskentät puuttuvat"
