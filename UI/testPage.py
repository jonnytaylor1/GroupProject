from tkinter import *
from UI import *



class Test(Page):

    def __init__(self, mainUI):
        super().__init__(mainUI)

    def show(self):
        super().show()
        self.grid()
        self.hb = HoverButton(self, text="click me", command=self.click)
        self.hb.grid()

    def click(self):
        self.hb["state"] = DISABLED
        self.hb["bg"] = "green"