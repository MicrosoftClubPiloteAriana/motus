from ctypes import *
from pathlib import Path


CFILE = Path(__file__).parent / "gamelogic.so"


class CBridge:
    def __init__(self):
        self.gamelogic = CDLL(str(CFILE))

        self.gamelogic.interpret.argtypes = [ c_char_p ]
        self.gamelogic.interpret.restype = POINTER(c_int)

    def init(self):
        self.gamelogic.init()

    def interpret(self, word: str):
        result = self.gamelogic.interpret(word.encode())
        return result


__all__ = ["CBridge"]
