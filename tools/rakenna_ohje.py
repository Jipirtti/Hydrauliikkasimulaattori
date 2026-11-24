"""Rakentaa käyttöohjeen HTML-sivut kolmella kielellä:
docs/kayttoohje.md -> docs/kayttoohje.html (suomi), docs/user-manual.md -> docs/user-manual.html (englanti),
docs/bedienungsanleitung.md -> docs/bedienungsanleitung.html (saksa).

Ajetaan julkaisutyönkulussa automaattisesti. Paikallisesti:
    pip install markdown
    python tools/rakenna_ohje.py
"""
import pathlib
import re
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
GH = "https://github.com/Jipirtti/Hydrauliikkasimulaattori"
LANGS = {
    "fi": dict(src="kayttoohje", title="Hydrauliikkasimulaattori – käyttöohje", school="Seinäjoen ammattikorkeakoulu", toc="Sisällys", open="Avaa simulaattori",
               note=r"^> Tämä tiedosto on käyttöohjeen versioitu kopio.*$",
               footer='Juho Pirttilahti, Seinäjoen ammattikorkeakoulu (SEAMK), 2026. Suunnittelu, sisältö ja validointi: Juho Pirttilahti. Ohjelmakoodi toteutettu tekoälyavusteisesti (Claude, Anthropic). <a href="https://creativecommons.org/licenses/by/4.0/deed.fi" rel="license">CC BY 4.0</a>.\nLähdekoodi ja palaute: <a href="' + GH + '">' + GH[8:] + '</a>.'),
    "en": dict(src="user-manual", title="Hydraulics Simulator – user manual", school="Seinäjoki University of Applied Sciences", toc="Contents", open="Open the simulator",
               note=r"^> This file is the versioned copy of the user manual.*$",
               footer='Juho Pirttilahti, Seinäjoki University of Applied Sciences (SEAMK), 2026. Design, content and validation: Juho Pirttilahti. Code implemented with AI assistance (Claude, Anthropic). <a href="https://creativecommons.org/licenses/by/4.0/deed.en" rel="license">CC BY 4.0</a>.\nSource code and feedback: <a href="' + GH + '">' + GH[8:] + '</a>.'),
    "de": dict(src="bedienungsanleitung", title="Hydraulik-Simulator – Bedienungsanleitung", school="Fachhochschule Seinäjoki", toc="Inhalt", open="Simulator öffnen",
               note=r"^> Diese Datei ist die versionierte Kopie der Bedienungsanleitung.*$",
               footer='Juho Pirttilahti, Fachhochschule Seinäjoki (SEAMK), 2026. Konzeption, Inhalt und Validierung: Juho Pirttilahti. Der Programmcode wurde KI-gestützt erstellt (Claude, Anthropic). <a href="https://creativecommons.org/licenses/by/4.0/deed.de" rel="license">CC BY 4.0</a>.\nQuellcode und Feedback: <a href="' + GH + '">' + GH[8:] + '</a>.'),
}

