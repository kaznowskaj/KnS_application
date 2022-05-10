import random
from string import ascii_lowercase
import numpy as np
from copy import deepcopy


# declaration of global variables
# n - number of tokens
n = -1
# r - number of colours
r = -1
# colours_dict - dictionary letter: sequence length
colours_dict = {}
# curr_seq - current sequence
curr_seq = []
# colours_list - used colours
colours_list = []
# col_disp - colours display
col_disp = ""


def winning_computer_condition():
    # checking if the computer won
    # (is there a monochromatic sequence of color i, length k_i in the string being built)
    #
    # True - if the arithmetic sequence exists
    # False - otherwise

    global colours_dict, curr_seq

    for letter in colours_dict.keys():
        if colours_dict[letter] == 1:
            if letter in curr_seq:
                return True

    for letter_idx in range(len(curr_seq)):  # letter index
        letter = curr_seq[letter_idx]
        for prog in range(1, len(curr_seq) - letter_idx):  # progression
            cnt = 0  # counter
            while (letter_idx + cnt * prog) < len(curr_seq) and curr_seq[letter_idx + cnt * prog] == letter:
                cnt += 1
            if cnt >= colours_dict[letter]:
                return True

    return False


def computer():
    # computer's turn
    # inserts '_' in the chosen place
    #
    # returns the index corresponding to the insertion point of the new token

    global curr_seq

    pos = find_position()  # chosen position
    curr_seq.insert(pos, '_')

    return pos


def computer_random():
    # computer random strategy
    # draw a place in the sequence where the player must place a token
    # inserts '_' in the chosen place
    #
    # returns the index corresponding to the insertion point of the new token

    global curr_seq

    pos = random.randint(0, len(curr_seq))  # chosen position
    curr_seq.insert(pos, '_')

    return pos


# TO_DO:
# - input handling
def player(pos):
    # player's turn
    # inserts colour chosen by player into the place chosen by computer

    global curr_seq, n, col_disp

    print("Wstaw kolor ( dostępne", col_disp, "): ")
    col = input()
    curr_seq[pos] = col
    print("Pozostało żetonów: ", n - len(curr_seq))


def find_position():
    # computer strategy
    # finds a place in the sequence where the player must place a token
    # if the win is one move away it returns specific winning index, else it returns the index where placing the token
    # will lead to the best situation in 2 moves
    # returns an index of the best found position

    global curr_seq, colours_dict

    position_max_values = []  # max value for each position

    for pos in range(len(curr_seq) + 1):  # check position
        col_values = []  # value for each colour
        for col in colours_dict.keys():  # check colour
            new_seq = deepcopy(curr_seq)
            new_seq.insert(pos, col)
            col_value = rate_position(new_seq)  # rate sequence
            col_values.append(col_value)
        if max(col_values) == 0:
            return pos
        else:
            col_values = []
            for col in colours_dict.keys():  # check colour
                new_seq = deepcopy(curr_seq)
                new_seq.insert(pos, col)
                col_value = find_rating(new_seq)  # rate sequence
                col_values.append(col_value)
        position_max_values.append(max(col_values))

    sequence_min_value = min(position_max_values)  # min value of the sequence
    min_index = position_max_values.index(sequence_min_value)  # chosen position

    return min_index


def find_rating(seq):
    # same as find_position, but takes sequence as argument and returns minimal possible rating of given sequence
    global colours_dict

    position_max_values = []  # max value for each position

    for pos in range(len(seq) + 1):  # check position
        col_values = []  # value for each colour
        for col in colours_dict.keys():  # check colour
            new_seq = deepcopy(seq)
            new_seq.insert(pos, col)
            col_value = rate_position(new_seq)  # rate sequence
            col_values.append(col_value)
        position_max_values.append(max(col_values))

    sequence_min_value = min(position_max_values)  # min value of the sequence
    # min_index = position_max_values.index(sequence_min_value)  # chosen position

    return sequence_min_value


