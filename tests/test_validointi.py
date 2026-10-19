"""Hydrauliikkasimulaattorin ilmiöiden automaattinen validointi.

Jokainen testi vastaa VALIDOINTI.md-tiedoston riviä samalla tunnuksella (V01, V02, ...).
Odotusarvot lasketaan tässä tiedostossa käsinlaskukaavoilla simulaattorin parametreista,
jotta opettaja voi tarkistaa kaavat ja testi suojaa ilmiötä muutoksilta.
Yksiköt: p bar, Q L/min, pinta-alat mm², voimat N, nopeudet m/s.
"""
import math

G = 9.81


def bar_to_npmm2(p):          # 1 bar = 0,1 N/mm²
    return p / 10.0


def areas(sim, label):
    """Pinta-alat lasketaan itsenäisesti mitoista, ei simulaattorin omalla koodilla."""
    c = sim.call("param", label)
    A = math.pi / 4 * c["D"] ** 2
    a = math.pi / 4 * c.get("d", 0) ** 2
    return {"A_mm2": A, "Aring_mm2": A - a}


def test_V00_sylinterin_geometria(sim, check):
    sim.call("loadExample", "ex1")
    ref = areas(sim, "SYL1"); got = sim.call("areas", "SYL1")
    check("V00a", "Männän pinta-ala A = π/4·D²", got["A_mm2"], ref["A_mm2"], 0.001, "mm²")
    check("V00b", "Rengaspinta-ala A − a = π/4·(D² − d²)", got["Aring_mm2"], ref["Aring_mm2"], 0.001, "mm²")


# ---------------------------------------------------------------- pumppu ja paineenrajoitus
def test_V01_paineenrajoitus_rajaa_paineen(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 3)
    prv = sim.call("param", "PRV1")
    q = sim.call("q", "PRV1", "P")
    # p = ps + Q/Qn · Δp(Qn)   (venttiilin ominaiskäyrä)
    expected = prv["ps"] + q / prv["Qn"] * prv["dpo"]
    check("V01", "PRV rajaa paineen, p = ps + (Q/Qn)·Δpo", sim.call("p", "P1", "P"), expected, 0.01, "bar")


def test_V02_pumpun_tuotto_ja_vuoto(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 3)
    pp = sim.call("param", "P1"); p = sim.call("p", "P1", "P")
    q_th = pp["Vg"] * pp["n"] / 1000
    q_leak = q_th * (1 - pp["etav"]) * p / pp["pr"]          # vuoto kasvaa lineaarisesti paineen mukana
    check("V02", "Pumpun tuotto Q = Vg·n/1000 − vuoto(p)", -sim.call("q", "P1", "P"), q_th - q_leak, 0.01, "L/min")


def test_V03_ulosajonopeus(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.2)
    a = areas(sim, "SYL1")
    q = sim.call("q", "SV1", "P")                              # venttiiliin tuleva tuotto
    expected = q / 60000 / (a["A_mm2"] * 1e-6)
    check("V03", "Ulosajonopeus v = Q / A", sim.call("state", "SYL1")["v"], expected, 0.03, "m/s")


def test_V04_sisaanajonopeus(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 4)
    sim.call("setValve", "SV1", -1); sim.call("run", 0.8)
    a = areas(sim, "SYL1")
    q = sim.call("q", "SV1", "P")
    expected = -q / 60000 / (a["Aring_mm2"] * 1e-6)
    check("V04", "Sisäänajonopeus v = Q / (A − a)", sim.call("state", "SYL1")["v"], expected, 0.03, "m/s")


def test_V05_kuorma_maaraa_paineen(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.2)
    c = sim.call("param", "SYL1"); a = areas(sim, "SYL1"); v = sim.call("state", "SYL1")["v"]
    pB = sim.call("p", "SYL1", "B")
    # voimatasapaino: pA·A = F + Fc + cv·v + pB·(A − a)
    F = c["F"] + c["Fc"] + c["cv"] * v + bar_to_npmm2(pB) * a["Aring_mm2"]
    expected = F / a["A_mm2"] * 10
    check("V05", "Paine kuorman mukaan, pA = (F + Fc + cv·v + pB·(A−a)) / A", sim.call("p", "SYL1", "A"), expected, 0.02, "bar")


