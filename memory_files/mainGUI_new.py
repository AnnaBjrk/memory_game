import wx
import random
from memory_logic import Memory
import json
from datetime import datetime

# Konvertering av VisualMemApp från Tkinter till wxPython
# Baserat på original av Anna Björklund, December 2024


class VisualMemApp(wx.Frame):
    '''This class handles the graphical interface for the Memory game. It consists of 3 views:
    1 - a starting board where the user types in name and level and then starts the game
    2 - the game board with memorycards that are turned to find matches
    3 - high score view showing the users score and the current high scores'''

    def __init__(self, parent, turn=0, size=2, rounds=0):
        super().__init__(parent, title="Memory", size=(800, 600))

        # Skapa huvudpanel och sätt layout
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

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
        self.create_start_widgets_and_board()
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

        # Sätt layouten och centrera fönstret
        self.panel.SetSizer(self.main_sizer)
        self.Centre()
        self.Show(True)

    def create_start_widgets_and_board(self):
        '''Creates the widgets and the board for the start view. 
        The gamer can choose gaming name. And the self.gamer_name will be set
        The game will also choose size of the board, setting self.size to 2, 4 or 6.
        When the button self.start_game_button is pressed the game starts - by activating the method create_memoryboard_view()'''

        start_grid = wx.GridBagSizer(10, 10)

        # Skapa widgets
        self.headline_label = wx.StaticText(
            self.panel, label="MEMORY", style=wx.ALIGN_CENTER)
        font = self.headline_label.GetFont()
        font.SetPointSize(20)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.headline_label.SetFont(font)
        self.headline_label.SetForegroundColour("#5C2A2E")

        self.spacing_dots1 = wx.StaticText(self.panel, label="............")
        font_dots = self.spacing_dots1.GetFont()
        font_dots.SetPointSize(12)
        font_dots.SetStyle(wx.FONTSTYLE_ITALIC)
        self.spacing_dots1.SetFont(font_dots)
        self.spacing_dots1.SetForegroundColour("#5C2A2E")

        self.instruction_label1 = wx.StaticText(
            self.panel, label="Gamingnamn (byt om du vill)")
        self.instruction_label1.SetFont(font_dots)
        self.instruction_label1.SetForegroundColour("#5C2A2E")

        self.instruction_label2 = wx.StaticText(
            self.panel, label="Välj svårighetsgrad")
        self.instruction_label2.SetFont(font_dots)
        self.instruction_label2.SetForegroundColour("#5C2A2E")

        self.gamer_name_entry = wx.TextCtrl(self.panel, value=self.gamer_name)

        self.submitname_button = wx.Button(self.panel, label="Spara namn")
        btn_font = self.submitname_button.GetFont()
        btn_font.SetPointSize(14)
        btn_font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.submitname_button.SetFont(btn_font)
        self.submitname_button.SetForegroundColour("#5C2A2E")
        self.submitname_button.Bind(wx.EVT_BUTTON, self.update_gamer_name)

        # Radio knappar för svårighetsgrad
        self.level_radio = wx.RadioBox(self.panel, label="",
                                       choices=["Lätt - 2x2",
                                                "Medel - 4x4", "Svår - 6x6"],
                                       style=wx.RA_HORIZONTAL)
        self.level_radio.SetSelection(0)  # Standard är 2x2
        self.level_radio.Bind(wx.EVT_RADIOBOX, self.update_size_in_memory)

        self.start_game_button = wx.Button(self.panel, label="Starta spelet")
        self.start_game_button.SetFont(btn_font)
        self.start_game_button.SetForegroundColour("#5C2A2E")
        self.start_game_button.Bind(wx.EVT_BUTTON, self.on_start_game)

        self.spacing_dots2 = wx.StaticText(
            self.panel, label=".....................")
        self.spacing_dots2.SetFont(font_dots)
        self.spacing_dots2.SetForegroundColour("#5C2A2E")

        # Lägg till allt i layout
        start_grid.Add(self.headline_label, pos=(0, 1), flag=wx.ALIGN_CENTER)
        start_grid.Add(self.spacing_dots1, pos=(1, 1), flag=wx.ALIGN_CENTER)
        start_grid.Add(self.instruction_label1,
                       pos=(2, 1), flag=wx.ALIGN_CENTER)
        start_grid.Add(self.gamer_name_entry, pos=(3, 1), flag=wx.EXPAND)
        start_grid.Add(self.submitname_button,
                       pos=(4, 1), flag=wx.ALIGN_CENTER)
        start_grid.Add(self.instruction_label2,
                       pos=(6, 1), flag=wx.ALIGN_CENTER)
        start_grid.Add(self.level_radio, pos=(7, 1), flag=wx.ALIGN_CENTER)
        start_grid.Add(self.start_game_button,
                       pos=(9, 1), flag=wx.ALIGN_CENTER)
        start_grid.Add(self.spacing_dots2, pos=(10, 1), flag=wx.ALIGN_CENTER)

        # Lägg till grid i huvudlayouten
        self.main_sizer.Add(start_grid, proportion=1,
                            flag=wx.ALL | wx.EXPAND, border=20)

    def create_default_gamer_name(self):
        '''Creates a default gamer name that will be used if the user has not typed in a name'''
        words_for_name = ["star", "gamer", "guy", "wizard",
                          "alien", "noob", "pro", "smarty", "winner", "bok", "chair", "radio", "baby", "boy", "girl", "steam", "racer", "god", "kitten", "puppy"]
        name_part1 = random.choice(words_for_name)
        name_part0 = random.choice(words_for_name)

        name_part2 = random.randint(100, 999)
        gamer_name = f"{name_part0}_{name_part1}_{name_part2}"
        return gamer_name

    def update_gamer_name(self, event=None):
        '''Updates the gamer name if the user chooses another name'''
        self.gamer_name = self.gamer_name_entry.GetValue()
        if len(self.gamer_name) > 20:
            self.gamer_name = self.gamer_name[:20]
            self.gamer_name_entry.SetValue(self.gamer_name)

    def update_size_in_memory(self, event=None):
        '''Default size in a game is 2x2 memory cards, if the user chooses another level it
        is set with this method'''
        selection = self.level_radio.GetSelection()
        if selection == 0:
            self.size = 2
        elif selection == 1:
            self.size = 4
        else:
            self.size = 6

        # sets the size in the Memory object to the choosen size
        self.player_memory_game.change_size(self.size)
        self.memory_card_button = self.create_memorycard_button_dictionary()
        self.button_position = self.create_button_position_dictionary()

    def on_start_game(self, event):
        """Event handler för start-knappen"""
        self.create_memoryboard_view()

    def create_memorycard_button_dictionary(self):
        '''Creates a dictionary containing the memory_card buttons for the game, returns that dictionary '''
        memorycard_button = {}
        # gets the list of all available positions from the Memory class
        all_positions = self.player_memory_game.create_record_of_all_postions()

        for pos in range(len(all_positions)):
            card_name = f"self.card{all_positions[pos][0]}{all_positions[pos][1]}"
            position = all_positions[pos]
            text_on_card = self.player_memory_game.get_word_in_position(
                position)

            # Knappar skapas här men läggs till i layouten senare
            button = wx.Button(self.panel, label="?", size=(120, 100))
            button.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            button.SetForegroundColour("#5C2A2E")

            # Spara vår extra data i knappen
            button.card_name = card_name
            button.Bind(wx.EVT_BUTTON, lambda evt,
                        name=card_name: self.click_make_a_turn(name))

            memorycard_button[card_name] = button
        return memorycard_button

    def create_button_position_dictionary(self):
        '''creates a dictionary with card_name as key and position as a value'''
        button_position = {}
        all_positions = self.player_memory_game.create_record_of_all_postions()

        for pos in range(len(all_positions)):
            card_name = f"self.card{all_positions[pos][0]}{all_positions[pos][1]}"
            position = all_positions[pos]
            button_position[card_name] = position
        return button_position

    def create_memoryboard_view(self):
        '''Creates the second view with the memory game. The cards are chosen two at the time and the logic is run 
        by the click_make_a_turn() function and the reset_unmatched_cards() function.
        This method also starts the timer.
        '''
        self.start_timer()

        # Rensa panelen och skapa ny layout
        self.panel.DestroyChildren()
        main_game_sizer = wx.BoxSizer(wx.VERTICAL)

        # Top section with info
        top_info_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.headline_label = wx.StaticText(self.panel, label="MEMORY")
        font = self.headline_label.GetFont()
        font.SetPointSize(20)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.headline_label.SetFont(font)
        self.headline_label.SetForegroundColour("#5C2A2E")

        self.spacing_dots1 = wx.StaticText(self.panel, label="............")
        font_dots = self.spacing_dots1.GetFont()
        font_dots.SetPointSize(12)
        font_dots.SetStyle(wx.FONTSTYLE_ITALIC)
        self.spacing_dots1.SetFont(font_dots)
        self.spacing_dots1.SetForegroundColour("#5C2A2E")

        self.infomation_during_game = wx.StaticText(
            self.panel, label="Nu kör vi!!")
        info_font = self.infomation_during_game.GetFont()
        info_font.SetPointSize(14)
        info_font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.infomation_during_game.SetFont(info_font)
        self.infomation_during_game.SetForegroundColour("#5C2A2E")

        self.gamer_name_show = wx.StaticText(
            self.panel, label=f"{self.gamer_name}")
        self.gamer_name_show.SetFont(info_font)
        self.gamer_name_show.SetForegroundColour("#5C2A2E")

        top_info_sizer.Add(self.headline_label, 0, wx.ALL, 5)
        top_info_sizer.Add(self.spacing_dots1, 0, wx.ALL, 5)
        top_info_sizer.Add(self.infomation_during_game,
                           0, wx.ALL | wx.EXPAND, 5)
        top_info_sizer.Add(self.gamer_name_show, 0, wx.ALL | wx.EXPAND, 5)

        main_game_sizer.Add(top_info_sizer, 0, wx.ALL | wx.CENTER, 10)

        # Memory card grid
        memory_grid = wx.GridSizer(
            rows=self.size, cols=self.size, hgap=5, vgap=5)

        # Lägg till memorykort
        all_positions = self.player_memory_game.create_record_of_all_postions()
        for pos in range(len(all_positions)):
            card_name = f"self.card{all_positions[pos][0]}{all_positions[pos][1]}"
            memory_grid.Add(self.memory_card_button[card_name], 0, wx.EXPAND)

        main_game_sizer.Add(memory_grid, 1, wx.ALL | wx.EXPAND, 10)

        # Bottom controls
        bottom_controls = wx.BoxSizer(wx.HORIZONTAL)

        self.headline_rounds = wx.StaticText(self.panel, label="Rundor")
        self.headline_rounds.SetFont(info_font)
        self.headline_rounds.SetForegroundColour("#5C2A2E")

        self.counts_number_of_rounds = wx.StaticText(
            self.panel, label=f"{self.rounds}")
        rounds_font = self.counts_number_of_rounds.GetFont()
        rounds_font.SetPointSize(20)
        rounds_font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.counts_number_of_rounds.SetFont(rounds_font)
        self.counts_number_of_rounds.SetForegroundColour("#5C2A2E")

        self.close_cards_new_round = wx.Button(self.panel, label="Ny runda")
        btn_font = self.close_cards_new_round.GetFont()
        btn_font.SetPointSize(14)
        btn_font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.close_cards_new_round.SetFont(btn_font)
        self.close_cards_new_round.SetForegroundColour("#5C2A2E")
        self.close_cards_new_round.Bind(
            wx.EVT_BUTTON, self.on_reset_unmatched_cards)

        bottom_controls.Add(self.headline_rounds, 0, wx.ALL, 5)
        bottom_controls.Add(self.counts_number_of_rounds, 0, wx.ALL, 5)
        bottom_controls.Add(wx.StaticText(
            self.panel, label="    "), 1, wx.EXPAND)
        bottom_controls.Add(self.close_cards_new_round, 0, wx.ALL, 5)

        main_game_sizer.Add(bottom_controls, 0, wx.ALL | wx.EXPAND, 10)

        # Uppdatera och visa
        self.panel.SetSizer(main_game_sizer)
        self.panel.Layout()

    def click_make_a_turn(self, card_name):
        '''This method is activated by a button click in the memoryboard, the instance parameter card_name is set by the button.
        it handles all logic and communicates with the Memoryclass for game logic.
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

            self.memory_card_button[card_name].SetLabel(card_text)
            self.memory_card_button[card_name].Disable()

        elif self.turn == 2:
            self.reset = False
            self.button2 = card_name  # choosen button is found in the dictionary
            self.player_memory_game.update_presentation_board(position)
            card_text = self.player_memory_game.get_word_in_position(position)

            self.memory_card_button[card_name].SetLabel(card_text)
            self.memory_card_button[card_name].Disable()

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
                    # hide the button that creates a new turn
                    self.close_cards_new_round.Hide()
                    # pauses the game in 3 sek and then creates the high score view
                    wx.CallLater(3000, self.create_high_score_widgets_and_view)
            else:
                self.update_infomation_during_game_label("Ingen träff...")

        elif self.turn > 2:  # if the gamer presses more than two memory cards in a round, this is true
            self.update_infomation_during_game_label("Tryck på ny runda")

    def on_reset_unmatched_cards(self, event):
        """Event handler för ny runda-knappen"""
        self.reset_unmatched_cards()

    def reset_unmatched_cards(self):
        ''' Resets unmatched cards in the game. Is used by the method "click_make_a_turn()'''

        # is True if the player have already reset the game, or if the player has only turned one card.
        if self.reset == True:
            self.update_infomation_during_game_label("Vänd två kort")
        else:
            self.reset = True
            if self.its_a_match == False:
                self.player_memory_game.reset_presentation_board(
                    self.button_position[self.button1], self.button_position[self.button2])

                # Återställ knapparna
                self.memory_card_button[self.button1].SetLabel("?")
                self.memory_card_button[self.button1].Enable()

                self.memory_card_button[self.button2].SetLabel("?")
                self.memory_card_button[self.button2].Enable()

                self.turn = 0
            else:
                # Matchade kort förblir inaktiva
                self.its_a_match = False
                self.Button1 = None
                self.Button2 = None
                self.turn = 0

    def update_runda(self):
        '''Updates the label that shows how many rounds have been played'''
        self.counts_number_of_rounds.SetLabel(f"{self.rounds}")

    def update_infomation_during_game_label(self, new_instruction: str):
        '''Updates the label that gives the player information and instructions during the game'''
        self.infomation_during_game.SetLabel(f"{new_instruction}")

    def update_all_scores(self):
        '''ads the new result to the dictionary self.all_scores'''
        size_ap = self.size
        round_ap = self.rounds
        gamer_ap = self.gamer_name
        min_ap = self.time[0]
        sec_ap = self.time[1]

        # Skapa listan för denna storlek om den inte finns
        if str(size_ap) not in self.all_scores:
            self.all_scores[str(size_ap)] = []

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

    def create_high_score_widgets_and_view(self):
        '''Creates the last view on the board - displaying the high score and the players final result, rounds and time
        It also activates the methods managing the scores - the one that sorts the score and the one that prints the score to the high_score.json file'''

        # sorted in order by this method
        self.sorts_score()
        self.print_score_to_file()

        # Rensa panelen och skapa ny layout
        self.panel.DestroyChildren()
        highscore_sizer = wx.BoxSizer(wx.VERTICAL)

        # Headline
        self.headline_label = wx.StaticText(self.panel, label="MEMORY")
        font = self.headline_label.GetFont()
        font.SetPointSize(20)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.headline_label.SetFont(font)
        self.headline_label.SetForegroundColour("#5C2A2E")

        # Player result
        self.headline_rounds = wx.StaticText(self.panel, label="Rundor")
        info_font = wx.Font(14, wx.FONTFAMILY_TELETYPE,
                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.headline_rounds.SetFont(info_font)
        self.headline_rounds.SetForegroundColour("#5C2A2E")

        self.counts_number_of_rounds = wx.StaticText(
            self.panel, label=f"{self.rounds}")
        rounds_font = wx.Font(20, wx.FONTFAMILY_TELETYPE,
                              wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.counts_number_of_rounds.SetFont(rounds_font)
        self.counts_number_of_rounds.SetForegroundColour("#5C2A2E")

        self.infomation_during_game = wx.StaticText(
            self.panel, label=f"Klarade på {self.time[0]} min, {self.time[1]} sek")
        self.infomation_during_game.SetFont(info_font)
        self.infomation_during_game.SetForegroundColour("#5C2A2E")

        self.gamer_name_show = wx.StaticText(
            self.panel, label=f"{self.gamer_name}")
        self.gamer_name_show.SetFont(info_font)
        self.gamer_name_show.SetForegroundColour("#5C2A2E")

        # Dividers
        self.spacing_dots3 = wx.StaticText(self.panel, label="............")
        font_dots = wx.Font(12, wx.FONTFAMILY_TELETYPE,
                            wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        self.spacing_dots3.SetFont(font_dots)
        self.spacing_dots3.SetForegroundColour("#5C2A2E")

        self.spacing_dots4 = wx.StaticText(self.panel, label="............")
        self.spacing_dots4.SetFont(font_dots)
        self.spacing_dots4.SetForegroundColour("#5C2A2E")

        # High score headline
        headline_text = f" ... TOPP-RESULTAT {self.size}x{self.size} ... "
        self.high_score_headline = wx.StaticText(
            self.panel, label=headline_text)
        hs_font = wx.Font(16, wx.FONTFAMILY_TELETYPE,
                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.high_score_headline.SetFont(hs_font)
        self.high_score_headline.SetForegroundColour("#5C2A2E")

        # Lägg till widgets i layouten
        highscore_sizer.Add(self.headline_label, 0, wx.ALL | wx.CENTER, 10)
        highscore_sizer.Add(self.headline_rounds, 0, wx.ALL | wx.CENTER, 5)
        highscore_sizer.Add(self.counts_number_of_rounds,
                            0, wx.ALL | wx.CENTER, 5)
        highscore_sizer.Add(self.infomation_during_game,
                            0, wx.ALL | wx.CENTER, 5)
        highscore_sizer.Add(self.spacing_dots3, 0, wx.ALL | wx.CENTER, 5)
        highscore_sizer.Add(self.high_score_headline,
                            0, wx.ALL | wx.CENTER, 10)

        # Skapa och visa high score lista
        if str(self.size) in self.all_scores:
            scores_to_show = min(5, len(self.all_scores[str(self.size)]))

            for i in range(scores_to_show):
                score_data = self.all_scores[str(self.size)][i]
                score_text = f"{score_data[1]} : {score_data[0]} rundor : tid {score_data[2]} min, {score_data[3]} sek"

                score_label = wx.StaticText(self.panel, label=score_text)
                score_label.SetFont(info_font)
                score_label.SetForegroundColour("#5C2A2E")

                highscore_sizer.Add(score_label, 0, wx.ALL | wx.CENTER, 5)

        highscore_sizer.Add(self.spacing_dots4, 0, wx.ALL | wx.CENTER, 5)
        highscore_sizer.Add(self.gamer_name_show, 0, wx.ALL | wx.CENTER, 5)

        # Uppdatera panel
        self.panel.SetSizer(highscore_sizer)
        self.panel.Layout()

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
        minutes = (time_diff.seconds % 3600) // 60
        seconds = time_diff.seconds % 60
        microseconds = time_diff.microseconds
        decimal_sec = float(f"{seconds}.{microseconds}")
        shorter_sec = round(decimal_sec, 2)
        self.time = [minutes, shorter_sec]

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
    app = wx.App()
    frame = VisualMemApp(None)
    app.MainLoop()
