from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QRadioButton, 
                               QPushButton, QLineEdit, QGridLayout, QWidget, QVBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import random
from memory_logic import Memory
import json
from datetime import datetime
import sys

# Anna Björklund
# December 2024
# Course code DD100N HT24 Programmeringsteknik webbkurs (10118)

#  GUIprogram for the Memory class that creates a graphic interface for the game. The game has 3 views:
# In the first view the player chooses a gamer name and level of difficulty 2x2 (entry-widget), 4x4 and 6x6 memory cards (radio buttons).
# The second view shows the memory board with the memory cards. Each card is represented by a button widget - that changes when pressed and are disabled when the
# part of a match.
# The last view shows the result for the gamer -time and amount of rounds it took to complete the game. There is also a list of the top 5 gamers.
# Since many gamers could have the same amount of rounds the time it took to finnish the game - are taken into account.

# This program needs to create an object of the Memory class found in the memory_logic file, is also utilizes the same
# documents - high_score.json and memo_words.txt as the terminal version of the program ( found in the memory_logic file )


class VisualMemApp(QMainWindow):
    '''This class handles the graphical interface for the Memory game. It consists of 3 views:
    1 - a starting board where the user types in name and level and then starts the game
    2 - the game board with memorycards that are turned to find matches
    3 - high score view showing the users score and the current high scores'''

    def __init__(self, turn=0, size=2, rounds=0):
        super().__init__()

        # int keeps track if the move is the first (1) or the second move (2)
        self.turn = turn
        # sets the size of the game board, size is the length or width, default is 2x2
        self.size = size
        self.rounds = rounds  # int keeps track of the rounds the player has
        # true if a reset has been done will be set to false when the next round starts, prevents a reset twice.
        self.reset = False

        # the dictionary that keeps track of game scores, key=size, [rounds, gaming_name, minutes, seconds, is set after the game ends]
        self.all_scores = None
        # the gamers name, is used in the communication during the game and also when registering high score
        self.gamer_name = self.create_default_gamer_name()
        # creates an instance of the Memory class that is used for the game logic, default is size 2x2.
        self.player_memory_game = Memory(self.size)
        # instance variable used to store info about the first choosen cards in a game round
        self.button1 = None
        # instance variable used to store info about the second choosen cards in a game round
        self.button2 = None
        self.all_moves_done = False  # will be set to True when all words are found
        self.its_a_match = False  # sets to True if there is a match sets to False next round

        # Setup the main window
        self.setWindowTitle("Memory Game")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create layout
        self.grid_layout = QGridLayout(self.central_widget)

        # creates the startview with widgets
        self.create_start_view_widgets_and_board()
        # creates a dictionary with the memorycards - buttons
        self.memory_card_button = self.create_memorycard_button_dictionary()
        # creates a dictionary with card_name and their positions
        self.button_position = self.create_button_position_dictionary()
        # a dictionary that stores all high score labels, for the final view - displaying highscore
        self.high_scores_labels = {}
        # creates a dictionary of previous scores from a file. If no scores an empty dictionary is created
        self.all_scores = self._import_score_from_file()
        self.start_time = None  # stores the time when the game starts
        self.end_time = None  # stores the time when the game ends
        self.player_game_time = None  # calculated total time for the gamer
        # list with time in [minutes and sec] to be used in print outs and storing the results
        self.time = None

    def create_start_view_widgets_and_board(self):
        '''Creates the widgets and the board for the start view. 
        The gamer can choose gaming name. And the self.gamer_name will be set
        The game will also choose size of the board, setting self.size to 2, 4 or 6.
        When the button self.start_game_button is pressed the game starts - by activating the method create_memoryboard_view()'''

        # Define a bold font
        headline_font = QFont("Courier", 20)
        headline_font.setBold(True)
        
        normal_font = QFont("Courier", 12)
        normal_font.setItalic(True)
        
        button_font = QFont("Courier", 14)
        button_font.setBold(True)

        # Create widgets
        self.headline_label = QLabel("MEMORY")
        self.headline_label.setFont(headline_font)
        self.headline_label.setStyleSheet("color: #5C2A2E")

        self.spacing_dots1 = QLabel("............")
        self.spacing_dots1.setFont(normal_font)
        self.spacing_dots1.setStyleSheet("color: #5C2A2E")
        
        self.instruction_label1 = QLabel("Gamingnamn (byt om du vill)")
        self.instruction_label1.setFont(normal_font)
        self.instruction_label1.setStyleSheet("color: #5C2A2E")
        
        self.instruction_label2 = QLabel("Välj svårighetsgrad")
        self.instruction_label2.setFont(normal_font)
        self.instruction_label2.setStyleSheet("color: #5C2A2E")

        self.gamer_name_entry = QLineEdit(self.gamer_name)
        
        self.extra_space1 = QLabel("   ")

        self.submitname_button = QPushButton("Spara namn")
        self.submitname_button.setFont(button_font)
        self.submitname_button.setStyleSheet("color: #5C2A2E")
        self.submitname_button.clicked.connect(self.update_gamer_name)

        # Radio buttons for difficulty
        self.size2_level_radio = QRadioButton("Lätt - 2x2")
        self.size2_level_radio.setFont(button_font)
        self.size2_level_radio.setStyleSheet("color: #5C2A2E")
        self.size2_level_radio.setChecked(True)
        self.size2_level_radio.toggled.connect(lambda: self.update_size_in_memory(2))
        
        self.size4_level_radio = QRadioButton("Medel - 4x4")
        self.size4_level_radio.setFont(button_font)
        self.size4_level_radio.setStyleSheet("color: #5C2A2E")
        self.size4_level_radio.toggled.connect(lambda: self.update_size_in_memory(4))
        
        self.size6_level_radio = QRadioButton("Svår - 6x6")
        self.size6_level_radio.setFont(button_font)
        self.size6_level_radio.setStyleSheet("color: #5C2A2E")
        self.size6_level_radio.toggled.connect(lambda: self.update_size_in_memory(6))

        self.extra_space2 = QLabel(" ")

        self.start_game_button = QPushButton("Starta spelet")
        self.start_game_button.setFont(button_font)
        self.start_game_button.setStyleSheet("color: #5C2A2E")
        self.start_game_button.clicked.connect(self.create_memoryboard_view)

        self.spacing_dots2 = QLabel(".....................")
        self.spacing_dots2.setFont(normal_font)
        self.spacing_dots2.setStyleSheet("color: #5C2A2E")

        # Add widgets to layout
        self.grid_layout.addWidget(self.headline_label, 0, 1)
        self.grid_layout.addWidget(self.spacing_dots1, 1, 1)
        self.grid_layout.addWidget(self.instruction_label1, 2, 1)
        self.grid_layout.addWidget(self.gamer_name_entry, 3, 1)
        self.grid_layout.addWidget(self.submitname_button, 4, 1)
        self.grid_layout.addWidget(self.extra_space1, 5, 1)
        self.grid_layout.addWidget(self.instruction_label2, 6, 1)
        self.grid_layout.addWidget(self.size2_level_radio, 7, 0)
        self.grid_layout.addWidget(self.size4_level_radio, 7, 1)
        self.grid_layout.addWidget(self.size6_level_radio, 7, 2)
        self.grid_layout.addWidget(self.extra_space2, 8, 1)
        self.grid_layout.addWidget(self.start_game_button, 9, 1)
        self.grid_layout.addWidget(self.spacing_dots2, 10, 1)

    def create_default_gamer_name(self):
        '''Creates a default gamer name that will be used if the user has not typed in a name'''
        words_for_name = ["star", "gamer", "guy", "wizard",
                          "alien", "noob", "pro", "smarty", "winner", "bok", "chair", "radio", "baby", "boy", "girl", "steam", "racer", "god", "kitten", "puppy"]
        name_part1 = random.choice(words_for_name)
        name_part0 = random.choice(words_for_name)

        name_part2 = random.randint(100, 999)
        gamer_name = f"{name_part0}_{name_part1}_{name_part2}"
        return gamer_name

    def update_gamer_name(self):
        '''Updates the gamer name if the user chooses another name'''
        self.gamer_name = self.gamer_name_entry.text()
        if len(self.gamer_name) > 20:
            self.gamer_name = self.gamer_name[:20]
            self.gamer_name_entry.setText(self.gamer_name)

    def update_size_in_memory(self, size):
        '''Default size in a game is 2x2 memory cards, if the user chooses another level it
        is set with this method'''
        self.size = size
        # sets the size in the Memory object to the choosen size
        self.player_memory_game.change_size(self.size)
        self.memory_card_button = self.create_memorycard_button_dictionary()
        self.button_position = self.create_button_position_dictionary()

    def create_memorycard_button_dictionary(self):
        '''Creates a dictionary containing the memory_card buttons for the game, returns that dictionary '''
        memorycard_button = {}
        # gets the list of all available positions from the Memory class
        all_postitions = self.player_memory_game.create_record_of_all_postions()

        button_font = QFont("Courier", 12)
        button_font.setBold(True)

        for pos in range(len(all_postitions)):
            card_name = f"self.card{all_postitions[pos][0]}{all_postitions[pos][1]}"
            position = all_postitions[pos]
            text_on_card = self.player_memory_game.get_word_in_position(position)

            button = QPushButton(text_on_card)
            button.setFont(button_font)
            button.setStyleSheet("color: #5C2A2E")
            button.setMinimumSize(100, 120)  # Approximate equivalent to padx=30, pady=50
            button.clicked.connect(lambda checked=False, name=card_name: self.click_make_a_turn(name))

            memorycard_button[card_name] = button
        return memorycard_button

    def create_button_position_dictionary(self):
        '''creates a dictionary with card_name as key and position as a value'''
        button_postition = {}
        all_postitions = self.player_memory_game.create_record_of_all_postions()

        for pos in range(len(all_postitions)):
            card_name = f"self.card{all_postitions[pos][0]}{all_postitions[pos][1]}"
            position = all_postitions[pos]
            button_postition[card_name] = position
        return button_postition

    def create_memoryboard_view(self):
        '''Creates the second view with the memory game, reuses some label-widgets from the first game, takes out most of them
        and adds some new and the memory cards from the instance attribute self.memory_card_button, a dictionary. 
        The cards are choosen two at the time and the logic is run by the click_make_a_turn() function and the reset_unmatched_cards() function.
        This method also starts the timer.
        '''
        self.start_timer()

        # Clear the layout of all widgets
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Define fonts
        headline_font = QFont("Courier", 20)
        headline_font.setBold(True)
        
        normal_font = QFont("Courier", 14)
        normal_font.setBold(True)

        # Recreate needed widgets
        self.headline_label = QLabel("MEMORY")
        self.headline_label.setFont(headline_font)
        self.headline_label.setStyleSheet("color: #5C2A2E")
        
        self.spacing_dots1 = QLabel("............")
        self.spacing_dots1.setFont(QFont("Courier", 12))
        self.spacing_dots1.setStyleSheet("color: #5C2A2E")

        # Create new widgets for game view
        self.infomation_during_game = QLabel("Nu kör vi!!")
        self.infomation_during_game.setFont(normal_font)
        self.infomation_during_game.setStyleSheet("color: #5C2A2E")
        
        self.gamer_name_show = QLabel(self.gamer_name)
        self.gamer_name_show.setFont(normal_font)
        self.gamer_name_show.setStyleSheet("color: #5C2A2E")
        
        self.headline_rounds = QLabel("Rundor")
        self.headline_rounds.setFont(normal_font)
        self.headline_rounds.setStyleSheet("color: #5C2A2E")
        
        self.counts_number_of_rounds = QLabel(str(self.rounds))
        self.counts_number_of_rounds.setFont(headline_font)
        self.counts_number_of_rounds.setStyleSheet("color: #5C2A2E")
        
        self.close_cards_new_round = QPushButton("Ny runda")
        self.close_cards_new_round.setFont(normal_font)
        self.close_cards_new_round.setStyleSheet("color: #5C2A2E")
        self.close_cards_new_round.clicked.connect(self.reset_unmatched_cards)

        # Add widgets to layout
        self.grid_layout.addWidget(self.headline_label, 0, 0)
        self.grid_layout.addWidget(self.spacing_dots1, 1, 0)
        self.grid_layout.addWidget(self.infomation_during_game, 3, 0)
        self.grid_layout.addWidget(self.gamer_name_show, 1, 1)
        self.grid_layout.addWidget(self.headline_rounds, 20, 0)
        self.grid_layout.addWidget(self.counts_number_of_rounds, 21, 0)
        self.grid_layout.addWidget(self.close_cards_new_round, 21, 1)

        # Add memory cards to the layout
        row_nr = 12  # the row in the GUI where the first memorycards are placed
        all_postitions = self.player_memory_game.create_record_of_all_postions()

        for pos in range(len(all_postitions)):
            card_name = f"self.card{all_postitions[pos][0]}{all_postitions[pos][1]}"

            # if the position letter has canged in this loop we need a new row.
            if pos > 0 and all_postitions[pos][0] != all_postitions[pos-1][0]:
                row_nr += 1
                
            self.grid_layout.addWidget(self.memory_card_button[card_name], 
                                      row_nr, all_postitions[pos][1])

    def click_make_a_turn(self, card_name):
        '''This method is activated by a button click in the memoryboard, the instance parameter card_name is set by the button.
        it handles all logic and communicates with the Memoryclass for game logic. When there is a match, if all words has been found and the game will end.
        a label widget update_infomation_during_game_label - gives the player information during the game.
        When the game ends the timer is stoped and the final game board is created by the create_high_score_widgets_and_view() method. 
        '''

        # choosen position is found in the dictionary by using the key = card_name
        position = self.button_position[card_name]

        self.turn += 1

        if self.turn == 1:
            self.rounds += 1
            self.update_runda()
            self.update_infomation_during_game_label("Välj nästa kort")

            self.button1 = card_name  # choosen button is found in the dictionary

            self.player_memory_game.update_presentation_board(position)
            card_text = self.player_memory_game.get_word_in_position(position)

            self.memory_card_button[card_name].setEnabled(False)
            self.memory_card_button[card_name].setText(card_text)

        elif self.turn == 2:
            self.reset = False
            self.button2 = card_name  # choosen button is found in the dictionary
            self.player_memory_game.update_presentation_board(position)
            card_text = self.player_memory_game.get_word_in_position(position)
            
            self.memory_card_button[card_name].setEnabled(False)
            self.memory_card_button[card_name].setText(card_text)
            
            self.its_a_match = self.player_memory_game.its_a_match(
                self.button_position[self.button1], self.button_position[self.button2])

            if self.its_a_match:
                # returns true if the game should end
                self.all_moves_done = self.player_memory_game.check_if_all_words_are_found()
                self.update_infomation_during_game_label("En match!!!")

                # activates the highscore view and closes down the game board
                if self.all_moves_done:
                    self.stop_timer()
                    self.update_infomation_during_game_label(f"Alla hittade!!")
                    # appends result and gamer_name to self.all_scores the dictionary with all previous scores
                    self.update_all_scores()
                    # takes out the button that creates a new turn
                    self.close_cards_new_round.setParent(None)
                    # pauses the game in 3 sek and then creates the high score view
                    QApplication.processEvents()
                    QTimer.singleShot(3000, self.create_high_score_widgets_and_view)

            else:
                self.update_infomation_during_game_label("Ingen träff...")

        elif self.turn > 2:  # if the gamer presses more than two memory cards in a round, this is true
            self.update_infomation_during_game_label("Tryck på ny runda")

    # The rest of the methods would be converted similarly...
    # I'll include a few more key methods and then show how to run the app

    def reset_unmatched_cards(self):
        ''' Resets unmatched cards in the game. Is used by the method "click_make_a_turn()'''

        # is True if the player have allready reset the game, or if the player has only turned one card.
        if self.reset == True:
            self.update_infomation_during_game_label("Vänd två kort")
        else:
            self.reset = True
            if self.its_a_match == False:
                self.player_memory_game.reset_presentation_board(
                    self.button_position[self.button1], self.button_position[self.button2])
                
                card_text1 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button1])
                self.memory_card_button[self.button1].setEnabled(True)
                self.memory_card_button[self.button1].setText(card_text1)
                
                card_text2 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button2])
                self.memory_card_button[self.button2].setEnabled(True) 
                self.memory_card_button[self.button2].setText(card_text2)
                
                self.turn = 0

            else:
                card_text1 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button1])
                self.memory_card_button[self.button1].setEnabled(False)
                self.memory_card_button[self.button1].setText(card_text1)
                
                card_text2 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button2])
                self.memory_card_button[self.button2].setEnabled(False)
                self.memory_card_button[self.button2].setText(card_text2)

                self.its_a_match = False
                self.Button1 = None
                self.Button2 = None
                self.turn = 0

    def update_runda(self):
        '''Updates the lable that shows how many rounds have been played'''
        self.counts_number_of_rounds.setText(str(self.rounds))

    def update_infomation_during_game_label(self, new_instruction: str):
        '''Updates the lable that gives the player information and instructions during the game'''
        self.infomation_during_game.setText(new_instruction)

    # Add the rest of the methods (update_all_scores, sorts_score, etc.)...

    # Include the timer methods
    def start_timer(self):
        '''Registers the time when the game starts, when the memory board is creates and updates that instance variable'''
        current_time = datetime.now()
        self.start_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')

    def stop_timer(self):
        '''Registers when the game ends, calculates and returns the time it took as a list
        [minutes, sec]'''
        current_time = datetime.now()
        self.stop_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')

        dt1 = datetime.strptime(self.stop_time, '%Y-%m-%d %H:%M:%S.%f')
        dt2 = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S.%f')

        time_diff = abs(dt1-dt2)
        minutes = (time_diff.seconds % 3600) // 60,
        seconds = time_diff.seconds % 60,
        microseconds = time_diff.microseconds
        decimal_sec = float(f"{seconds[0]}.{microseconds}")
        shorter_sec = round(decimal_sec, 2)
        min_plain = minutes[0]
        self.time = [min_plain, shorter_sec]


# Add missing imports for QTimer
from PySide6.QtCore import QTimer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VisualMemApp()
    window.show()
    sys.exit(app.exec())
