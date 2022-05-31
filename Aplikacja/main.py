import random
from string import ascii_lowercase
import numpy as np
from copy import deepcopy, Error
import os
from colorama import Fore
from colorama import init
from itertools import chain

# declaration of global variables
# n - number of tokens
n = -1
# r - number of colours
r = -1
# colours_dict - dictionary letter: sequence length
# col_counts - counts of particular colors in sequence
colours_dict = {}
col_counts = {}
# curr_seq - current sequence
curr_seq = []
# colours_list - used colours
colours_list = []
# col_disp - colours display
col_disp = ""
# computers strategy
strategy = -1


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_curr_situation():
    # prints current game info
    global colours_dict, curr_seq, n, strategy

    if strategy == 1:
        print("Player 1's strategy: Advanced strategy")
    else:
        print("Player 1's strategy: Random strategy")
    print("Colors and lengths: ", end="")
    for key, val in colours_dict.items():
        s = "" + str(key) + "(" + str(val) + "), "
        print(s, end="")
    print("\nTokens left: ", n - len(curr_seq) + 1)
    print("\n----------------------------------------------------------------------------------------------------------"
          "--------------")
    print("Sequence: ", print_seq())
    print("------------------------------------------------------------------------------------------------------------"
          "------------")
    print("Choose color: ")


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
                return True, [curr_seq.index(letter)]

    for letter_idx in range(len(curr_seq)):  # letter index
        letter = curr_seq[letter_idx]
        for prog in range(1, len(curr_seq) - letter_idx):  # progression
            cnt = 0  # counter
            while (letter_idx + cnt * prog) < len(curr_seq) and curr_seq[letter_idx + cnt * prog] == letter:
                cnt += 1
            if cnt >= colours_dict[letter]:
                return True, [i for i in range(letter_idx, letter_idx + prog*(colours_dict[letter] - 1) + 1, prog)]

    return False, []


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


def player(pos):
    # player's turn
    # inserts colour chosen by player into the place chosen by computer

    global curr_seq, n, col_disp, col_counts

    cls()
    while True:
        try:
            display_curr_situation()
            col = input()
            if col not in colours_dict.keys():
                raise ValueError
            break
        except ValueError:
            cls()
            print(Fore.RED + "Select the correct option.\n")
    curr_seq[pos] = col
    col_counts[col] += 1



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
    possible_indexes = []
    for i in range(len(position_max_values)):
        if position_max_values[i] == sequence_min_value:
            possible_indexes.append(i)
    min_index = random.choice(possible_indexes) # chosen position
    # position_max_values.index(sequence_min_value)  # chosen position

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
    return displayed_seq


def create_colours_dict(list_of_integers):
    # creates colours_dict dictionary

    global colours_dict, colours_list

    keys = colours_list
    colours_dict = dict(zip(keys, list_of_integers))


def create_col_disp():
    # creates col_disp string

    global colours_list, col_disp

    for i in colours_list:
        col_disp = col_disp + i + ", "
    col_disp = col_disp[:-2]
    return col_disp


def check_if_n(table):
    good = True
    for i in table:
        if i < 1:
            good = False
            break
    return good


def display_comp_win(win_idx):
    # message about computers win
    global curr_seq

    print("Sequence: ", end="")
    for ix, letter in enumerate(curr_seq):
        if ix in win_idx:
            print(Fore.YELLOW + "" + letter, end="")
        else:
            print(letter, end="")
    print("\n\nPlayer 1 won :(\n")


def display_player_win():
    # message about players win
    print("Sequence: ", print_seq(), "\n")
    print("You won!\n")

