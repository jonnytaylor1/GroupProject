from tkinter import *
from UI import *
import time
from datetime import datetime

# this is the main controller for UI pages


class MainUI():

    def __init__(self):
        self.root = Tk()
        self.root.title("Quiz")
        self.root.geometry("750x750")
        self.root.minsize(500, 500)

        self.clock = datetime.now()
        self.listeners = []

        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        self.curr_page = None
        self.prev_page = None

        # specify here which page you would like to add
        self.pages = {"Welcome": Welcome(self),
                      "Settings": Settings(self),
                      "MultipleChoice": MultipleChoice(self),
                      "PackageMenu": PackageMenu(self),
                      "EndScreen": EndScreen(self),
                      "Statistics": Statistics(self),
                      "Hangman": Hangman(self),
                      "Test": Test(self),
                      "Login": LoginPage(self),
                      "ChooseVer": UserTypePage(self),
                      "SettingsMenu": SettingsPage(self)}

        # this is the first page to show
        self.pages["ChooseVer"].show()
        self.update_clock()

    def add_listener(self, func):
        self.listeners.append(func)
        return len(self.listeners) - 1


    def update_clock(self):
        # clock 2 will track real time, clock 1 will be manually changed
        self.clock = datetime.now()

        for listener in self.listeners: listener()

        # Updates the clock every 50 ms
        self.root.after(50, self.update_clock)


    def update_window_size(self):
        self.root.update()
        height = max(self.root.winfo_reqheight(), self.root.winfo_height())
        width = max(self.root.winfo_reqwidth(), self.root.winfo_width())
        self.root.geometry(f'{width}x{height}')

    def run(self):
        self.root.mainloop()