def test_V06_suurin_tyontovoima(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 4)
    a = areas(sim, "SYL1"); p = sim.call("p", "SYL1", "A")
    check("V06", "Päädyssä F = p·A (kN)", sim.call("forceKN", "SYL1"), bar_to_npmm2(p) * a["A_mm2"] / 1000, 0.01, "kN")
    assert abs(sim.call("state", "SYL1")["x"] - sim.call("param", "SYL1")["L"] / 1000) < 1e-6, "Sylinteri ei ole iskun päässä"


def test_V07_massatase(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 2)
    tanks = lambda: sum(sim.call("state", s)["lvl"] for s in ("S1", "S2", "S3"))
    v0 = tanks(); sim.call("setValve", "SV1", 1); sim.call("run", 4)
    a = areas(sim, "SYL1"); L = sim.call("param", "SYL1")["L"]
    rod_volume_l = (a["A_mm2"] - a["Aring_mm2"]) * L / 1e6        # männänvarren syrjäyttämä tilavuus
    check("V07", "Massatase: säiliöistä poistuu varren tilavuus", v0 - tanks(), rod_volume_l, 0.04, "L")


def test_V08_kuorman_pito_keskiasennossa(sim):
    sim.call("loadExample", "ex1"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.0)
    sim.call("setValve", "SV1", 0); sim.call("run", 0.5)
    x0 = sim.call("state", "SYL1")["x"]; sim.call("run", 5)
    assert abs(sim.call("state", "SYL1")["x"] - x0) < 0.001, "V08: suljettu keskiasento ei pidä sylinteriä paikallaan"


# ---------------------------------------------------------------- nopeudensäätö ja paineen vahvistuminen
def test_V09_paineen_vahvistuminen_meter_out(sim, check):
    sim.call("loadExample", "ex2"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.5)
    c = sim.call("param", "SYL1"); a = areas(sim, "SYL1"); v = sim.call("state", "SYL1")["v"]
    pA = sim.call("p", "SYL1", "A")
    # pB = (pA·A − F − Fc − cv·v) / (A − a)
    expected = (bar_to_npmm2(pA) * a["A_mm2"] - c["F"] - c["Fc"] - c["cv"] * v) / a["Aring_mm2"] * 10
    check("V09", "Meter-out: pB = (pA·A − F) / (A − a)", sim.call("p", "SYL1", "B"), expected, 0.02, "bar")
    assert sim.call("p", "SYL1", "B") > pA, "V09: rengaspuolen paine ei noussut yli järjestelmäpaineen"
    assert sim.call("q", "PRV1", "P") > 1, "V09: ylimääräinen tuotto ei mene paineenrajoitusventtiilin kautta"


# ---------------------------------------------------------------- hydraulimoottori
def test_V10_moottorin_nopeus(sim, check):
    sim.call("loadExample", "ex3"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 4)
    m = sim.call("param", "M1")
    dp = sim.call("p", "M1", "A") - sim.call("p", "M1", "B")
    q = abs(sim.call("q", "FI1", "A")) - m["leak"] * dp / 100
    check("V10", "Moottorin nopeus n = (Q − vuoto) / Vg", sim.call("rpm", "M1"), q * 1000 / m["Vg"], 0.02, "r/min")


def test_V11_moottorin_vaanto(sim, check):
    sim.call("loadExample", "ex3"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 4)
    m = sim.call("param", "M1"); w = sim.call("rpm", "M1") * 2 * math.pi / 60
    dp = sim.call("p", "M1", "A") - sim.call("p", "M1", "B")
    check("V11a", "Vääntö T = Δp·Vg·ηhm / (20π)", sim.call("torqueNm", "M1"), dp * m["Vg"] * m["etahm"] / (20 * math.pi), 0.01, "Nm")
    check("V11b", "Tasainen ajo: T = TL + b·ω", sim.call("torqueNm", "M1"), m["TL"] + m["b"] * w, 0.02, "Nm")


# ---------------------------------------------------------------- yksitoiminen pystysylinteri
def test_V12_nostopaine(sim, check):
    sim.call("loadExample", "ex4"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 0.6)
    c = sim.call("param", "SYL1"); st = sim.call("state", "SYL1"); a = areas(sim, "SYL1")
    F = c["m"] * G + c["F0"] + c["k"] * st["x"] * 1000 + c["Fc"] + c["cv"] * st["v"]
    check("V12", "Nosto: p = (m·g + F0 + k·x + Fc + cv·v) / A", sim.call("p", "SYL1", "A"), F / a["A_mm2"] * 10, 0.02, "bar")


