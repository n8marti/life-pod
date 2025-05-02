from tkinter import IntVar
from tkinter import Toplevel
from tkinter import ttk


class LengthWindow:
    def __init__(self, text):
        self.value = None
        self.win = Toplevel()
        self.frame = ttk.Frame(self.win)
        self.frame.pack()

        self.var = IntVar()
        ttk.Label(self.frame, text=text)
        ttk.Entry(self.frame, textvariable=self.var)
        ttk.Button(self.frame, text="OK", command=self.set_value)
        for w in self.frame.winfo_children():
            w.pack()

    def set_value(self):
        print('setting var value')
        self.value = self.var.get()
        self.win.destroy()


class PickPlayerWindow:
    def __init__(self):
        self.value = None
        self.win = Toplevel()
        self.win.title("Pick Player")
        self.frame = ttk.Frame(self.win)
        self.frame.pack()

        ttk.Button(self.frame, text="Red", command=self.select_red)
        ttk.Button(self.frame, text="Yellow", command=self.select_yellow)
        ttk.Button(self.frame, text="Green", command=self.select_green)
        ttk.Button(self.frame, text="Blue", command=self.select_blue)
        for w in self.frame.winfo_children():
            w.pack()
    
    def set_player(self, color):
        self.value = color
        print(self.value)
        self.win.destroy()

    def select_red(self):
        self.set_player('red')

    def select_yellow(self):
        self.set_player('yellow')
    
    def select_green(self):
        self.set_player('green')

    def select_blue(self):
        self.set_player('blue')


class PlayerWindow:
    def __init__(self, player):
        self.win = Toplevel()
        self.win.title(str(player))
        self.frame = ttk.Frame(self.win)
        self.frame.pack()

        self.moneyvar = IntVar()
        row = 0
        ttk.Label(self.frame, text="Money:").grid(column=0, row=row)
        ttk.Label(self.frame, textvariable=self.moneyvar).grid(column=1, row=row)
        row += 1
        self.lifevar = IntVar()
        ttk.Label(self.frame, text="Life points:").grid(column=0, row=row)
        ttk.Label(self.frame, textvariable=self.lifevar).grid(column=1, row=row)
        row += 1
        ttk.Button(self.frame, text="Roll")


class MainWindow(ttk.Frame):
    def __init__(self, app):
        self.root = app.root
        self.root.title("LIFE Twists & Turns")
        ttk.Button(self.root, text="Start", command=app.ask_player).pack()
