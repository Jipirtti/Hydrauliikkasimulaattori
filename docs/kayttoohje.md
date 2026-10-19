# Hydrauliikkasimulaattori – käyttöohje

Juho Pirttilahti, Seinäjoen ammattikorkeakoulu (SEAMK), 2026 · CC BY 4.0

> Tämä tiedosto on käyttöohjeen versioitu kopio. Kun simulaattoriin tehdään muutoksia, päivitä tämä ohje samassa pull requestissa.

## Mikä simulaattori on

Hydrauliikkasimulaattori on selaimessa toimiva harjoitusympäristö, jossa rakennetaan hydraulipiiri ISO 1219 -tyyppisistä piirrosmerkeistä ja nähdään heti, miten paine, tilavuusvirta, voima ja nopeus käyttäytyvät. Asennusta ei tarvita, ja piiri tallentuu automaattisesti selaimeen.

Simulaattorilla voi harjoitella esimerkiksi:

- miten paineenrajoitusventtiili rajaa järjestelmän paineen ja minne pumpun tuotto menee, kun toimilaite pysähtyy
- miksi kaksitoiminen sylinteri liikkuu sisään nopeammin ja pienemmällä voimalla kuin ulos
- miten kuristus tulopuolella ja poistopuolella eroavat ja miksi poistopuolen kuristus voi nostaa rengaspuolen paineen yli järjestelmäpaineen
- miten suuntaventtiilin keskiasento vaikuttaa kuorman pitoon, pumpun kuormitukseen ja moottorin pysäytykseen
- komponenttien mitoitusta: sylinterin halkaisija voimasta, pumpun kierrostilavuus tuotosta ja moottorin kierrostilavuus väännöstä.

Simulaattori on tarkoitettu ilmiöiden ymmärtämiseen. Sen tulokset eivät korvaa järjestelmätoimittajan mitoituslaskelmia (ks. kohta Mallin rajoitukset).

## Yksinkertainen ja kehittynyt malli

Yläpalkin valitsimella **Yksinkertainen | Kehittynyt** vaihdetaan simulointimallia samalla tavalla kuin kieltä. Vaihto tehdään lennosta, piiri säilyy, ja valinta muistetaan selaimessa.

| | Yksinkertainen | Kehittynyt |
| --- | --- | --- |
| Tarkoitus | Perusyhtälöiden opettelu: tulos vastaa suoraan käsinlaskua | Todellisen järjestelmän häviöiden ja niiden vaikutusten tarkastelu |
| Pumppu | Ei vuotoa eikä hyötysuhdetta: Q = Vg·n/1000 | Volumetrinen ja hydromekaaninen hyötysuhde, vuoto kasvaa paineen mukana |
| Paineenrajoitusventtiili | Paine pysyy asetusarvossa | Paine nousee virtauksen mukana (ominaiskäyrä) |
| Suunta-, vasta- ja virranjakoventtiilit | Ei käytännössä painehäviötä eikä vuotoa | Painehäviö Δp = Δpn·(Q/Qn)², vuoto |
| Sylinteri | Ei kitkaa: p = F / A | Kitka, tartuntakitka ja viskoosi vaimennus |
| Hydraulimoottori | Ei vuotoa eikä kitkaa: n = Q / Vg, Δp = 20π·T / Vg | Vuoto, hyötysuhde ja viskoosi kitka |
| Ominaisuuspaneeli | Vain perusmitoitus (esim. sylinterin D, d, isku, massa, kuorma) | Kaikki parametrit |

Kuristus- ja vastusventtiilin kuristus toimii molemmissa malleissa samalla tavalla, koska kuristus on niiden tehtävä. Yksinkertaisessa mallissa toimilaitteiden vaimennus vaikuttaa vain nopeuden muutoksiin: se vaimentaa värähtelyt, mutta tasaisen liikkeen paineet ja nopeudet vastaavat perusyhtälöitä. Kiihdytyksen jälkeen paine asettuu noin sekunnissa.

Mallin vaihto ei hävitä arvoja. Kehittyneessä mallissa asetetut häviöparametrit (esim. kitkavoima) säilyvät tallessa ja palaavat käyttöön, kun vaihdat takaisin kehittyneeseen malliin.

Linkkiin voi kirjoittaa mallin valmiiksi: `?malli=yksinkertainen` tai `?malli=kehittynyt` (englanniksi `?mode=simple` tai `?mode=advanced`), esimerkiksi https://jipirtti.github.io/Hydrauliikkasimulaattori/?malli=yksinkertainen. Kieli ja malli voidaan yhdistää: `?lang=en&mode=simple`.