def insertTest(max_length, color):
    # seq = ['a', 'b', 'c', 'a', 'b', 'a', 'a', 'a', 'b', 'a']
    global curr_seq, colours_dict
    seq = curr_seq
    indexes = []
    diffs = []
    # indexy koloru + odleglosci

    for i in range(len(seq)):
        if seq[i] == color:
            indexes.append(i)
    diffs = [(indexes[i]-indexes[i-1]) for i in range(1, len(indexes))]
    print(indexes)
    print(diffs)
    max_diff = max(diffs)

    # jesli skrajny zeton jest tym ktory powoduje ze max diff jest wieksze, i mamy wieksza liczbe zetonow niz minimalna
    #mozna go wywalic

    while True:

        # if diffs[0]==max_diff and len(diffs)>=colours_dict[color]:
        #     diffs.pop(0)
        #     indexes.pop(0)
        #     max_diff=max(diffs)
        #
        # elif diffs[len(diffs)-1]==max_diff and len(diffs)>=colours_dict[color]:
        #     diffs.pop(len(diffs)-1)
        #     indexes.pop(len(indexes)-1)
        #     max_diff=max(diffs)

        # Shortening array of indexes needed to form progression after spreading

        if diffs[len(diffs)-1]>diffs[0] and len(diffs)>=colours_dict[color]:
            diffs.pop(len(diffs) - 1)
            indexes.pop(len(indexes) - 1)
            max_diff = max(diffs)
        elif diffs[len(diffs)-1]<=diffs[0] and len(diffs)>=colours_dict[color]:
            diffs.pop(0)
            indexes.pop(0)
            max_diff=max(diffs)
        else:
            break
    #print(indexes)
    #print(diffs)

    # uzupelnienie ciągu
    seq_len = 0
    for i in range(len(diffs)-1, 0-1, -1):
        seq_len += max_diff - diffs[i]

    # # sprawdzenie
    # indexes = []
    # diffs = []
    # for i in range(len(seq)):
    #     if seq[i] == color:
    #         indexes.append(i)
    # diffs = [(indexes[i] - indexes[i - 1]) for i in range(1, len(indexes))]
    # print(seq)
    # print(indexes)
    # print(diffs)

    if seq_len+len(curr_seq) > max_length:
        return None
    else:
        return list(chain(*[[indexes[i]]*(max_diff-diffs[i]) for i in range(len(diffs))]))


