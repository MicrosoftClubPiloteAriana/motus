import tkinter as tk
from cbridge import CBridge
from basescreen import BaseScreen
from gamescreen import GameScreen
from homescreen import HomeScreen


class MainWindow(tk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.root = root
        self.root.title("Motus")

        self.cbridge = CBridge()
        self.cbridge.init()

        self.gamescreen = GameScreen(self, self.cbridge)
        self.homescreen = HomeScreen(self)
        self.active_screen = None

        self.switch(self.gamescreen)

    def show(self):
        self.pack()

    def switch(self, screen: BaseScreen):
        if self.active_screen is not None:
            self.active_screen.hide()
            self.active_screen = screen
        screen.show()
