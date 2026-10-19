"""Yksinkertaisen ja kehittyneen simulointimallin testit (M01–M07).

Yksinkertaisessa mallissa kitka, vuodot, hyötysuhteet ja venttiilien painehäviöt on jätetty pois,
joten tulosten pitää vastata suoraan oppikirjan perusyhtälöitä ilman häviötermejä.
Odotusarvot lasketaan tässä tiedostossa itsenäisesti mitoista (ks. areas()).
"""
import math
from test_validointi import areas, bar_to_npmm2, G


def simple(sim, example):
    sim.call("setMode", "simple")
    sim.call("loadExample", example)


def test_M01_pumppu_ihanteellinen(sim, check):
    simple(sim, "ex1"); sim.call("run", 2)
    pp = sim.call("param", "P1")
    check("M01", "Yksinkertainen: pumpun tuotto Q = Vg·n/1000 (ei vuotoa)", -sim.call("q", "P1", "P"),
          pp["Vg"] * pp["n"] / 1000, 0.005, "L/min")


def test_M02_ulosajo_ilman_haviota(sim, check):
    simple(sim, "ex1"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.5)
    pp = sim.call("param", "P1"); c = sim.call("param", "SYL1"); a = areas(sim, "SYL1")
    Q = pp["Vg"] * pp["n"] / 1000
    check("M02a", "Yksinkertainen: v = Q / A pumpun teoreettisella tuotolla", sim.call("state", "SYL1")["v"],
          Q / 60000 / (a["A_mm2"] * 1e-6), 0.005, "m/s")
    check("M02b", "Yksinkertainen: p = F / A (ei kitkaa eikä venttiilihäviötä)", sim.call("p", "SYL1", "A"),
          c["F"] / a["A_mm2"] * 10, 0.01, "bar")


def test_M03_paineenrajoitus_ihanteellinen(sim, check):
    simple(sim, "ex1"); sim.call("run", 2)
    sim.call("setValve", "SV1", 1); sim.call("run", 4)
    check("M03", "Yksinkertainen: päädyssä p = ps", sim.call("p", "SYL1", "A"), sim.call("param", "PRV1")["ps"], 0.01, "bar")


def test_M04_moottori_ihanteellinen(sim, check):
    simple(sim, "ex3"); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 4)
    m = sim.call("param", "M1"); pp = sim.call("param", "P1")
    check("M04a", "Yksinkertainen: n = Q / Vg (ei vuotoa)", sim.call("rpm", "M1"),
          pp["Vg"] * pp["n"] / m["Vg"], 0.01, "r/min")
    dp = sim.call("p", "M1", "A") - sim.call("p", "M1", "B")
    check("M04b", "Yksinkertainen: Δp = 20π·T / Vg (ηhm = 1)", dp, 20 * math.pi * m["TL"] / m["Vg"], 0.01, "bar")


def test_M05_pikaliike_ja_virranjako(sim, check):
    simple(sim, "ex5"); sim.call("setParam", "SYL1", "L", 2000); sim.call("reset"); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 2.0)
    pp = sim.call("param", "P1"); a = areas(sim, "SYL1"); Q = pp["Vg"] * pp["n"] / 1000
    check("M05a", "Yksinkertainen: pikaliike v = Q / a", sim.call("state", "SYL1")["v"],
          Q / 60000 / ((a["A_mm2"] - a["Aring_mm2"]) * 1e-6), 0.01, "m/s")
    simple(sim, "ex7"); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 2.5)
    m = sim.call("param", "M1")
    check("M05b", "Yksinkertainen: virranjako, moottori n = Q/2 / Vg", sim.call("rpm", "M1"), Q / 2 * 1000 / m["Vg"], 0.01, "r/min")


def test_M06_nostopaine_pystyssa(sim, check):
    simple(sim, "ex6"); sim.call("setParam", "M1", "TL", 40); sim.call("run", 1)
    sim.call("setValve", "SV1", 1); sim.call("run", 1.5)
    c = sim.call("param", "SYL1"); a = areas(sim, "SYL1")
    check("M06", "Yksinkertainen: pystykuorman nostopaine p = m·g / A", sim.call("p", "SYL1", "A"),
          c["m"] * G / a["A_mm2"] * 10, 0.01, "bar")


def test_M07_mallin_vaihto_sailyttaa_parametrit(sim):
    sim.call("setMode", "advanced"); sim.call("loadExample", "ex1")
    sim.call("setParam", "SYL1", "Fc", 333); sim.call("setParam", "SV1", "Qn", 17)
    sim.call("setMode", "simple")
    assert sim.call("param", "SYL1")["Fc"] == 0, "M07: kitka ei poistunut yksinkertaisessa mallissa"
    assert sim.call("userParam", "SYL1")["Fc"] == 333, "M07: käyttäjän arvo hävisi mallia vaihdettaessa"
    saved = sim.call("serialize")
    assert '"Fc":333' in saved, "M07: tallennukseen ei mennyt käyttäjän arvo"
    sim.call("setMode", "advanced")
    assert sim.call("param", "SYL1")["Fc"] == 333 and sim.call("param", "SV1")["Qn"] == 17, \
        "M07: kehittyneen mallin parametrit eivät palautuneet"
