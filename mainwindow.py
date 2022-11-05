import tkinter as tk
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

        # Initialize communication with C
        self.cbridge = CBridge()
        self.cbridge.init()

        # Initialize home screen and game screen
        self.gamescreen = GameScreen(self, self.cbridge)
        self.homescreen = HomeScreen(self)
        self.active_screen = None

        self.switch(self.gamescreen)

    def show(self):
        """
        Shows the window
        """
        self.pack()

    def switch(self, screen: BaseScreen):
        """
        Switches between home screen and base screen

        :param screen: GameScreen or HomeScreen
        """
        if self.active_screen is not None:
            self.active_screen.hide()
            self.active_screen = screen
        screen.show()