**Tehtävissä** kannattaa aina kertoa, kummalla mallilla tehtävä tehdään. Hyvä etenemistapa on laskea ilmiö ensin käsin, tarkistaa se yksinkertaisella mallilla ja katsoa sitten kehittyneellä mallilla, paljonko häviöt muuttavat tulosta.

## Näkymän osat

Näkymä jakautuu viiteen alueeseen. Kapealla näytöllä, kuten puhelimessa, alueet pinoutuvat allekkain ja paletti vierii vaakasuunnassa.

| Alue | Sijainti | Mitä siinä tehdään |
| --- | --- | --- |
| Yläpalkki | Ylhäällä | Käynnistä tai pysäytä simulointi, nollaa tila, valitse nopeus (1×–0,1×), lataa esimerkkipiiri, kumoa, tallenna tai lataa, sovita näkymä, tyhjennä alusta, avaa ohje. Simulaatioaika näkyy muodossa t = … s. |
| Paletti | Vasen reuna | Komponentit ryhmiteltyinä: pumput ja säiliöt, suuntaventtiilit, paine- ja virtaventtiilit, toimilaitteet, mittarit. |
| Piirtoalusta | Keskellä | Piiri rakennetaan ja simuloidaan tässä. Vasemmassa yläkulmassa on työkalurivi (Valitse ja kytke, Paine, Virtaus, Voima, Nopeus, Lukemat). Alhaalla ovat paineen väriasteikko ja varoitukset. |
| Ominaisuuspaneeli | Oikea reuna | Valitun komponentin tunnus, ohjaus, mitoitusparametrit, lasketut arvot ja mitoitusapu. Kun mitään ei ole valittu, paneeli näyttää piirin yhteenvedon ja pikaohjeen. |
| Mittauspaneeli | Alhaalla keskellä | Jokaisen anturin nykyinen lukema ja 10 sekunnin käyrä. Anturi poistetaan ✕-painikkeella. |

Piirtoalustaa siirretään vetämällä tyhjästä kohdasta ja zoomataan hiiren rullalla. Sovita näkymä tuo koko piirin ruudulle.

## Piirin rakentaminen

Piiri syntyy kolmessa vaiheessa: komponentit alustalle, letkut liitännästä liitäntään, mitoitusarvot kohdalleen.

### Komponentin lisääminen ja siirtäminen

1. Vedä komponentti paletista piirtoalustalle. Vaihtoehtoisesti klikkaa sitä, jolloin se ilmestyy näkymän keskelle.
2. Siirrä komponenttia vetämällä sen runkoa. Sijainti tarttuu 10 pikselin ruudukkoon.
3. Kierrä valittua komponenttia 90° R-näppäimellä tai ominaisuuspaneelin Kierrä 90° -painikkeella.
4. Poista valittu komponentti Delete-näppäimellä tai Poista-painikkeella. Siihen liitetyt letkut ja anturit poistuvat samalla.

### Linjojen piirtäminen

1. Varmista, että työkalurivillä on valittuna Valitse ja kytke. Jos anturityökalu on päällä, klikkaus lisää anturin eikä aloita linjaa. Esc palauttaa valintatyökalun.
2. Paina hiiren painike pohjaan liitännän pienen ympyrän päällä. Kursori muuttuu ristiksi. Jos painat rungosta, komponentti lähtee liikkumaan.
3. Vedä toisen liitännän päälle ja päästä irti. Katkoviiva näyttää kiinnityskohdan, ja noin 14 pikselin etäisyys liitännästä riittää.

Linjan reitti piirtyy automaattisesti suorakulmaisena, eikä siihen voi lisätä taitepisteitä. Reitti muuttuu, kun siirrät tai kierrät komponentteja, joten sijoita komponentit niin, että liitännät osoittavat toisiaan kohti.

- **Haara (T-liitos):** kytke toinen letku samaan liitäntään. Linjan keskelle ei voi kytkeä.
- **Tulppa:** kytkemätön liitäntä on tulpattu. Esimerkiksi 4/2-venttiilin B voi jäädä kytkemättä yksitoimisen sylinterin piirissä.
- **Kytkentätila:** kytketty liitäntä näkyy täytettynä pisteenä, kytkemätön tyhjänä ympyränä.
- **Linjan poisto:** klikkaa linjaa, jolloin se paksunee, ja paina Delete tai Poista kytkentä.
- **Kumoa:** Ctrl+Z tai Kumoa-painike peruu viimeisimmän muutoksen. Muistissa on 60 askelta.

Jos liitäntöihin on vaikea osua, zoomaa lähemmäs hiiren rullalla.

## Komponentit ja mitoitus

Paletissa on 15 komponenttia. Kun komponentti on valittuna, ominaisuuspaneelin Mitoitus-osassa muutetaan sen parametreja. Lasketut arvot päivittyvät simuloinnin aikana, ja Mitoitusapu laskee käänteisesti tarvittavan koon.

