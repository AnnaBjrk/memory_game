
# För att styla använd https://docs.python.org/3/library/tkinter.ttk.html


from tkinter import *
import time


class VisualMemoryBoard():
    def __init__(self, first_card_turned=" ", second_card_turned=" ", turn=0, positions: list, size: int):
        self.first_card_turned = first_card_turned
        self.second_card_turned = second_card_turned
        self.turn = turn
        self.size = size
        self.positions = positions
        self.button_postition = self._create_button_postition_dictionary()

    # keps track of what button has what position
    def _create_button_postition_dictionary(self):
        # the list orgins from the Memory class an is listing all positions starting with the first row, then second and so on. so
        # a 2x2 board would be listed, A0, A1, B0, B1,
        # key is the buttons name value a list of two values the position and the button status, initally set to
        # NORMAL but will be changed to DISABLED when there is a match
        button_positions = {}
        for pos in range(len(self.positions)):
            button_positions = {
                f"Button{self.positions[pos]}": [pos, "NORMAL"]}
        return button_positions

    def handle_visual_cards(self):
        # skriver ut alla korten
        pass

    def button_click_to_position(self, button) -> str:
        # returnar knappens position, så att Memoryklassen kan
        # uppdatera sina dictionaries
        self.turn += 1
        if self.turn < 2:
            self.first_card_turned = button
            letter_number_pos = self.positions(button)
            return letter_number_pos
        else:
            self.second_card_turned = button
            letter_number_pos = self.positions(button)
            return letter_number_pos
            # ev nollar vi turn här

    def end_round_adjust_visual(self, match: bool):
        if match == True:
            self.positions[self.first_card_turned][1] = "DISABLED"
            self.positions[self.second_card_turned][1] = "DISABLED"
            self.turn = 0
        else:
            # programmet pausar i 5 sek ev behöver vi lägga den här någon annan stans
            time.sleep(5)
            self.turn = 0


# ska läggas i main funktionen
root = Tk()
# root.configure(bg='white')
root.title("MEMORY")


def print_buttons(presentation_board)  # from presentation_board from the


# Memory class we get the text for the cards, the status NORMAL/DEFAULT is set by
# the instance variable dictionary positions
ButtonA0 = Button(root, text=presentation_board["A"][0], command=lambda: button_click_to_position(
    ButtonA0), padx=50, pady=50, state=self.positions[ButtonA0][1])
ButtonA1 = Button(root, text=presentation_board["A"][1], command=lambda: button_click_to_position(
     ButtonA1), padx=50, pady=50, state=self.positions[ButtonA1][1])
 ButtonB0 = Button(root, text=presentation_board["B"][0], command=lambda: button_click_to_position(
      ButtonB0), padx=50, pady=50, state=self.positions[ButtonB0][1])
  ButtonB1 = Button(root, text=presentation_board["B"][1], command=lambda: button_click_to_position(
       ButtonB1), padx=50, pady=50, state=self.positions[ButtonB1][1])

   if self.size > 2:  # parametrarna inte korrekta nedan
        back_card = "????"  # koppla till dictionary sen
        ButtonA2 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonA2), padx=50, pady=50)
        ButtonA3 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonA3), padx=50, pady=50)
        ButtonB2 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonB2), padx=50, pady=50)
        ButtonB3 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonB3), padx=50, pady=50)
        ButtonC0 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonC0), padx=50, pady=50)
        ButtonC1 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonC1), padx=50, pady=50)
        ButtonC2 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonC2), padx=50, pady=50)
        ButtonC3 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonC3), padx=50, pady=50)
        ButtonD0 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonD0), padx=50, pady=50)
        ButtonD1 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonD1), padx=50, pady=50)
        ButtonD2 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonD2), padx=50, pady=50)
        ButtonD3 = Button(root, text=back_card, command=lambda: button_click_to_position(
            ButtonD3), padx=50, pady=50)
    if size == 6:
        pass  # fyll på med alla

# säkra att det följer logiken från dictionaryn
    ButtonA0.grid(row=0, column=0)
    ButtonA1.grid(row=0, column=1)
    ButtonB0.grid(row=1, column=0)
    ButtonB1.grid(row=1, column=1)
    if size > 4:
        ButtonA2.grid(row=0, column=2)
        ButtonA3.grid(row=0, column=3)
        ButtonB2.grid(row=1, column=2)
        ButtonB3.grid(row=1, column=3)
        ButtonC0.grid(row=2, column=0)
        ButtonC1.grid(row=2, column=1)
        ButtonC2.grid(row=2, column=2)
        ButtonC3.grid(row=2, column=3)
        ButtonD0.grid(row=3, column=0)
        ButtonD1.grid(row=3, column=1)
        ButtonD2.grid(row=3, column=2)
        ButtonD3.grid(row=3, column=3)
    if size == 6:
        pass  # fyll på med alla


root.mainloop()
