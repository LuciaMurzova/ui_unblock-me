from dataclasses import dataclass
from numpy import *
import const
import time

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

    with open('stav.txt', 'r') as file1:
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
    # na novu poziciu nastavi zaciatocne pismeno auta a na staru 0, zmeni polohu auta v stave
    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] - 1] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] - 1 + auto[const.DLZKA]] = 0
        auto[const.POLOHA_S] -= 1


def over_posun_vlavo(auto, uzol: Uzol):
    # overuje vsetky mozne posunutia po koniec plochy, pokial nenarazi na auto
    for pole in range(auto[const.POLOHA_S]):
        # pozicia sa musi nachadzat v hracej ploche a zaroven byt vola, pri prvej obsadenej konci - nemoze ist cez auto
        if auto[const.POLOHA_S] - (pole + 1) >= 0 and \
                uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] - (pole + 1)] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 4
            potomok.pohyb_d = pole + 1
            vykonaj_posun_vlavo(auto, potomok)
            uzol.potomkovia.append(potomok)
        else:
            return


def vykonaj_posun_vpravo(auto_rodica, uzol: Uzol):
    # do funkcie prislo auto zo stavu rodica, je ho potrebne vymanit za auto aktualneho uzla
    for nove_auta in uzol.stav:
        if nove_auta == auto_rodica:
            auto = nove_auta
    # na novu poziciu nastavi zaciatocne pismeno auta a na staru 0, zmeni polohu auta v stave
    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + auto[const.DLZKA]] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]] = 0
        auto[const.POLOHA_S] += 1


def over_posun_vpravo(auto, uzol: Uzol):
    # overuje vsetky mozne posunutia po koniec plochy, pokial nenarazi na auto
    for pole in range(const.VELKOST_S - 1 - (auto[const.POLOHA_S] + auto[const.DLZKA] - 1)):
        # pozicia sa musi nachadzat v hracej ploche a zaroven byt vola, pri prvej obsadenej konci - nemoze ist cez auto
        if auto[const.POLOHA_S] + pole + auto[const.DLZKA] < const.VELKOST_S and \
                uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S] + pole + auto[const.DLZKA]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 2
            potomok.pohyb_d = pole + 1
            vykonaj_posun_vpravo(auto, potomok)
            uzol.potomkovia.append(potomok)
        else:
            return


def vykonaj_posun_hore(auto_rodica, uzol: Uzol):
    # do funkcie prislo auto zo stavu rodica, je ho potrebne vymanit za auto aktualneho uzla
    for nove_auta in uzol.stav:
        if nove_auta == auto_rodica:
            auto = nove_auta
    # na novu poziciu nastavi zaciatocne pismeno auta a na staru 0, zmeni polohu auta v stave
    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R] - 1][auto[const.POLOHA_S]] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA] - 1][auto[const.POLOHA_S]] = 0
        auto[const.POLOHA_R] -= 1


def over_posun_hore(auto, uzol: Uzol):
    # overuje vsetky mozne posunutia po koniec plochy, pokial nenarazi na auto
    for pole in range(auto[const.POLOHA_R]):
        # pozicia sa musi nachadzat v hracej ploche a zaroven byt vola, pri prvej obsadenej konci - nemoze ist cez auto
        if auto[const.POLOHA_R] - (pole + 1) >= 0 and \
                uzol.plocha[auto[const.POLOHA_R] - (pole + 1)][auto[const.POLOHA_S]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 1
            potomok.pohyb_d = pole + 1
            vykonaj_posun_hore(auto, potomok)
            uzol.potomkovia.append(potomok)
        else:
            return


def vykonaj_posun_dole(auto_rodica, uzol: Uzol):
    # do funkcie prislo auto zo stavu rodica, je ho potrebne vymanit za auto aktualneho uzla
    for nove_auta in uzol.stav:
        if nove_auta == auto_rodica:
            auto = nove_auta
    # na novu poziciu nastavi zaciatocne pismeno auta a na staru 0, zmeni polohu auta v stave
    for posunutie in range(uzol.pohyb_d):
        uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA]][auto[const.POLOHA_S]] = auto[const.MENO][0]
        uzol.plocha[auto[const.POLOHA_R]][auto[const.POLOHA_S]] = 0
        auto[const.POLOHA_R] += 1


