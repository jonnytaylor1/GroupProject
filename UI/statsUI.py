from tkinter import *


class Statistics(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        helloworld = Label(self, text="Hello World! \n This is where the statistics will be")
        helloworld.grid(row = 1, column = 1)
