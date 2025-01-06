# TEE PELI TÄHÄN
import pygame
from random import randint
import time
pygame.init()

class Hirvio:
    def __init__(self):
        self.hirvio = pygame.image.load("iivo.png")
        self.pituus = self.hirvio.get_height()
        self.leveys = self.hirvio.get_width()

        self.hirviot = [self.uusi_hirvio(i) for i in range(5)]
        

    def uusi_hirvio(self, i : int):
        #joka kolmas hirviö ylhäältä, muut sivuilta
        if i % 3 == 0:
            x_hirvio = randint(0, 640 - self.pituus) 
            y_hirvio = randint(-700, -self.pituus)
            suunta = "Y" #ylhäältä
        else:
            if randint(0,1): #kumpi sivu?
                x_hirvio = randint(-700, -self.leveys)
                y_hirvio = randint(0, 480 - self.pituus - 50) #alapalkkikorjaus
                suunta = "V" #vasemmalta
            else:
                x_hirvio = randint(640, 640+700)
                y_hirvio = randint(0, 480 - self.pituus - 50) #alapalkkikorjaus
                suunta = "O" #oikealta
        
        return {"x_hirvio": x_hirvio, "y_hirvio":y_hirvio, "suunta":suunta}

    def liikuta(self):
        i=0
        x_muutos = 0
        y_muutos = 0
        for hirvio in self.hirviot:
            if hirvio["suunta"] == "V":
                x_muutos = 1
                y_muutos = 0
            if hirvio["suunta"] == "O":
                x_muutos = -1
                y_muutos = 0
            if hirvio["suunta"] == "Y":
                y_muutos = 1
                x_muutos = 0

            hirvio["x_hirvio"] += x_muutos
            hirvio["y_hirvio"] += y_muutos


                #poisto ja uuden lisäys
            if hirvio["x_hirvio"] < -100 and hirvio["suunta"] == "O":
                self.hirviot.remove(hirvio)
                i += 1
                self.hirviot.append(self.uusi_hirvio(i))
                
            if hirvio["x_hirvio"] > 740 and hirvio["suunta"] == "V":
                self.hirviot.remove(hirvio)
                self.hirviot.append(self.uusi_hirvio(i))

            if hirvio["y_hirvio"] > 480 - self.pituus -50:
                self.hirviot.remove(hirvio)
                i += 1
                self.hirviot.append(self.uusi_hirvio(i))
        
        return self.hirviot


class Robo:
    def __init__(self):
        self.robo = pygame.image.load("kleebutin.png")
        self.pituus = self.robo.get_height()
        self.leveys = self.robo.get_width()
        self.x , self.y = (randint(0, 640 - self.leveys) , randint(0, 480 - self.pituus - 50))

    def liikuta(self, vasen, oikea, ylos, alas):
        #not-määreet estävät sivuliidon
        if vasen and not ylos and not alas:
            if self.x - 3 >= 0:
                self.x -= 3
        elif oikea and not ylos and not alas:
            if self.x + 3 <= 640 - self.leveys:
                self.x += 3
        elif ylos and not vasen and not oikea:
            if self.y - 3 >= 0:
                self.y -= 3
        elif alas and not vasen and not oikea:
            if self.y + 3 <= 480 - self.pituus - 50: #alapalkkikorjaus
                self.y += 3

        return (self.x, self.y)