def over_posun_dole(auto, uzol: Uzol):
    # overuje vsetky mozne posunutia po koniec plochy, pokial nenarazi na auto
    for pole in range(const.VELKOST_R - 1 - (auto[const.POLOHA_R] + auto[const.DLZKA] - 1)):
        # pozicia sa musi nachadzat v hracej ploche a zaroven byt vola, pri prvej obsadenej konci - nemoze ist cez auto
        if auto[const.POLOHA_R] + auto[const.DLZKA] + pole < const.VELKOST_R and \
                uzol.plocha[auto[const.POLOHA_R] + auto[const.DLZKA] + pole][auto[const.POLOHA_S]] == 0:
            potomok = novy_uzol(uzol)
            potomok.pohyb_f = auto[const.MENO]
            potomok.pohyb_s = 3
            potomok.pohyb_d = pole + 1
            vykonaj_posun_dole(auto, potomok)
            uzol.potomkovia.append(potomok)
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


def novy_uzol(rodic: Uzol):
    potomok = Uzol(rodic.hlbka_uzla + 1, None, 0, 0)
    potomok.rodic = rodic
    # skopiruje stav a plochu rodica, potom ich vo vykonaj_posun upravi
    potomok.stav = [row[:] for row in rodic.stav]
    potomok.plocha = [row[:] for row in rodic.plocha]
    potomok.potomkovia = []
    return potomok


def hladaj_ciel(aktualny_uzol: Uzol, max_hlbka: int):
    global pocet_uzlov, cielovy_stav
    pocet_uzlov += 1

    # prejde pole ulozenych aut, porovnava polohy cerveneho s cielovou
    for auto in aktualny_uzol.stav:
        if auto[const.MENO] == 'cervene' and (auto[const.POLOHA_S] + auto[const.DLZKA] - 1) == const.VELKOST_S - 1:
            print("cervene je v cieli")
            cielovy_stav = aktualny_uzol
            return

    # sme v max hlbke
    if aktualny_uzol.hlbka_uzla == max_hlbka:
        return

    # vygeneruje vsetkych moznych potomkov daneho uzla
    generuj_stavy(aktualny_uzol)

    # prechadza ulozenych potomkov,
    for potomok in aktualny_uzol.potomkovia:
        rovnaky = 0

        if aktualny_uzol.rodic is not None and potomok.stav == aktualny_uzol.rodic.stav:
            aktualny_uzol.potomkovia.remove(potomok)
            continue
        else:
            kontrolovany = aktualny_uzol
            while kontrolovany.rodic is not None:
                if potomok.stav == kontrolovany.stav:
                    rovnaky = 1
                    break
                kontrolovany = kontrolovany.rodic

        if rovnaky == 0:
            # rekurzivne kontroluje potomkov
            hladaj_ciel(potomok, max_hlbka)

            if cielovy_stav is not None:
                return

        # odstranenie prejdeneho potomka
        aktualny_uzol.potomkovia.remove(potomok)

    aktualny_uzol.potomkovia.clear()


def vypis_cestu(uzol: Uzol):
    # v koreni nebol pohyb, nepotrebujeme ho vypisovat
    if uzol.rodic.rodic is not None:
        vypis_cestu(uzol.rodic)
    print(f"{const.pohyb[uzol.pohyb_s - 1]} {uzol.pohyb_f} {uzol.pohyb_d}")
    vypis_plochu(uzol.plocha)


if __name__ == '__main__':

    start_time = time.time()
    zaciatocny_stav = nacitaj_vstup()
    k: int = 1
    while k < 50:
        print('-----Prehladavam s k ------', k)

        pocet_uzlov = 0
        hladaj_ciel(zaciatocny_stav, k)

        # treba vypisat vsetky kroky od korena po vysledok
        if cielovy_stav is not None:
            print("-----------------HOTOVO---------------")
            print("UZLY: ", k, pocet_uzlov)
            vypis_cestu(cielovy_stav)
            break
        print(k, pocet_uzlov)

        k += 1

    print("--- %s seconds ---" % (time.time() - start_time))
    if cielovy_stav is None:
        print('nepodarilo sa najst riesenie')

    exit()
