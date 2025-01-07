Tehtävänanto oli seuraava:

Tässä tehtävässä tehdään sovellus, jonka avulla on mahdollista tarkastella NHL-jääkiekkoliigan tilastoja muutamassa hieman erilaisessa muodossa.

Tehtäväpohjan mukana tulee kaksi json-muodossa olevaa tiedostoa osa.json ja kaikki.json, näistä ensimmäinen on tarkoitettu lähinnä testailun avuksi. Jälkimmäinen sisältää kaikkien kaudella 2019-20 pelanneiden pelaajien statistiikat.

Yksittäisen pelaajan tiedot ovat muodossa

{
    "name": "Patrik Laine",
    "nationality": "FIN",
    "assists": 35,
    "goals": 28,
    "penalties": 22,
    "team": "WPG",
    "games": 68
},

ja molemmat tiedostoista sisältävät yksittäisten pelaajien tiedot taulukossa.

Jos et muista, miten json-muotoinen tiedosto saadaan luettua Python-ohjelmaan, voit kerrata tämän osan 7 materiaalista.

Tee nyt ohjelma, joka kysyy aluksi tiedoston nimeä ja tarjoaa sitten seuraavat toiminnot:

    yksittäisen pelaajan tietojen haku nimen perusteella
    listaus joukkueiden nimien lyhenteistä (aakkosjärjestyksessä)
    listaus maiden nimien lyhenteistä (aakkosjärjestyksessä)

Näistä toiminnoista saa yhden pisteen. Ohjelman tulee toimia seuraavasti:
Esimerkkitulostus

tiedosto: osa.json
luettiin 14 pelaajan tiedot

komennot:
0 lopeta
1 hae pelaaja
2 joukkueet
3 maat
4 joukkueen pelaajat
5 maan pelaajat
6 eniten pisteitä
7 eniten maaleja

komento: 1
nimi: Travis Zajac

Travis Zajac         NJD   9 + 16 =  25

komento: 2
BUF
CGY
DAL
NJD
NYI
OTT
PIT
WPG
WSH

komento: 3
CAN
CHE
CZE
SWE
USA

komento: 0

Huomaa, että pelaajien tulostusasun pitää olla täsmälleen seuraavanlainen:
Esimerkkitulostus

Leon Draisaitl       EDM  43 + 67 = 110
Connor McDavid       EDM  34 + 63 =  97
Travis Zajac         NJD   9 + 16 =  25
Mike Green           EDM   3 +  8 =  11
Markus Granlund      EDM   3 +  1 =   4
123456789012345678901234567890123456789

Alimman rivin numerot on lisätty helpottamaan oikean merkkimäärän laskemista. Joukkueen nimen lyhenne siis tulostetaan alkaen rivin 22. merkistä. Plus on rivin 30. merkki ja = rivin 35. merkki. Kaikki luvut tulee tasata oikeaan reunaan omaa tulostusaluettaan. Tyhjät kohdat ovat välilyöntejä.

Tulostuksen muotoilu kannattaa hoitaa f-merkkijonoina samaan tapaan kuin tässä osan 6 tehtävässä.

Seuraavat toiminnot tuovat toisen pisteen:

    joukkueen pelaajien listaaminen pisteiden (joka saadaan laskemalla goals + assits) mukaisessa järjestyksessä
    tietyn maan pelaajien listaaminen pisteiden mukaisessa järjestyksessä

Toiminnallisuus on seuraava:
Esimerkkitulostus

tiedosto: osa.json
luettiin 14 pelaajan tiedot

komennot:
0 lopeta
1 hae pelaaja
2 joukkueet
3 maat
4 joukkueen pelaajat
5 maan pelaajat
6 eniten pisteitä
7 eniten maaleja

komento: 4
joukkue: OTT

Drake Batherson      OTT   3 +  7 =  10
Jonathan Davidsson   OTT   0 +  1 =   1

komento: 5
maa: CAN

Jared McCann         PIT  14 + 21 =  35
Travis Zajac         NJD   9 + 16 =  25
Taylor Fedun         DAL   2 +  7 =   9
Mark Jankowski       CGY   5 +  2 =   7
Logan Shaw           WPG   3 +  2 =   5

komento: 0

Kolmannen pisteen saa seuraavilla toiminnoilla:

    n eniten pistettä saanutta pelaajaa
        jos kahden pelaajan pistemäärä on sama, ratkaisee maalimäärä
    n eniten maaleja (goals) tehnyttä pelaajaa
        jos kahden pelaajan maalimäärä on sama, järjestyksen ratkaisee se kummalla on vähemmän otteluja (games)

Toiminnallisuus on seuraava:
Esimerkkitulostus

tiedosto: osa.json
luettiin 14 pelaajan tiedot

komennot:
0 lopeta
1 hae pelaaja
2 joukkueet
3 maat
4 joukkueen pelaajat
5 maan pelaajat
6 eniten pisteitä
7 eniten maaleja

komento: 6
kuinka monta: 2

Jakub Vrana          WSH  25 + 27 =  52
Jared McCann         PIT  14 + 21 =  35

komento: 6
kuinka monta: 5

Jakub Vrana          WSH  25 + 27 =  52
Jared McCann         PIT  14 + 21 =  35
John Klingberg       DAL   6 + 26 =  32
Travis Zajac         NJD   9 + 16 =  25
Conor Sheary         BUF  10 + 13 =  23

komento: 7
kuinka monta: 6

Jakub Vrana          WSH  25 + 27 =  52
Jared McCann         PIT  14 + 21 =  35
Conor Sheary         BUF  10 + 13 =  23
Travis Zajac         NJD   9 + 16 =  25
John Klingberg       DAL   6 + 26 =  32
Mark Jankowski       CGY   5 +  2 =   7

komento: 0
