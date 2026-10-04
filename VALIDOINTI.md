# Validointisuunnitelma

Simulaattorin ilmiöt validoidaan kahdella tasolla, jotka käyttävät samoja tunnuksia:

1. **Automaattinen regressiovalidointi** (`tests/test_validointi.py`). GitHub Actions ajaa testit jokaisen muutoksen yhteydessä ja ajastetusti kerran viikossa. Testi vertaa simulaattorin tulosta käsinlaskukaavaan. Testi ei todista, että kaava on oikea; se varmistaa, että kerran validoitu käyttäytyminen ei muutu huomaamatta.
2. **Opettajan ilmiövalidointi**. Opettaja tarkistaa, että ilmiö, kaava ja numeerinen tulos vastaavat hydrauliikan teoriaa ja tarvittaessa laboratoriomittausta. Vasta tämän jälkeen ilmiö merkitään validoiduksi. Validointikierros avataan automaattisesti issueksi lukukausien alussa (`.github/workflows/katselmointi.yml`).

Tilat: **Ei validoitu** → **Validoitu** (päivämäärä ja validoija) → **Vanhentunut**, jos ilmiöön liittyvää fysiikkaa on muutettu validoinnin jälkeen. Jokainen fysiikkaa muuttava pull request palauttaa koskemiensa rivien tilan Ei validoitu -tilaan.

## A. Määrälliset ilmiöt (automaattinen testi + opettajan validointi)

Odotusarvot ovat esimerkkipiirien oletusparametreilla. Toleranssi on testin hyväksymä suhteellinen poikkeama kaavasta.

| ID | Ilmiö | Piiri ja toimenpide | Käsinlaskukaava | Odotettu (oletus) | Tol. | Opettajan validointi |
| --- | --- | --- | --- | --- | --- | --- |
| V00 | Sylinterin pinta-alat | Esim. 1, SYL1 | A = π/4·D², A − a = π/4·(D² − d²) | 1963 / 1348 mm² | 0,1 % | Ei validoitu |
| V01 | Paineenrajoitusventtiili rajaa paineen | Esim. 1, lepotila | p = ps + (Q/Qn)·Δpo | 102,8 bar | 1 % | Ei validoitu |
| V02 | Pumpun tuotto ja vuoto | Esim. 1, lepotila | Q = Vg·n/1000 − Qth·(1 − ηv)·p/pn | 14,2 L/min | 1 % | Ei validoitu |
| V03 | Ulosajonopeus | Esim. 1, kela a | v = Q / A | 123 mm/s | 3 % | Ei validoitu |
| V04 | Sisäänajonopeus | Esim. 1, kela b | v = Q / (A − a) | 178 mm/s | 3 % | Ei validoitu |
| V05 | Kuorma määrää paineen | Esim. 1, kela a, liikkeen aikana | pA = (F + Fc + cv·v + pB·(A − a)) / A | 11,9 bar | 2 % | Ei validoitu |
| V06 | Suurin työntövoima päädyssä | Esim. 1, kela a, iskun pää | F = p·A | 20,2 kN | 1 % | Ei validoitu |
| V07 | Massatase | Esim. 1, ulosajo loppuun | ΔV_säiliöt = (A − (A − a))·L = a·L | 0,185 L | 4 % | Ei validoitu |
| V08 | Kuorman pito suljetussa keskiasennossa | Esim. 1, kela a → 0 | Asema ei muutu (Δx < 1 mm / 5 s) | 0 mm | – | Ei validoitu |
| V09 | Paineen vahvistuminen, meter-out | Esim. 2, kela a | pB = (pA·A − F − Fc − cv·v) / (A − a) | 123 bar (pA 101 bar) | 2 % | Ei validoitu |
| V10 | Hydraulimoottorin nopeus | Esim. 3, kela a | n = (Q − vuoto)·1000 / Vg | 700 r/min | 2 % | Ei validoitu |
| V11 | Hydraulimoottorin vääntö | Esim. 3, kela a | T = Δp·Vg·ηhm / (20π) ja T = TL + b·ω | 21,5 Nm | 1–2 % | Ei validoitu |
| V12 | Pystykuorman nostopaine | Esim. 4, kela a | p = (m·g + F0 + k·x + Fc + cv·v) / A | 14,4 bar | 2 % | Ei validoitu |
| V13 | Hallittu lasku kuristimella | Esim. 4, kela pois | v = Q_kuristin / A | 123 mm/s | 3 % | Ei validoitu |
| V14 | Painesäädetty pumppu | Esim. 1, pumppu painesäädetyksi, pc 90 bar | p ≈ pc, PRV ei avaudu | 88–93 bar | – | Ei validoitu |
| V15 | Toistettavuus | Esim. 2 | Kaksi samaa ajoa antaa saman tuloksen | – | 0 | Ei validoitu |
| V16 | Ylipainevaroitus | Esim. 1, PRV 300 bar | Varoitus, kun p > sylinterin 250 bar | – | – | Ei validoitu |

