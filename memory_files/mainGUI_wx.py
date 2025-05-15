import wx
import random
from memory_logic import Memory
import json
from datetime import datetime

# Anna Björklund
# December 2024
# Course code DD100N HT24 Programmeringsteknik webbkurs (10118)

# GUI program for the Memory class that creates a graphic interface for the game using wxPython.
# The game has 3 views:
# 1. Player chooses a gamer name and level of difficulty (2x2, 4x4, 6x6)
# 2. Memory board with cards that can be flipped
# 3. Results view showing time, rounds, and top 5 scores


class VisualMemApp(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Memory Game', size=(800, 600))

        # Game state variables
        self.turn = 0
        self.size = 2
        self.rounds = 0
        self.reset = False
        self.all_scores = None
        self.gamer_name = self.create_default_gamer_name()
        self.player_memory_game = Memory(self.size)
        self.button1 = None
        self.button2 = None
        self.all_moves_done = False
        self.its_a_match = False
        self.start_time = None
        self.end_time = None
        self.player_game_time = None
        self.time = None

        # Create main panel and sizer
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(
            wx.Colour(5, 60, 128))  # Medium blue background
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.main_sizer)

        # Initialize dictionaries
        self.memory_card_button = {}
        self.button_position = {}
        self.high_scores_labels = {}
        self.all_scores = self._import_score_from_file()

        # Create the start view
        self.create_start_widgets_and_board()

        self.Centre()
        self.Show()

    def reset_game_state(self):
        """Resets all game state variables to their initial values"""
        # Reset game state variables
        self.turn = 0
        self.rounds = 0
        self.reset = False
        self.button1 = None
        self.button2 = None
        self.all_moves_done = False
        self.its_a_match = False
        self.start_time = None
        self.end_time = None
        self.player_game_time = None
        self.time = None

        # Reset game board
        self.player_memory_game = Memory(self.size)

        # Clear dictionaries
        self.memory_card_button = {}
        self.button_position = {}
        self.high_scores_labels = {}

    def create_start_widgets_and_board(self):
        """Creates the widgets and the board for the start view"""
        # Reset game state before creating new view
        self.reset_game_state()

        # Clear any existing widgets
        self.main_sizer.Clear(True)

        # Add spacer at the top
        self.main_sizer.AddSpacer(50)  # Adds 50 pixels of vertical space

        # Title
        title = wx.StaticText(self.panel, label="MEMORY")
        title.SetFont(
            wx.Font(wx.FontInfo(50).Family(wx.FONTFAMILY_MODERN).Bold()))
        title.SetForegroundColour(wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        # Dots separator
        dots = wx.StaticText(
            self.panel, label="...............................................................")
        dots.SetFont(wx.Font(wx.FontInfo(12).Family(
            wx.FONTFAMILY_MODERN).Italic()))
        dots.SetForegroundColour(wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(dots, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Add spacer
        self.main_sizer.AddSpacer(20)  # Adds 20 pixels of vertical space

        # Name input
        name_label = wx.StaticText(
            self.panel, label=f"Ditt gamingnamn är {self.gamer_name} (byt om du vill)")
        name_label.SetFont(
            wx.Font(wx.FontInfo(16).Family(wx.FONTFAMILY_MODERN).Bold()))
        name_label.SetForegroundColour(wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(name_label, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.name_text = wx.TextCtrl(self.panel, value=self.gamer_name)
        self.name_text.SetBackgroundColour(
            wx.Colour(204, 220, 245))  # Light yellow background
        self.name_text.SetForegroundColour(
            wx.Colour(64, 64, 64))  # Dark gray text
        self.main_sizer.Add(self.name_text, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Save name button
        save_name_btn = wx.Button(self.panel, label="Spara namn")
        save_name_btn.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        save_name_btn.Bind(wx.EVT_BUTTON, self.update_gamer_name)
        self.main_sizer.Add(save_name_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.main_sizer.AddSpacer(20)  # Adds 20 pixels of vertical space

        # Difficulty selection
        diff_label = wx.StaticText(self.panel, label="Välj svårighetsgrad")
        diff_label.SetFont(
            wx.Font(wx.FontInfo(16).Family(wx.FONTFAMILY_MODERN).Bold()))
        diff_label.SetForegroundColour(wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(diff_label, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Create a StaticBox for radio buttons
        diff_box = wx.StaticBox(self.panel, label="")
        diff_box.SetBackgroundColour(
            wx.Colour(204, 220, 245))  # Light blue background
        diff_box_sizer = wx.StaticBoxSizer(diff_box, wx.VERTICAL)

        # Radio buttons for difficulty
        self.diff_radio = wx.RadioBox(
            self.panel,
            label="",
            choices=["Lätt - 2x2", "Medel - 4x4", "Svår - 6x6"],
            style=wx.RA_HORIZONTAL
        )
        self.diff_radio.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        self.diff_radio.Bind(wx.EVT_RADIOBOX, self.update_size_in_memory)
        diff_box_sizer.Add(self.diff_radio, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.main_sizer.Add(diff_box_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Start game button
        start_btn = wx.Button(self.panel, label="Starta spelet")
        start_btn.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        start_btn.Bind(wx.EVT_BUTTON, self.create_memoryboard_view)
        self.main_sizer.Add(start_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Dots separator
        dots2 = wx.StaticText(self.panel, label=".....................")
        dots2.SetFont(wx.Font(wx.FontInfo(12).Family(
            wx.FONTFAMILY_MODERN).Italic()))
        dots2.SetForegroundColour(wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(dots2, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.Layout()

    def create_default_gamer_name(self):
        """Creates a default gamer name"""
        words_for_name = ["star", "gamer", "guy", "wizard", "alien", "noob", "pro", "smarty",
                          "winner", "bok", "chair", "radio", "baby", "boy", "girl", "steam",
                          "racer", "god", "kitten", "puppy"]
        name_part1 = random.choice(words_for_name)
        name_part0 = random.choice(words_for_name)
        name_part2 = random.randint(100, 999)
        return f"{name_part0}_{name_part1}_{name_part2}"

    def update_gamer_name(self, event):
        """Updates the gamer name from the text input"""
        self.gamer_name = self.name_text.GetValue()
        if len(self.gamer_name) > 20:
            self.gamer_name = self.gamer_name[:20]

    def update_size_in_memory(self, event):
        """Updates the game size based on difficulty selection"""
        # Update size and memory game state
        size_map = {0: 2, 1: 4, 2: 6}
        self.size = size_map[self.diff_radio.GetSelection()]
        self.player_memory_game.change_size(self.size)

        # Clear the button dictionaries - they will be recreated when the game starts
        self.memory_card_button = {}
        self.button_position = {}

    def create_memorycard_button_dictionary(self):
        """Creates a dictionary of memory card buttons"""
        memorycard_button = {}
        all_positions = self.player_memory_game.create_record_of_all_postions()

        for pos in all_positions:
            card_name = f"self.card{pos[0]}{pos[1]}"
            text_on_card = self.player_memory_game.get_word_in_position(pos)

            button = wx.Button(self.panel, label=text_on_card,
                               size=(40, 40))  # Set fixed size
            button.SetFont(
                wx.Font(wx.FontInfo(12).Family(wx.FONTFAMILY_MODERN).Bold()))
            button.SetForegroundColour(wx.Colour(92, 42, 46))
            button.SetBackgroundColour(
                wx.Colour(204, 220, 245))  # Light blue background
            button.Bind(wx.EVT_BUTTON, lambda evt,
                        name=card_name: self.click_make_a_turn(name))

            memorycard_button[card_name] = button

        return memorycard_button

    def create_button_position_dictionary(self):
        """Creates a dictionary mapping card names to positions"""
        button_position = {}
        all_positions = self.player_memory_game.create_record_of_all_postions()

        for pos in all_positions:
            card_name = f"self.card{pos[0]}{pos[1]}"
            button_position[card_name] = pos

        return button_position

    def create_memoryboard_view(self, event=None):
        """Creates the second view with the memory game, reuses some label-widgets from the first game, takes out most of them
        and adds some new and the memory cards from the instance attribute self.memory_card_button, a dictionary. 
        The cards are choosen two at the time and the logic is run by the click_make_a_turn() function and the reset_unmatched_cards() function.
        This method also starts the timer.
        """
        self.start_timer()

        # Clear the main sizer
        self.main_sizer.Clear(True)

        # Recreate the memory card buttons and position dictionary
        self.memory_card_button = self.create_memorycard_button_dictionary()
        self.button_position = self.create_button_position_dictionary()

        # Create a grid sizer for the game board
        grid_sizer = wx.GridSizer(self.size, self.size, 5, 5)

        # Add memory cards to the grid
        all_positions = self.player_memory_game.create_record_of_all_postions()
        row_nr = 12  # the row in the GUI where the first memorycards are placed

        for pos in all_positions:
            card_name = f"self.card{pos[0]}{pos[1]}"
            if card_name in self.memory_card_button:
                # if the position letter has changed in this loop we need a new row
                if pos[0] != all_positions[all_positions.index(pos)-1][0] if all_positions.index(pos) > 0 else False:
                    row_nr += 1
                grid_sizer.Add(
                    self.memory_card_button[card_name], 0, wx.EXPAND)
            else:
                print(f"Warning: Card {card_name} not found in dictionary")
                print(
                    f"Available keys: {list(self.memory_card_button.keys())}")

        # Add game info at the top
        info_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create new information label
        self.infomation_during_game = wx.StaticText(
            self.panel, label=f"Nu kör vi, {self.gamer_name}!!")
        self.infomation_during_game.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        self.infomation_during_game.SetForegroundColour(
            wx.Colour(204, 220, 245))  # Light blue

        rounds_label = wx.StaticText(
            self.panel, label=f"Rundor: {self.rounds}")
        rounds_label.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        rounds_label.SetForegroundColour(
            wx.Colour(204, 220, 245))  # Light blue

        # Add elements to vertical sizer
        info_sizer.Add(self.infomation_during_game,
                       0, wx.ALL | wx.ALIGN_LEFT, 5)
        info_sizer.Add(rounds_label, 0, wx.ALL | wx.ALIGN_LEFT, 5)

        # Add new round button
        self.close_cards_new_round = wx.Button(self.panel, label="Ny runda")
        self.close_cards_new_round.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        self.close_cards_new_round.Bind(
            wx.EVT_BUTTON, self.reset_unmatched_cards)

        # Add everything to main sizer
        self.main_sizer.Add(info_sizer, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.main_sizer.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(self.close_cards_new_round, 0,
                            wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.Layout()

    def update_infomation_during_game_label(self, new_instruction: str):
        """Updates the label that gives the player information and instructions during the game"""
        if hasattr(self, 'infomation_during_game') and self.infomation_during_game:
            try:
                self.infomation_during_game.SetLabel(new_instruction)
                self.panel.Layout()  # Force layout update to show new text
            except RuntimeError:
                # If the widget was deleted, recreate it
                self.infomation_during_game = wx.StaticText(
                    self.panel, label=new_instruction)
                self.infomation_during_game.SetFont(
                    wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
                self.infomation_during_game.SetForegroundColour(
                    wx.Colour(204, 220, 245))
                self.panel.Layout()

    def check_if_game_is_finished(self):
        """Checks if all pairs have been found"""
        if self.player_memory_game.check_if_all_words_are_found():
            self.stop_timer()
            self.create_high_score_widgets_and_view()

    def click_make_a_turn(self, card_name):
        """Handles card clicks during the game"""
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

            if self.button1 is not None:  # Add check for None
                self.its_a_match = self.player_memory_game.its_a_match(
                    self.button_position[self.button1], self.button_position[self.button2])

                if self.its_a_match:
                    # returns true if the game should end
                    self.all_moves_done = self.player_memory_game.check_if_all_words_are_found()
                    self.update_infomation_during_game_label(
                        f"{self.gamer_name} - En match!!!")

                    # activates the highscore view and closes down the game board
                    if self.all_moves_done:
                        self.stop_timer()
                        self.update_infomation_during_game_label(
                            f"Alla hittade, snyggt jobbat {self.gamer_name}!!")
                        # appends result and gamer_name to self.all_scores the dictionary with all previous scores
                        size_ap = self.size
                        round_ap = self.rounds
                        gamer_ap = self.gamer_name
                        min_ap = self.time[0]
                        sec_ap = self.time[1]
                        self.all_scores[str(size_ap)].append(
                            [round_ap, gamer_ap, min_ap, sec_ap])
                        # hide the button that creates a new turn
                        self.close_cards_new_round.Hide()
                        # pauses the game in 3 sek and then creates the high score view
                        wx.CallLater(
                            3000, self.create_high_score_widgets_and_view)
                else:
                    self.update_infomation_during_game_label("Ingen träff...")

        elif self.turn > 2:  # if the gamer presses more than two memory cards in a round, this is true
            self.update_infomation_during_game_label("Tryck på ny runda")

    def reset_unmatched_cards(self, event):
        """Resets unmatched cards for the next round"""
        # is True if the player have already reset the game, or if the player has only turned one card.
        if self.reset == True:
            self.update_infomation_during_game_label("Vänd två kort")
        else:
            self.reset = True
            if self.its_a_match == False and self.button1 is not None and self.button2 is not None:
                self.player_memory_game.reset_presentation_board(
                    self.button_position[self.button1], self.button_position[self.button2])

                # Reset the buttons
                card_text1 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button1])
                self.memory_card_button[self.button1].SetLabel(card_text1)
                self.memory_card_button[self.button1].Enable()

                card_text2 = self.player_memory_game.get_word_in_position(
                    self.button_position[self.button2])
                self.memory_card_button[self.button2].SetLabel(card_text2)
                self.memory_card_button[self.button2].Enable()

                self.turn = 0
                self.button1 = None
                self.button2 = None
            else:
                # Matched cards remain disabled
                self.its_a_match = False
                self.button1 = None
                self.button2 = None
                self.turn = 0

    def update_runda(self):
        """Updates the round counter"""
        # Update the rounds display
        for child in self.panel.GetChildren():
            if isinstance(child, wx.StaticText) and "Rundor:" in child.GetLabel():
                child.SetLabel(f"Rundor: {self.rounds}")
                break

    def create_high_score_widgets_and_view(self):
        """Creates the last view on the board - displaying the high score and the players final result, rounds and time"""
        self.main_sizer.Clear(True)

        # Add spacer at the top
        self.main_sizer.AddSpacer(50)  # Adds 20 pixels of vertical space

        # Title
        title = wx.StaticText(self.panel, label="SPELET ÄR ÖVER!!!")
        title.SetFont(
            wx.Font(wx.FontInfo(40).Family(wx.FONTFAMILY_MODERN).Bold()))
        title.SetForegroundColour(wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        # Player's score
        score_text = f"Spelare: {self.gamer_name}\nRundor: {self.rounds}\nTid: {self.time[0]} min {self.time[1]} sek"
        score_label = wx.StaticText(self.panel, label=score_text)
        score_label.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        score_label.SetForegroundColour(
            wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(score_label, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Add dots separator
        dots = wx.StaticText(
            self.panel, label="...............................")
        dots.SetFont(wx.Font(wx.FontInfo(12).Family(
            wx.FONTFAMILY_MODERN).Italic()))
        dots.SetForegroundColour(wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(dots, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Add spacer
        self.main_sizer.AddSpacer(20)  # Adds 20 pixels of vertical space

        # High scores
        high_score_title = wx.StaticText(self.panel, label="TOPP 5 SPELARE")
        high_score_title.SetFont(
            wx.Font(wx.FontInfo(30).Family(wx.FONTFAMILY_MODERN).Bold()))
        high_score_title.SetForegroundColour(
            wx.Colour(204, 220, 245))  # Light blue
        self.main_sizer.Add(high_score_title, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Create high score list
        self.sorts_score()
        self.print_score_to_file()

        high_score_sizer = wx.BoxSizer(wx.VERTICAL)
        for i, score in enumerate(self.all_scores.get(str(self.size), [])[:5]):
            score_text = f"{i+1}. {score[1]} - {score[0]} rundor, {score[2]} min {score[3]} sek"
            score_label = wx.StaticText(self.panel, label=score_text)
            score_label.SetFont(
                wx.Font(wx.FontInfo(12).Family(wx.FONTFAMILY_MODERN).Bold()))
            score_label.SetForegroundColour(
                wx.Colour(204, 220, 245))  # Light blue
            high_score_sizer.Add(score_label, 0, wx.ALL | wx.ALIGN_CENTER, 2)

        self.main_sizer.Add(high_score_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # New game button
        new_game_btn = wx.Button(self.panel, label="Nytt Spel")
        new_game_btn.SetFont(
            wx.Font(wx.FontInfo(14).Family(wx.FONTFAMILY_MODERN).Bold()))
        new_game_btn.Bind(
            wx.EVT_BUTTON, lambda evt: self.create_start_widgets_and_board())
        self.main_sizer.Add(new_game_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.Layout()

    def start_timer(self):
        """Starts the game timer"""
        self.start_time = datetime.now()

    def stop_timer(self):
        """Stops the game timer and calculates total time"""
        self.end_time = datetime.now()
        self.player_game_time = self.end_time - self.start_time
        minutes = self.player_game_time.seconds // 60
        seconds = self.player_game_time.seconds % 60
        self.time = [minutes, seconds]

    def sorts_score(self):
        """Sorts the scores by rounds and time"""
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

    def _import_score_from_file(self) -> dict:
        """Imports scores from the JSON file"""
        try:
            with open('high_score.json', 'r') as file:
                scores = json.load(file)
                # Ensure all sizes have empty lists
                for size in ["2", "4", "6"]:
                    if size not in scores:
                        scores[size] = []
                return scores
        except FileNotFoundError:
            # Initialize with empty lists for all sizes
            return {"2": [], "4": [], "6": []}

    def print_score_to_file(self):
        """Saves scores to the JSON file"""
        with open('high_score.json', 'w') as file:
            json.dump(self.all_scores, file)


if __name__ == '__main__':
    app = wx.App()
    frame = VisualMemApp()
    app.MainLoop()
