# coloursDict - global? n - tez global? seq - global???
# n - jakie dlugosci? (1 bez sensu troche, 2 chyba tez ...)
# 1 <= r <= 26
# dlugosci ciagow - pozwolic na 1? - max n
import random
from string import ascii_lowercase

def winningComputerCondition():
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
    global coloursDict, seq, n, r
    print("Wstaw kolor (dostępne", list(coloursDict.keys()), "): ")
    col = input()
    ### obsluga bledow
    ### _ w seq = col
    ### ewentualnie mozna przekazywac nr indeksu z funkcji computer
    ### i po prostu zamienic
    seq[pos] = col
    print("Pozostało żetonów: ", n-len(seq))

def createColoursDict(values):
    # input -> dict
    global coloursDict, seq, n, r
    a_list = values.split()
    map_object = map(int, a_list)
    list_of_integers = list(map_object)
    keys = list(ascii_lowercase)[:r]
    coloursDict = dict(zip(keys, list_of_integers))

### można dodać jeszcze funkcje ładnie wyświetlające
### np aktualny ciąg (seq) albo litery (podawane przy
### pobraniu danych i następnie w turze gracza)

def main():
    global coloursDict, seq, n, r
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

        print("Grasz w grę")
        print("Jesteś graczem")
        print("Twoje zadanie to")
        print("############")

        ##### Pobranie wartości #####

        n = int(input("Podaj liczbę żetonów: "))
        r = int(input("Podaj liczbę dopuszczalnych kolorów: "))
        ### moze zmienic na po przecinkach litery (albo po spacjach)
        print("Kolory to: ", list(ascii_lowercase)[:r])
        values = input("Podaj długości ciągów (liczby naturalne oddzielone spacją): ")
        ### dodac obsluge wyjatkow / bledow

        ##### Przygotowanie słownika #####
        createColoursDict(values)
        print(coloursDict)

        ##### Gra właściwa #####

        win = False
        while not win and len(seq) < n:
            position = computer_random()
            print(seq)
            player(position)
            print(seq)
            win = winningComputerCondition()

        if win:
            print("Wygrana komputera")
        else:
            print("Wygrana gracza")

        ##### Po zakończeniu #####
        cont = input("Czy chcesz zagrać ponownie? [y/n]")
        if cont.lower() == "y":
            print("gramy  \n\n\n")
            ### gramy dalej
        else:
            return 0


if __name__ == "__main__":
    main()