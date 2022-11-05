from ctypes import *
from pathlib import Path


CFILE = Path(__file__).parent / "gamelogic.so"


class CBridge:
    """
    Ensures communication between Python and C
    """
    def __init__(self):
        self.gamelogic = CDLL(str(CFILE))

        # configuring the arguments type and return type of
        # int* interpret(const char* word)
        self.gamelogic.interpret.argtypes = [c_char_p]
        self.gamelogic.interpret.restype = POINTER(c_int)

    def init(self):
        """
        Initializes words list in C
        """
        self.gamelogic.init()

    def interpret(self, word: str):
        """
        Checks the try of the player
        :param word: The word to check
        :return: An array of int values.
        Refer to the documentation in "gamelogic.c" for more details
        """
        result = self.gamelogic.interpret(word.encode())
        return result

    def reset_word(self):
        """
        Picks up a new word randomly
        """
        self.gamelogic.reset_word()


__all__ = ["CBridge"]
