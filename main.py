from copy import deepcopy
from dataclasses import dataclass
import random
from numpy import *

# rozmery hracej plochy  0 - X-1
VELKOST_R = 5
VELKOST_S = 5
hracia_plocha = [[0 for i in range(VELKOST_R)] for j in range(VELKOST_S)]

# usporiadanie dat pre auta v poli stav
MENO = 0
DLZKA = 1
POLOHA_R = 2
POLOHA_S = 3
SMER = 4

POCET_AUT = 0


@dataclass
class Uzol:
    stav = []
    plocha = [[0 for i in range(VELKOST_R)] for j in range(VELKOST_S)]
    potomok_l = None
    potomok_p = None
    rodic = None
    hlbka_uzla: int
    pohyb_f = None  # farba auta, ktore sa oproti rodicovi pohlo
    pohyb_s: int  # smer - 1 HORE, 2 VPRAVO, 3 DOLE, 4 VLAVO
    pohyb_d: int  # pocet policok o ktore sa auto posunulo


def vypis_plochu():
    for riadok in range(VELKOST_R):
        for stlpec in range(VELKOST_S):
            print(hracia_plocha[riadok][stlpec], end=' ')
        print('')


def nacitaj_vstup():
    global POCET_AUT
    zaciatocny_stav = []

    with open('stav.txt', 'r') as file1:
        zaciatocny_stav = [line.split() for line in file1]
        file1.close()

    POCET_AUT = len(zaciatocny_stav)
    global hracia_plocha

    for auto in zaciatocny_stav:
        # ak pri zapisovani auta na poziciu tam uz nie je 0, na vstupe boli zadane auta nespravne
        auto[DLZKA] = int(auto[DLZKA])
        auto[POLOHA_R] = int(auto[POLOHA_R])
        auto[POLOHA_S] = int(auto[POLOHA_S])

        if auto[SMER] == 'h':
            for stlpec in range(int(auto[DLZKA])):
                if hracia_plocha[int(auto[POLOHA_R])][int(auto[POLOHA_S]) + stlpec] != 0:
                    print('kolizia aut')
                    exit()
                hracia_plocha[int(auto[POLOHA_R])][int(auto[POLOHA_S]) + stlpec] = auto[MENO][0]

        elif auto[SMER] == 'v':
            for riadok in range(int(auto[DLZKA])):
                if hracia_plocha[int(auto[POLOHA_R]) + riadok][int(auto[POLOHA_S])] != 0:
                    print('kolizia aut')
                    exit()
                hracia_plocha[int(auto[POLOHA_R]) + riadok][int(auto[POLOHA_S])] = auto[MENO][0]

        print()

    vypis_plochu()

    zaciatocny_uzol: Uzol = Uzol(0, 0, 0)
    zaciatocny_uzol.stav = zaciatocny_stav
    zaciatocny_uzol.plocha = deepcopy(hracia_plocha)

    return zaciatocny_uzol


def posun_auto(auto, smer: int, pocet_posunuti: int):
    # upravi hraciu plochu a poziciu auta
    global hracia_plocha

    print(f"FUNKCIA POSUN, smer {smer}, pocet {pocet_posunuti}, {auto}")
    #hore
    if smer == 1:
        for posunutie in range(pocet_posunuti):
            print('posuvam hore', auto[POLOHA_R], auto[POLOHA_S], posunutie )
            hracia_plocha[auto[POLOHA_R]-1][auto[POLOHA_S]] = auto[MENO][0]
            hracia_plocha[auto[POLOHA_R]+auto[DLZKA]-1][auto[POLOHA_S]] = 0
            auto[POLOHA_R] -= 1
            print(auto[POLOHA_R])
            vypis_plochu()
        return

    # vpravo
    if smer == 2:
        for posunutie in range(pocet_posunuti):
            print('posuvam doprava', auto[POLOHA_S] + auto[DLZKA])
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S] + auto[DLZKA]] = auto[MENO][0]
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S]] = 0
            auto[POLOHA_S] += 1
            print(auto[POLOHA_S])
        return
    # dole
    if smer == 3:
        for posunutie in range(pocet_posunuti):
            print('posuvam dole', int(auto[POLOHA_R])+int(auto[DLZKA]))
            hracia_plocha[int(auto[POLOHA_R])+int(auto[DLZKA])][int(auto[POLOHA_S])] = auto[MENO][0]
            hracia_plocha[int(auto[POLOHA_R])][int(auto[POLOHA_S])] = 0
            auto[POLOHA_R] += 1
            print(auto[POLOHA_R])
        return
    # vlavo
    if smer == 4:
        for posunutie in range(pocet_posunuti):
            print('posuvam dolava', auto[POLOHA_S] + auto[DLZKA])
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S]-1] = auto[MENO][0]
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S]-1 + auto[DLZKA]] = 0
            auto[POLOHA_S] -= 1
            print(auto[POLOHA_S])
        return


