# Muutosloki

## 1.4.0 – 2026-10-19

- Letkun reittiä voi muokata vetämällä letkun osaa. Päät pysyvät kytkettyinä, reitti pysyy suorakulmaisena ja seuraa komponentteja, kun niitä siirretään. Muokattu reitti tallentuu piirin mukana.
- Kaksoisklikkaus letkuun tai ominaisuuspaneelin Automaattinen reitti -painike palauttaa automaattisen reitin.
- Uudet käyttöliittymätestit U01–U03 (`tests/test_kaytto.py`).

## 1.3.0 – 2026-10-19

- Simulointimallin valinta yläpalkissa: **Yksinkertainen** (ihanteelliset komponentit, tulos vastaa käsinlaskua) ja **Kehittynyt** (kitka, vuodot, hyötysuhteet ja venttiilien painehäviöt). Valinta vaihtuu lennosta kuten kieli, muistetaan selaimessa ja voidaan antaa linkissä (`?malli=yksinkertainen`, `?mode=simple`).
- Yksinkertaisessa mallissa ominaisuuspaneeli näyttää vain perusmitoituksen. Kehittyneen mallin häviöparametrit säilyvät tallessa mallia vaihdettaessa.
- Käyttöohjeeseen osio malleista, esimerkkien arvot yksinkertaisella mallilla, harjoitustehtäviin mallimerkinnät ja kaksi mallien vertailutehtävää.
- Uudet testit M01–M07 (`tests/test_malli.py`) ja kielitesti K04.

## 1.2.0 – 2026-10-19

- Uudet komponentit: 3/2-suuntaventtiili ja virranjakoventtiili (säädettävä jakosuhde). Paletissa on nyt 15 komponenttia.
- Sylinterin asentoon lisätty vaihtoehto Pysty, ulosajo alas (männänvarsi alaspäin, riippuva kuorma).
- Uudet esimerkkipiirit 5–7: pikaliikekytkentä 3/2-venttiilillä, moottori sylinterin rinnalla sekä virranjakoventtiilit ja vastaventtiilit.
- Vastaventtiilin avautumiskäyrää terävöitetty, jotta suljettu venttiili ei vuoda virranjakajan kaltaisissa silmukoissa.
- Uudet validointitestit V17–V22 ja laadulliset tarkistukset L09–L11. Käyttöohjeeseen lisätty uudet komponentit, esimerkit ja harjoitustehtävät.

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
