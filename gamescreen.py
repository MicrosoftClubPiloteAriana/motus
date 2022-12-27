import tkinter as tk
from tkinter import messagebox
from cbridge import CBridge
from basescreen import BaseScreen
import time
from string import ascii_lowercase
import functools

from internal_ui.betterbutton import BetterButton

WORD_LENGTH = 5
LINES_COUNT = 6


class GameScreen(BaseScreen):
    def __init__(self, root, cbridge: CBridge):
        super().__init__(root)

        self.cbridge = cbridge
        self.hintmode = False
        self.total_hints = 1

        self.init_ui()

    def init_ui(self):
        # This frame contains all the rows
        self.wordsframe = WordsFrame(self, self.cbridge)
        self.clock = ClockWidget(self)
        self.toolsframe = tk.Frame(self)
        self.hintbutton = BetterButton(self.toolsframe, text=str(self.total_hints),
                                       compound="left", command=self.toggle_hint)
        self.hintbutton.set_image("./assets/hint.png", 20)
        self.restartbutton = BetterButton(self.toolsframe, command=self.restart_game)
        self.restartbutton.set_image("./assets/restart.png", 20)
        self.aboutbutton = tk.Button(self.toolsframe, text="About",
                                     command=lambda: self.root.switch(self.root.aboutscreen))

        self.wordsframe.focus_set()
        self.wordsframe.grid(row=0, column=0)
        self.clock.grid(row=1, column=0)
        self.toolsframe.grid(row=0, column=1, sticky="n", padx=10, pady=10, rowspan=2)
        self.hintbutton.grid()
        self.restartbutton.grid(row=1, column=0, sticky="ew", pady=10, ipady=5)
        self.aboutbutton.grid(row=2, column=0, sticky="ew", pady=(100, 0))

        self.clock.start()

    def toggle_hint(self):
        if self.hintmode:
            self.hintmode = not self.hintmode
            self.hintbutton["text"] = str(self.total_hints)
            if self.total_hints == 0:
                self.hintbutton["state"] = "disabled"
        elif self.total_hints > 0:
            self.hintmode = not self.hintmode

    def get_elapsed_time(self):
        """
        :return: The elapsed time since the beginning of the current game
        """
        return int(self.clock.elapsed_time)

    def stop_game(self):
        self.clock.stop()

    def restart_game(self):
        self.wordsframe.restart()
        self.clock.start()
        self.total_hints = 2
        self.hintbutton["text"] = str(self.total_hints)
        self.hintbutton["state"] = "normal"


COLOR_GRAY = 0
COLOR_YELLOW = 1
COLOR_GREEN = 2
ALPHABET_EN = ascii_lowercase


