import tkinter as tk


class BaseScreen(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)

        self.root = root

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack()
