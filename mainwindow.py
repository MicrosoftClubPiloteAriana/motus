import tkinter as tk

from aboutscreen import AboutScreen
from cbridge import CBridge
from basescreen import BaseScreen
from gamescreen import GameScreen
from homescreen import HomeScreen


class MainWindow(tk.Frame):
    """
    Main game window:
     - switches between home screen and game screen
     - initializes communication with C

    """
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.root = root
        self.root.title("Motus")
        self.root.resizable(False, False)

        # Initialize communication with C
        self.cbridge = CBridge()
        self.cbridge.init()

        # Initialize screens
        self.gamescreen = GameScreen(self, self.cbridge)
        self.homescreen = HomeScreen(self)
        self.aboutscreen = AboutScreen(self)
        self.gamescreen.hide()
        self.homescreen.hide()
        self.aboutscreen.hide()

        self.active_screen = None

        self.switch(self.gamescreen)

    def show(self):
        """
        Shows the window
        """
        self.pack()

    def switch(self, screen: BaseScreen):
        """
        Switches between screens
        """
        if self.active_screen is not None:
            self.active_screen.hide()
            self.active_screen = screen
        self.active_screen = screen
        screen.show()
