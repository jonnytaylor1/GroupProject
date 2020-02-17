from tkinter import *
from UI import *

class MainUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("Quiz")
        self.root.geometry("1000x500")
        self.pages = {"Welcome": Welcome(self),
                      "Settings": Settings(self),
                      "MultipleChoice": MultipleChoice(self)}
        self.curr_window = self.pages["Welcome"]

    def run(self):
        self.curr_window.grid()
        self.root.mainloop()