## B. Laadulliset ilmiöt (opettajan validointi simulaattorissa)

Näille ei ole automaattista testiä. Opettaja tarkistaa käyttäytymisen silmämääräisesti ja kirjaa havainnon.

| ID | Ilmiö | Miten tarkistetaan | Odotettu käyttäytyminen | Opettajan validointi |
| --- | --- | --- | --- | --- |
| L01 | Keskiasentojen erot | Esim. 1, vaihda keskiasento suljettu → tandem → avoin → kelluva | Suljettu: PRV avautuu, sylinteri pysyy. Tandem: pumppu paineeton, sylinteri pysyy. Avoin ja kelluva: sylinteri vapaa liikkumaan ulkoisen voiman vaikutuksesta. | Ei validoitu |
| L02 | Painepiikki päätyyn osuttaessa | Esim. 1, nopeus 0,1×, seuraa pA-käyrää iskun päässä | Paine nousee jyrkästi PRV:n avautumispaineeseen; ylitys riippuu öljytilavuudesta ja PRV:n ominaiskäyrästä. | Ei validoitu |
| L03 | Ryntäävä kuorma ja kavitaatio | Esim. 1, kuorma 5000 N vakiovoimana, kela b | Sylinteri ajaa sisään pumpun tuottoa nopeammin, B-puolelle alipaine ja kavitaatiovaroitus. | Ei validoitu |
| L04 | Vastaventtiilin suunta | Esim. 2, kela b | Sisäänajo vapaasti vastaventtiilin kautta; ulosajo kuristettu. | Ei validoitu |
| L05 | Jousipalautteinen ohjaus | Vaihda SV1 jousipalautteiseksi | Kela on päällä vain painettaessa; venttiili palaa keskiasentoon. | Ei validoitu |
| L06 | Moottorin pysäytys tandem-keskiasennossa | Esim. 3, kela a → 0 | Moottori jarruttaa, A- tai B-puolen paine nousee hetkellisesti hitausmomentin vuoksi. | Ei validoitu |
| L07 | Pumppu ilman imua | Irrota pumpun S-liitäntä | Tuotto loppuu ja varoitus imusta näkyy. | Ei validoitu |
| L08 | Lepotilan häviöteho | Esim. 1, valitse PRV1 | Häviöteho p·Q/600 ≈ 2,4 kW. | Ei validoitu |

## C. Validoinnin kirjaaminen

Kun opettaja on validoinut rivin, hän päivittää sen sarakkeeseen muodon `Validoitu 2026-10-15 / JP / käsinlasku` tai `Validoitu 2026-10-15 / JP / laboratoriomittaus, piiri X`. Mahdolliset poikkeamat kirjataan issueksi tunnisteella `fysiikka`.

Menetelmävaihtoehdot:

- **Käsinlasku**: kaava ja tulos tarkistettu itsenäisesti.
- **Kirjallisuus**: verrattu oppikirjan tai valmistajan esimerkkiin (lähde mainitaan).
- **Laboratoriomittaus**: verrattu hydrauliikkalaboratorion harjoituslaitteen mittaukseen samalla piirillä.

## D. Mallin rajaukset

Seuraavia ilmiöitä malli ei kuvaa, joten niitä ei validoida: letkujen ja liittimien painehäviöt, lämpeneminen ja viskositeetin muutos, venttiilien ohjausdynamiikka (karan liike on lineaarinen ramppi), sylinterin päätyvaimennus, ilman liukeneminen öljyyn ja letkukohtainen virtaus rinnakkaisissa silmukoissa.
