# Kodskellett
# Anna Björklund, 2024-11-21
# Kurskod: DD100N HT24 (10118)

# P-uppgift Memory spel

# Data strukturer:

# Filer
# Programmet består av - filerna:
# *** memory_main: i den finns en main funktion, några extra funktioner samt en klass Memory, med tillhörande funktioner.
# *** memo_words.txt en lista av ord på tre bokstäver
# *** all_scores - en JSON fil som lagrar spelarens namn och score, för spelets tre svårighetsnivårer,
# 2x2, 4x4 eller 6x6 brickor. Formatet för detta är en dictionary där storleken på board är key och variabeln
# är en lista med en lista av poäng och namn.:all_scores = {size: [[score1, name1], [score2, name2]] …. osv}

# Spelets uppdelning
# *** Memory klassen
# Memory klassen sköter själva spelet, instans-attributen är två dictionaries med samma struktur.
# De håller reda på vilka ord som finns gömda var och vilka brickor som ska visas.

# ***Exempel på spelplan och koppling till dictionary

#    1   2         1   2
# A --- ---     A hej top
# B --- ---     B top hej

# Exempel dessa spelplaner ovan -  har size 2 eftersom de består av två rader och kolumner.
# första versionen av dictionaryn för presentation_board (den vänstra)blir:
# {A:[“---”, ‘’---’], B:[“---”, ‘’---’]}
# och hidden_word_dictionary (som från början har all info för att visa den högra) ser ut så här. {A:[“fin”, ‘’hej], B:[“fin”, ‘’hej’]}
# Dessa två är ryggraden i hela spelet. presentation_board uppdateras under spelets gång, hidden_word_dictionary är samma hela tiden.

# Flera funktionerna i klassenr är interna och används bla vid instansieringen av attributen.
# Närmare förklaringar till funktioner, instansvariabler och attribut finns vid varje funktion.

# *** Main
# Main - kallar på en funktion def run_a_round_of_the_game. det är den som hanterar en hel spelrunda
# och i den skapas en instans av Memory. Main håller också reda på spelets övergripande logik,och callar på
# funktioner som hanterar som  import av spelarna poäng, presentation av highscore och uppdatering
# av filen som lagrar high_score.


import random
import json


class Memory():

    def __init__(self, size: int):
        # size of one row or column on the game board
        self.size = size
        # dictionary with information to be printed out to create the game board, Key is a letter and the positions are stored in a list. Is set by a class function
        self.presentation_board = self._create_first_versions_of_game_board()
        # a dictionary with all the chosen words on the right position in each row. Keys are the letters. Is set by a class function
        self.hidden_words_board = self._create_hidden_words_board()

    def _import_all_words_from_txt(self) -> list:
        	'''Imports all words from the memo_words.txt file.
        	Returns a list with all words'''
            # import all words from file
            # return list of all words
        pass

    def _pick_random_words(self) -> list:
        '''Picks random words from a list of words.Takes input from the instance variable size - that determines the size of the board.
            Returns: a list with size*size/2 numbers of unique words, that will populate the board
            calls the function import_all_words_from_txt(self) and creates a list of words'''
            #uses a random function to pick words from the word list and 
            #populates a new list with the exact number of needed words
            #double checks each time that the word does not already exist in the new list.'''
        pass



    def _create_record_of_all_postions(self):
        '''Returns a list of positions = [letter, index] with all positions on the board with SizeXSize numbers of rows and columns. 
        The list is used when deciding position for the chosen words in the create_hidden_words_board() function'''
        # Takes input from the instance variable size - that determines the size of the board.
        pass  

    def _create_hidden_words_board(self):
        '''Creates a dictionary with all chosen words, an instance attribute. The structure of the dictionary makes it possible to se the location of each word. The dictionary is mirroring the dictionary that will be used for printing out the board, also an instance attribute.
        Keys are the letters naming each row. Each row is a list where the index corresponds to the columns in the board column = index+1'''
        #Returns the dictionary - hidden_words_board 
        #creates a board with the self._create_first_versions_of_game_board() function
        #populates the board with words from a list created by the _pick_random_words(self) function
        #the positions are chosen and put in the hidden_words_board using a random function and the list of all available positions created by the_create_record_of_all_postions(self) function.
        #When a position has been chosen that entry in the positions list is deleted, so it can not be chosen again
        pass

    def _create_first_versions_of_game_board(self):
        '''Returns a dictionary with all the info needed to print out a board in the terminal. Keys are the letters naming each row. Each row is a list where the index corresponds to the columns in the board column = index+1. Is used to create the instance attributes: create_hidden_words_board() and presentation_board.
        Takes input from the instance variable size - that determines the size of the board.'''
        #Create dictionary keys are letters A, B, C…, the positions will get the value “---” for a start
        #Returns dictionary
        pass
      


    def print_board(self, board=dict):
        '''Prints out the presentation_board - a dictionary as a memory board in the terminal using spaces and the right column numbers'''
        #Print out the board in the terminal'''
        pass

    def update_presentation_board(self, position: list):
        '''The input variable is the position a list of two values [row/letter, column/index] (not the number displayed when printed)
        	Updates the chosen position in .presentation_board with the word that is registered on that position in hidden_words_board'''
        #set a word as a value on the chosen position
        pass

    def reset_presentation_board(self, position_1: list, position_2=list):
        '''Resets the presentation board after an unsuccessful round, '''
            # word is deleted from the presentation_board and the default “---” is displayed again
        pass

    def its_a_match(self, position_1, position_2) -> bool:
        '''Checks if the two chosen tiles are matching
        	Returns True if that is the case -  False if they doesn't match'''
        # checks if two tiles are missing by comparing the values from their positions
        pass

    def check_if_all_words_are_found(self) -> bool:
        '''Checks if there are any more words to look for.
        	Returns true if the game should end Fals if it shouldnt'''
        # iterates through the dictionary for the entry “---” if its found there are more tiles to match
        pass

