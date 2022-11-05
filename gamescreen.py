import tkinter as tk
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
        self.wordsframe = tk.LabelFrame(self, text="Game")

        # Fill the frame according to the number of lines and word length
        for row in range(LINES_COUNT):
            for col in range(WORD_LENGTH):
                letter = tk.Label(self.wordsframe, text="A", borderwidth=1, relief="solid", padx=20, pady=20)
                letter.grid(row=row, column=col)

        self.wordsframe.pack()
