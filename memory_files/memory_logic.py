# Files
# The program consists of the following files:
# *** memory_main: contains a main function, some extra functions, and a class Memory, with associated methods.
# *** memo_words.txt: a list of three-letter words.
# *** all_scores: a JSON file that stores the player's name and score for the game's three difficulty levels,
# 2x2, 4x4, or 6x6 tiles. The format is a dictionary where the board size is the key, and the value
# is a list containing lists of scores and names: all_scores = {size: [[score1, name1], [score2, name2]] … etc.}

# Game Structure
# *** Memory Class
# The Memory class handles the game itself. The instance attributes consist of two dictionaries with the same structure.
# These keep track of where the hidden words are located and which tiles should be displayed.

# *** Example of game board and connection to dictionary

#    1   2         1   2
# A --- ---     A hej top
# B --- ---     B top hej

# Example: the boards above have a size of 2 because they consist of two rows and columns.
# The initial version of the dictionary for the presentation_board (the left one) is:
# {A: ["---", "---"], B: ["---", "---"]}
# and hidden_word_dictionary (which initially contains all the data to display the right one) looks like this:
# {A: ["hej", "top"], B: ["top", "hej"]}
# These two dictionaries are the backbone of the entire game. The presentation_board is updated as the game progresses,
# while hidden_word_dictionary remains the same throughout.

# Several methods in the class are internal and are used, among other things, when instantiating the attributes.
# Detailed explanations of methods, instance variables, and attributes are provided with each function.

# *** Main
# Main calls a function def_run_a_round_of_the_game, which manages a full round of the game
# and creates an instance of Memory. Main also tracks the overall game logic and calls
# functions that handle importing player scores, presenting the high scores, and updating
# the file that stores the high scores.


# Anna Björklund
# Date December 2024
# Course code DD100N HT24 Programmeringsteknik webbkurs (10118)# Namn


import random
import json
from datetime import datetime


