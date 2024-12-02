import random
import json
# TODO Fundera på hur man bäst gör sätter något som instansvariabel och sedan kopierar - eller att man låter en funktion returnera.
# OBS!!De delar av programmet som skriver ut ska inte ligga i klassen. Då kan vi behandla utskriften av presentationsdictionary och en
# temporär kopia på samma sätt. Det borde också bli lättare att lägga på graiskt lager sedan när det inte finns några terminalutskrifter i klassen.
# det kommer att kräva några nya funktioner - en som returnerar dictionaries, en som uppdaterar dictionaries

# TODO i logiken - ändra till bara en dictionary för utskrift och ändra fram och tillbaka i den.
# TODO jobba med logiken för import och export av användare och high_score
# - behöver bli en dictionary [key= level] och för varje level en lista med av listor med två värden [score, namn].
# tror den exporteras bäst till JSON.


class Memory():

    def __init__(self, size: int):
        '''Size must be an even number. '''  # fundera på var vi felhanterar even number.

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
        all_words = self.import_all_words_from_txt()
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

    def _create_record_of_all_postions(self):
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
        available_positions = self._create_record_of_all_postions()
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

    # ta bort denna behövs inte längre räcker med print board
    def print_presentation_board(self):
        '''Prints out the current presentation board, using the function _print_board '''
        self._print_board(self.presentation_board)

    def _print_board(self, board=dict):
        '''Prints out the inparameter - a dictionary as a memory board with spaces and the right column numbers'''
        for column in range(self.size):
            print(f"   {column+1}", end="")
        print("\n")
        for key in board:
            print(f"{key}", end="")
            for col in board[key]:
                print(f" {col}", end="")
            print("\n")

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
    '''Imports all scores from the file and puts it in a list of lists [gamer_name, score, level], if no file exists an empty list will be created for now.
    a file will be created at the end of the game, when the high_score list is updated'
    Returns: a dictionary all_scores'''
    all_scores = {}
    try:
        with open("all_scores.json", "r") as file:
            all_scores = json.load(file)
            return all_scores
    except FileNotFoundError:
        all_scores = {2: [], 4: [], 6: []}
        return all_scores

    # felhantera om listan är tom TODO lägg till level också i logiken


def print_high_scores(size: int, high_score_number: int, all_scores: dict):
    '''The high_score is  presented - the top players. If more than one player has the same score they will be 
    presented on the same row. 
    In parameters: Number of high scores to be presented, the size of the board and the dictionary with all results. 
    The key in the dictionary is size, and the results are stored in a list of lists [score, name]
    Development - comment on the players position using index after looping'''
    score_position = 1  # position on the score list
    index = 0  # position in the first list in all_scores[size]
    score_list_length = len(all_scores[size])

    if score_list_length > 1:
        all_scores[size] = sorted(
            # sorting the list from highest to lowest score
            all_scores[size], key=lambda x: x[0])
    print(f"\n***THE TOP PLAYERS FOR THE {size}x{size} board*** \n")
    print_scores = True
    while print_scores:
        if score_list_length < index+1:
            print_scores = False
        else:
            if score_position < 6:
                print(f"Rank {score_position}: ", end="")
                # prints score and name of the player
                print(
                    f"{all_scores[size][index][0]} rounds - {all_scores[size][index][1]}", end="")
                check_same_score = True
                while check_same_score:
                    if index == score_list_length-1:
                        print("\n")
                        check_same_score = False
                        print_scores = False
                    elif all_scores[size][index][0] != all_scores[size][index+1][0]:
                        index += 1
                        score_position += 1
                        print("\n")
                        check_same_score = False
                    else:
                        index += 1
                        print(f", {all_scores[size][index][1]} ", end="")

    # felhantera om listan är tom, hantera om flera har samma poäng TODO lägg till level också i logiken


def print_score_to_file(all_scores: dict):
    # TODO kolla hur i hanterar detta bäst ev göra en dictionary med list of lists. keys =size -ev bättre att köra json då.
    "Prints the high_score_file dictionary to the high_score.json file"

    with open("high_score.json", "w") as file:
        json.dump(all_scores, file)


def choose_difficulty_level() -> int:
    '''Prints the menue, lets the user choose level of difficulty.
    Returns size of the board, amount of rows and columns'''
    while True:
        print("At what level would you like to play?")
        print("[1] - Easy board 2x2 rows and columns")
        print("[2] - Medium board 4x4 rows and columns")
        print("[3] - Hard board 6x6 rows and columns")

        menue_choice = input("\nType in the number of your choice: ")
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
            print("you have made an unvalid choice - please try again")


def run_a_round_of_the_game(size: int) -> int:
    '''Creates an instance of the Memory class - player_memory_game and runs a round of the game whith the help of the functions in the Memory class.
    Returns the score'''
    player_memory_game = Memory(size)  # skapar instans av Memory
    rounds = 0
    position_1 = []
    position_2 = []
    while True:

        rounds += 1
        player_memory_game.print_presentation_board()
        print("Make your first move, choose tile column and row")
        position_1.append(input("Type the letter of the row: "))
        position_1.append(int(input("Type number of the column: "))-1)
        player_memory_game.update_presentation_board(position_1)
        player_memory_game.print_presentation_board()
        print("Make your second move, choose tile column and row")
        position_2.append(input("Type the letter of the row: "))
        position_2.append(int(input("Type number of the column: "))-1)
        player_memory_game.update_presentation_board(position_2)
        player_memory_game.print_presentation_board()
        matching_tiles = player_memory_game.its_a_match(position_1, position_2)
        if matching_tiles:
            # player_memory_game.update_presentation_board_if_a_match()
            game_over = player_memory_game.check_if_all_words_are_found()
            if game_over:
                return rounds
            else:

                del position_1[0:2]
                del position_2[0:2]
                print("\n Match, snyggt! - nästa drag")
        else:
            # resetts the position_1 and position_2 and deletes the values
            player_memory_game.reset_presentation_board(position_1, position_2)
            del position_1[0:2]
            del position_2[0:2]

            input("\n...nytt försök tryck RETUR\n")


def main():
    '''Main progam to the Memory game. Handles all interaction with the player - printouts and menues. 
    calls function for different tasks'''
    size = int  # size of a row or column of the board
    my_score = 0
    high_score_number = 5  # highscores to display
    gaming_name = str  # the players name
    # A list of a list with previous high scores [score, player_name] - imported from a separate file - high_score_memory.txt
    # high_score = import_score_from_file()

    print("\n**MEMORY GAME**\n")
    run = True
    leave = "go"
    while run:
        leave = input(
            "Press return to start a new game!!\n...would you like to leave the game type q + return")
        if leave == "q" or "Q":  # Den här funkar inte
            run = False

        gaming_name = input("Please type in your gaming name: ")
        size = choose_difficulty_level()  # prints the menue and returns menue choice
        print("\nGame on!!")
        my_score = run_a_round_of_the_game(size)
        print(f" Din score är: {my_score}")  # ta bort sen
        all_scores = import_score_from_file()
        all_scores[size].append([my_score, gaming_name])
        print(all_scores)
        print_high_scores(size, high_score_number, all_scores)
        print_score_to_file(all_scores)


if __name__ == "__main__":
    main()
