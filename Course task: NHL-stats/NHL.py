# tee ratkaisusi tänne
from json import loads

class Tiedosto:
    def __init__(self, nimi):
        self.nimi=nimi
    
    def hae_data(self):
        with open(self.nimi) as tiedosto:
            data=tiedosto.read()
            return loads(data)
        

class Tilasto:
    def __init__(self):
        self.__tiedot=None
    
    def lisaa_tietoa(self, tiedot: list):
        self.__tiedot=tiedot

    def etsi_pelaaja(self, pelaaja: str):
        return [sanis for sanis in self.__tiedot if sanis["name"]==pelaaja][0]
    
    def tulosta_pelaaja(self, pelaajan_tiedot: dict):
        nimi=pelaajan_tiedot["name"]
        joukkue=pelaajan_tiedot["team"]
        maalit=pelaajan_tiedot["goals"]
        syotot=pelaajan_tiedot["assists"]
        pojot=maalit+syotot
        print(f"{nimi:21}{joukkue}{maalit:4} + {syotot:2} = {pojot:3}")

    def etsi_joukkueet(self):
        joukkueet=[pelaaja["team"] for pelaaja in self.__tiedot]
        return sorted(set(joukkueet))

    def etsi_maat(self):
        maat = [pelaaja["nationality"] for pelaaja in self.__tiedot]
        return sorted(set(maat))

    def valitse_pelaajat_maittain(self,maa: str):
        pelaajat = [pelaaja for pelaaja in self.__tiedot if pelaaja["nationality"]==maa]
        return sorted(pelaajat,key=lambda x: x["goals"]+x["assists"], reverse=True)
    
    def valitse_pelaajat_joukkueittain(self, joukkue: str):
        pelaajat = [pelaaja for pelaaja in self.__tiedot if pelaaja["team"]==joukkue]
        return sorted(pelaajat,key=lambda x: x["goals"]+x["assists"], reverse=True)
    
    def jarjesta_pisteiden_mukaan(self, montako: int):
        data = sorted(self.__tiedot, key=lambda x: (x["goals"]+x["assists"], x["goals"]), reverse=True)  
        return data[:montako]

    def jarjesta_maalien_mukaan(self, montako: int):
        data = sorted(self.__tiedot, key=lambda x: (x["goals"], -1*x["games"]), reverse=True)
        return data[:montako]

class Tilastosovellus:
    def __init__(self):
        self.__tilasto = Tilasto()

    ohjeet = """
komennot:
0 lopeta
1 hae pelaaja
2 joukkueet
3 maat
4 joukkueen pelaajat
5 maan pelaajat
6 eniten pisteitä
7 eniten maaleja"""

    def hae_pelaaja(self):
        pelaaja = input("nimi: ")
        pelaajan_tiedot = self.__tilasto.etsi_pelaaja(pelaaja)
        self.__tilasto.tulosta_pelaaja(pelaajan_tiedot)

    def kysy_tiedosto(self):
        tiedoston_nimi = input("tiedosto: ")
        tiedot=Tiedosto(tiedoston_nimi).hae_data()
        self.__tilasto.lisaa_tietoa(tiedot) #lisätään data Tilasto-oliolle, jotta sen luokan metodit pääsevät töihin
        print(f"luettiin {len(tiedot)} pelaajan tiedot")
    
    def tulosta_joukkueet(self):
        data=self.__tilasto.etsi_joukkueet()
        for nimi in data:
            print(nimi)
    
    def tulosta_maat(self):
        data=self.__tilasto.etsi_maat()
        for nimi in data:
            print(nimi)
    
    def maan_pelaajat(self):
        maa=input("maa: ")
        data=self.__tilasto.valitse_pelaajat_maittain(maa)
        for pelaaja in data:
            self.__tilasto.tulosta_pelaaja(pelaaja)
    
    def joukkueen_pelaajat(self):
        joukkue=input("joukkue: ")
        data=self.__tilasto.valitse_pelaajat_joukkueittain(joukkue)
        for pelaaja in data:
            self.__tilasto.tulosta_pelaaja(pelaaja)
    
    def eniten_pojoja(self):
        montako=input("kuinka monta: ")
        data = self.__tilasto.jarjesta_pisteiden_mukaan(int(montako))
        for pelaaja in data:
            self.__tilasto.tulosta_pelaaja(pelaaja)
    
    def eniten_maaleja(self):
        montako=input("kuinka monta: ")
        data = self.__tilasto.jarjesta_maalien_mukaan(int(montako))
        for pelaaja in data:
            self.__tilasto.tulosta_pelaaja(pelaaja)

    def suorita(self):
        self.kysy_tiedosto()

        print(Tilastosovellus.ohjeet)

        while True:
            syote = int(input("komento: "))
            if syote==0:
                break
            if syote==1:
                self.hae_pelaaja()
            if syote==2:
                self.tulosta_joukkueet()
            if syote==3:
                self.tulosta_maat()
            if syote==4:
                self.joukkueen_pelaajat()
            if syote==5:
                self.maan_pelaajat()
            if syote==6:
                self.eniten_pojoja()
            if syote==7:
                self.eniten_maaleja()

Tilastosovellus().suorita()
