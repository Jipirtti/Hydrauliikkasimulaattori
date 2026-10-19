"""Käyttöliittymän testit (U01–U03): letkun reitin muokkaus vetämällä.

Reitin muokkaus on pelkkää piirustusta: se ei saa irrottaa letkua liitännöistä eikä muuttaa laskentaa.
"""
import json
import re


def _wire_index(sim, a, b):
    d = json.loads(sim.call("serialize"))
    for i, w in enumerate(d["wires"]):
        if {w["a"], w["b"]} == {a, b}:
            return i, d
    raise AssertionError(f"letkua {a}–{b} ei löydy")


def _segment_screen_points(sim, a, b):
    """Palauttaa letkun pisimmän välisegmentin keskipisteen ja suunnan näyttökoordinaateissa."""
    return sim.js(f"""(() => {{
      const g=[...document.querySelectorAll('#lWires .wire')].find(g=>{{const w=HydSim._wire(g.dataset.w);return w&&((w.a==='{a}'&&w.b==='{b}')||(w.a==='{b}'&&w.b==='{a}'));}});
      const path=g.querySelector('.wb');const pts=path.getAttribute('d').slice(1).split('L').map(s=>s.split(',').map(Number));
      let best=null,bl=-1;for(let i=1;i<pts.length-2;i++){{const l=Math.abs(pts[i+1][0]-pts[i][0])+Math.abs(pts[i+1][1]-pts[i][1]);if(l>bl){{bl=l;best=i;}}}}
      if(best===null)best=0;
      const p=pts[best],q=pts[best+1];const m=path.getScreenCTM();
      const sp=new DOMPoint((p[0]+q[0])/2,(p[1]+q[1])/2).matrixTransform(m);
      return {{x:sp.x,y:sp.y,horiz:Math.abs(p[1]-q[1])<0.5,k:m.a}};}})()""")


def _drag(sim, x, y, dx, dy):
    sim.js(f"""(() => {{const el=document.elementFromPoint({x},{y});const cv=document.querySelector('#cv');
      const o={{bubbles:true,pointerId:1,button:0,pointerType:'mouse'}};
      el.dispatchEvent(new PointerEvent('pointerdown',{{...o,clientX:{x},clientY:{y}}}));
      for(let s=1;s<=5;s++)cv.dispatchEvent(new PointerEvent('pointermove',{{...o,clientX:{x}+{dx}*s/5,clientY:{y}+{dy}*s/5}}));
      cv.dispatchEvent(new PointerEvent('pointerup',{{...o,clientX:{x}+{dx},clientY:{y}+{dy}}}));}})()""")


def _orthogonal(d):
    pts = [tuple(map(float, s.split(","))) for s in d[1:].split("L")]
    return all(abs(p[0] - q[0]) < 0.5 or abs(p[1] - q[1]) < 0.5 for p, q in zip(pts, pts[1:])), pts


def test_U01_letkun_reitin_veto(sim):
    sim.call("loadExample", "ex1"); sim.call("pause")
    n0 = len(json.loads(sim.call("serialize"))["wires"])
    s = _segment_screen_points(sim, "c6:A", "c8:A")
    dx, dy = (0, 60) if s["horiz"] else (-60, 0)
    _drag(sim, s["x"], s["y"], dx, dy)
    i, d = _wire_index(sim, "c6:A", "c8:A")
    assert len(d["wires"]) == n0, "U01: letkujen määrä muuttui vedossa"
    assert d["wires"][i].get("pts"), "U01: reitin muutos ei tallentunut"
    path = sim.js("[...document.querySelectorAll('#lWires .wire.manual .wb')].map(p=>p.getAttribute('d'))")
    assert path, "U01: muokattua reittiä ei piirretty"
    ok, pts = _orthogonal(path[0])
    assert ok, f"U01: reitti ei ole suorakulmainen: {pts}"


def test_U02_paat_seuraavat_komponenttia(sim):
    sim.call("loadExample", "ex1"); sim.call("pause")
    s = _segment_screen_points(sim, "c6:A", "c8:A")
    _drag(sim, s["x"], s["y"], *((0, 60) if s["horiz"] else (-60, 0)))
    sim.js("(()=>{const d=JSON.parse(HydSim.serialize());const c=d.comps.find(c=>c.id==='c8');c.x+=40;c.y-=30;HydSim.loadCircuit(d);})()")
    i, d = _wire_index(sim, "c6:A", "c8:A")
    assert d["wires"][i].get("pts"), "U02: muokattu reitti hävisi tallennuksen ja latauksen yhteydessä"
    path = sim.js("[...document.querySelectorAll('#lWires .wire.manual .wb')].map(p=>p.getAttribute('d'))")[0]
    ok, pts = _orthogonal(path)
    assert ok, f"U02: reitti ei pysynyt suorakulmaisena komponenttia siirrettäessä: {pts}"
    port = sim.js("(()=>{const c=document.querySelector('[data-port=\"c8:A\"]');return [+c.getAttribute('cx'),+c.getAttribute('cy')];})()")
    assert any(abs(p[0] - port[0]) < 0.5 and abs(p[1] - port[1]) < 0.5 for p in (pts[0], pts[-1])), \
        "U02: letkun pää ei seurannut siirrettyä liitäntää"


