import sys
from dataclasses import dataclass
from numpy import *
import const
import time

#hracia_plocha = [[0 for i in range(const.VELKOST_R)] for j in range(const.VELKOST_S)]

POCET_AUT = 0
pocet_uzlov = 0
cielovy_stav = None
#nespracovane = []

@dataclass
class Uzol:
    stav = []
    plocha = [[0 for i in range(const.VELKOST_R)] for j in range(const.VELKOST_S)]
    potomkovia = []
    rodic = None
    hlbka_uzla: int
    pohyb_f: str  # farba auta, ktore sa oproti rodicovi pohlo
    pohyb_s: int  # smer - 1 HORE, 2 VPRAVO, 3 DOLE, 4 VLAVO
    pohyb_d: int  # pocet policok o ktore sa auto posunulo


def vypis_plochu(plocha):
    for riadok in range(const.VELKOST_R):
        for stlpec in range(const.VELKOST_S):
            print(plocha[riadok][stlpec], end=' ')
        print('')


def nacitaj_vstup():
    global POCET_AUT
    zaciatocny_uzol: Uzol = Uzol(0, None, 0, 0)

    with open('stav1.txt', 'r') as file1:
        zaciatocny_uzol.stav = [line.split() for line in file1]
        file1.close()

    POCET_AUT = len(zaciatocny_uzol.stav)

    for auto in zaciatocny_uzol.stav:
        auto[const.DLZKA] = int(auto[const.DLZKA])
        auto[const.POLOHA_R] = int(auto[const.POLOHA_R])
        auto[const.POLOHA_S] = int(auto[const.POLOHA_S])

        # ak pri zapisovani auta na poziciu tam uz nie je 0, na vstupe boli zadane auta nespravne
        if auto[const.SMER] == 'h':
            for stlpec in range(auto[const.DLZKA]):
                if zaciatocny_uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + stlpec] != 0:
                    print('nespravny vstup - auta sa prekryvaju alebo su mimo plochy')
                    exit()
                zaciatocny_uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + stlpec] = auto[const.MENO][0]

        elif auto[const.SMER] == 'v':
            for riadok in range(auto[const.DLZKA]):
                if zaciatocny_uzol.plocha[auto[const.POLOHA_R] + riadok][auto[const.POLOHA_S]] != 0:
                    print('nespravny vstup - auta sa prekryvaju alebo su mimo plochy')
                    exit()
                zaciatocny_uzol.plocha[auto[const.POLOHA_R] + riadok][auto[const.POLOHA_S]] = auto[const.MENO][0]

    vypis_plochu(zaciatocny_uzol.plocha)

    return zaciatocny_uzol


def vykonaj_posun_vlavo(auto_rodica, uzol: Uzol):
    # do funkcie prislo auto zo stavu rodica, je ho potrebne vymanit za auto aktualneho uzla
    for nove_auta in uzol.stav:
        if nove_auta == auto_rodica:
            auto = nove_auta

    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] - 1] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] - 1 + auto[const.DLZKA]] = 0
        auto[const.POLOHA_S] -= 1


def over_posun_vlavo(auto, uzol: Uzol):
    for pole in range(auto[const.POLOHA_S]):
        if auto[const.POLOHA_S] - (pole+1) >= 0 and \
                uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]-(pole+1)] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 4
            potomok.pohyb_d = pole + 1
            vykonaj_posun_vlavo(auto, potomok)
            uzol.potomkovia.append(potomok)
           # nespracovane.append(potomok)
            #print('pridavam', potomok, potomok.stav)
        else:
            return


def vykonaj_posun_vpravo(auto_rodica, uzol: Uzol):
    # do funkcie prislo auto zo stavu rodica, je ho potrebne vymanit za auto aktualneho uzla
    for nove_auta in uzol.stav:
        if nove_auta == auto_rodica:
            auto = nove_auta

    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + auto[const.DLZKA]] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]] = 0
        auto[const.POLOHA_S] += 1


def over_posun_vpravo(auto, uzol: Uzol):
    for pole in range(const.VELKOST_S-1 - (auto[const.POLOHA_S] + auto[const.DLZKA] - 1)):
        if auto[const.POLOHA_S] + pole + auto[const.DLZKA] < const.VELKOST_S and \
                uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + pole + auto[const.DLZKA]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 2
            potomok.pohyb_d = pole+1
            vykonaj_posun_vpravo(auto, potomok)
            uzol.potomkovia.append(potomok)
            #.append(potomok)
            #print('pridavam', potomok, potomok.stav)
        else:
            return


def vykonaj_posun_hore(auto_rodica, uzol: Uzol):
    # do funkcie prislo auto zo stavu rodica, je ho potrebne vymanit za auto aktualneho uzla
    for nove_auta in uzol.stav:
        if nove_auta == auto_rodica:
            auto = nove_auta

    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R] - 1][auto[const.POLOHA_S]] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA] - 1][auto[const.POLOHA_S]] = 0
        auto[const.POLOHA_R] -= 1


def over_posun_hore(auto, uzol: Uzol):
    for pole in range(auto[const.POLOHA_R]):
        if auto[const.POLOHA_R] - (pole+1) >= 0 and \
                uzol.plocha[auto[const.POLOHA_R] - (pole+1)][auto[const.POLOHA_S]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 1
            potomok.pohyb_d = pole + 1
            vykonaj_posun_hore(auto, potomok)
            uzol.potomkovia.append(potomok)
           # nespracovane.append(potomok)
            #print('pridavam', potomok, potomok.stav)
        else:
            return


def vykonaj_posun_dole(auto_rodica, uzol: Uzol):
    # do funkcie prislo auto zo stavu rodica, je ho potrebne vymanit za auto aktualneho uzla
    for nove_auta in uzol.stav:
        if nove_auta == auto_rodica:
            auto = nove_auta

    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA]][auto[const.POLOHA_S]] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]] = 0
        auto[const.POLOHA_R] += 1