#—-----------------------Memory class ends—---------------------------------

#Extra functions:


def import_score_from_file() -> dict:
 '''Imports all scores from the file and puts it in a list of lists [gamer_name, score, level], if no file exists an empty list will be created for now. a file will be created at the end of the game, when the high_score list is updated'
    	Returns: a dictionary all_scores, Here a JSON format will be used since its easer to import and export dictionaries to them.'''
    # Imports the dictionary from the JSON file
    # If no JSON file exists an empty dictionary will be created
    pass


def print_high_scores(size: int, high_score_number: int, all_scores: dict):
    '''The high_score of the top players  are  printed out in the terminal. If more than one player has the same score they will be 
    	presented on the same row. 
    	In parameters: Ranks  to be presented, the size of the board and the dictionary with all results. 
    	The key in the dictionary all_score - is size(the size of the board), and the results are stored in a list of lists [score, name]'''
	
    # sorts the list where the highscores should be printed from, if there is only one entry the list will not be sorted
    # stops printing if there are no more values
    # prints out rank 1 to  a chosen number score_number - in this program it will be 5. 
    # if several players has the same rank they will be printed out on the same row.
	pass



def print_score_to_file(all_scores: dict):
    "Prints the high_score_file dictionary to the high_score.json file"
    # print the current all_scores dictionary to the JSON file, replaces the old data
    pass



def choose_difficulty_level() -> int:
    '''Prints the menu, lets the user choose the level of difficulty.
    Returns size of the board, amount of rows and columns
        Easy board 2x2 rows and columns")
        Medium board 4x4 rows and columns")
        Hard board 6x6 rows and columns")'''

    # prints out a menu t
    # takes input for the size chosen 
    # returns size
    pass


def run_a_round_of_the_game(size: int) -> int:
    '''Creates an instance of the Memory class - player_memory_game and runs a round of the game with the help of the functions in the Memory class.
    Returns the score'''
	
    # Creates an instance of the Memory class, player_memory_game
    # Keeps track of the score =  amount of rounds the player needs to end the game
    # Asks the user for input on what tiles to turn.
    # Gives the user a new turn - when there still are tiles that has not found a match
    # Ads the words of for the chosen tiles to the board presented in the terminal presentation_board using the function update_presentation_board()
    # Prints the current status of the board to the terminal using print_presentation_board()
    # Checks if the chosen words are a match with the function its_a_match()
    # If there is a match checks if all words have been chosen, and the game is over -  with the function  game.check_if_all_words_are_found()
    # If there are more tiles to turn, the game continues with the matching word tiles now visible.
    # If there is not a match after a move the presentation_board dictionary will be reset so that the choosen words from the round no longer is showing - that is done with the function reset_presentation_board()
    # when all tiles have been found and the round has ended the score will be returned
	pass
 


def main():
   	'''Main program to the Memory game. Handles the over all interaction with the player and over all logic for the game.
Calls the run_a_round_of_the_game function to run a round of a game, asks for player input. 
Imports, presents and exports user scores with the help of dedicated functions.'''
	
    # Calls the run_a_round_of_the_game() function to run a game.
    # Greets the user wellcome to the game
    # Asks for the players name
    # Asks for difficulty level with the function choose_difficulty_level() 
    # Starts a round by calling the run_a_round_of_the_game() function - in this function an instance of Memory is created
    # Imports high_score from JSON file using import_score_from_file()
    # Prints highscore using the print_high_scores() function
    # Saves highscore to JSON file using the print_score_to_file(all_scores) function
    pass

if __name__ == "__main__":
    main()