class Memory():
    '''The class that executes all game logic for the Memory game, can be used with a terminal program and a GUI '''

    def __init__(self, size: int):
        '''Instance attributes and variables size must be an even number, 2, 4 or 6. '''

        self.size = size  # size of one row or column on the game board
        # dictionary with information to be printed out to create the game board, Key is a letter and the positions are stored in a list
        self.presentation_board = self._create_first_versions_of_game_board()
        # a dictionary with all the choosen words on the right position in each row. Keys are the letters
        self.hidden_words_board = self._create_hidden_words_board()

    def _import_all_words_from_txt(self) -> list:
        '''Imports all words from the memo_words.txt file.
        Returns a list with all words'''
        all_words = []
        with open("memo_words.txt", "r") as memo_file:
            for row in memo_file:
                all_words.append(row)
        return all_words

    def _pick_random_words(self) -> list:
        '''Picks random words from a list of words
            Returns: a list with size*size/2 numbers of unique words'''
        choosen_words = []
        all_words = self._import_all_words_from_txt()
        list_length = len(all_words)
        pick_word = True
        while pick_word:
            index_word = random.randrange(list_length)
            word = str(all_words[index_word]).strip("\n")
            if word in choosen_words:  # if the word is allready choosen, make a new try
                continue
            else:
                choosen_words.append(word)
            # the board has self size x self size positions, each word needs two positions
            amount_of_words = int(self.size**2)/2
            if len(choosen_words) == amount_of_words:
                pick_word = False
                return choosen_words

    def create_record_of_all_postions(self):
        '''Returns a list of lists(row, index) with all positions on the board with the choosen size, the index is the column number-1'''
        count_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        all_positions = []
        for row in range(self.size):
            letter = count_letters[row]
            for index in range(self.size):
                position = [letter, index]
                all_positions.append(position)

        return all_positions

    def _create_hidden_words_board(self):
        choosen_words = self._pick_random_words()
        # the dictinary registering all words in their, for this game, choosen positions.
        hidden_words_board = self._create_first_versions_of_game_board()
        # a list of lists with the position [row/letter, column/index, not the number shown on the board]
        available_positions = self.create_record_of_all_postions()
        count_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        # The dictionary is populated with the choosen words, using a random function and the list with the dictionarys all available positions.

        for word in choosen_words:  # goes through all words in the list
            for place_word in range(2):  # we have to position the word twice
                # TODO kolla att detta stämmer med intervallen
                index_picked = random.randrange(len(available_positions))
                # sets position to the value and deletes it from the list, so the position cant be choosen again
                position = available_positions[index_picked]
                hidden_words_board[position[0]][position[1]] = word
                # available_positions.pop[index_picked]
                # available_positions.remove(index_picked)
                del available_positions[index_picked]
        return hidden_words_board

    def _create_first_versions_of_game_board(self):

        game_board = {}
        count_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for row in range(self.size):
            key = count_letters[row]
            game_board[key] = ["---"]*self.size

        return game_board

    def change_size(self, size):
        '''GUI function - not used in terminal game. The default size of a game i 2x2 memory cards, if the user
        chooses to go with a harder level the size is changed with this method -
        presentation_board and hidden_words_board are uppdated accordingly'''
        self.size = size
        self.presentation_board = self._create_first_versions_of_game_board()
        self.hidden_words_board = self._create_hidden_words_board()

    def print_presentation_board(self):
        '''Prints out the inparameter - a dictionary as a memory board with spaces and the right column numbers'''
        board = self.presentation_board
        print("\n")
        for column in range(self.size):
            print(f"    {column+1}", end="")
        print("\n")
        for key in board:
            print(f"{key}", end="")
            for col in board[key]:
                if len(col) == 3:
                    print(f"  {col}", end="")
                else:
                    print(f" {col}", end="")
            print("\n")

    def get_word_in_position(self, position) -> str:
        ''' Returns the hidden word from a position in the dictionary presentation_board
        in parameter is the position a list with two values [letter, number], Used by the GUI'''
        word = self.presentation_board[position[0]][position[1]]
        return word

    def update_presentation_board(self, position: list):
        '''
        The input variable is the position a list of two values row/letter, column/index (not the number displayed when printed)
        Updates the choosen position in self.presentation_board with the word that is registered on that position (in hidden_words_board)'''
        self.presentation_board[position[0]][position[1]
                                             ] = self.hidden_words_board[position[0]][position[1]]

    def reset_presentation_board(self, position_1: list, position_2=list):  # NY
        '''Resets the presentation board after an unsuccessfull move'''
        self.presentation_board[position_1[0]][position_1[1]] = "---"
        self.presentation_board[position_2[0]][position_2[1]] = "---"

    def reset_presentation_board_one_value_only(self, position_1: list):
        '''Resets the presentation board after an error in move2'''
        self.presentation_board[position_1[0]][position_1[1]] = "---"

    def its_a_match(self, position_1, position_2) -> bool:
        '''checks if the two choosen tiles are matching
        Returns True if that is the case -  False if they doesent'''
        word_1 = self.presentation_board[position_1[0]][position_1[1]]
        word_2 = self.presentation_board[position_2[0]][position_2[1]]
        if word_1 == word_2:
            return True
        else:
            return False

    def check_if_all_words_are_found(self) -> bool:
        '''Checks if there are any more words to look for.
        Returns true if the game should end'''
        all_moves_done = True
        for key in self.presentation_board:
            for index in range(len(self.presentation_board[key])):
                if self.presentation_board[key][index] == "---":
                    all_moves_done = False
                    return all_moves_done
        return all_moves_done