| Komponentti | Liitännät | Tärkeimmät mitoitusparametrit | Mitoitusapu |
| --- | --- | --- | --- |
| Vakiotilavuuspumppu | P, S (imu) | Vg (cm³/r), n (r/min), nimellispaine, ηv, ηhm | Vg halutusta tuotosta |
| Painesäädetty pumppu | P, S | Kuten edellä + säätöpaine | Vg halutusta tuotosta |
| Öljysäiliö | T | Tilavuus, öljymäärä alussa | – |
| 4/3-suuntaventtiili | P, T, A, B | Keskiasento (suljettu, tandem, avoin, kelluva), ohjaus (lukittuva tai jousipalautteinen), Qn ja Δp tietä kohden, vuoto | Painehäviö annetulla virtauksella |
| 4/2-suuntaventtiili | P, T, A, B | Ohjaus, Qn, Δp, vuoto. Lepoasento b: P→B, A→T | Painehäviö annetulla virtauksella |
| 3/2-suuntaventtiili | P, A, T | Ohjaus, Qn, Δp, vuoto. Asento a: P→A, T suljettu. Lepoasento b: A→T, P suljettu | Painehäviö annetulla virtauksella |
| Paineenrajoitusventtiili | P, T | Asetuspaine, Qn, paineen nousu Qn:llä | – |
| Vastaventtiili | A → B | Avautumispaine, Qn, Δp Qn:llä | – |
| Kuristusventtiili | A, B | Avaus %, Qn täysin auki, Δp Qn:llä | Avaus % halutusta virtauksesta ja paine-erosta |
| Vastusventtiili | A, B | Kuristus A→B, vapaa virtaus B→A vastaventtiilin kautta | – |
| Virranjakoventtiili | P (tulo), A, B (lähdöt) | Jakosuhde A-lähtöön (%), Qn, Δp Qn:llä. Jakaa tulovirran lähtöihin kiinteässä suhteessa kuormapaineista riippumatta. Jos toinen lähtö tukkeutuu, myös toinen pysähtyy. Paluusuunnassa venttiili yhdistää virrat samassa suhteessa. | – |
| Kaksitoiminen sylinteri | A (mäntäpuoli), B (varsipuoli) | D, d, isku, massa, kuorma ja sen tyyppi, asento, kitka, vaimennus, alkuasema | D voimasta ja paineesta (ehdottaa vakiokokoa D/d), Q halutusta nopeudesta |
| Yksitoiminen sylinteri | A | D, isku, massa, kuorma, jousen esijännitys ja jousivakio, asento | D voimasta ja paineesta |
| Hydraulimoottori | A, B | Vg, kuormitusmomentti, hitausmomentti, kitka, ηhm, vuoto | Vg väännöstä ja paine-erosta, Q nopeudesta |
| Paine- ja virtausmittari | P / A, B | Mitta-alue | – |

Kaikilla paineenalaisilla komponenteilla on Suurin sallittu paine. Jos piirin paine ylittää sen, alustalle tulee varoitus.

**Sylinterin kuorman tyyppi** kannattaa valita tarkoituksella:

- *Vastustaa liikettä* toimii kuin kitka. Se jarruttaa sekä ulos- että sisäänajoa.
- *Vakiovoima* painaa vartta sisäänpäin, kun F on positiivinen (negatiivinen F vetää ulos). Se auttaa sisäänajossa ja voi aiheuttaa ryntäävän kuorman ja kavitaation.
- *Pysty, ulosajo ylös* lisää painovoiman m·g, joka vastustaa ulosajoa ja laskee kuorman, kun A-puoli avataan säiliöön.
- *Pysty, ulosajo alas* (männänvarsi alaspäin, riippuva kuorma) kääntää painovoiman suunnan: m·g avustaa ulosajoa ja vastustaa sisäänajoa, joten sisäänajo vaatii rengaspuolelle paineen m·g / (A − a). Ilman jarrutusta kuorma ryntää ulosajossa pumpun tuottoa nopeammin ja A-puoli kavitoi.

Mitoitusavun kaavat:

$$D = \sqrt{\frac{4F}{\pi p}} \qquad V_g = \frac{Q \cdot 1000}{n \cdot \eta_v} \qquad V_g = \frac{20\pi T}{\Delta p \cdot \eta_{hm}}$$

Yksiköt: D (m), F (N), p (Pa); Vg (cm³/r), Q (L/min), n (r/min); T (Nm), Δp (bar).

## Simuloinnin ajaminen ja ohjaus