def test_U03_reitti_ei_vaikuta_laskentaan(sim):
    def ajo(muokkaa):
        sim.call("loadExample", "ex1"); sim.call("pause")
        if muokkaa:
            s = _segment_screen_points(sim, "c6:A", "c8:A")
            _drag(sim, s["x"], s["y"], *((0, 60) if s["horiz"] else (-60, 0)))
            sim.call("reset")
        sim.call("run", 1.0); sim.call("setValve", "SV1", 1); sim.call("run", 1.0)
        return sim.call("p", "SYL1", "A"), sim.call("state", "SYL1")["x"]
    assert ajo(False) == ajo(True), "U03: letkun reitin muutos muutti simulointitulosta"
    sim.call("loadExample", "ex1"); sim.call("pause")
    s = _segment_screen_points(sim, "c6:A", "c8:A")
    _drag(sim, s["x"], s["y"], *((0, 60) if s["horiz"] else (-60, 0)))
    sim.js("document.querySelector('#undoBtn').click()")
    i, d = _wire_index(sim, "c6:A", "c8:A")
    assert not d["wires"][i].get("pts"), "U03: Kumoa ei palauttanut reittiä"


def _pointer(sim, kind, x, y, shift=False, target="cv"):
    sim.js(f"""(() => {{const el={'document.elementFromPoint(%s,%s)' % (x, y) if target == 'pt' else "document.querySelector('#cv')"};
      el.dispatchEvent(new PointerEvent('{kind}',{{bubbles:true,pointerId:1,button:0,pointerType:'mouse',shiftKey:{str(shift).lower()},clientX:{x},clientY:{y}}}));}})()""")


def _comp_center(sim, cid):
    return sim.js(f"(()=>{{const r=document.querySelector('.comp[data-id=\"{cid}\"] .hit').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2];}})()")


def _empty_point(sim):
    """Tyhjä kohta piirtoalustan vasemmassa alakulmassa, missä ei ole komponentteja."""
    return sim.js("(()=>{const r=document.querySelector('#cv').getBoundingClientRect();return [r.x+r.width-20,r.y+r.height-20];})()")


def test_U04_laatikkovalinta_ja_ryhmasiirto(sim):
    sim.call("loadExample", "ex1"); sim.call("pause")
    # laatikko sylinterin ja suuntaventtiilin ympäri (näyttökoordinaatit komponenttien rajoista)
    box = sim.js("""(()=>{const rs=['c6','c8'].map(id=>document.querySelector(`.comp[data-id="${id}"] .hit`).getBoundingClientRect());
      return [Math.min(...rs.map(r=>r.left))-15,Math.min(...rs.map(r=>r.top))-15,Math.max(...rs.map(r=>r.right))+15,Math.max(...rs.map(r=>r.bottom))+15];})()""")
    _pointer(sim, "pointerdown", box[0], box[1], shift=True, target="pt")
    _pointer(sim, "pointermove", (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, shift=True)
    _pointer(sim, "pointermove", box[2], box[3], shift=True)
    _pointer(sim, "pointerup", box[2], box[3], shift=True)
    selected = set(sim.call("selection"))
    assert {"SV1", "SYL1"} <= selected, f"U04: laatikko ei valinnut komponentteja: {selected}"
    before = {c["id"]: (c["x"], c["y"]) for c in json.loads(sim.call("serialize"))["comps"]}
    x, y = _comp_center(sim, "c8")
    _pointer(sim, "pointerdown", x, y, target="pt")
    for s in range(1, 6):
        _pointer(sim, "pointermove", x + 12 * s, y + 8 * s)
    _pointer(sim, "pointerup", x + 60, y + 40)
    after = {c["id"]: (c["x"], c["y"]) for c in json.loads(sim.call("serialize"))["comps"]}
    moved = [cid for cid in before if before[cid] != after[cid]]
    sel_ids = {c["id"] for c in json.loads(sim.call("serialize"))["comps"] if c["label"] in selected}
    assert set(moved) == sel_ids, f"U04: ryhmäsiirto siirsi väärät komponentit: {moved} vs {sel_ids}"
    d = {cid: (after[cid][0] - before[cid][0], after[cid][1] - before[cid][1]) for cid in moved}
    assert len(set(d.values())) == 1, f"U04: komponentit eivät siirtyneet yhtä paljon: {d}"


def test_U05_kopioi_liita_ja_poista(sim):
    sim.call("loadExample", "ex1"); sim.call("pause")
    n_c = len(json.loads(sim.call("serialize"))["comps"]); n_w = len(json.loads(sim.call("serialize"))["wires"])
    for cid, shift in (("c6", False), ("c8", True)):
        x, y = _comp_center(sim, cid)
        _pointer(sim, "pointerdown", x, y, shift=shift, target="pt"); _pointer(sim, "pointerup", x, y, shift=shift)
    assert set(sim.call("selection")) == {"SV1", "SYL1"}, "U05: Shift+klikkaus ei lisännyt valintaan"
    sim.js("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'c',ctrlKey:true,bubbles:true}))")
    sim.js("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'v',ctrlKey:true,bubbles:true}))")
    d = json.loads(sim.call("serialize"))
    assert len(d["comps"]) == n_c + 2, "U05: liittäminen ei lisännyt kahta komponenttia"
    assert len(d["wires"]) == n_w + 2, "U05: komponenttien väliset letkut (A ja B) eivät kopioituneet"
    pasted = set(sim.call("selection"))
    assert pasted and not pasted & {"SV1", "SYL1"}, f"U05: liitetyt eivät ole valittuina uusilla tunnuksilla: {pasted}"
    sim.js("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Delete',bubbles:true}))")
    d2 = json.loads(sim.call("serialize"))
    assert len(d2["comps"]) == n_c and len(d2["wires"]) == n_w, "U05: valittujen poisto ei palauttanut alkuperäistä piiriä"
    sim.call("run", 0.5)