def main():
    # main function - start of the programme

    global colours_dict, curr_seq, n, r, colours_list, col_disp, strategy, col_counts
    init(autoreset=True)  # coloring settings
    os.system("title " + "Off-diagonal Van der Waerden online")

    # exceptions classes
    class ValueTooSmallError(Error):
        """Raised when the input value is too small"""
        pass

    class ValueTooBigError(Error):
        """Raised when the input value is too big"""
        pass

    class ValueBadError(Error):
        """Raised when the value is bad lol"""
        pass

    # main function

    while True:

        # variable reset
        n = None
        r = None
        colours_dict = {}
        curr_seq = []
        colours_list = []
        col_disp = ""
        strategy = -1

        # initial prompt
        print(" _____  __  __           _ _                               _                                            "
              "   ")
        print("|  _  |/ _|/ _|         | (_)                             | |                                           "
              "   ")
        print("| | | | |_| |_ ______ __| |_  __ _  __ _  ___  _ __   __ _| |                                           "
              "   ")
        print("| | | |  _|  _|______/ _` | |/ _` |/ _` |/ _ \| '_ \ / _` | |                                           "
              "   ")
        print("\ \_/ / | | |       | (_| | | (_| | (_| | (_) | | | | (_| | |                                           "
              "   ")
        print(" \___/|_| |_|        \__,_|_|\__,_|\__, |\___/|_| |_|\__,_|_|                                           "
              "   ")
        print("                                    __/ |                                                               "
              "   ")
        print("                                   |___/                                                                "
              "   ")
        print(" _   _                   _             _    _                    _                          _ _         "
              "   ")
        print("| | | |                 | |           | |  | |                  | |                        | (_)        "
              "   ")
        print("| | | | __ _ _ __     __| | ___ _ __  | |  | | __ _  ___ _ __ __| | ___ _ __     ___  _ __ | |_ _ __   _"
              "__ ")
        print("| | | |/ _` | '_ \   / _` |/ _ \ '__| | |/\| |/ _` |/ _ \ '__/ _` |/ _ \ '_ \   / _ \| '_ \| | | '_ \ / "
              "_ \\")
        print("\ \_/ / (_| | | | | | (_| |  __/ |    \  /\  / (_| |  __/ | | (_| |  __/ | | | | (_) | | | | | | | | |  "
              "__/")
        print(" \___/ \__,_|_| |_|  \__,_|\___|_|     \/  \/ \__,_|\___|_|  \__,_|\___|_| |_|  \___/|_| |_|_|_|_| |_|\_"
              "__|")
        print("                                                                                                        "
              "   ")

        print("You are player 2!")
        print("Your goal is to build a string consisting of n tokens using r colors.")
        print("Player 1 chooses the place where you have to insert the token (marked with \"_\").")
        print("You have to choose the color of the token.")
        print("Your task is to prevent the formation of a monochromatic arithmetic progression with a given length \n"
              "for each color. \n")
        print("The game is over when:")
        print("1. monochromatic arithmetic progression of any color with a given length has been formed "
              "(Player 1 wins).")
        print("2. n tokens have been placed (Player 2 wins)")
        print("Good luck!\n\n")

        input("Press Enter to continue...")
        cls()

        # input

        # n - number of tokens
        while True:
            try:
                n = input("Enter the number of tokens to be placed (n): ")
                n = int(n)
                if n < 1:
                    raise ValueTooSmallError
                break
            except ValueError:
                cls()
                print(Fore.RED + "The number of tokens must be a natural number. Try again.\n")
            except ValueTooSmallError:
                cls()
                print(Fore.RED + "The number of tokens must be a natural number. Try again.\n")
        cls()

        # r - number of colors
        while True:
            try:
                print("The number of tokens to be placed (n):", n)
                r = input("Enter the number of colors (r): ")
                r = int(r)
                if r < 1:
                    raise ValueTooSmallError
                if r > n:
                    raise ValueTooBigError
                break
            except ValueError:
                cls()
                print(Fore.RED + "The number of colors must be a natural number. Try again.\n")
            except ValueTooBigError:
                cls()
                print(Fore.RED + "The number of colors cannot exceed the number of tokens.\n")
            except ValueTooSmallError:
                cls()
                print(Fore.RED + "The number of colors must be a natural number. Try again.\n")
        cls()

        colours_list = list(ascii_lowercase)[:r]
        col_disp = create_col_disp()
        col_counts = dict(zip(colours_list, [0 for x in range(len(colours_list))]))

        # values - lengths
        while True:
            try:
                print("The number of tokens to be placed (n):", n)
                print("Colors:", col_disp, "\n")
                values = input("Enter the lengths of the monochromatic arithmetic progressions (natural numbers"
                               " separated by a space): ")
                a_list = values.split()

                if len(a_list) != r:
                    raise ValueBadError

                all([isinstance(int(item), type(int))] for item in a_list)
                map_object = map(int, a_list)
                list_of_integers = list(map_object)
                good = check_if_n(list_of_integers)
                if not good:
                    raise ValueTooSmallError
                break
            except ValueError:
                cls()
                print(Fore.RED + "Lengths must be natural numbers. Try again.\n")
            except ValueTooSmallError:
                cls()
                print(Fore.RED + "Lengths must be natural numbers. Try again.\n")
            except ValueBadError:
                cls()
                print(Fore.RED + "The number of lengths must be the same as the number of colors. Try again.\n")
        cls()
        create_colours_dict(list_of_integers)

        # chose computer strategy
        while True:
            try:
                print("The number of tokens to be placed (n):", n)
                print("Colors and lengths: ", end="")
                for key, val in colours_dict.items():
                    s = "" + str(key) + "(" + str(val) + "), "
                    print(s, end="")
                print("\n\nChoose player 1's strategy (enter 1 or 2): ")
                print("\t 1. Advanced strategy")
                print("\t 2. Random strategy")
                strategy = int(input())
                if strategy != 1 and strategy != 2:
                    raise ValueBadError
                break
            except ValueError:
                cls()
                print(Fore.RED + "Enter the correct option (1 or 2).\n")
            except ValueBadError:
                cls()
                print(Fore.RED + "Enter the correct option (1 or 2).\n")
        cls()

        # the game is on
        win = False
        win_idx = []
        indexes = None
        while not win and len(curr_seq) < n:

            if strategy == 1:
                # if there is posibility to spread tokens to win
                if indexes is None:
                    indexes = None
                    for col in col_counts:
                        if col_counts[col] >= colours_dict[col]:
                            indexes = insertTest(n, col)
                            if indexes:
                                break
                if indexes:
                    position = indexes.pop()+1
                    curr_seq.insert(position, '_')
                else:
                    position = computer()
            else:
                position = computer_random()

            player(position)
            win, win_idx = winning_computer_condition()
        cls()

        # game over
        while True:
            try:
                if win:
                    display_comp_win(win_idx)
                else:
                    display_player_win()
                cont = input("Do you want to play again? [y/n]: ")
                if cont.lower() != "y" and cont.lower() != "n":
                    raise ValueBadError
                if cont.lower() == "y":
                    cls()
                else:
                    return 0
                break

            except ValueBadError:
                cls()
                print(Fore.RED + "Enter the correct option [y/n].\n")


if __name__ == "__main__":
    main()
