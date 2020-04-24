from tkinter import *
from UI import *



class Test(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent

    def show(self):
        self.grid()
        self.hb = HoverButton(self, text="click me", command=self.click)
        self.hb.grid()

    def click(self):
        self.hb["state"] = DISABLED
        self.hb["bg"] = "green"