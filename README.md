# Hydrauliikkasimulaattori / Hydraulics Simulator

[![Validointi](../../actions/workflows/validointi.yml/badge.svg)](../../actions/workflows/validointi.yml)

Selaimessa toimiva hydrauliikan perusteiden opetussimulaattori. Piiri rakennetaan ISO 1219 -tyyppisistä piirrosmerkeistä vetämällä, liitännät kytketään letkuilla, ja paine, tilavuusvirta, voima ja nopeus näkyvät reaaliajassa antureilla, letkujen väreillä ja käyrinä. Jokaisen komponentin voi mitoittaa.

**Kokeile:** <https://jipirtti.github.io/Hydrauliikkasimulaattori/> tai avaa `index.html` suoraan selaimessa. Asennusta tai palvelinta ei tarvita.

**Kieli / Language:** käyttöliittymä on suomeksi ja englanniksi. Kieltä vaihdetaan yläpalkin FI | EN -valitsimella lennosta, ja valinta muistetaan selaimessa. Suoran linkin englanninkieliseen versioon saa parametrilla `?lang=en`: <https://jipirtti.github.io/Hydrauliikkasimulaattori/?lang=en>. The user interface is available in Finnish and English; switch with the FI | EN toggle or use `?lang=en`.

Tekijä: Juho Pirttilahti, Seinäjoen ammattikorkeakoulu (SEAMK), 2026. Suunnittelu, sisältö ja validointi: Juho Pirttilahti. Ohjelmakoodi toteutettu tekoälyavusteisesti (Claude, Anthropic). Lisenssi: [CC BY 4.0](LICENSE).

## Ominaisuudet

- 13 komponenttia: vakiotilavuus- ja painesäädetty pumppu, öljysäiliö, 4/3- ja 4/2-suuntaventtiili, paineenrajoitus-, vasta-, kuristus- ja vastusventtiili, kaksi- ja yksitoiminen sylinteri, hydraulimoottori, paine- ja virtausmittari.
- Paine-, virtaus-, voima- ja nopeusanturit, joiden lukemat piirtyvät 10 sekunnin käyriksi.
- Mitoitusparametrit, lasketut arvot ja käänteinen mitoitusapu jokaiselle komponentille.
- Aikatason laskenta: öljyn kokoonpuristuvuus, sylinterin massa ja kitka, moottorin hitausmomentti. Painepiikit, kavitaatio ja ryntäävä kuorma näkyvät.
- Neljä esimerkkipiiriä ja harjoitustehtävät käyttöohjeessa.

## Dokumentaatio

| Tiedosto | Sisältö |
| --- | --- |
| [docs/kayttoohje.md](docs/kayttoohje.md) | Käyttöohje, esimerkkikaavio vaiheittain ja harjoitustehtävät. Verkkosivuna: <https://jipirtti.github.io/Hydrauliikkasimulaattori/docs/kayttoohje.html> |
| [VALIDOINTI.md](VALIDOINTI.md) | Validoitavat ilmiöt, käsinlaskukaavat ja opettajan validoinnin tila |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Kehitysohjeet, testien ajaminen ja palautteen antaminen |
| [CHANGELOG.md](CHANGELOG.md) | Versiohistoria |

## Validointi

Simulaattorin ilmiöt validoidaan kahdella tasolla, ks. [VALIDOINTI.md](VALIDOINTI.md):

- **Automaattisesti:** 17 validointitestiä vertaa simulaattorin tuloksia käsinlaskukaavoihin (esim. v = Q/A, F = p·A, massatase, moottorin vääntö). GitHub Actions ajaa ne jokaisesta muutoksesta ja maanantaisin ajastetusti. Jos ajastettu ajo epäonnistuu, siitä avautuu automaattisesti issue. Raportti näkyy ajon yhteenvedossa.
- **Opettajan validointi:** jokainen ilmiö tarkistetaan käsinlaskulla, kirjallisuudesta tai laboratoriomittauksella ja kirjataan validoiduksi. Validointikierros avautuu issueksi automaattisesti 15.1. ja 15.8.

Lisäksi kolme kielitestiä (`tests/test_kieli.py`) varmistaa, että englanninkielisessä näkymässä ei ole kääntämättömiä tekstejä ja että kielen vaihto ei vaikuta laskentaan.

Testien ajaminen omalla koneella:

```bash
pip install -r requirements-test.txt
python -m playwright install chromium
python -m pytest tests -v
```

## Palaute

Palaute on tervetullutta, ja sitä käytetään simulaattorin parantamiseen:

- **Fysiikka ei vastaa odotusta:** avaa issue mallilla *Fysiikka ei vastaa odotusta* ja liitä piiri JSON-muodossa (simulaattorin Tallenna / lataa).
- **Virhe käyttöliittymässä:** mallilla *Virheilmoitus*.
- **Ideat ja kysymykset:** Discussions-osio tai malli *Kehitysehdotus*.

## Rakenne

```
index.html                  Simulaattori (yksi tiedosto, ei riippuvuuksia eikä käännösvaihetta)
docs/                       Käyttöohje (markdown) ja kuvat
tools/rakenna_ohje.py       Rakentaa käyttöohjeen HTML-sivun julkaisun yhteydessä
tests/                      Validointitestit (pytest + Playwright)
VALIDOINTI.md               Validointisuunnitelma ja -tila
.github/workflows/          Validointi, validointikierros ja GitHub Pages -julkaisu
.github/ISSUE_TEMPLATE/     Palautelomakkeet
```

## Lisenssi

Simulaattori ja käyttöohje on lisensoitu [Creative Commons Nimeä 4.0 Kansainvälinen -lisenssillä (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.fi). Saat kopioida, jakaa ja muokata aineistoa mihin tahansa tarkoitukseen, kunhan mainitset tekijän ja oppilaitoksen, merkitset lisenssin ja kerrot tekemistäsi muutoksista.

Suositeltu viittaus: Pirttilahti, J. (2026). *Hydrauliikkasimulaattori ja käyttöohje.* Seinäjoen ammattikorkeakoulu. CC BY 4.0.