def posun_auto1(uzol: Uzol):
    # upravi hraciu plochu a poziciu auta
    global hracia_plocha

    smer = uzol.pohyb_s
    pocet_posunuti = uzol.pohyb_d

    for auta in uzol.stav:
        print(uzol.pohyb_f, auta)
        if auta[MENO] == uzol.pohyb_f:
            auto = auta
            break
        return

    print(f"FUNKCIA POSUN, smer {smer}, pocet {pocet_posunuti}, {auto}")
    # hore
    if smer == 1:
        for posunutie in range(pocet_posunuti):
            print('posuvam hore', auto[POLOHA_R], auto[POLOHA_S], posunutie)
            hracia_plocha[auto[POLOHA_R] - 1][auto[POLOHA_S]] = auto[MENO][0]
            hracia_plocha[auto[POLOHA_R] + auto[DLZKA] - 1][auto[POLOHA_S]] = 0
            auto[POLOHA_R] -= 1
            print(auto[POLOHA_R])
            vypis_plochu()
        return

    # vpravo
    if smer == 2:
        for posunutie in range(pocet_posunuti):
            print('posuvam doprava', auto[POLOHA_S] + auto[DLZKA])
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S] + auto[DLZKA]] = auto[MENO][0]
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S]] = 0
            auto[POLOHA_S] += 1
            print(auto[POLOHA_S])
        return
    # dole
    if smer == 3:
        for posunutie in range(pocet_posunuti):
            print('posuvam dole', int(auto[POLOHA_R]) + int(auto[DLZKA]))
            hracia_plocha[int(auto[POLOHA_R]) + int(auto[DLZKA])][int(auto[POLOHA_S])] = auto[MENO][0]
            hracia_plocha[int(auto[POLOHA_R])][int(auto[POLOHA_S])] = 0
            auto[POLOHA_R] += 1
            print(auto[POLOHA_R])
        return
    # vlavo
    if smer == 4:
        for posunutie in range(pocet_posunuti):
            print('posuvam dolava', auto[POLOHA_S] + auto[DLZKA])
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S] - 1] = auto[MENO][0]
            hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S] - 1 + auto[DLZKA]] = 0
            auto[POLOHA_S] -= 1
            print(auto[POLOHA_S])
        return