def test_V13_hallittu_lasku(sim, check):
    sim.call("loadExample", "ex4"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 2.0)
    sim.call("setValve", "SV1", -1); sim.call("run", 0.6)
    a = areas(sim, "SYL1"); q = sim.call("q", "KV1", "A")
    check("V13", "Lasku kuristimen kautta: v = Q_kuristin / A", -sim.call("state", "SYL1")["v"],
          q / 60000 / (a["A_mm2"] * 1e-6), 0.03, "m/s")


# ---------------------------------------------------------------- painesäädetty pumppu
def test_V14_painesaadetty_pumppu(sim):
    sim.call("loadExample", "ex1")
    sim.call("setParam", "P1", "kind", "saato"); sim.call("setParam", "P1", "pc", 90)
    sim.call("run", 3)
    p = sim.call("p", "P1", "P")
    assert 87 <= p <= 93, f"V14: painesäädetyn pumpun paine {p:.1f} bar ei ole säätöpaineen 90 bar lähellä"
    assert sim.call("q", "PRV1", "P") < 0.1, "V14: paineenrajoitusventtiilin ei pitäisi avautua"


# ---------------------------------------------------------------- numeriikka
def test_V15_toistettavuus(sim):
    def ajo():
        sim.call("loadExample", "ex2"); sim.call("run", 1)
        sim.call("setValve", "SV1", 1); sim.call("run", 2)
        return sim.call("p", "SYL1", "B"), sim.call("state", "SYL1")["x"]
    assert ajo() == ajo(), "V15: kaksi samaa ajoa antoivat eri tuloksen"


def test_V16_varoitukset(sim):
    sim.call("loadExample", "ex1"); sim.call("run", 2)
    assert "ylipaine" not in sim.call("warningCodes"), "V16: ylipainevaroitus ilman syytä"
    sim.call("setParam", "PRV1", "ps", 300); sim.call("setValve", "SV1", 1); sim.call("run", 5)
    assert "ylipaine" in sim.call("warningCodes"), "V16: ylipainevaroitus puuttuu (300 bar > sylinterin 250 bar)"


# ---------------------------------------------------------------- riippuva kuorma (versio 1.2.0)
def test_V17_riippuva_kuorma(sim, check):
    """Männänvarsi alaspäin: paino avustaa ulosajoa ja sisäänajo vaatii pB·(A − a) − pA·A = m·g + Fc + cv·v."""
    sim.call("loadExample", "ex1")
    for k, v in (("ori", "alas"), ("m", 1000), ("F", 0), ("x0", 300)):
        sim.call("setParam", "SYL1", k, v)
    sim.call("reset"); sim.call("run", 1.0)
    assert abs(sim.call("state", "SYL1")["x"] - 0.3) < 1e-6, "V17: riippuva kuorma ei pysynyt alhaalla"
    sim.call("setValve", "SV1", -1); sim.call("run", 1.0)
    c = sim.call("param", "SYL1"); a = areas(sim, "SYL1"); v = sim.call("state", "SYL1")["v"]
    assert v < -0.01, "V17: sylinteri ei nostanut riippuvaa kuormaa"
    F_hydr = bar_to_npmm2(sim.call("p", "SYL1", "B")) * a["Aring_mm2"] - bar_to_npmm2(sim.call("p", "SYL1", "A")) * a["A_mm2"]
    check("V17", "Riippuvan kuorman nosto: pB·(A−a) − pA·A = m·g + Fc + cv·|v|", F_hydr,
          c["m"] * G + c["Fc"] + c["cv"] * abs(v), 0.02, "N")


# ---------------------------------------------------------------- pikaliikekytkentä
def test_V18_pikaliike_nopeus(sim, check):
    sim.call("loadExample", "ex5"); sim.call("setParam", "SYL1", "L", 2000); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.5)
    a = areas(sim, "SYL1"); q = sim.call("q", "SV1", "P")
    # regeneratiivinen ulosajo: v·A = Q + v·(A − a)  →  v = Q / a
    check("V18", "Pikaliike: v = Q / a (varren pinta-ala)", sim.call("state", "SYL1")["v"],
          q / 60000 / ((a["A_mm2"] - a["Aring_mm2"]) * 1e-6), 0.03, "m/s")