def over_posun_dole(auto, uzol: Uzol):
    for pole in range(const.VELKOST_R-1 - (auto[const.POLOHA_R] + auto[const.DLZKA] - 1)):
        if auto[const.POLOHA_R] + auto[const.DLZKA] + pole < const.VELKOST_R and \
                uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA] + pole][auto[const.POLOHA_S]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 3
            potomok.pohyb_d = pole + 1
            vykonaj_posun_dole(auto, potomok)
            uzol.potomkovia.append(potomok)
            #nespracovane.append(potomok)
            #print('pridavam', potomok, potomok.stav)
        else:
            return


def generuj_stavy(uzol: Uzol):
    # prejdem vsetky auta a ulozim vsetky ich mozne pohyby
    for auto in uzol.stav:

        if auto[const.SMER] == 'h':  # posuva sa doprava a dolava
            over_posun_vpravo(auto, uzol)
            over_posun_vlavo(auto, uzol)

        elif auto[const.SMER] == 'v':  # posuva sa hore a dole
            over_posun_dole(auto, uzol)
            over_posun_hore(auto, uzol)

    # print("POTOMKOVIA ", len(uzol.potomkovia), uzol.potomkovia)


def novy_uzol(rodic: Uzol):
    potomok = Uzol(rodic.hlbka_uzla+1, None, 0, 0)
    potomok.rodic = rodic
    potomok.stav = [row[:] for row in rodic.stav]
    potomok.plocha = [row[:] for row in rodic.plocha]
    potomok.potomkovia = []
    return potomok


def hladaj_ciel(aktualny_uzol: Uzol, max_hlbka: int):
    global pocet_uzlov, cielovy_stav
    pocet_uzlov += 1

    #print('mazem', aktualny_uzol.stav, aktualny_uzol)
    #nespracovane.remove(aktualny_uzol)

    # prejde pole ulozenych aut, porovnava polohy cerveneho s cielovou
    for auto in aktualny_uzol.stav:
        if auto[const.MENO] == 'cervene' and (auto[const.POLOHA_S] + auto[const.DLZKA] - 1) == const.VELKOST_S-1:
            print("cervene je v cieli")
            cielovy_stav = aktualny_uzol
            return

    # je v max hlbke
    if aktualny_uzol.hlbka_uzla == max_hlbka:
        #print(f"sme v max hlbke {max_hlbka} {aktualny_uzol.potomkovia}")
        return

    # print(f"som v hlbke {aktualny_uzol.hlbka_uzla}")
    #vypis_plochu(aktualny_uzol.plocha)

    generuj_stavy(aktualny_uzol)

    # ulozi vsetkych moznych potomkov do pola, treba toto pole prejst a kontrolovat
    for potomok in aktualny_uzol.potomkovia:
        #for auto in potomok.stav:
        #    if auto[const.MENO] == potomok.pohyb_f:
        #        posun_auto1(auto, potomok)
        #        break

        rovnaky = 0

        if aktualny_uzol.rodic is not None and potomok.stav == aktualny_uzol.rodic.stav:
            #print('rovnaky ', potomok.stav, len(nespracovane))
            #nespracovane.remove(potomok)
            rovnaky = 1
            break

        kontrolovany = aktualny_uzol
        while kontrolovany.rodic is not None:
            if potomok.stav == kontrolovany.rodic.stav:
                #nespracovane.remove(potomok)
                #print('rovnaky ', potomok.stav, len(nespracovane))
                rovnaky = 1
                break
            kontrolovany = kontrolovany.rodic

        #if len(nespracovane) == 1:
        #    print('NEMA RIESENIE')
        #    exit()

        if rovnaky == 0:
            #print('idem kontrolovat ', potomok)
            hladaj_ciel(potomok, max_hlbka)

            if cielovy_stav is not None:
                return

        #for vymazat in potomok.potomkovia:
         #   vymazat.potomkovia.clear()
         #   vymazat.plocha.clear()
         #   vymazat.stav.clear()

        potomok.plocha.clear()
        potomok.stav.clear()
        potomok.potomkovia.clear()
        aktualny_uzol.potomkovia.remove(potomok)

    aktualny_uzol.potomkovia.clear()


def vypis_cestu(uzol: Uzol):
    # v koreni nebol pohyb, nepotrebujeme ho vypisovat
    if uzol.rodic.rodic is not None:
        vypis_cestu(uzol.rodic)
    print(f"{const.pohyb[uzol.pohyb_s-1]} {uzol.pohyb_f} {uzol.pohyb_d}")
    #vypis_plochu(uzol.plocha)


if __name__ == '__main__':
    k: int = 1
    start_time = time.time()
    zaciatocny_stav = nacitaj_vstup()

    while True:
        # skontorlovat ci nejde o finalny stav
        # skontrolovat maximalnu hlbku --- ANO --- navysujeme K a ideme od zaciatku
        #                              \---NIE --- generujeme obe deti a kontrolujeme tie
        print('????????Prehladavam s k ', k)
        #nespracovane.clear()
        #nespracovane.append(zaciatocny_stav)
        zaciatocny_stav.potomkovia.clear()
        pocet_uzlov = 0
        hladaj_ciel(zaciatocny_stav, k)
        print("CIEL", cielovy_stav)
            # treba vypisat vsetky kroky od korena po vysledok
        if cielovy_stav is not None :
            print("-----------------HOTOVO---------------")
            print("UZLY: ", k, pocet_uzlov)
            break
        print(k, pocet_uzlov)

        k += 1

    print("--- %s seconds ---" % (time.time() - start_time))
    vypis_cestu(cielovy_stav)

    exit()
