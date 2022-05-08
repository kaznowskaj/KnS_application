# coloursDict - global? n - tez global? seq - global???
# n - jakie dlugosci? (1 bez sensu troche, 2 chyba tez ...)
# 1 <= r <= 26
# dlugosci ciagow - pozwolic na 1? - max n

import random
from string import ascii_lowercase

def winning_computer_condition():
    # sprawdza czy wygrana komputera
    global coloursDict, seq

    for letter in coloursDict.keys():
        if coloursDict[letter] == 1:
            if letter in seq:
                return True

    for letter_idx in range(len(seq)):  # letter index
        letter = seq[letter_idx]
        for prog in range(1, len(seq) - letter_idx):  # progression
            cnt = 0  # counter
            while (letter_idx + cnt * prog) < len(seq) and seq[letter_idx + cnt * prog] == letter:
                cnt += 1
            if cnt >= coloursDict[letter]:
                return True

    return False


def computer():
    # odpowiada za ture komputera
    # ALGORYTM - znajduje miejsce do wstawienia "_"
    # oznaczone np nr indeksu poprzedzającego miejsce wstawienia
    # wtedy podzielić, wstawić _
    global coloursDict, seq, n, r
    print(seq)
    '''

    :return:
    '''

def computer_random():
    # tura komputera; losowa strategia
    global coloursDict, seq, n, r
    pos = random.randint(0, len(seq)) # pozycja, którą wybrał komputer
    seq.insert(pos, '_')
    return pos


def player(pos):
    # odpowiada za turę gracza
    global coloursDict, seq, n, r, str
    print("Wstaw kolor ( dostępne", str, "): ")
    col = input()
    ### obsluga bledow
    ### _ w seq = col
    ### ewentualnie mozna przekazywac nr indeksu z funkcji computer
    ### i po prostu zamienic
    seq[pos] = col
    print("Pozostało żetonów: ", n-len(seq))


def create_colours_dict(values):
    # input -> dict
    global coloursDict, seq, n, r, lett
    a_list = values.split()
    map_object = map(int, a_list)
    list_of_integers = list(map_object)
    keys = lett
    coloursDict = dict(zip(keys, list_of_integers))


def print_seq():
    global seq
    r = ""
    for i in seq:
        r += i
    print(r)


def make_str():
    global lett, str
    for i in lett:
        str = str + i + ", "
    str = str[:-2]
    return str



def main():
    global coloursDict, seq, n, r, lett, str
    ###### Wstępny prompt #####
    while True:

        # n - liczba żetonów
        n = None
        # r - liczba kolorów
        r = None
        # coloursDict - słownik litera:długość ciągu
        coloursDict = {}
        # seq - aktualny ciąg
        seq = []
        # lett - lista używanych kolorów
        lett = []
        # str - ładne wyświetlanie kolorów
        str = ""

        print("\nLiczby Off-diagonal Van der Waerdena online")
        print("Jesteś graczem 2. Razem z graczem 1 budujecie ciąg żetonów o maksymalnej długości n za pomocą r kolorów.")
        print("Gracz 1 wybiera miejsce, w które musisz wstawić żeton (oznaczone \"_\"). Wybierasz kolor żetonu, jaki wstawisz w to miejsce.")
        print("Twoim zadaniem jest niedopuszczenie do ułożenia ciągu arytmetycznego z dowolnego z kolorów o długości przypisanej do tego koloru.")
        print("Gra kończy się zatem, gdy zostanie ułożone n żetonów (wygrana gracza 2) lub zostanie ułożony ciag arytmetyczny z dowolnego koloru o zadanej długości (wygrana gracza 1).")
        print("Powodzenia!\n")
        print("############\n")

        ##### Pobranie wartości #####

        n = int(input("Podaj liczbę żetonów: "))
        r = int(input("Podaj liczbę dopuszczalnych kolorów: "))
        lett = list(ascii_lowercase)[:r]
        str = make_str()
        print("Kolory to:", str)
        values = input("Podaj długości ciągów (liczby naturalne oddzielone spacją): ")
        ### dodac obsluge wyjatkow / bledow

        ##### Przygotowanie słownika #####
        create_colours_dict(values)
        print(coloursDict)

        ##### Gra właściwa #####

        win = False
        while not win and len(seq) < n:
            position = computer_random()
            print_seq()
            player(position)
            print_seq()
            win = winning_computer_condition()

        if win:
            print("Wygrana komputera")
        else:
            print("Wygrana gracza")

        ##### Po zakończeniu #####
        cont = input("Czy chcesz zagrać ponownie? [y/n]: ")
        if cont.lower() == "y":
            print("gramy  \n\n\n")
            ### gramy dalej
        else:
            return 0


if __name__ == "__main__":
    main()