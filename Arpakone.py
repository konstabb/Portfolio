#tasaiset jaot
import numpy as np
import matplotlib.pyplot as plt

def rosteri(pelaajat):
    roster = [("Kaapeli",91) , ("Antti",94) , ("Konsta",93) , ("Pasi",92), ("Aku",91), ("Tero",88) , ("Teemu",93) , ("Hannu",92) , ("Antero",90) , ("Pekka",92), ("Paavo", 93), 
              ("Tuomo", 96), ("Atro", 95), ("Timo", 89), ("Julli", 91), ("Harri", 91)]
    pelkat_pelaajat = [pelaaja[0] for pelaaja in roster]
    for peluri in pelaajat:
        if peluri not in pelkat_pelaajat:
            roster.append((peluri,91))
    return [peluri for peluri in roster if peluri[0] in pelaajat]


def kombinaatiot(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indx = list(range(r))
    yield tuple(pool[i] for i in indx)
    while True:
        for i in reversed(range(r)):
            if indx[i] != i + n - r:
                break
        else:
            return
        indx[i] += 1
        for j in range(i+1, r):
            indx[j] = indx[j-1] + 1
        yield tuple(pool[i] for i in indx)

def pariton_maara(jalkeilla):
    poistettu1 = jalkeilla.pop(0)
    lopussa_lisattava = jalkeilla.pop(jalkeilla.index(min(jalkeilla,key = lambda x: x[1])))
    raakajaot = list(map(list,kombinaatiot(jalkeilla,(len(jalkeilla) + 1) // 2 - 1)))
    for alkio in raakajaot:
        alkio.append(poistettu1)
    tasaisuus = []
    for alkio in raakajaot:
        tasaisuus.append(([pelaaja[0] for pelaaja in alkio],sum([pelaaja[1] for pelaaja in alkio]), sum([pelaaja[1] for pelaaja in jalkeilla if pelaaja not in alkio])) )

    tasaisuus_jarkassa = sorted(tasaisuus,key = lambda x: abs(x[1]-x[2]))
    jaot = []
    for alkio in tasaisuus_jarkassa:
        vastapuoli = []
        for peluri in jalkeilla:
            if peluri[0] not in alkio[0]:
                vastapuoli.append(peluri[0])
        
        if alkio[1] > alkio[2]:
            vastapuoli.append(lopussa_lisattava[0])
            tasoero = alkio[1] - alkio[2] - lopussa_lisattava[1]
        else:
            alkio[0].append(lopussa_lisattava[0])
            tasoero = alkio[1] - alkio[2] + lopussa_lisattava[1]

        jaot.append((alkio[0],vastapuoli, tasoero))    

    return jaot

def tasaiset_jaot(pelaajat: list):
    jalkeilla = rosteri(pelaajat)
    if len(jalkeilla) % 2 != 0:
        return pariton_maara(jalkeilla)
    poistettu = jalkeilla.pop(0) 
    raakajaot = list(map(list,kombinaatiot(jalkeilla,len(pelaajat) // 2 - 1)))
    for alkio in raakajaot:
        alkio.append(poistettu)
    tasaisuus = []
    for alkio in raakajaot:
        tasaisuus.append(([pelaaja[0] for pelaaja in alkio],sum([pelaaja[1] for pelaaja in alkio]), sum([pelaaja[1] for pelaaja in jalkeilla if pelaaja not in alkio])) )

    tasaisuus_jarkassa = sorted(tasaisuus,key = lambda x: abs(x[1]-x[2]))
    jaot = []
    for alkio in tasaisuus_jarkassa:
        vastapuoli = []
        for peluri in jalkeilla:
            if peluri[0] not in alkio[0]:
                vastapuoli.append(peluri[0])
        tasoero = alkio[1] - alkio[2]
        jaot.append((alkio[0],vastapuoli, tasoero))
    return jaot



def arpakone(jalkeilla):
    if len(jalkeilla) % 2 == 0:
        lista = np.array([alkio[:2] for alkio in tasaiset_jaot(jalkeilla) if abs(alkio[2])<6])
        np.random.shuffle(lista)
        eka = ", ".join(lista[0][0])
        toka = ", ".join(lista[0][1])
        print(f"{eka} vs. {toka}")
    else:
        #kehitysvaiheessa:
        lista = tasaiset_jaot(jalkeilla)
        arvontapooli = list(range(len(lista)))
        lopullinen_pooli = []
        for alkio in arvontapooli:
            if alkio < 3:
                lopullinen_pooli.append(alkio)
                lopullinen_pooli.append(alkio)
                lopullinen_pooli.append(alkio)
                lopullinen_pooli.append(alkio)
            else:
                lopullinen_pooli.append(alkio)
        valitaan = lista[np.random.choice(lopullinen_pooli)]
        eka = ", ".join(valitaan[0])
        toka = ", ".join(valitaan[1])
        print(f"{eka} vs. {toka}")
    

def main(jalkeilla):
    print("Jaot tasaisuusjärjestyksessä:",end="\n\n")
    for alkio in tasaiset_jaot(jalkeilla):
        eka = ", ".join(alkio[0])
        toka = ", ".join(alkio[1])
        print(f"{eka} vs. {toka}; tasoero: {alkio[2]}")

eilen = ["Atro","Aku","Antti","Konsta","Timo","Tero", "Hannu", "Tuomo", "Harri", "Julli", "Paavo", "Antero"]
neljanelja = ["Kaapeli", "Konsta", "Antti","Tero","Pekka","Pasi","Teemu","Antero"]
#print(tasaiset_jaot(eilen))

main(eilen)
roster = [("Kaapeli",91) , ("Antti",94) , ("Konsta",93) , ("Pasi",92), ("Aku",91), ("Tero",88) , ("Teemu",93) , ("Hannu",92) , ("Antero",90) , ("Pekka",92), ("Paavo", 93), 
              ("Tuomo", 96), ("Atro", 95), ("Timo", 89), ("Julli", 91), ("Harri", 91)]
roster = sorted(roster, key=lambda x:x[1])
roster = list(zip(*roster))
print(roster)
plt.scatter(roster[0], roster[1])
plt.show()