def import_score_from_file() -> dict:
    '''Imports all scores from the file and puts it in a dictionary with level as key and value a list - [gamer_name, score, time], if no file exists an empty list will be created for now.
    a file will be created at the end of the game, when the high_score list is updated'
    Returns: a dictionary all_scores'''
    all_scores = {}
    try:
        with open("high_score.json", "r") as file:
            all_scores = json.load(file)
            return all_scores
    except FileNotFoundError:
        all_scores = {2: [], 4: [], 6: []}
        return all_scores

    # felhantera om listan är tom TODO lägg till level också i logiken


def print_score_to_file(all_scores: dict):
    "Prints the high_score_file dictionary to the high_score.json file"

    with open("high_score.json", "w") as file:
        json.dump(all_scores, file)


def print_high_scores(size: int, high_score_number: int, all_scores: dict):
    '''The high_score is  printed out in the terminal - the top players. The players are ranked primarily on amount of rounds.
    But if more player than have the same amount of rounds, the time it took to complete the round will determine. '''

    score_list_length = len(all_scores[str(size)])
    if score_list_length < high_score_number:
        high_score_number = score_list_length

    if score_list_length > 1:
        # sorting the list from highest to lowest sec
        all_scores[str(size)] = sorted(
            all_scores[str(size)], key=lambda x: x[3])
        # sorting the list from highest to lowest min
        all_scores[str(size)] = sorted(
            all_scores[str(size)], key=lambda x: x[2])
        # sorting the list from highest to lowest score
        all_scores[str(size)] = sorted(
            all_scores[str(size)], key=lambda x: x[0])
    print(f"\n***BÄSTA SPELARNA FÖR {size}x{size} BRICKOR*** \n")
    for result in range(high_score_number):
        print(f"{all_scores[str(size)][result][1]} : {all_scores[str(size)][result][0]} rundor : tid {
              all_scores[str(size)][result][2]} minuter, {all_scores[str(size)][result][3]} sekunder ")


def choose_difficulty_level() -> int:
    '''Prints the menue, lets the user choose level of difficulty.
    Returns size of the board, amount of rows and columns'''
    print("\n")
    while True:
        print("Vilken spelnivå väljer du?")
        print("[1] - Lätt 2x2 rader och kolumner")
        print("[2] - Medium 4x4 rader och kolumner")
        print("[3] - Svårt 6x6 rader och kolumner")

        menue_choice = input("\nSkriv in ditt val: ")
        if menue_choice == "1":
            size = int(2)
            return size
        elif menue_choice == "2":
            size = int(4)
            return size
        elif menue_choice == "3":
            size = int(6)
            return size
        else:
            print("\nDu har gjort ett ogilltigt val - försök igen\n")