Simulointi käynnistyy itsestään, kun sivu avataan, ja laskee reaaliajassa. Valitse ensin yläpalkista simulointimalli (Yksinkertainen tai Kehittynyt, ks. edellä). Piiriä voi muokata simuloinnin pyöriessä: uusi kytkentä tulee voimaan heti.

- **Käynnistä / Pysäytä** (tai välilyönti) jäädyttää ajan. Lukemat ja käyrät jäävät näkyviin tarkastelua varten.
- **Nopeus** 0,5×, 0,2× tai 0,1× hidastaa nopeita tapahtumia, kuten painepiikkiä sylinterin osuessa päätyyn.
- **Nollaa tila** asettaa paineet nollaan, sylinterit alkuasemaansa, säiliöt alkutäyttöön ja tyhjentää käyrät. Piiri ja mitoitus säilyvät.

**Suuntaventtiilin ohjaus.** Klikkaa venttiilin kelaa, eli piirrosmerkin päädyssä olevaa vinoviivallista laatikkoa. Vasen kela vaihtaa asentoon a (P→A, B→T), oikea asentoon b (P→B, A→T). Aktiivinen kela näkyy oranssina, ja venttiilin ruudut liukuvat niin, että käytössä oleva ruutu on liitäntöjen kohdalla. Asennon voi valita myös ominaisuuspaneelin painikkeista a, 0 ja b.

- *Lukittuva:* kela pysyy päällä, kunnes klikkaat sitä uudelleen.
- *Jousipalautteinen:* kela on päällä vain niin kauan kuin pidät hiiren painiketta pohjassa, ja jousi palauttaa venttiilin keskiasentoon tai 4/2-venttiilillä lepoasentoon b.

**Pumpun ohjaus.** Klikkaa pumpun sähkömoottoria M tai paneelin painiketta. Käyvän moottorin ympärillä pyörii oranssi katkoviiva. Pumpun pyörimisnopeus nousee käynnistyksessä noin 0,1 sekunnissa.

**Kuristimen avaus** säädetään ominaisuuspaneelin liukusäätimellä, ja muutos näkyy nopeudessa välittömästi.

## Mittaukset ja anturit

Mittaustietoa saa neljällä tavalla: anturit, mittarikomponentit, letkujen värit ja hiiren alla näkyvä pikalukema.

### Anturit (probe-työkalut)

Valitse työkaluriviltä anturi ja klikkaa kohdetta. Anturin lappu ilmestyy piirrokseen ja sen käyrä mittauspaneeliin. Lapun voi siirtää vetämällä.

| Anturi | Kiinnitetään | Näyttää | Yksikkö |
| --- | --- | --- | --- |
| Paine (p) | Liitäntään (myös letkun päähän tai komponenttiin lähimpään liitäntään) | Liitännän paine | bar |
| Virtaus (Q) | Liitäntään | Tilavuusvirta liitännän läpi. Positiivinen = virtaa komponenttiin sisään. | L/min |
| Voima (F) | Sylinteriin | Hydraulinen voima pA·A − pB·(A − a). Positiivinen työntää ulos. | kN |
| Voima (T) | Moottoriin | Vääntömomentti | Nm |
| Nopeus (v) | Sylinteriin | Männän nopeus. Positiivinen = ulosajo. | mm/s |
| Nopeus (n) | Moottoriin | Pyörimisnopeus | r/min |

Käyrä näyttää 10 sekunnin historian ja skaalautuu automaattisesti. Asteikon ylä- ja alaraja näkyvät käyrän vasemmassa reunassa. Anturi poistetaan mittauspaneelin ✕-painikkeella.

### Muut lukemat

- **Letkun väri** kertoo paineen: sininen on matala, vihreä ja keltainen keskitaso, punainen lähellä asteikon maksimia. Maksimin (100, 160, 250 tai 400 bar) voi vaihtaa alanurkan valitsimesta. Violetti tarkoittaa alipainetta.
- **Liikkuva katkoviiva** letkussa näyttää virtauksen suunnan, ja sen nopeus kasvaa virtauksen mukana. Paikallaan pysyvä yhtenäinen viiva = ei virtausta.
- **Lukemat**-valinta näyttää jokaisen komponentin alla lyhyen lukeman, kuten sylinterin aseman ja nopeuden, pumpun tuoton tai venttiilin asennon.
- **Hiiren vieminen** liitännän tai letkun päälle näyttää hetkellisen paineen ja virtauksen.
- **Painemittari** ja **virtausmittari** ovat piirin komponentteja. Ne sopivat, kun mittaus halutaan näkyviin piirustukseen kuten oikeassa koneessa.
- **Sylinterin kammiot** värjäytyvät paineen mukaan, joten paine-ero A- ja B-puolen välillä näkyy suoraan piirrosmerkistä.

