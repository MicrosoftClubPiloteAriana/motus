import webbrowser

from basescreen import BaseScreen
import tkinter as tk
from tkinter import ttk

from internal_ui.betterbutton import BetterButton


class AboutScreen(BaseScreen):
    def __init__(self, root):
        super().__init__(root)

        self.init_ui()

    def init_ui(self):
        greeting = tk.Label(
            self,
            text="Welcome to motus",
            fg="blue"
        )
        greeting.config(font=("", 32))

        main_text = tk.Label(
            self,
            text="In this game you are asked to guess a word of 5 letters.\n"
                 "You have a maximum of 5 trials.\n",
        )
        gray_frame = tk.Frame(self)
        gray_letter = tk.Label(gray_frame, text="A", highlightbackground="black", highlightthickness=1, bg="#cecece")
        gray_description = tk.Label(
            gray_frame,
            text="If the letter is marked as gray,\n"
                 "the letter you put in is not part of the word.",
            fg="black",
            justify="left"
        )

        yellow_frame = tk.Frame(self)
        yellow_letter = tk.Label(
            yellow_frame,
            text="B", highlightbackground="black", highlightthickness=1, bg="#ffff33")
        yellow_description = tk.Label(
            yellow_frame,
            text="If the letter is marked as yellow,\n"
                 "the input letter is part of the word but is not in the correct place.",
            fg="black",
            justify="left"
        )

        green_frame = tk.Frame(self)
        green_letter = tk.Label(
            green_frame,
            text="C", highlightbackground="black", highlightthickness=1, bg="#22ff55")
        green_description = tk.Label(
            green_frame,
            text="If the letter is marked as green,\n"
                 "the input letter is correct and in the correct place.",
            fg="black",
            justify="left"
        )

        frame_social = tk.Frame(self)
        github = BetterButton(
            master=frame_social,
            relief=tk.FLAT,
        )
        github.set_image('./assets/github.png', 3)

        facebook = BetterButton(
            master=frame_social,
            relief=tk.FLAT,
        )
        facebook.set_image('./assets/facebook.png', 4)

        producers = tk.Label(
            self,
            text="Developers:\n"
                 "\t- Amin Guermazi\n"
                 "\t- Hichem Zouaoui ",
            justify="left"
        )
        github.bind("<Button-1>", lambda e: self.link("https://github.com/Mino260806/motus"))
        facebook.bind("<Button-1>", lambda e: self.link("https://www.facebook.com/MicrosoftPiloteAriana/"))

        greeting.pack()
        main_text.pack()

        gray_frame.pack(padx=5, pady=(0, 10), fill="x")
        gray_letter.pack(padx=10, ipadx=15, ipady=10, side="left")
        gray_description.pack(anchor="center", side="left")
        yellow_frame.pack(padx=5, pady=(0, 10), fill="x")
        yellow_letter.pack(padx=10, ipadx=15, ipady=10, side="left")
        yellow_description.pack(anchor="center", side="left")
        green_frame.pack(padx=5, pady=(0, 10), fill="x")
        green_letter.pack(padx=10, ipadx=15, ipady=10, side="left")
        green_description.pack(anchor="center", side="left")

        producers.pack(anchor="w", padx=20)
        frame_social.pack(side="right")
        facebook.pack(side="right")
        github.pack(side="right")

        return_button = tk.Button(self, text="Ok",
                                  command=lambda: self.root.switch(self.root.gamescreen))
        return_button.place(x=0, y=0, rely=1.0, anchor="sw")

    def show(self):
        self.pack(padx=10, pady=10)

    @staticmethod
    def link(url):
        webbrowser.open(url, new=0, autoraise=True)