def run_a_round_of_the_game(size: int) -> int:
    '''Creates an instance of the Memory class - player_memory_game and runs a round of the game whith the help of the functions in the Memory class.
    Returns the score'''
    player_memory_game = Memory(size)  # skapar instans av Memory
    rounds = 0
    position_1_letter = str
    position_1_number = int
    position_2_letter = str
    position_2_number = int

    while True:

        rounds += 1
        player_memory_game.print_presentation_board()
        print("Välj din första bricka, ange kolumn och rad")
        position_1_letter = (input("Skriv bokstaven för raden: ")).upper()
        try:
            position_1_number = int(input("Skriv kolumnens nummer: "))-1
            if position_1_number < 0:
                print("\nDen positionen finns inte - försök igen")
                continue
        except (ValueError):
            print("Du behöver skriva in ett nummer från 1 till {size}")
            continue

        try:
            if player_memory_game.presentation_board[position_1_letter][position_1_number] != "---":
                print("\nDu har redan valt den brickan...nytt försök")
                continue

            player_memory_game.update_presentation_board(
                [position_1_letter, position_1_number])
        except (IndexError, KeyError):
            print("\nDen positionen finns inte - försök igen")
            continue

        player_memory_game.print_presentation_board()
        print("Välj din andra bricka, ange kolumn och rad")

        position_2_letter = (input("Skriv bokstaven för raden: ").upper())
        try:
            position_2_number = int(input("Skriv kolumnens nummer: "))-1
            if position_2_number < 0:
                print("\nDen positionen finns inte - försök igen")
                player_memory_game.reset_presentation_board_one_value_only(
                    [position_1_letter, position_1_number])
                continue
        except ValueError:
            print("Du behöver skriva in ett nummer från 1 till {size}")
            player_memory_game.reset_presentation_board_one_value_only(
                [position_1_letter, position_1_number])
            continue
        try:
            if player_memory_game.presentation_board[position_2_letter][position_2_number] != "---":
                print("\nDu har redan valt den brickan")
                player_memory_game.reset_presentation_board_one_value_only(
                    [position_1_letter, position_1_number])
                continue

            player_memory_game.update_presentation_board(
                [position_2_letter, position_2_number])
        except (IndexError, KeyError):
            print("Den positionen finns inte - försök igen")
            player_memory_game.reset_presentation_board_one_value_only(
                [position_1_letter, position_1_number])
            continue
        player_memory_game.print_presentation_board()
        matching_tiles = player_memory_game.its_a_match(
            [position_1_letter, position_1_number], [position_2_letter, position_2_number])
        if matching_tiles:
            # player_memory_game.update_presentation_board_if_a_match()
            game_over = player_memory_game.check_if_all_words_are_found()
            if game_over:
                return rounds
            else:
                print("\n Match, snyggt!")
        else:
            # resetts the position_1 and position_2 and deletes the values
            player_memory_game.reset_presentation_board(
                [position_1_letter, position_1_number], [position_2_letter, position_2_number])
            input("\n...försök igen tryck RETUR \n")


def start_timer():
    '''Sets the start time and returns the start time'''
    current_time = datetime.now()
    start_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    return start_time


def stop_timer_return_time(start_time) -> float:
    '''sets stop time and calculates and returns the gamers time'''
    current_time = datetime.now()
    stop_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')

    dt1 = datetime.strptime(stop_time, '%Y-%m-%d %H:%M:%S.%f')
    dt2 = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')

    time_diff = abs(dt1-dt2)
    total_second = time_diff.total_seconds()
    minutes = (time_diff.seconds % 3600) // 60,
    seconds = time_diff.seconds % 60,
    microseconds = time_diff.microseconds
    decimal_sec = float(f"{seconds[0]}.{microseconds}")
    shorter_sec = round(decimal_sec, 2)
    time = [minutes[0], shorter_sec]
    return time


def main():
    '''Main progam to the Memory game. Handles all interaction with the player - printouts and menues.
    calls function for different tasks'''
    size = int  # size of a row or column of the board
    my_score = 0
    high_score_number = 5  # highscores to display
    gaming_name = str  # the players name
    # A list of a list with previous high scores [score, player_name] - imported from a separate file - high_score_memory.txt
    # high_score = import_score_from_file()

    print("\n**MEMORY SPEL**")
    run = True
    leave = "go"
    while run:
        leave = input(
            "\nTryck RETUR för att starta ett nytt spel!!\n...vill du avsluta spelet skriv q + RETUR \n")
        if leave == "q" or leave == "Q":
            print("Spelet avslutas")
            break

        gaming_name = input("Skriv in ditt gaming namn: ")
        size = choose_difficulty_level()  # prints the menue and returns menue choice
        start_time = start_timer()
        print("\nNu kör vi!!")
        my_score = run_a_round_of_the_game(size)
        time = stop_timer_return_time(start_time)
        player_game_time = f"{time[0]} minuter och {time[1]} sekunder "
        print(f" Du klarade det på: {
              my_score} rundor - på tiden: {player_game_time}")
        all_scores = import_score_from_file()
        all_scores[str(size)].append([my_score, gaming_name, time[0], time[1]])
        print_high_scores(size, high_score_number, all_scores)
        print_score_to_file(all_scores)


if __name__ == "__main__":
    main()
