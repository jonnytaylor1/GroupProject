from tkinter import *
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
        label = Label(self, text="Welcome!", font=("MS", 15, "bold"))
        label.grid(row=0, column=0, sticky=N+S+E+W)

        b1 = Button(self, text="Start", font = ("MS", 8, "bold"))
        self.bind_hover(b1)
        b1.grid(row=1, column=0, sticky=N+S+E+W)

        b1["command"] = self.start_quiz

        #J Goes to packages menu

        b2 = Button(self, text="Packages Menu", font=("MS", 8, "bold"))
        self.bind_hover(b2)
        b2.grid(row = 2, column=0, sticky=N+S+E+W)

        b2["command"] = self.go_to_packages

        b3 = Button(self, text="Statistics", font=("MS", 8, "bold"))
        self.bind_hover(b3)
        b3.grid(row=3, column=0, sticky=N+S+E+W)
        b3["command"] = self.go_to_statistics

        b4 = Button(self, text="Hangman", font=("MS", 8, "bold"),command=lambda x=self: x.go_to_hangman())
        self.bind_hover(b4)
        b4.grid(row=4, column=0, sticky=N+S+E+W)

    # Bind Hover
    @staticmethod
    def bind_hover(element):
        """

        :param element: Button element on which the hover is applied
        :return:
       """
        element.bind("<Enter>", lambda event, h=element: h.configure(bg="#a6a6a6", fg="#ffffff"))
        element.bind("<Leave>", lambda event, h=element: h.configure(bg="#e8e6e6", fg="#000000"))
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
