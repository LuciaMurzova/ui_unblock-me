from dataclasses import dataclass
from numpy import *
import const
import time

#hracia_plocha = [[0 for i in range(const.VELKOST_R)] for j in range(const.VELKOST_S)]

POCET_AUT = 0
pocet_uzlov = 0
cielovy_stav = None


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


def posun_auto1(auto, uzol: Uzol):
    # upravi hraciu plochu a poziciu auta
    smer = uzol.pohyb_s
    pocet_posunuti = uzol.pohyb_d

    # print(f"FUNKCIA POSUN 1, smer {smer}, pocet {pocet_posunuti}, {auto}")
    # hore
    if smer == 1:
        for posunutie in range(pocet_posunuti):
            #print('posuvam hore', auto[const.POLOHA_R], auto[const.POLOHA_S], posunutie, pocet_posunuti)
            uzol.plocha[auto[const.POLOHA_R] - 1][auto[const.POLOHA_S]] = auto[const.MENO][0]
            uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA] - 1][auto[const.POLOHA_S]] = 0
            auto[const.POLOHA_R] -= 1
            #print(auto[const.POLOHA_R])
            #vypis_plochu(uzol.plocha)
        return

    # vpravo
    if smer == 2:
        for posunutie in range(pocet_posunuti):
            #print('posuvam doprava', auto[const.POLOHA_S] + auto[const.DLZKA], pocet_posunuti)
            uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + auto[const.DLZKA]] = auto[const.MENO][0]
            uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]] = 0
            auto[const.POLOHA_S] += 1
            #print(auto[const.POLOHA_S])
            #vypis_plochu(uzol.plocha)
        return
    # dole
    if smer == 3:
        for posunutie in range(pocet_posunuti):
            #print('posuvam dole', auto[const.POLOHA_R] + auto[const.DLZKA], pocet_posunuti)
            uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA]][auto[const.POLOHA_S]] = auto[const.MENO][0]
            uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]] = 0
            auto[const.POLOHA_R] += 1
            #print(auto[const.POLOHA_R])
            #vypis_plochu(uzol.plocha)
        return
    # vlavo
    if smer == 4:
        for posunutie in range(pocet_posunuti):
            #print('posuvam dolava', uzol.pohyb_d, pocet_posunuti)
            uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] - 1] = auto[const.MENO][0]
            uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] - 1 + auto[const.DLZKA]] = 0
            auto[const.POLOHA_S] -= 1
            #print(auto[const.POLOHA_S])
            #vypis_plochu(uzol.plocha)
        return


def over_posun_vlavo(auto, uzol: Uzol):
    for pole in range(auto[const.POLOHA_S]):
        #print(f"zistujem posun vlavo 1 - {auto[const.POLOHA_S] + pole + auto[const.DLZKA]}")
        if auto[const.POLOHA_S] - (pole+1) >= 0 and uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]-(pole+1)] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 4
            potomok.pohyb_d = pole + 1
            #print(f'OVER - POSUVAM {potomok.pohyb_d}')
            # vykonaj_posun_vpravo(auto, potomok)
            uzol.potomkovia.append(potomok)
            #print(uzol.potomkovia)
        else:
            return


def over_posun_vpravo(auto, uzol: Uzol):
    for pole in range(const.VELKOST_S-1 - (auto[const.POLOHA_S] + auto[const.DLZKA] - 1)):
        #print(f"zistujem posun vpravo {auto[const.POLOHA_S]} {pole} {uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + pole + auto[const.DLZKA]]}")
        if auto[const.POLOHA_S] + pole + auto[const.DLZKA] < const.VELKOST_S and \
                uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + pole + auto[const.DLZKA]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 2
            potomok.pohyb_d = pole+1
            #print(f'OVER - POSUVAM {potomok.pohyb_d}')
            # vykonaj_posun_vpravo(auto, potomok)
            #if (potomok.rodic is not None and potomok.stav == potomok.rodic) or (potomok.rodic is not None and )
            uzol.potomkovia.append(potomok)
            #print(uzol.potomkovia)
        else:
            return


def over_posun_hore(auto, uzol: Uzol):
    for pole in range(auto[const.POLOHA_R]):
        #print(f"zistujem posun hore 1 - {auto[const.POLOHA_S] + pole + auto[const.DLZKA]}")
        if auto[const.POLOHA_R] - (pole + 1) >= 0 and \
                uzol.plocha[auto[const.POLOHA_R] - (pole + 1)][auto[const.POLOHA_S]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 1
            potomok.pohyb_d = pole + 1
            #print(f'OVER - POSUVAM {potomok.pohyb_d}')
            # vykonaj_posun_vpravo(auto, potomok)
            uzol.potomkovia.append(potomok)
            #print(uzol.potomkovia)
        else:
            return


def over_posun_dole(auto, uzol: Uzol):
    for pole in range(const.VELKOST_R-1 - (auto[const.POLOHA_R] + auto[const.DLZKA] - 1)):
        #print(f"zistujem posun dole 1 - {auto[const.POLOHA_S] + pole + auto[const.DLZKA]}")
        if auto[const.POLOHA_R] + auto[const.DLZKA] + pole < const.VELKOST_R and \
                uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA] + pole][auto[const.POLOHA_S]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 3
            potomok.pohyb_d = pole + 1
            #print(f'OVER - POSUVAM {potomok.pohyb_d}')
            # vykonaj_posun_vpravo(auto, potomok)
            uzol.potomkovia.append(potomok)
            #print(uzol.potomkovia)
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
        for auto in potomok.stav:
            if auto[const.MENO] == potomok.pohyb_f:
                posun_auto1(auto, potomok)
                break

        #print('idem kontrolovat ', potomok)

        kontrolovany = aktualny_uzol
        rovnaky = 0
        #print("MIMO", potomok.stav, kontrolovany.stav)
        while kontrolovany.rodic is not None:
            if potomok.stav == kontrolovany.rodic.stav:
                rovnaky = 1
                break

            kontrolovany = kontrolovany.rodic

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
    if uzol.rodic is not None:
        vypis_cestu(uzol.rodic)
    print(f"POHYB {uzol.pohyb_f} {uzol.pohyb_s} {uzol.pohyb_d}")
    vypis_plochu(uzol.plocha)


if __name__ == '__main__':
    k: int = 1
    start_time = time.time()
    zaciatocny_stav = nacitaj_vstup()
    while True:
        # skontorlovat ci nejde o finalny stav
        # skontrolovat maximalnu hlbku --- ANO --- navysujeme K a ideme od zaciatku
        #                              \---NIE --- generujeme obe deti a kontrolujeme tie
        print('????????Prehladavam s k ', k)
        zaciatocny_stav.potomkovia.clear()

        hladaj_ciel(zaciatocny_stav, k)
        print("CIEL", cielovy_stav)
            # treba vypisat vsetky kroky od korena po vysledok
        if cielovy_stav is not None :
            print("-----------------HOTOVO---------------")
            print("UZLY: ", pocet_uzlov, k)
            break

        k += 1

    print("UZLY: ", pocet_uzlov, k)
    print("--- %s seconds ---" % (time.time() - start_time))
    vypis_cestu(cielovy_stav)
    #print("idem vypisovat strom")
    #vypis_plochu(koren.plocha)
    #vypis_strom(koren)
    #print(koren)