## Esimerkkikaavio: kaksitoiminen sylinteri ja 4/3-venttiili

Tämän kohdan lukuarvot on laskettu kehittyneellä mallilla. Yksinkertaisella mallilla A-puolen paine ulosajossa on 10,2 bar (= 2 kN / 19,6 cm², ei kitkaa) ja päädyssä tasan 100 bar.

Esimerkkipiiri 1 on hydrauliikan peruspiiri: pumppu syöttää 14,5 L/min, paineenrajoitusventtiili rajaa paineen 100 bariin, ja 4/3-venttiili ohjaa Ø50/28-sylinteriä, jonka kuormana on 2 kN. Lataa se yläpalkin valikosta Esimerkkipiirit → 1.

### Piirin osat

| Tunnus | Komponentti | Tehtävä piirissä |
| --- | --- | --- |
| P1 | Vakiotilavuuspumppu 10 cm³/r, 1450 r/min | Tuottaa noin 14,5 L/min. Imee säiliöstä S1. |
| PRV1 | Paineenrajoitusventtiili, asetus 100 bar | Avautuu, kun pumpun tuotolle ei ole muuta reittiä, ja johtaa öljyn säiliöön S2. |
| PI1 | Painemittari | Näyttää painelinjan paineen. |
| SV1 | 4/3-suuntaventtiili, suljettu keskiasento | Ohjaa öljyn sylinterin A- tai B-puolelle. Paluu säiliöön S3. |
| SYL1 | Kaksitoiminen sylinteri Ø50/28, isku 300 mm | Toimilaite. Kuorma 2000 N vastustaa liikettä. |

Piirissä on valmiina neljä anturia: paine SYL1:n A-liitännässä, virtaus SV1:n P-liitännässä sekä SYL1:n voima ja nopeus.

### Vaihe 1: lepotila

Kun SV1 on keskiasennossa, P-liitäntä on suljettu, joten pumpun koko tuotto menee PRV1:n kautta säiliöön. PI1 näyttää noin 103 bar, ja PRV1:n lukema on noin 14 L/min. Painelinja on oranssi ja PRV1:n paluulinja sininen, jossa katkoviiva liikkuu säiliöön päin. Tämä on lepotilan häviöteho: noin 2,4 kW muuttuu lämmöksi, minkä näet valitsemalla PRV1:n.

### Vaihe 2: ulosajo (kela a)

Klikkaa SV1:n vasenta kelaa. Kela muuttuu oranssiksi ja vasen ruutu, jossa nuolet ovat suoraan ylös ja alas, liukuu liitäntöjen kohdalle: P→A ja B→T.

![Esimerkkipiiri 1 ulosajon aikana: sylinteri liikkuu 123 mm/s, A-puolen paine 11,9 bar](kuvat/esim1_ulosajo.png)

Kuvassa näkyy:

1. **Paine laskee kuorman mukaiseksi.** A-puolella on 11,9 bar, koska paine määräytyy kuormasta eikä pumpusta: 2 kN kuorma ja kitka jaettuna männän pinta-alalla 19,6 cm² vastaa noin 11–12 baria. Kaikki letkut ovat sinisiä eli matalassa paineessa.
2. **Koko tuotto menee sylinteriin.** SV1:n P-liitännän virtaus on 14,5 L/min, ja PRV1 on kiinni (sen lukema palaa asetusarvoon 100 bar).
3. **Nopeus tulee tuotosta ja pinta-alasta.** v = Q / A = 14,5 L/min / 19,6 cm² ≈ 123 mm/s, sama kuin nopeusanturissa.
4. **Voima-anturi** näyttää 2,25 kN, eli kuorman ja kitkan summan.
5. **Virtauksen suunta** näkyy katkoviivoista: painelinjassa pumpulta venttiilille ja sylinterin A-puolelle, B-puolelta venttiilin kautta säiliöön S3.
6. **Sylinterin kammiot** ovat lähes samanvärisiä, koska paine-ero on pieni.

### Vaihe 3: sylinteri päädyssä

Kun mäntä saavuttaa 300 mm iskun pään, öljyllä ei ole minne mennä, joten paine nousee PRV1:n avautumispaineeseen.

![Sylinteri iskun päässä: A-puolen paine 102,8 bar, voima 20,19 kN](kuvat/esim1_paaty.png)

