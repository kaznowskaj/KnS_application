# coloursDict - global? n - tez global? seq - global???
# n - jakie dlugosci? (1 bez sensu troche, 2 chyba tez ...)
# 1 <= r <= 26
# dlugosci ciagow - pozwolic na 1? - max n

from string import ascii_lowercase
seq = []
# n - liczba żetonów
# r - liczba kolorów
# coloursDict - słownik litera:długość ciągu
# seq - aktualny ciąg


def winningComputerCondition(coloursDict):
    # sprawdza czy wygrana komputera
    for i in coloursDict:
        win = checkSeq(i, coloursDict)
        if win:
            return True
    return False


def checkSeq(letter, coloursDict):
    # sprawdza miejsca pojawienia się danej litery w ciągu (seq)
    # następnie sprawdza czy występuje jakikolwiek ciąg spełniający warunki
    indexes = []

    for i in range(len(seq)):
        if seq[i] == letter:
            indexes.append(i)

    if len(indexes) < coloursDict[letter]:
        return False

    ### poszukiwanie ciagow
    ### sprawdzić długość znalezionych ciągów
    ### jak znalezione o dobrej długości, to super, return True


def computer():
    # odpowiada za ture komputera
    # ALGORYTM - znajduje miejsce do wstawienia "_"
    # oznaczone np nr indeksu poprzedzającego miejsce wstawienia
    # wtedy podzielić, wstawić _
    print(seq)
    '''

    :return:
    '''


def player(coloursDict, n):
    # odpowiada za turę gracza
    print("Wstaw kolor (dostępne", list(coloursDict.keys()), "): ")
    col = input()
    ### obsluga bledow
    ### _ w seq = col
    ### ewentualnie mozna przekazywac nr indeksu z funkcji computer
    ### i po prostu zamienic
    print(seq)
    print("Pozostało żetonów: ", n-len(seq))

def valuesToList(values):
    # funkcja zmieniająca podane przez gracza długości ciągów
    # w listę, potrzebna do utworzenia słownika
    a_list = values.split()
    map_object = map(int, a_list)
    list_of_integers = list(map_object)
    return list_of_integers


def createColoursDict(r, values):
    # utworzenie słownika litera:długość ciągu
    keys = list(ascii_lowercase)[:r]
    coloursDict = dict(zip(keys, values))
    return coloursDict

### można dodać jeszcze funkcje ładnie wyświetlające
### np aktualny ciąg (seq) albo litery (podawane przy
### pobraniu danych i następnie w turze gracza)

def main():

    ###### Wstępny prompt #####

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

    values = valuesToList(values)
    coloursDict = createColoursDict(r, values)

    ##### Gra właściwa #####

    win = False
    while not win and len(seq) < n:
        computer()
        player(coloursDict, n)
        print()
        win = winningComputerCondition(coloursDict)

    if win:
        print("Wygrana komputera")
    else:
        print("Wygrana gracza")

    ##### Po zakończeniu #####
    cont = input("Czy chcesz zagrać ponownie? [y/n]")
    if cont.lower =="y":
        print("gramy dalej")
        ### gramy dalej
    else:
        return 0


if __name__ == "__main__":
    main()