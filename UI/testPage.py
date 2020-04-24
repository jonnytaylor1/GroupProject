from tkinter import *
from UI import *
from UI.hoverButton import HoverOptionMenu


class Test(Page):

    def __init__(self, mainUI):
        super().__init__(mainUI)

    def show(self):
        super().show()
        self.grid()
        var = StringVar()
        var.set("hohoho")
        self.opts = OptionMenu(self, var, "hoh", "hello", "there")
        self.opts.configure(bg ="#e8e6e6")
        self.opts.configure(fg="#000000")
        # self.opts.configure(selectbackground ="#a6a6a6")
        # self.opts.configure(selectforeground="#ffffff")
        self.opts.grid()


    def click(self):
        self.hb["state"] = DISABLED
        self.hb["bg"] = "green"