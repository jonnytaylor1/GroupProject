from tkinter import *
from UI import *

# This is a start page for the program
class Welcome(Page):
    def __init__(self, mainUI):
        super().__init__(mainUI)

    def show(self):
        super().show()
        self.mainUI.root.geometry("500x500") # decides the size of the window

    def create(self):
        # Creating the grid
        self.autoresize_grid(rows=6, columns=1)

        b_font = ("MS", 8, "bold")
        GridLabel(self, text="Welcome!", font=("MS", 15, "bold"), pos=(0, 0, NSEW))

        #Button goes to multiplechoice quiz
        HoverButton(self, text="Start", font=b_font, pos=(1, 0, NSEW), command=self.go_to("MultipleChoice"))

        #J Goes to packages menu
        HoverButton(self, text="Packages Menu", font=b_font, pos=(2, 0, NSEW), command=self.go_to("PackageMenu"))

        #Button goes to statistics
        HoverButton(self, text="Statistics", font=b_font, pos=(3, 0, NSEW), command=self.go_to("Statistics"))

        #Button goes to hangman
        HoverButton(self, text="Hangman", font=b_font, pos=(4, 0, NSEW), command=self.go_to("Hangman"))

        #Button goes to a test area for debugging
        HoverButton(self, text="Test", font=b_font, pos=(5, 0, NSEW), command=self.go_to("Test"))
