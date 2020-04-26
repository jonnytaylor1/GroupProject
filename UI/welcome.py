from tkinter import *
from UI import *

# This is a start page for the program
class Welcome(Page):

    def show(self):
        super().show()
        self.mainUI.root.geometry("500x500") # decides the size of the window

    def create(self):
        # Creating the grid
        self.autoresize_grid(rows=6, columns=1)

        b_font = ("MS", 14, "bold")
        GridLabel(self, text="Welcome!", font=("MS", 22, "bold"), pos=(0, 0, NSEW))

        #Button goes to multiplechoice quiz
        HoverButton(self, text="Start multiplechoice quiz", font=b_font, pos=(1, 0, NSEW), command=self.go_to("MultipleChoice"))

        #J Goes to packages menu
        HoverButton(self, text="Packages menu", font=b_font, pos=(4, 0, NSEW), command=self.go_to("PackageMenu"))

        #Button goes to statistics
        HoverButton(self, text="View Statistics", font=b_font, pos=(3, 0, NSEW), command=self.go_to("Statistics"))

        #Button goes to hangman
        HoverButton(self, text="Start a game of hangman", font=b_font, pos=(2, 0, NSEW), command=self.go_to("Hangman"))

        #Button goes to a test area for debugging
        # HoverButton(self, text="Test", font=b_font, pos=(5, 0, NSEW), command=self.go_to("Test"))