def generuj_stav(uzol: Uzol):
    # prejde vsetky auta v stave a zistuje ci sa moze pohnut
    nahodne_poradie = uzol.stav

    # usporiada nacitane auta do nahodneho zoznamu

    random.shuffle(nahodne_poradie)
    print("NAHODNE: ", nahodne_poradie)

    for auto in nahodne_poradie:
        print(f"zistujem moznost {auto[MENO]}")
        if auto[SMER] == 'h':  # posuva sa doprava a dolava
            # doprava    # pole hned vedla auta je volne, zisti o ko2ko najviac sa vie posunut
            for pole in range(VELKOST_S-1 - (int(auto[POLOHA_S])+int(auto[DLZKA])-1)):
                if auto[POLOHA_S] + pole < VELKOST_S and hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S] + pole] == 0:
                    uzol.pohyb_d += 1
                    auto[POLOHA_S] += 1
            if uzol.pohyb_d != 0:
                uzol.pohyb_f = auto[MENO]
                uzol.pohyb_s = 2
                break

            # dolava
            for pole in range(auto[POLOHA_S] + 1):
                if auto[POLOHA_S] - pole >= 0 and hracia_plocha[auto[POLOHA_R]][auto[POLOHA_S] - pole] == 0:
                    uzol.pohyb_d += 1
                    auto[POLOHA_S] -= 1
            if uzol.pohyb_d != 0:
                uzol.pohyb_f = auto[MENO]
                uzol.pohyb_s = 4
                break

        elif auto[SMER] == 'v':  # posuva sa hore a dole
            # dole
            for pole in range(VELKOST_R-1 - (auto[POLOHA_R]+auto[DLZKA]-1)):
                if auto[POLOHA_R] + auto[DLZKA] + pole < VELKOST_R and \
                        hracia_plocha[auto[POLOHA_R] + auto[DLZKA] + pole][auto[POLOHA_S]] == 0:
                    uzol.pohyb_d += 1
                    auto[POLOHA_R] += 1
            if uzol.pohyb_d != 0:
                uzol.pohyb_f = auto[MENO]
                uzol.pohyb_s = 3
                break

            # hore
            for pole in range(auto[POLOHA_R] + 1):
                if auto[POLOHA_R] - pole >= 0 and hracia_plocha[auto[POLOHA_R] - pole][auto[POLOHA_S]] == 0:
                    uzol.pohyb_d += 1
                    auto[POLOHA_R] -= 1
            if uzol.pohyb_d != 0:
                uzol.pohyb_f = auto[MENO]
                uzol.pohyb_s = 1
                break

    #potomok.stav = novy_stav
    #posun_auto(auto, potomok.pohyb_s, potomok.pohyb_d)
    print("potomok: ", uzol, uzol.stav, "rodic: ", uzol.rodic, uzol.rodic.stav)

    vypis_plochu()

    #return uzol


def novy_uzol(rodic: Uzol):
    potomok = Uzol(rodic.hlbka_uzla+1, 0, 0)
    potomok.rodic = rodic
    potomok.stav = deepcopy(rodic.stav)
    return potomok


def hladaj_ciel(aktualny_uzol: Uzol, max_hlbka: int):
    # prejde pole ulozenych aut, porovnava polohy cerveneho s cielovou
    for auto in aktualny_uzol.stav:
        if auto[MENO] == 'cervene' and (int(auto[POLOHA_S]) + int(auto[DLZKA])-1) == VELKOST_S-1:
            print("cervene je v cieli")
            return True

    # je v max hlbke
    if aktualny_uzol.hlbka_uzla == max_hlbka:
        print(f"sme v max hlbke {max_hlbka}")
        return False

    print(f"som v hlbke {aktualny_uzol.hlbka_uzla}, {aktualny_uzol.stav}")
    #posun_auto1(aktualny_uzol)

    #if aktualny_uzol.potomok_l is None:
        #print(f"lavy je None, generujem")
        #aktualny_uzol.potomok_l = generuj_stav(aktualny_uzol)
    aktualny_uzol.potomok_l = novy_uzol(aktualny_uzol)
    generuj_stav(aktualny_uzol.potomok_l)

    #if aktualny_uzol.potomok_p is None:
        #print(f"pravy je None, generujem")
        #aktualny_uzol.potomok_p = generuj_stav(aktualny_uzol)
    aktualny_uzol.potomok_p = novy_uzol(aktualny_uzol)
    generuj_stav(aktualny_uzol.potomok_p)

    print("IDEM KONTROLOVAT LAVE")
    return hladaj_ciel(aktualny_uzol.potomok_l, max_hlbka)
    print("IDEM KONTROLOVAT PRAVE")
    return hladaj_ciel(aktualny_uzol.potomok_p, max_hlbka)
    return False


if __name__ == '__main__':
    koren = nacitaj_vstup()

    k: int = 20
    aktualny_stav = koren

   # while True:
        # skontorlovat ci nejde o finalny stav
        # skontrolovat maximalnu hlbku --- ANO --- navysujeme K a ideme od zaciatku
        #                              \---NIE --- generujeme obe deti a kontrolujeme tie

    if hladaj_ciel(koren, k):
            # treba vypisat vsetky kroky od korena po vysledok
        print("-----------------HOTOVO---------------")

    k += 1


