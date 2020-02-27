from tkinter import *
# This is a start page for the program
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
#J To remove
        # b2 = Button(self, text = "Settings", font = ("MS", 8, "bold"))
        # b2.grid(row = 4, column = 3, columnspan = 5)
        # b2["command"] = self.go_to_settings
#J Goes to packages menu
        b3 = Button(self, text = "Packages Menu", font = ("MS", 8, "bold"))
        b3.grid(row = 5, column = 3, columnspan = 5)
        b3["command"] = self.go_to_packages

    # goes to  the Multiple choice page
    def start_quiz(self):
        self.grid_forget()
        self.parent.pages["MultipleChoice"].show()

#J To remove
    # # goes to the settings page
    # def go_to_settings(self):
    #     self.grid_forget()
    #     self.parent.pages["Settings"].grid()

    # Go to package page
    def go_to_packages(self):
        self.grid_forget()
        self.parent.pages["PackageMenu"].grid()