def rate_position(sequence):
    # rates the position (lower is better)
    #
    # if min(k_i - l_i) == 0
    #   returns 0
    # else
    #   returns max(k_i - l_i),
    # where k_i is length of the monochromatic (i-th color) sequence that is needed for computer to win
    # and l_i is the length of the longest monochromatic (i-th color) sequence found.

    global colours_dict

    # dictionary colour: [indexes in current sequence]
    col_indexes = {col: [] for col in colours_dict.keys()}
    # dictionary colour: max length of arithmetic sequence
    arithmetic_max_lens = {col: 1 for col in colours_dict.keys()}

    for start_ix, letter in enumerate(sequence):  # fill col_indexes
        col_indexes[letter].append(start_ix)

    for col in colours_dict.keys():  # for each colour

        if len(col_indexes[col]) == 0:  # case with 0 occurrences
            arithmetic_max_lens[col] = 0
            continue

        for start_ix in range(len(col_indexes[col])):  # for arithmetic sequences which starts in index start_ix

            # possible progressions (without 0, which is default)
            possible_progressions = (np.array(col_indexes[col]) - col_indexes[col][start_ix])[start_ix+1:]

            if len(col_indexes[col]) - start_ix <= arithmetic_max_lens[col]:  # there cannot be longer sequence
                break

            for prog in possible_progressions:  # check every progression

                arithmetic_len = 1
                last = start_ix

                for i in range(start_ix + 1, len(col_indexes[col])):
                    if col_indexes[col][i] < col_indexes[col][last] + prog:
                        continue
                    elif col_indexes[col][i] == col_indexes[col][last] + prog:
                        arithmetic_len += 1
                        last = i
                    else:
                        break

                if arithmetic_len > arithmetic_max_lens[col]:  # new max length
                    arithmetic_max_lens[col] = arithmetic_len

    # computer wins
    if min(np.array(list(colours_dict.values())) - np.array(list(arithmetic_max_lens.values()))) == 0:
        return 0

    # no win
    return max(np.array(list(colours_dict.values())) - np.array(list(arithmetic_max_lens.values())))


def print_seq():
    # displays the sequence

    global curr_seq

    displayed_seq = ""
    for letter in curr_seq:
        displayed_seq += letter
    print(displayed_seq)


def create_colours_dict(values):
    # creates colours_dict dictionary

    global colours_dict, colours_list

    a_list = values.split()
    map_object = map(int, a_list)
    list_of_integers = list(map_object)
    keys = colours_list
    colours_dict = dict(zip(keys, list_of_integers))


def create_col_disp():
    # creates col_disp string

    global colours_list, col_disp

    for i in colours_list:
        col_disp = col_disp + i + ", "
    col_disp = col_disp[:-2]
    return col_disp


# TO_DO:
# - input handling
def main():
    # main function - start of the programme

    global colours_dict, curr_seq, n, r, colours_list, col_disp

    while True:

        # variable reset
        n = None
        r = None
        colours_dict = {}
        curr_seq = []
        colours_list = []
        col_disp = ""

        # initial prompt
        print("\nLiczby Off-diagonal Van der Waerdena online")
        print("Jesteś graczem 2.")
        print("Razem z graczem 1 budujecie ciąg żetonów o maksymalnej długości n za pomocą r kolorów.")
        print("Gracz 1 wybiera miejsce, w które musisz wstawić żeton (oznaczone \"_\").")
        print("Wybierasz kolor żetonu, jaki wstawisz w to miejsce.")
        print("Twoim zadaniem jest niedopuszczenie do ułożenia ciągu arytmetycznego z dowolnego z kolorów "
              "o długości przypisanej do tego koloru.")
        print("Gra kończy się zatem, gdy zostanie ułożone n żetonów (wygrana gracza 2) lub"
              " zostanie ułożony ciag arytmetyczny z dowolnego koloru o zadanej długości (wygrana gracza 1).")
        print("Powodzenia!\n")
        print("############\n")

        # input
        n = int(input("Podaj liczbę żetonów: "))
        r = int(input("Podaj liczbę dopuszczalnych kolorów: "))
        colours_list = list(ascii_lowercase)[:r]
        col_disp = create_col_disp()
        print("Kolory to:", col_disp)
        values = input("Podaj długości ciągów (liczby naturalne oddzielone spacją): ")
        create_colours_dict(values)

        # chose computer strategy
        print("Wybierz strategię komputera (wpisz 1 lub 2): ")
        print("\t 1. Strategia zaawansowana")
        print("\t 2. Strategia losowa")
        strategy = int(input())

        # the game is on
        win = False
        while not win and len(curr_seq) < n:

            if strategy == 1:
                position = computer()
            else:
                position = computer_random()

            print_seq()
            player(position)
            print_seq()
            win = winning_computer_condition()

        if win:
            print("Wygrana komputera")
        else:
            print("Wygrana gracza")

        # game over
        cont = input("Czy chcesz zagrać ponownie? [y/n]: ")
        if cont.lower() == "y":
            print("Nowa gra \n\n\n")
        else:
            return 0


if __name__ == "__main__":
    main()