1. **Paine nousee järjestelmäpaineeseen.** A-puolen paine on 102,8 bar ja letkut ovat oransseja. 100 barin asetuksen päälle tulee 2,8 bar, koska PRV1 tarvitsee paineen nousua läpäistäkseen 14 L/min.
2. **Voima on suurin mahdollinen.** 102,8 bar × 19,6 cm² = 20,2 kN, sama kuin voima-anturissa. Tämä on sylinterin työntövoima tällä painetasolla.
3. **Nopeus on nolla ja P-virtaus on 0 L/min.** Koko tuotto kiertää PRV1:n kautta säiliöön S2, mikä näkyy PRV1:n lukemasta (14,2 L/min).
4. **Käyrät** mittauspaneelissa näyttävät porrastuksen: paine pysyy matalana liikkeen ajan ja hyppää ylös pysähdyksessä, samalla kun nopeus putoaa nollaan.

### Vaihe 4: sisäänajo (kela b)

Klikkaa oikeaa kelaa. Ristikkäiset nuolet tulevat liitäntöjen kohdalle: P→B ja A→T. Sylinteri ajaa sisään noin 178 mm/s, eli nopeammin kuin ulos, koska rengaspinta-ala (13,5 cm²) on männän pinta-alaa pienempi. Samasta syystä suurin vetovoima jää noin 14 kN:iin.

### Koko näkymä

![Koko käyttöliittymä: paletti vasemmalla, piirtoalusta keskellä, ominaisuuspaneeli oikealla ja mittauspaneeli alhaalla](kuvat/esim1_kokonakyma.png)

Oikean reunan ominaisuuspaneelissa on valittuna SV1: kelan asema a, mitoitusarvot ja lasketut arvot. Alhaalla mittauspaneeli piirtää jokaisen anturin käyrän.

## Muut esimerkkipiirit ja harjoitustehtävät

Esimerkkipiirit ladataan yläpalkin valikosta. Lataus korvaa nykyisen piirin, mutta Kumoa palauttaa sen. Alla olevan taulukon lukuarvot ovat kehittyneestä mallista; yksinkertaisen mallin arvot ovat taulukon jälkeen.

| Esimerkki | Mitä tehdään | Mitä pitäisi nähdä |
| --- | --- | --- |
| 2. Nopeudensäätö poistopuolelta (meter-out) | Klikkaa SV1:n vasenta kelaa. | Sylinteri ajaa ulos noin 65 mm/s, vaikka vapaa nopeus olisi 123 mm/s. Pumpun ylimääräinen tuotto menee paineenrajoitusventtiilin kautta säiliöön, joten A-puolella on noin 101 bar. B-puolella paine nousee noin 123 bariin, eli yli järjestelmäpaineen, koska rengaspinta on männän pintaa pienempi. Sisäänajo kulkee vastaventtiilin kautta täydellä nopeudella. |
| 3. Hydraulimoottori ja virtausmittari | Klikkaa SV1:n kelaa a tai b. | Moottori pyörii noin 700 r/min kumpaankin suuntaan, ja A-puolen paine on noin 67–76 bar (20 Nm kuorma). Tandem-keskiasennossa moottori pysähtyy ja pumppu kierrättää öljyn lähes paineettomana säiliöön. |
| 4. Yksitoiminen pystysylinteri, hallittu lasku | Klikkaa 4/2-venttiilin kelaa päälle ja uudelleen pois. | Nosto noin 190 mm/s noin 15 barin paineella (150 kg kuorma). Laskussa A-puoli avautuu säiliöön ja kuristin rajoittaa laskunopeuden noin 120 mm/s:iin. Ilman kuristinta kuorma putoaisi lähes vapaasti. |
| 5. Pikaliikekytkentä 3/2-venttiilillä | Pumppu 43,5 L/min, paineenrajoitus 50 bar, sylinteri Ø60/30, 1000 kg vaakasuorassa. SV2 on lepoasennossa (pikaliike): klikkaa SV1:n kelaa a. Vaihda sitten SV2 asentoon a (normaali) ja aja uudelleen. | Pikaliikkeessä rengaspuolen öljy kiertää A-puolelle, ja nopeus on v = Q / a ≈ 1,0 m/s. Normaalisti ulosajo on 256 mm/s ja sisäänajo 341 mm/s. Sisäänajo onnistuu vain SV2:n asennossa a, koska lepoasennossa pääventtiilin B-linja on suljettu. Asenna sylinteri pystyyn (Asento: Pysty, ulosajo ylös): pikaliike ei nosta 1000 kg:n kuormaa, koska voima on vain p·a = 50 bar · 707 mm² ≈ 3,9 kN. Pikaliikkeen nopeus jää teoriasta, jos SV2 on alimitoitettu (kokeile Qn 30 L/min). |
| 6. Moottori sylinterin rinnalla | Sama pumppu ja sylinteri pystyssä, moottori Vg 20 cm³/r on kytketty A- ja B-linjan väliin. Klikkaa SV1:n kelaa a ja kokeile moottorin kuormitusmomenttia 0, 5 ja 40 Nm. | Virtaus menee pienimmän paineen tietä. 0 Nm: moottori vie koko tuoton (noin 2160 r/min) eikä kuorma nouse. 5 Nm: sylinteri lähtee nousemaan, mutta hidastuu sitä mukaa kuin moottori kiihtyy. 40 Nm: moottori tarvitsisi noin 140 bar, joten se ei pyöri ja sylinteri saa koko tuoton (253 mm/s). |
| 7. Virranjakoventtiilit ja vastaventtiilit | Kuten esimerkki 6, mutta A- ja B-linjoissa on virranjakoventtiilit (50/50) ja niiden rinnalla paluuvirtauksen vastaventtiilit. Klikkaa SV1:n kelaa a ja pidä se päällä, kunnes sylinteri on päädyssä. | Sylinteri (127 mm/s) ja moottori (noin 1070 r/min) liikkuvat yhtä aikaa, koska kumpikin saa puolet tuotosta kuormapaineista riippumatta. Kun sylinteri on päädyssä, virranjakajan sylinterilähtö tukkeutuu ja myös moottori pysähtyy; paine nousee paineenrajoitusventtiilin avautumispaineeseen. Vastaventtiilit päästävät poistuvan öljyn ohi virranjakajan, jolloin paluuvirtaus ei kulje jakajan läpi. |

