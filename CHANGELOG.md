# Muutosloki

## 1.1.1 – 2026-10-07

- Oppilaitoksen lyhenne muotoon SEAMK.
- Tekijämerkintään lisätty työnjako ja maininta tekoälyavusteisesta toteutuksesta.

## 1.1.0 – 2026-10-05

- Englanninkielinen käyttöliittymä. Kieli vaihdetaan lennosta yläpalkin FI | EN -valitsimella, valinta muistetaan selaimessa, ja suoran linkin saa parametrilla `?lang=en`. Lukuarvot näytetään valitun kielen desimaalierottimella.
- Varoituksilla on kielestä riippumattomat koodit (testirajapinta `warningCodes`), ja testi V16 käyttää niitä.
- Uudet kielitestit K01–K03 (`tests/test_kieli.py`).

## 1.0.1 – 2026-10-04

- Käyttöohje julkaistaan verkkosivuna simulaattorin rinnalla (docs/kayttoohje.html), ja simulaattorin yläpalkissa ja Ohje-ikkunassa on linkki siihen.

## 1.0.0 – 2026-10-04

Ensimmäinen julkinen versio.

- 13 komponenttia, letkukytkennät, paine-, virtaus-, voima- ja nopeusanturit sekä käyrät.
- Mitoitusparametrit, lasketut arvot ja mitoitusapu.
- Neljä esimerkkipiiriä.
- Käyttöohje (docs/kayttoohje.md).
- Testirajapinta `window.HydSim` ja 17 automaattista validointitestiä (V00–V16).
- Ajastettu validointi, lukukausittainen opettajan validointikierros ja GitHub Pages -julkaisu.