def test_V19_pikaliike_voima(sim, check):
    sim.call("loadExample", "ex5"); sim.call("setParam", "SYL1", "ori", "pysty"); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 3)
    a = areas(sim, "SYL1"); p = sim.call("p", "SYL1", "A")
    rod = a["A_mm2"] - a["Aring_mm2"]
    assert sim.call("state", "SYL1")["x"] < 0.002, "V19: pikaliike nosti kuorman, vaikka p·a < m·g"
    check("V19", "Pikaliikkeen voima F = p·a", sim.call("forceKN", "SYL1"), bar_to_npmm2(p) * rod / 1000, 0.03, "kN")
    sim.call("setValve", "SV2", 1); sim.call("run", 1.5)
    assert sim.call("state", "SYL1")["v"] > 0.1, "V19: normaali kytkentä ei nostanut kuormaa"


# ---------------------------------------------------------------- rinnakkaiset toimilaitteet
def test_V20_rinnakkainen_moottori(sim, check):
    sim.call("loadExample", "ex6"); sim.call("setParam", "M1", "TL", 0); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 5)
    m = sim.call("param", "M1"); q = sim.call("q", "SV1", "P")
    dp = sim.call("p", "M1", "A") - sim.call("p", "M1", "B")
    check("V20a", "Kevyt moottori vie koko virtauksen: n = (Q − vuoto) / Vg", sim.call("rpm", "M1"),
          (q - m["leak"] * dp / 100) * 1000 / m["Vg"], 0.03, "r/min")
    assert sim.call("state", "SYL1")["x"] < 0.05, "V20: sylinteri nousi, vaikka moottori tarvitsee pienemmän paineen"
    sim.call("loadExample", "ex6"); sim.call("setParam", "M1", "TL", 40); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.5)
    a = areas(sim, "SYL1"); q = sim.call("q", "SV1", "P")
    check("V20b", "Raskas moottori pysyy, sylinteri saa virtauksen: v = Q / A", sim.call("state", "SYL1")["v"],
          q / 60000 / (a["A_mm2"] * 1e-6), 0.03, "m/s")
    assert abs(sim.call("rpm", "M1")) < 20, "V20: moottori pyörii, vaikka sen kuorma vaatii yli asetuspaineen"


# ---------------------------------------------------------------- virranjakoventtiili
def test_V21_virranjako(sim, check):
    sim.call("loadExample", "ex7"); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 2)
    r = sim.call("param", "VJ1")["r"] / 100
    qP = sim.call("q", "VJ1", "P"); qA = -sim.call("q", "VJ1", "A"); qB = -sim.call("q", "VJ1", "B")
    check("V21a", "Virranjako: Q_A = r·Q_P", qA, r * qP, 0.01, "L/min")
    check("V21b", "Virranjako: Q_B = (1 − r)·Q_P", qB, (1 - r) * qP, 0.01, "L/min")
    a = areas(sim, "SYL1")
    check("V21c", "Sylinterin nopeus jaetulla virralla v = Q_A / A", sim.call("state", "SYL1")["v"],
          qA / 60000 / (a["A_mm2"] * 1e-6), 0.03, "m/s")
    for vv in ("VV1", "VV2"):
        assert abs(sim.call("q", vv, "A")) < 0.05, f"V21: {vv} päästää virtausta väärään suuntaan"


def test_V22_virranjako_paadyssa(sim):
    sim.call("loadExample", "ex7"); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 7)
    L = sim.call("param", "SYL1")["L"] / 1000
    assert abs(sim.call("state", "SYL1")["x"] - L) < 1e-6, "V22: sylinteri ei ajanut päätyyn"
    assert abs(sim.call("rpm", "M1")) < 5, "V22: moottori pyörii, vaikka virranjakajan toinen lähtö on tukossa"
    assert sim.call("q", "PRV1", "P") > 0.95 * -sim.call("q", "P1", "P"), "V22: pumpun tuotto ei ohjautunut paineenrajoitukselle"
