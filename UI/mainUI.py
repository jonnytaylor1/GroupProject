from tkinter import *
from UI.welcome import Welcome
from UI.settings import Settings
from UI.multiple_choice import MultipleChoice

class MainUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("Quiz")
        self.root.geometry("1000x500")
        self.pages = [Welcome(self), Settings(self), MultipleChoice(self)]
        self.curr_window = self.pages[0]

    def run(self):
        self.curr_window.grid()
        self.root.mainloop()





