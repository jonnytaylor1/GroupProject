from tkinter import *
from UI import *



class Test(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent

    def show(self):
        self.grid()
        BetterText(self, bgText="Enter here").grid()
        BetterText(self, bgText="Or here").grid()

