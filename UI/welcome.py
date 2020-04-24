from tkinter import *
from UI import *

# This is a start page for the program


class Welcome(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent.root)
        self.show()

    def show(self):
        self.parent.root.geometry("500x500") # decides the size of the window

        # Make responsive grid
        self.grid(row=0, column=0, sticky=N+S+E+W)
        Grid.rowconfigure(self.parent.root, 0, weight=1)
        Grid.columnconfigure(self.parent.root, 0, weight=1)
        self.grid()
        self.create_welcome()

    def create_welcome(self):
        # Creating the grid
        for rows in range(6):   # Number of rows
            Grid.rowconfigure(self, rows, weight=1)
        for columns in range(1):  # Number of columns
            Grid.columnconfigure(self, columns, weight=1)

        b_font = ("MS", 8, "bold")
        GridLabel(self, text="Welcome!", font=("MS", 15, "bold"), pos=(0, 0, NSEW))

        #Button goes to multiplechoice quiz
        HoverButton(self, text="Start", font=b_font, pos=(1, 0, NSEW), command=self.start_quiz)

        #J Goes to packages menu
        HoverButton(self, text="Packages Menu", font=b_font, pos=(2, 0, NSEW), command=self.go_to_packages)

        #Button goes to statistics
        HoverButton(self, text="Statistics", font=b_font, pos=(3, 0, NSEW), command=self.go_to_statistics)

        #Button goes to hangman
        HoverButton(self, text="Hangman", font=b_font, pos=(4, 0, NSEW), command=self.go_to_hangman)

        #Button goes to a test area for debugging
        # HoverButton(self, text="Test", font=b_font, pos=(5, 0, NSEW), command=self.go_to_test)

    # goes to  the Multiple choice page

    def start_quiz(self):
        self.grid_forget()
        self.parent.pages["MultipleChoice"].show()

    # Go to package page
    def go_to_packages(self):
        self.grid_forget()
        self.parent.pages["PackageMenu"].show()

    def go_to_statistics(self):
        self.grid_forget()
        self.parent.pages["Statistics"].grid()

    def go_to_hangman(self):
        self.grid_forget()
        self.parent.pages["Hangman"].grid()

    def go_to_test(self):
        self.grid_forget()
        self.parent.pages["Test"].show()