class Peli:

    def __init__(self, parasaik=0, paraspist=0):
        #hahmot
        self.pahikset = Hirvio()
        self.kolikko = pygame.image.load("juusto.png")
        self.robo1 = Robo()
        self.kolikko_uuteen_paikkaan()
        #grafiikat
        self.ikkuna = pygame.display.set_mode((640,480))
        self.pisteet = 0
        self.fontti1 = pygame.font.SysFont("Arial", 24)
        self.fontti2 = pygame.font.SysFont("Impact", 100)
        self.fontti3 = pygame.font.SysFont("Arial", 40)
        self.fontti4 = pygame.font.SysFont("Arial", 20)
        #apumuuttujat
        self.valeaika = 0
        self.aika = 0
        self.maxpist = paraspist
        self.maxaika = parasaik
        self.vasen1 = False
        self.oikea1 = False
        self.ylos1 = False
        self.alas1 = False
        self.voittiko = False
        self.robon_koordinaatit = None
        #äänet:
        self.loppu_aani = pygame.mixer.Sound("nauru.mp3")
        self.kolikon_aani = pygame.mixer.Sound("vau.mp3")
        self.voittoaani = pygame.mixer.Sound("voitto.mp3")
    
    def osuma_kolikkoon(self):
        robon_oikx = self.robo1.x + self.robo1.leveys
        robon_vasx = self.robo1.x
        robon_ylay = self.robo1.y
        robon_alay = self.robo1.y + self.robo1.pituus
        if robon_oikx - 7 > self.kolikon_paikka[0] and robon_vasx + 7 < self.kolikon_paikka[0] + self.kolikko.get_width():
            if robon_alay > self.kolikon_paikka[1] and robon_ylay < self.kolikon_paikka[1] + self.kolikko.get_height():
                return True

        return False
    
    def kolikko_uuteen_paikkaan(self):
        #varmistetaan, ettei kolikon paikka ole sellainen, että robo sen heti nappaa
        while True:
            self.kolikon_paikka = (randint(0, 640 - self.kolikko.get_width()), randint(0, 480 - self.kolikko.get_height() -50))
            if not self.osuma_kolikkoon():
                return self.kolikon_paikka
            
    
    def osuma_hirvioon(self):
        #Tarkastellaan erikseen tilanteet, joissa ollaan kleebun tai iivon päässä verrattuna torsoon, koska eri muotoiset.
        for hirvio in self.pahikset.hirviot:
            if self.robo1.y + self.robo1.pituus < hirvio["y_hirvio"] + self.pahikset.pituus/2 + 6 or self.robo1.y > hirvio["y_hirvio"] + self.pahikset.pituus/2 - 3:
                if self.robo1.x + 24 < hirvio["x_hirvio"] + self.pahikset.leveys and self.robo1.x + self.robo1.leveys - 24 > hirvio["x_hirvio"]:
                    if self.robo1.y + 1 < hirvio["y_hirvio"] + self.pahikset.pituus and self.robo1.y + self.robo1.pituus - 1 > hirvio["y_hirvio"]:
                        return True
            else:
                if self.robo1.x + 5 < hirvio["x_hirvio"] + self.pahikset.leveys and self.robo1.x + self.robo1.leveys - 5 > hirvio["x_hirvio"]:
                    if self.robo1.y + 1 < hirvio["y_hirvio"] + self.pahikset.pituus and self.robo1.y + self.robo1.pituus - 1 > hirvio["y_hirvio"]:
                        return True
        
        return False


    
    def high_score(self):
        #tarkistaa pelin loputtua, onko nyt saatu piste määrä isoin jne.
        if self.pisteet >= self.maxpist:
            if self.pisteet == self.maxpist:
                if self.aika < self.maxaika:
                    self.maxaika = self.aika
            else:
                self.maxpist = self.pisteet
                self.maxaika = self.aika
        
    

    def loppu(self):
        if self.voittiko:
            overi = self.fontti2.render("LÄPÄISIT PELIN", True, (255,0,0))
            overi_x = 35
            overi_y = 110
        else:
            overi = self.fontti2.render("GAME OVER", True, (255,0,0))
            overi_x = 100
            overi_y = 100
        
        #kirjataan mahdollisesti paras tulos
        self.high_score()
        
        teksti1 = self.fontti1.render(f"Aika: {self.aika: .1f}", True, (255, 0, 0))
        vallari = self.fontti3.render(f"Välilyönti = uusi peli", True, (255,0,0))

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_SPACE:
                        Peli(self.maxaika, self.maxpist).suorita()

            self.ikkuna.blit(self.robo1.robo, self.robon_koordinaatit)
            self.ikkuna.blit(self.kolikko, self.kolikon_paikka)
            self.alapalkki()
            self.ikkuna.blit(overi, (overi_x,overi_y))
            self.ikkuna.blit(teksti1, (500, 480-40))
            self.ikkuna.blit(vallari, (160, 250))
            pygame.display.flip()

    def ajanotto(self):
        self.valeaika += 1
        if self.valeaika % 200:
            self.aika = self.valeaika / 200

        teksti1 = self.fontti1.render(f"Aika: {self.aika: .1f}", True, (255, 0, 0))
        self.ikkuna.blit(teksti1, (500, 480-40))

    def alapalkki(self):
        alapalkki = pygame.Rect((0,480-50), (640, 50))
        pygame.draw.rect(self.ikkuna, (0, 0, 0), alapalkki)
        teksti = self.fontti1.render(f"Pisteet: {self.pisteet}", True, (255, 0, 0))
        high = self.fontti1.render(f"Parhaat: {self.maxpist} p ja {self.maxaika: .1f} s", True, (255,0,0)) 
        self.ikkuna.blit(high, (200, 480-40))
        self.ikkuna.blit(teksti, (10, 480 - 40))
    
    def ohjeet(self):
        teksti = self.fontti3.render("Tehtävänäsi on kerätä 20 juustoa.", True, (0, 0, 0))
        pygame.display.set_caption("Kleebun juustonmetsästys")
        teksti2 = self.fontti3.render("Kuinka nopeasti pystyt?", True, (0,0,0))
        teksti3 = self.fontti3.render("Huom! (w-a-s-d)", True, (0,0,0))
        starttiteksti = self.fontti4.render("Aloita", True, (0,0,0))
        starttinappula = pygame.Rect((280,370), (100, 30))
        self.ikkuna.fill((255,255,255))
        self.ikkuna.blit(teksti, (50,100))
        self.ikkuna.blit(teksti2, (50, 200))
        self.ikkuna.blit(teksti3, (50, 300))
        pygame.draw.rect(self.ikkuna, (150, 150, 150), starttinappula)
        self.ikkuna.blit(starttiteksti, (305,375))
        pygame.display.flip()
        #mahdollistetaan myös tässä vaiheessa raksitus
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    if tapahtuma.pos[1] > 370 and tapahtuma.pos[1] < 400:
                        if tapahtuma.pos[0] > 280 and tapahtuma.pos[0] < 380:
                            self.suorita()
        
    def suorita(self):
        kello = pygame.time.Clock()

        while True:
            
            self.ikkuna.fill((230,230,230))
            #alapalkki
            self.alapalkki()

            #ajanottoa
            self.ajanotto()

            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikea1 = True
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasen1 = True
                    if tapahtuma.key == pygame.K_DOWN:
                        self.alas1 = True
                    if tapahtuma.key == pygame.K_UP:
                        self.ylos1 = True

                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikea1 = False
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasen1 = False
                    if tapahtuma.key == pygame.K_DOWN:
                        self.alas1 = False
                    if tapahtuma.key == pygame.K_UP:
                        self.ylos1 = False
            
            #pahikset liikkuu
            for hirvio in self.pahikset.liikuta():
                self.ikkuna.blit(self.pahikset.hirvio, (hirvio["x_hirvio"],hirvio["y_hirvio"]))

            if self.osuma_kolikkoon():
                self.pisteet += 1
                self.kolikon_aani.play()
                if self.pisteet == 20:
                    self.voittiko = True
                    self.voittoaani.play()
                    time.sleep(0.4)
                    break
                self.kolikko_uuteen_paikkaan()
            
            self.ikkuna.blit(self.kolikko, self.kolikon_paikka)

            if self.osuma_hirvioon():
                self.loppu_aani.play(fade_ms=20)
                time.sleep(0.4)
                break
            
            #robon liike
            self.robon_koordinaatit = self.robo1.liikuta(self.vasen1,self.oikea1,self.ylos1,self.alas1)
            self.ikkuna.blit(self.robo1.robo, self.robon_koordinaatit)

            pygame.display.flip()
            kello.tick(200)

        #breakilla silmukasta ulos
        self.loppu()

#tässä on ns. pääkoodi :-)
Peli().ohjeet()
