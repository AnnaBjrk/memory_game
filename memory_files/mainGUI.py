import tkinter
from tkinter.ttk import *
from tkinter import ttk
import random
from memory_logic import Memory
import json
from datetime import datetime

# Anna Björklund
# December 2024
# Course code DD100N HT24 Programmeringsteknik webbkurs (10118)# Namn

#  GUIprogram for the Memory class that creates a graphic interface for the game. The game has 3 views:
# In the first view the player chooses a gamer name and level of difficulty 2x2 (entry-widget), 4x4 and 6x6 memory cards (radio buttons).
# The second view shows the memory board with the memory cards. Each card is represented by a button widget - that changes when pressed and are disabled when the
# part of a match.
# The last view shows the result for the gamer -time and amount of rounds it took to complete the game. There is also a list of the top 5 gamers.
# Since many gamers could have the same amount of rounds the time it took to finnish the game - are taken into account.

# This program needs to create an object of the Memory class found in the memory_logic file, is also utilizes the same
# documents - high_score.json and memo_words.txt as the terminal version of the program ( found in the memory_logic file )


class VisualMemApp():
    '''This class handles the graphical interface for the Memory game. It consists of 3 views:
    1 - a starting board where the user types in name and level and then starts the game
    2 - the game board with memorycards that are turned to find matches
    3 - high score view showing the users score and the current high scores'''

    def __init__(self, root, turn=0, size=2, rounds=0):
        super().__init__()

        self.root = root

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

        # creates the startview with widgets
        self.create_start_view_widgets_and_board = self.create_start_widgets_and_board()
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

    def create_start_widgets_and_board(self):
        '''Creates the widgets and the board for the start view. 
        The gamer can choose gaming name. And the self.gamer_name will be set
        The game will also choose size of the board, setting self.size to 2, 4 or 6.
        When the button self.start_game_button is pressed the game starts - by activating the method create_memoryboard_view()'''

        self.headline_label = tkinter.Label(
            self.root, text="MEMORY", font=("Courier", 20, "bold"), fg="#5C2A2E")

        self.spacing_dots1 = tkinter.Label(
            self.root, text="............", font=("Courier", 12, "italic"), fg="#5C2A2E")
        self.instruction_label1 = tkinter.Label(
            self.root, text="Gamingnamn (byt om du vill)", font=("Courier", 12, "italic"), fg="#5C2A2E")
        self.instruction_label2 = tkinter.Label(
            self.root, text="Välj svårighetsgrad", font=("Courier", 12, "italic"), fg="#5C2A2E")

        name_text_default = tkinter.StringVar()
        name_text_default.set(self.gamer_name)
        self.gamer_name_entry = tkinter.Entry(
            self.root, relief='flat', textvariable=name_text_default)

        self.extra_space1 = tkinter.Label(
            self.root, text="   ",)

        self.submitname_button = tkinter.Button(
            self.root, text="Spara namn", font=("Courier", 14, "bold"), fg="#5C2A2E", command=self.update_gamer_name)

        self.var = tkinter.IntVar()
        self.size2_level_radio = tkinter.Radiobutton(
            self.root, text="Lätt - 2x2", fg="#5C2A2E", font=("Courier", 14, "bold"), variable=self.var, value=2, command=self.update_size_in_memory)

        self.size4_level_radio = tkinter.Radiobutton(
            self.root, text="Medel - 4x4", fg="#5C2A2E", font=("Courier", 14, "bold"), variable=self.var, value=4, command=self.update_size_in_memory)

        self.size6_level_radio = tkinter.Radiobutton(
            self.root, text="Svår - 6x6 ", fg="#5C2A2E", font=("Courier", 14, "bold"), variable=self.var, value=6, command=self.update_size_in_memory)

        self.extra_space2 = tkinter.Label(self.root, text=" ")

        self.start_game_button = tkinter.Button(
            self.root, text="Starta spelet", font=("Courier", 14, "bold"), fg="#5C2A2E", command=self.create_memoryboard_view)

        self.spacing_dots2 = tkinter.Label(self.root, text=".....................", font=(
            "Courier", 12, "italic"), fg="#5C2A2E")

        self.size2_level_radio.select()  # size 2 choosen by default
        self.headline_label.grid(row=0, column=1)
        self.spacing_dots1.grid(row=1, column=1)
        self.instruction_label1.grid(row=2, column=1)
        self.gamer_name_entry.grid(row=3, column=1)
        self.submitname_button.grid(row=4, column=1)
        self.extra_space1.grid(row=5, column=1)
        self.instruction_label2.grid(row=6, column=1)
        self.size2_level_radio.grid(row=7, column=0)
        self.size4_level_radio.grid(row=7, column=1)
        self.size6_level_radio.grid(row=7, column=2)
        self.extra_space2.grid(row=8, column=1)
        self.start_game_button.grid(row=9, column=1)
        self.spacing_dots2.grid(row=10, column=1)

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
        self.gamer_name = str(self.gamer_name_entry.get())
        if len(self.gamer_name) > 20:
            self.gamer_name = self.gamer_name[:20]

    def update_size_in_memory(self):
        '''Default size in a game is 2x2 memory cards, if the user chooses another level it
        is set with this method'''
        self.size = int(self.var.get())
        # sets the size in the Memory object to the choosen size
        self.player_memory_game.change_size(self.size)
        self.memory_card_button = self.create_memorycard_button_dictionary()
        self.button_position = self.create_button_position_dictionary()

    def create_memorycard_button_dictionary(self):
        '''Creates a dictionary containing the memory_card buttons for the game, returns that dictionary '''
        memorycard_button = {}
        # gets the list of all available positions from the Memory class
        all_postitions = self.player_memory_game.create_record_of_all_postions()

        for pos in range(len(all_postitions)):
            card_name = f"self.card{all_postitions[pos][0]}{
                all_postitions[pos][1]}"
            position = all_postitions[pos]
            text_on_card = self.player_memory_game.get_word_in_position(
                position)

            button = tkinter.Button(self.root, text=f"{text_on_card}", font=(
                "Courier", 12, "bold"), fg="#5C2A2E", padx=30, pady=50, command=lambda name=card_name: self.click_make_a_turn(name))

            memorycard_button[card_name] = button
        return memorycard_button

    def create_button_position_dictionary(self):
        '''creates a dictionary with card_name as key and position as a value'''
        button_postition = {}
        all_postitions = self.player_memory_game.create_record_of_all_postions()

        for pos in range(len(all_postitions)):
            card_name = f"self.card{all_postitions[pos][0]}{
                all_postitions[pos][1]}"
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

        # excludes and moves some widgets from the first start view
        self.headline_label.grid_forget()
        self.headline_label.grid(row=0, column=0)

        self.spacing_dots1.grid_forget()
        self.spacing_dots1.grid(row=1, column=0)

        self.instruction_label1.grid_forget()
        self.instruction_label2.grid_forget()

        self.gamer_name_entry.grid_forget()
        self.submitname_button.grid_forget()
        self.extra_space1.grid_forget()
        self.size2_level_radio.grid_forget()
        self.size4_level_radio.grid_forget()
        self.size6_level_radio.grid_forget()
        self.extra_space2.grid_forget()
        self.start_game_button.grid_forget()
        self.spacing_dots2.grid_forget()

        self.infomation_during_game = tkinter.Label(
            self.root, text=f"Nu kör vi!!", font=("Courier", 14, "bold"), fg="#5C2A2E")
        self.gamer_name_show = tkinter.Label(
            self.root, text=f"{self.gamer_name}", font=("Courier", 14, "bold"), fg="#5C2A2E")
        self.headline_rounds = tkinter.Label(
            self.root, text="Rundor", font=("Courier", 14, "bold"), fg="#5C2A2E")
        self.counts_number_of_rounds = tkinter.Label(
            self.root, text=f"{self.rounds}", font=("Courier", 20, "bold"), fg="#5C2A2E")

        self.close_cards_new_round = tkinter.Button(
            self.root, text="Ny runda", font=("Courier", 14, "bold"), fg="#5C2A2E", command=self.reset_unmatched_cards)

        # adds new widgets
        self.infomation_during_game.grid(row=3, column=0)
        self.gamer_name_show.grid(row=1, column=1)
        self.headline_rounds.grid(row=20, column=0)
        # row 20 makes it not affected by even the 6x6 board
        self.counts_number_of_rounds.grid(row=21, column=0)
        self.close_cards_new_round.grid(row=21, column=1)

        # adds the memory cards from the dictionary of memory buttons.
        row_nr = 12  # the row in the GUI where the first memorycards are placed
        all_postitions = self.player_memory_game.create_record_of_all_postions()

        for pos in range(len(all_postitions)):
            card_name = f"self.card{
                all_postitions[pos][0]}{all_postitions[pos][1]}"

            # if the position letter has canged in this loop we nee a new row.
            if all_postitions[pos][0] != all_postitions[pos-1][0]:
                row_nr += 1
            self.memory_card_button[card_name].grid(
                row=row_nr, column=all_postitions[pos][1], padx=5, pady=5)

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
            card_text = self.player_memory_game.get_word_in_position(
                position)

            self.memory_card_button[card_name].config(
                state=tkinter.DISABLED, text=card_text)

        elif self.turn == 2:
            self.reset = False
            self.button2 = card_name  # choosen button is found in the dictionary
            self.player_memory_game.update_presentation_board(position)
            card_text = self.player_memory_game.get_word_in_position(
                position)
            self.memory_card_button[card_name].config(
                state=tkinter.DISABLED, text=card_text)
            self.its_a_match = self.player_memory_game.its_a_match(
                self.button_position[self.button1], self.button_position[self.button2])

            if self.its_a_match:
                # returns true if the game should end
                self.all_moves_done = self.player_memory_game.check_if_all_words_are_found()
                self.update_infomation_during_game_label(
                    "En match!!!")

                # activates the highscore view and closes down the game board
                if self.all_moves_done:
                    self.stop_timer()
                    self.update_infomation_during_game_label(
                        f"Alla hittade!!")
                    # appends result and gamer_name to self.all_scores the dictionary with all previous scores
                    self.update_all_scores()
                    # takes out the button that creates a new turn
                    self.close_cards_new_round.grid_forget()
                    # pauses the game in 3 sek and then creates the high score view
                    self.root.after(
                        3000, self.create_high_score_widgets_and_view)

            else:
                self.update_infomation_during_game_label("Ingen träff...")

        elif self.turn > 2:  # if the gamer presses more than two memory cards in a round, this is true
            self.update_infomation_during_game_label(
                "Tryck på ny runda")

    def reset_unmatched_cards(self):
        ''' Resets unmatched cards in the game. Is used by the method "click_make_a_turn()'''

        # is True if the player have allready reset the game, or if the player has only turned one card.
        if self.reset == True:
            self.update_infomation_during_game_label(
                "Vänd två kort")
        else:
            self.reset = True
            if self.its_a_match == False:
                self.player_memory_game.reset_presentation_board(
                    self.button_position[self.button1], self.button_position[self.button2])
                card_text1 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button1])
                self.memory_card_button[self.button1].config(
                    state=tkinter.NORMAL, text=card_text1)
                card_text2 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button2])
                self.memory_card_button[self.button2].config(
                    state=tkinter.NORMAL, text=card_text2)
                self.turn = 0

            else:

                card_text1 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button1])
                self.memory_card_button[self.button1].config(
                    state=tkinter.DISABLED, text=card_text1)
                card_text2 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button2])
                self.memory_card_button[self.button2].config(
                    state=tkinter.DISABLED, text=card_text2)

                self.its_a_match = False
                self.Button1 = None
                self.Button2 = None
                self.turn = 0

    def update_runda(self):
        '''Updates the lable that shows how many rounds have been played'''
        self.counts_number_of_rounds.config(text=f"{self.rounds}")

    def update_infomation_during_game_label(self, new_instruction: str):
        '''Updates the lable that gives the player information and instructions during the game'''
        self.infomation_during_game.config(text=f"{new_instruction}")

    def update_all_scores(self):
        '''ads the new result to the dictionary self.all_scores'''
        size_ap = self.size
        round_ap = self.rounds
        gamer_ap = self.gamer_name
        min_ap = self.time[0]
        sec_ap = self.time[1]
        self.all_scores[str(size_ap)].append(
            [round_ap, gamer_ap, min_ap, sec_ap])

    def sorts_score(self):
        '''Sorts the self.all_scores dictionary from highest to lowest result. Least rounds and shortest finnish time are at the top. Used before printing out the results'''

        score_list_length = len(self.all_scores[str(self.size)])

        if score_list_length > 1:
            # sorting the list from highest to lowest sec
            self.all_scores[str(self.size)] = sorted(
                self.all_scores[str(self.size)], key=lambda x: x[3])
            # sorting the list from highest to lowest min
            self.all_scores[str(self.size)] = sorted(
                self.all_scores[str(self.size)], key=lambda x: x[2])
            # sorting the list from highest to lowest score
            self.all_scores[str(self.size)] = sorted(
                self.all_scores[str(self.size)], key=lambda x: x[0])

    def create_high_score_labels(self):
        '''Creates a dictionary containing the high score labels for the game, returns that dictionary, if the player is the first
            gamer to set a high score the dictionary will only contain the current gamers name and result '''
        high_scores_labels = {}
        # gets the list of all available positions from the Memory class
        # all_postitions = self.player_memory_game.create_record_of_all_postions()
        if len(self.all_scores[str(self.size)]) <= 5:
            scores_to_print = len(self.all_scores[str(self.size)])
        else:
            scores_to_print = 5

        for pos in range(scores_to_print):
            label_name = f"gamer{pos}"
            label_text = f"{self.all_scores[str(self.size)][pos][1]} : {self.all_scores[str(self.size)][pos][0]} rundor : tid {
                self.all_scores[str(self.size)][pos][2]} min, {self.all_scores[str(self.size)][pos][3]} sek "
            label = tkinter.Label(self.root, name=label_name, text=label_text, font=(
                "Courier", 12, "bold"), fg="#5C2A2E")

            high_scores_labels[label_name] = label
        return high_scores_labels

    def create_high_score_widgets_and_view(self):
        '''Creates the last view on the board - displaying the high score and the players final result, rounds and time
        It also activates the methods managing the scores - the one that sorts the score and the one that prints the score to the high_score.json file'''

        # sorted in order by this method
        self.sorts_score()
        self.print_score_to_file()
        self.update_infomation_during_game_label(
            f"Klarade på {self.time[0]} min, {self.time[1]} sek")

        # takes out all memory_cards from the board
        for key in self.memory_card_button:
            self.memory_card_button[key].grid_forget()

        # adjusts some labels
        self.infomation_during_game.grid(row=5, column=0)
        self.headline_rounds.grid(row=4, column=0)
        self.counts_number_of_rounds.grid(row=3, column=0)
        self.gamer_name_show.grid(row=15, column=0)

        # add new labels
        self.spacing_dots3 = tkinter.Label(
            self.root, text="............", font=("Courier", 12, "italic"), fg="#5C2A2E")
        self.spacing_dots4 = tkinter.Label(
            self.root, text="............", font=("Courier", 12, "italic"), fg="#5C2A2E")
        headline_text = f" ... TOPP-RESULTAT {self.size}x{self.size} ... "
        self.high_score_headline = tkinter.Label(
            self.root, text=headline_text, font=("Courier", 16, "bold"), fg="#5C2A2E")

        self.spacing_dots3.grid(row=6, column=0)
        self.high_score_headline.grid(row=7, column=0)
        self.spacing_dots4.grid(row=14, column=0)

        self.high_scores_labels = self.create_high_score_labels()

        for pos in range(5):
            label_name = f"gamer{pos}"
            row_nr = 8 + pos
            self.high_scores_labels[label_name].grid(row=row_nr, column=0)

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

    def _import_score_from_file(self) -> dict:
        '''Imports all scores from the file high_score.json and puts it in a dictionary with game level as keys {level: [gamer_name, score]}, if no file exists an empty list will be created for now.
        a file will be created at the end of the game, when the high_score list is updated'
        Returns: a dictionary all_scores'''
        all_scores1 = {}
        try:
            with open("high_score.json", "r") as file:
                all_scores1 = json.load(file)
                return all_scores1
        except (FileNotFoundError, json.JSONDecodeError):
            all_scores1 = {"2": [], "4": [], "6": []}
            return all_scores1

    def print_score_to_file(self):
        '''Prints the self.all_scores file dictionary to the high_score.json file '''
        to_file = self.all_scores
        with open("high_score.json", "w") as file:
            json.dump(to_file, file)


if __name__ == "__main__":

    root = tkinter.Tk()
    start_game = VisualMemApp(root)
    root.mainloop()
