from tkinter import *
# This is a start page for the program
class Welcome(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent.root)
        self.create_welcome()

    def create_welcome(self):
        l = Label(self, text = "Welcome!", font = ("MS", 110, "bold"))
        l.grid(row = 2, column = 5, columnspan = 4)
        b1 = Button(self, text = "Multiple Choice Quiz", font = ("MS", 20, "bold"))
        b1.grid(row = 20, column = 5, columnspan = 4,rowspan= 3)
        b1["command"] = self.start_quiz
        b4 = Button(self, text="Hangman", font = ("MS", 20, "bold"), command=lambda x=self: x.go_to_hangman())
        b4.grid(row=25, column=5, columnspan=4, rowspan = 3)
	
#J Goes to packages menu
        b2 = Button(self, text="Packages Menu", font=("MS", 20, "bold"))
        b2.grid(row = 30, column = 5, columnspan=4, rowspan = 3)
        b2["command"] = self.go_to_packages
        b3 = Button(self, text="Statistics", font=("MS", 20, "bold"))
        b3.grid(row=40, column=5, columnspan=4, rowspan = 3)
        b3["command"] = self.go_to_statistics

    # goes to  the Multiple choice page
    def start_quiz(self):
        self.grid_forget()
        self.parent.pages["MultipleChoice"].show()

    # Go to package page
    def go_to_packages(self):
        self.grid_forget()
        self.parent.pages["PackageMenu"].grid()

    def go_to_statistics(self):
        self.grid_forget()
        self.parent.pages["Statistics"].grid()

    def go_to_hangman(self):
        self.grid_forget()
        self.parent.pages["Hangman"].grid()
