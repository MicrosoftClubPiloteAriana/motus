import tkinter as tk


class BetterButton(tk.Button):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.image = None

    def set_image(self, path, downscale):
        self.image = tk.PhotoImage(file=path)
        self.image = self.image.subsample(downscale, downscale)
        self["image"] = self.image
