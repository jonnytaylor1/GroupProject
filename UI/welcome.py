from tkinter import *
from UI.multiple_choice import MultipleChoice
from UI.settings import Settings
class Welcome(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent.root)
        self.create_welcome()

    def create_welcome(self):
        l = Label(self, text = "Welcome!", font = ("MS", 15, "bold"))
        l.grid(row = 2, column = 2, columnspan = 4)
        b1 = Button(self, text = "Start", font = ("MS", 8, "bold"))
        b1.grid(row = 3, column = 3, columnspan = 5)
        b1["command"] = self.start_quiz
        b2 = Button(self, text = "Settings", font = ("MS", 8, "bold"))
        b2.grid(row = 4, column = 3, columnspan = 5)
        b2["command"] = self.go_to_settings

    def start_quiz(self):
        self.grid_forget()
        self.parent.pages[2].grid()

    def go_to_settings(self):
        self.grid_forget()
        self.parent.pages[1].grid()
