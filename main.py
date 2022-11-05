import tkinter as tk
from mainwindow import MainWindow
from cbridge import CBridge


if __name__ == "__main__":
    root = tk.Tk()
    window = MainWindow(root)
    window.show()
    root.mainloop()
