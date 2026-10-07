# Kehitysohjeet

Kiitos, että haluat kehittää simulaattoria. Projektin tavoite on pysyä yksinkertaisena opetusvälineenä: yksi HTML-tiedosto, ei riippuvuuksia eikä käännösvaihetta, ja jokainen fysiikkaa koskeva ominaisuus validoitu.

## Työnkulku

1. Avaa tai valitse issue, johon muutos liittyy.
2. Tee muutos omaan haaraan ja avaa pull request. PR-pohjan tarkistuslista ohjaa läpi.
3. GitHub Actions ajaa validointitestit. PR yhdistetään vasta, kun testit menevät läpi ja vastuuopettaja on hyväksynyt fysiikkaa koskevat muutokset.

## Fysiikkaa koskevat muutokset

Fysiikka on kaikki, mikä vaikuttaa simuloituihin paineisiin, virtauksiin, voimiin tai liikkeisiin (komponenttien `fl`-, `mr`-, `pre`- ja `post`-funktiot, ratkaisija ja vakiot `index.html`-tiedoston alussa).

- Jokaisella ilmiöllä on tunnus VALIDOINTI.md:ssä ja mahdollisuuksien mukaan testi `tests/test_validointi.py`:ssä samalla tunnuksella.
- Testin odotusarvo lasketaan **itsenäisesti käsinlaskukaavalla**, ei simulaattorin omalla koodilla. Muuten virhe kumoutuu testissä.
- Kun muutat fysiikkaa, palauta muutoksen koskemat VALIDOINTI.md:n rivit tilaan *Ei validoitu*. Vastuuopettaja validoi ne uudelleen.
- Uusi komponentti tarvitsee vähintään yhden määrällisen testin ja rivin VALIDOINTI.md:hen.

## Testien ajaminen

```bash
pip install -r requirements-test.txt
python -m playwright install chromium
python -m pytest tests -v
```

Testit käyttävät simulaattorin testirajapintaa `window.HydSim` (määritelty `index.html`:n lopussa). Rajapinnan kautta voi ladata esimerkkipiirin, ohjata venttiileitä, ajaa simulaatiota halutun ajan ja lukea paineet, virtaukset, voimat ja nopeudet.

## Käyttöohje

Käyttöohje on tiedostossa `docs/kayttoohje.md`. Päivitä se samassa PR:ssä, jos käyttö, esimerkkien lukuarvot tai kuvakaappaukset muuttuvat. Julkaisutyönkulku rakentaa siitä verkkosivun `docs/kayttoohje.html` (`tools/rakenna_ohje.py`), joten HTML-tiedostoa ei muokata eikä tallenneta repositorioon.

## Kieli ja käännökset

Dokumentaatio ja issuet ovat suomeksi. Koodin kommentit voivat olla suomeksi tai englanniksi.

Käyttöliittymä on kaksikielinen (suomi ja englanti). Suomenkieliset tekstit ovat koodissa avaimina, ja englanninkieliset käännökset ovat `index.html`:n sanakirjassa `EN`. Kun lisäät tekstejä:

- Komponenttien nimet, parametrien nimet, valintalistojen vaihtoehdot ja lasketut suureet käännetään sanakirjan kautta funktiolla `T()`. Lisää uusi suomenkielinen teksti ja sen käännös `EN`-sanakirjaan.
- Lauseet ja numeroita sisältävät tekstit kirjoitetaan suoraan muodossa `tr('suomeksi', 'in English')`.
- Sivun kiinteään HTML:ään lisätään englanninkielinen teksti attribuutteihin `data-en`, `data-en-title` tai `data-en-aria`.
- Yksiköt, jotka eroavat kielittäin (esim. r/min → rpm), kulkevat funktion `U()` kautta.

Testi K01 renderöi kaikki komponentit englanniksi ja epäonnistuu, jos jokin teksti puuttuu sanakirjasta.

## Lisenssi

Lähettämällä muutoksen hyväksyt, että se julkaistaan projektin lisenssillä (CC BY 4.0).