TEMPLATE = """<!doctype html>
<!-- Hydrauliikkasimulaattori: __TITLE__. Juho Pirttilahti, Seinäjoen ammattikorkeakoulu (SEAMK), 2026. CC BY 4.0.
     Tämä tiedosto on generoitu tiedostosta docs/__SRC__ (tools/rakenna_ohje.py). Muokkaa lähdettä, älä tätä. -->
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<meta name="author" content="Juho Pirttilahti, __SCHOOL__ (SEAMK)">
<link rel="license" href="https://creativecommons.org/licenses/by/4.0/deed.__LANG__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;0,500;0,600;1,400&family=Barlow+Condensed:wght@600&display=swap" rel="stylesheet">
<style>
:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);
  --bg:#F7F9FA;--panel:#EDF1F4;--ink:#17212B;--muted:#56636F;--line:#C2CBD3;--acc:#E39B17;--link:#1E5DBA}
*,*::before,*::after{box-sizing:inherit}
html{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 16px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#131A20;--panel:#182028;--ink:#E2E8EE;--muted:#93A0AC;--line:#2A3540;--acc:#F0A82A;--link:#6FA7FF}}
:root[data-theme="dark"]{--bg:#131A20;--panel:#182028;--ink:#E2E8EE;--muted:#93A0AC;--line:#2A3540;--acc:#F0A82A;--link:#6FA7FF}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Barlow",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:17px;line-height:1.6}
a{color:var(--link)}
.wrap{max-width:1180px;margin:0 auto;padding:24px 20px 64px;display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px}
nav.toc{position:sticky;top:calc(env(safe-area-inset-top,0px) + 16px);align-self:start;font-size:15px}
nav.toc .open{display:block;background:var(--ink);color:var(--bg);text-decoration:none;text-align:center;border-radius:8px;padding:9px 12px;font-weight:600;margin-bottom:18px}
nav.toc .langs{margin:-6px 0 16px;text-align:center;font-size:14px}nav.toc .langs a,nav.toc .langs b{padding:0 6px}
nav.toc ul{list-style:none;margin:0;padding:0;border-left:2px solid var(--line)}
nav.toc li a{display:block;padding:4px 0 4px 12px;color:var(--muted);text-decoration:none;line-height:1.3}
nav.toc li a:hover{color:var(--ink)}
main{min-width:0;max-width:820px}
h1{font-family:"Barlow Condensed","Arial Narrow",sans-serif;font-size:clamp(34px,5vw,48px);line-height:1.05;margin:0 0 6px}
h2{font-size:26px;line-height:1.2;margin:48px 0 12px;padding-top:16px;border-top:2px solid var(--ink)}
h3{font-size:19px;margin:28px 0 8px}
p,li{max-width:72ch}
table{border-collapse:collapse;width:100%;font-size:15px;margin:12px 0 20px;display:block;overflow-x:auto}
th,td{text-align:left;vertical-align:top;padding:7px 10px;border-bottom:1px solid var(--line)}
th{border-bottom:2px solid var(--ink);white-space:nowrap}
img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:10px;display:block;margin:14px 0 6px}
code{background:var(--panel);padding:1px 5px;border-radius:4px;font-size:.92em}
.kaava{background:var(--panel);border-left:3px solid var(--acc);padding:10px 14px;font-size:18px;overflow-x:auto;white-space:nowrap}
footer{margin-top:48px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
@media (max-width:860px){.wrap{grid-template-columns:1fr;gap:12px}nav.toc{position:static}nav.toc ul{display:none}}
@media print{nav.toc{display:none}.wrap{display:block}h2{break-after:avoid}img{break-inside:avoid}}
</style>
</head>
<body>
<div class="wrap">
<nav class="toc" aria-label="__TOCLABEL__">
<a class="open" href="../?lang=__LANG__">__OPEN__</a>
<p class="langs">__LANGS__</p>
__TOC__
</nav>
<main>
__BODY__
<footer>__FOOTER__</footer>
</main>
</div>
</body>
</html>
"""


def build(lang):
    L = LANGS[lang]
    src = ROOT / "docs" / (L["src"] + ".md")
    if not src.exists():
        return
    md = src.read_text(encoding="utf-8")
    # Versioidun kopion huomautus koskee vain repositoriota.
    md = re.sub(L["note"], "", md, flags=re.M)
    # Kaavalohko ($$ ... $$) muutetaan luettavaksi tekstiksi, koska sivu ei lataa kaavakirjastoa.
    md = re.sub(r"\$\$.*?\$\$",
                '<p class="kaava">D = √(4F / (π·p))&emsp;&emsp;V<sub>g</sub> = Q·1000 / (n·η<sub>v</sub>)&emsp;&emsp;'
                'V<sub>g</sub> = 20π·T / (Δp·η<sub>hm</sub>)</p>', md, flags=re.S)
    body = markdown.Markdown(extensions=["tables", "toc", "sane_lists"]).convert(md)
    toc_list = "<ul>" + "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>'
                                for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)) + "</ul>"
    langs = " ".join(f"<b>{k.upper()}</b>" if k == lang else f'<a href="{v["src"]}.html" hreflang="{k}">{k.upper()}</a>'
                     for k, v in LANGS.items() if (ROOT / "docs" / (v["src"] + ".md")).exists())
    html = TEMPLATE
    for k, v in {"__LANG__": lang, "__TITLE__": L["title"], "__SRC__": L["src"] + ".md", "__SCHOOL__": L["school"], "__TOCLABEL__": L["toc"],
                 "__OPEN__": L["open"], "__LANGS__": langs, "__FOOTER__": L["footer"], "__TOC__": toc_list}.items():
        html = html.replace(k, v)
    html = html.replace("__BODY__", body)
    out = ROOT / "docs" / (L["src"] + ".html")
    out.write_text(html, encoding="utf-8")
    print(f"Kirjoitettu {out.relative_to(ROOT)}")


for lang in LANGS:
    build(lang)
