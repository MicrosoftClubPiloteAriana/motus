import tkinter as tk
from tkinter import messagebox
from cbridge import CBridge
from basescreen import BaseScreen


WORD_LENGTH = 5
LINES_COUNT = 6


class GameScreen(BaseScreen):
    def __init__(self, root, cbridge: CBridge):
        super().__init__(root)

        self.cbridge = cbridge

        self.init_ui()

    def init_ui(self):
        # This frame contains all the rows
        self.wordsframe = WordsFrame(self, self.cbridge)
        self.wordsframe.focus_set()
        self.wordsframe.pack()

    def restart_game(self):
        self.wordsframe.restart()


COLOR_GRAY = 0
COLOR_YELLOW = 1
COLOR_GREEN = 2


class WordsFrame(tk.LabelFrame):
    def __init__(self, root, cbridge):
        super().__init__(root, text="Game")

        self.root = root
        self.cbridge = cbridge

        self.current_line = 0
        self.current_letter = 0
        self.current_word = []

        self.letter_labels = []
        # Fill the frame according to the number of lines and word length
        for row in range(LINES_COUNT):
            self.letter_labels.append([])
            self.grid_rowconfigure(row, minsize=60)
            for col in range(WORD_LENGTH):
                if row == 0:
                    self.grid_columnconfigure(col, minsize=60)

                letter = tk.Label(self, text="", borderwidth=1, relief="solid", bg="white")
                letter.grid(row=row, column=col, sticky="nsew")

                self.letter_labels[-1].append(letter)

        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<Return>", self.on_return_press)
        self.bind("<BackSpace>", self.on_backspace_press)

    def on_key_press(self, event):
        if len(event.char) == 1 and event.char.isalpha():
            letter = event.char
            if self.current_letter < WORD_LENGTH:
                self.current_word.append(letter.lower())
                self.current_letter_label["text"] = letter.upper()
                self.current_letter += 1

    def on_return_press(self, event):
        if self.current_letter == WORD_LENGTH:
            self.validate_current_line()

    def on_backspace_press(self, event):
        if self.current_letter > 0:
            self.current_letter -= 1
            self.current_letter_label["text"] = ""
            self.current_word.pop()

    def validate_current_line(self):
        word = "".join(self.current_word)
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

        if win:
            messagebox.showinfo(
                "Youpi",
                f"Well done, you found the word in {self.current_line + 1} tries!")
            self.root.restart_game()
        elif self.current_line == LINES_COUNT - 1:
            messagebox.showinfo(
                "Looser",
                f"Better luck next time!\n"
                f"\n"
                f"The word was: {self.cbridge.get_secret_word()}")
            self.root.restart_game()
        else:
            self.current_line += 1
            self.current_letter = 0
            self.current_word.clear()

    def restart(self):
        for row in range(self.current_line + 1):
            for col in range(WORD_LENGTH):
                self.letter_labels[row][col]["text"] = ""
                self.letter_labels[row][col]["bg"] = "#ffffff"
        self.current_line = 0
        self.current_letter = 0
        self.current_word.clear()
        self.cbridge.reset_word()

    @property
    def current_letter_label(self):
        return self.letter_labels[self.current_line][self.current_letter]