Yksinkertaisen mallin arvot samoissa esimerkeissä (vastaavat käsinlaskua):

| Esimerkki | Yksinkertainen malli | Käsinlasku |
| --- | --- | --- |
| 1 | Ulos 123 mm/s ja 10,2 bar, sisään 179 mm/s, päädyssä 100 bar | v = Q/A, p = F/A, v = Q/(A − a) |
| 3 | 725 r/min, paine-ero 62,8 bar | n = Q/Vg, Δp = 20π·T/Vg |
| 5 | Pikaliike 1,02 m/s | v = Q/a |
| 6 (moottori 40 Nm) | Sylinteri 256 mm/s, nostopaine 34,7 bar | v = Q/A, p = m·g/A |
| 7 | Sylinteri 128 mm/s, moottori 1090 r/min | v = (Q/2)/A, n = (Q/2)/Vg |

### Harjoitustehtäviä

Suluissa on malli, jolla tehtävä on tarkoitettu tehtäväksi.

1. (Yksinkertainen) Laske esimerkissä 1 sylinterin ulos- ja sisäänajonopeus käsin pumpun tuotosta. Tarkista tulos nopeusanturilla.
2. (Kehittynyt) Vaihda esimerkin 1 venttiilin keskiasennoksi tandem. Mitä tapahtuu paineenrajoitusventtiilin läpi menevälle virtaukselle ja pumpun tehontarpeelle keskiasennossa?
3. (Yksinkertainen) Nosta esimerkin 1 sylinterin kuorma 25 kN:iin. Miksi sylinteri ei liiku ulos? Mitoita Mitoitusavulla uusi sylinteri ja kokeile.
4. (Kehittynyt) Vaihda esimerkin 2 kuristus tulopuolelle (A-linjaan) ja vertaa B-puolen painetta poistopuolen kuristukseen.
5. (Kehittynyt) Poista esimerkistä 4 kuristin ja kytke venttiili suoraan sylinteriin. Seuraa laskunopeutta ja A-puolen painetta laskun aikana.
6. (Kehittynyt) Vaihda esimerkin 1 pumppu painesäädetyksi (säätöpaine 90 bar). Mitä tapahtuu paineenrajoitusventtiilin virtaukselle sylinterin ollessa päädyssä?
7. (Yksinkertainen, sitten kehittynyt) Valitse esimerkin 1 sylinterin asennoksi Pysty, ulosajo alas ja massaksi 1000 kg. Aja sylinteriä molempiin suuntiin. Miksi ulosajo on pumpun tuottoa nopeampi, ja millä paineenrajoituksen asetuksella sylinteri nousee takaisin? Vertaa käsinlaskuun m·g / (A − a).
8. (Yksinkertainen) Poista esimerkin 7 virranjakoventtiilit ja vastaventtiilit ja korvaa ne suorilla letkuilla. Mitä moottorille ja sylinterille tapahtuu nyt, ja miksi tulos eroaa virranjakajan kanssa saadusta?
9. (Molemmat) Aja esimerkki 1 ulos ensin yksinkertaisella ja sitten kehittyneellä mallilla. Kirjaa molemmista A-puolen paine liikkeen aikana, nopeus ja paine päädyssä. Mistä häviöistä erot syntyvät? Laske kehittyneen mallin hydraulinen hyötysuhde liikkeen aikana (hyödyllinen teho F·v jaettuna pumpun teholla p·Q).
10. (Molemmat) Aja esimerkki 5 pikaliikkeellä molemmilla malleilla. Miksi kehittyneessä mallissa nopeus jää teoreettisesta, ja mitä tapahtuu, kun SV2:n nimellisvirtaus pienennetään 30 L/min:iin?