class WordsFrame(tk.LabelFrame):
    def __init__(self, root, cbridge):
        super().__init__(root, text="Game")

        self.root = root
        self.cbridge = cbridge

        self.current_line = 0
        self.current_letter = 0
        self.current_word = [""] * WORD_LENGTH

        self.revealed_letters = [""] * WORD_LENGTH
        self.letter_labels = []
        # Fill the frame according to the number of lines and word length
        for row in range(LINES_COUNT):
            self.letter_labels.append([])
            self.grid_rowconfigure(row, minsize=60)
            for col in range(WORD_LENGTH):
                if row == 0:
                    self.grid_columnconfigure(col, minsize=60)

                letter = tk.Label(self, text="", bg="white", borderwidth=1, relief="solid")
                letter.bind("<Enter>", functools.partial(self.on_letter_hover, letter, row, col))
                letter.bind("<Leave>", functools.partial(self.on_letter_unhover, letter, row, col))
                letter.bind("<Button-1>", functools.partial(self.on_letter_click, letter, row, col))
                letter.grid(row=row, column=col, sticky="nsew")

                self.letter_labels[-1].append(letter)

        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<Return>", self.on_return_press)
        self.bind("<BackSpace>", self.on_backspace_press)

    def on_key_press(self, event):
        # Check whether the key is a letter
        if len(event.char) == 1 and event.char.lower() in ALPHABET_EN:
            letter = event.char
            # Check if there's space for another letter
            while self.current_letter < WORD_LENGTH:
                if self.current_word[self.current_letter] == "":
                    self.current_word[self.current_letter] = letter.lower()
                    self.current_letter_label["text"] = letter.upper()
                    self.current_letter += 1
                    break
                self.current_letter += 1

    def on_return_press(self, event):
        # If the line is full, validate the word
        if all([l != "" for l in self.current_word]):
            self.validate_current_line()

    def on_backspace_press(self, event):
        # If the line isn't empty, delete the last letter
        while self.current_letter > 0:
            if self.revealed_letters[self.current_letter - 1] == "":
                self.current_letter -= 1
                self.current_word[self.current_letter] = ""
                self.current_letter_label["text"] = ""
                break
            self.current_letter -= 1

    def on_letter_hover(self, letter_label, row, col, event):
        if self.root.hintmode and row == self.current_line and \
           self.revealed_letters[col] == "":
            letter_label["borderwidth"] = 2

    def on_letter_unhover(self, letter_label, row, col, event):
        if letter_label["borderwidth"] != 1:
            letter_label["borderwidth"] = 1

    def on_letter_click(self, letter_label, row, col, event):
        if self.root.hintmode and row == self.current_line and \
           self.revealed_letters[col] == "":
            self.root.total_hints -= 1
            self.root.toggle_hint()
            letter_label["borderwidth"] = 1
            revealed_letter = self.cbridge.get_secret_word()[col].upper()
            letter_label["text"] = revealed_letter
            self.revealed_letters[col] = revealed_letter
            self.current_word[col] = revealed_letter

    def validate_current_line(self):
        """
        Inteprets the given answer, win or loss of the player
        is also determined here
        """
        word = "".join(self.current_word)

        # Word must be first valid grammatically speaking
        if not self.cbridge.is_word_valid(word):
            self.alert_invalid_word()
            return

        # Interpret the answer and color
        # the word according to the result
        result = self.cbridge.interpret(word)
        win = True
        for i in range(WORD_LENGTH):
            color = result[i]
            if color == COLOR_GRAY:
                self.letter_labels[self.current_line][i]["bg"] = "#cecece"
                win = False
            elif color == COLOR_YELLOW:
                self.letter_labels[self.current_line][i]["bg"] = "#ffff33"
                win = False
            elif color == COLOR_GREEN:
                self.letter_labels[self.current_line][i]["bg"] = "#22ff55"
            else:
                print("[e] Unknown color type", color)

        # The player may win or loose after each try,
        # so keep an eye on it...
        if win:
            self.root.stop_game()
            messagebox.showinfo(
                "Youpi",
                f"Well done, it took you {self.root.get_elapsed_time()}s "
                f"to find the word in {self.current_line + 1} tries!")
            self.root.restart_game()
        elif self.current_line == LINES_COUNT - 1:
            self.root.stop_game()
            messagebox.showinfo(
                "Looser",
                f"Better luck next time!\n"
                f"\n"
                f"The word was: {self.cbridge.get_secret_word()}")
            self.root.restart_game()
        else:
            self.next_line()

    def next_line(self):
        """
        Moves the cursor to the next line
        """
        self.current_line += 1
        self.current_letter = 0
        self.current_word = self.revealed_letters.copy()
        for i, letter in enumerate(self.revealed_letters):
            if letter != "":
                self.letter_labels[self.current_line][i]["text"] = letter

    def restart(self):
        """
        Clears the board and resets the secret word
        """
        for row in range(self.current_line + 1):
            for col in range(WORD_LENGTH):
                self.letter_labels[row][col]["text"] = ""
                self.letter_labels[row][col]["bg"] = "#ffffff"
        self.current_line = 0
        self.current_letter = 0
        self.current_word = [""] * WORD_LENGTH
        self.revealed_letters = [""] * WORD_LENGTH
        self.cbridge.reset_word()

    @property
    def current_letter_label(self):
        return self.letter_labels[self.current_line][self.current_letter]

    def alert_invalid_word(self, blinks=4, enable=True):
        """
        What's a better way of alerting the player than by blinking with red (:
        """
        if blinks <= 0 and enable: return
        for letter in self.letter_labels[self.current_line]:
            letter["foreground"] = "red" if enable else "black"
        self.after(200, lambda: self.alert_invalid_word(blinks - 1, not enable))


class ClockWidget(tk.Label):
    """
    More likely a TimerWidget, counts time and displays it
    """
    def __init__(self, root):
        super().__init__(root)

        self.start_time = 0
        self.update_id = None
        self["text"] = self.format_timedelta(0)

    def start(self):
        self.start_time = time.time()
        self.update_text()

    def update_text(self):
        delta = self.elapsed_time
        self["text"] = self.format_timedelta(delta)
        self.update_id = self.after(500, self.update_text)

    def stop(self):
        if self.update_id is not None:
            self.after_cancel(self.update_id)
            self.update_id = None

    @property
    def elapsed_time(self):
        return time.time() - self.start_time

    @staticmethod
    def format_timedelta(delta):
        hours, remainder = divmod(delta, 3600)
        minutes, seconds = divmod(remainder, 60)
        string = ""
        if hours > 0:
            string = f"{hours} : "
        return f"{string}{int(minutes):02} : {int(seconds):02}"