Kun laadit omia tehtäviä simulaattorille, anna tehtävässä pumpun tuotto, paineenrajoituksen asetus, sylinterin mitat ja isku, venttiilien nimellisvirtaus sekä moottorin kuormitusmomentti. Erityisesti pikaliikkeen nopeus ja rinnakkaisten toimilaitteiden käyttäytyminen riippuvat näistä arvoista.

## Varoitukset, tallennus ja rajoitukset

### Varoitukset ja vianetsintä

Varoitukset näkyvät piirtoalustan alareunassa punareunaisina laatikoina.

| Varoitus | Syy | Korjaus |
| --- | --- | --- |
| Paine ylittää sallitun | Liitännän paine on yli komponentin Suurin sallittu paine -arvon. | Laske paineenrajoitusventtiilin asetusta tai valitse kestävämpi komponentti. |
| Pumppu ei saa öljyä | Pumpun imuliitäntä S on kytkemättä tai tukossa. | Kytke S säiliön T-liitäntään. |
| Alipaine (kavitaatio) | Jonkin verkon paine on painunut alle −0,95 bar, esimerkiksi ryntäävä kuorma tai jarruttava moottori. | Lisää vastapaine, kuristus poistopuolelle tai täyttölinja. |
| Paine karkaa | Vakiotilavuuspumpun tuotolla ei ole reittiä, eikä piirissä ole paineenrajoitusventtiiliä. | Lisää paineenrajoitusventtiili pumpun painelinjaan. |
| Numeerinen virhe | Laskenta ei konvergoinut; paineet nollattiin. | Tarkista kytkennät ja äärimmäiset parametrit, paina Nollaa tila. |

Jos sylinteri ei liiku, tarkista ensin, että venttiilin kela on päällä ja pumppu käy. Katso sitten, riittääkö voima: hydraulinen voima on pienempi kuin kuorma, kitka ja tartuntakitka (1,25 × kitkavoima) yhteensä.

### Tallennus ja jakaminen

Piiri, mitoitus ja anturit tallentuvat automaattisesti selaimen muistiin, ja ne palautuvat kun sivu avataan samalla selaimella. Tallenna / lataa avaa piirin tekstimuodossa (JSON). Kopioi teksti talteen, niin voit jakaa sen esimerkiksi opiskelijoille tehtäväpohjaksi. Lataaminen tapahtuu liittämällä teksti kenttään ja valitsemalla Lataa.

### Mallin rajoitukset

Paineet ratkaistaan 1 ms aika-askeleella implisiittisesti öljyn kokoonpuristuvuudesta (tehollinen puristuvuusmoduuli 1,2 GPa) ja kuristusyhtälöstä Q = Cd·A·√(2Δp/ρ). Sylinterissä on massa, kitka, tartuntakitka ja vasteet, moottorissa hitausmomentti ja kuormitusmomentti. Mallissa ei ole letkujen painehäviöitä, lämpenemistä, viskositeetin muutosta, venttiilien ohjausdynamiikkaa eikä silmukoissa (rinnakkaisissa letkuissa) letkukohtaista virtausta.

### Pikanäppäimet

| Näppäin | Toiminto |
| --- | --- |
| Välilyönti | Käynnistä tai pysäytä |
| Delete / Backspace | Poista valittu komponentti tai letku |
| R | Kierrä valittua 90° |
| Ctrl+Z | Kumoa |
| V tai Esc | Valitse ja kytke -työkalu |
| Hiiren rulla | Zoomaa |

## Tekijä ja lisenssi

Tekijä: Juho Pirttilahti, Seinäjoen ammattikorkeakoulu (SEAMK), 2026. Suunnittelu, sisältö ja validointi: Juho Pirttilahti. Ohjelmakoodi toteutettu tekoälyavusteisesti (Claude, Anthropic).

Tämä käyttöohje ja Hydrauliikkasimulaattori-ohjelmisto on lisensoitu [Creative Commons Nimeä 4.0 Kansainvälinen -lisenssillä (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.fi). Saat kopioida, jakaa ja muokata aineistoa mihin tahansa tarkoitukseen, kunhan mainitset tekijän ja oppilaitoksen, merkitset lisenssin ja kerrot, jos olet muuttanut aineistoa.

Suositeltu viittaus: Pirttilahti, J. (2026). *Hydrauliikkasimulaattori ja käyttöohje.* Seinäjoen ammattikorkeakoulu. CC BY 4.0.
