from tkinter import *
from UI import *
import time

# this is the main controller for UI pages


class MainUI():

    def __init__(self):
        self.root = Tk()
        self.root.title("Quiz")
        self.root.geometry("750x750")

        self.timer = StringVar()
        self.clock1 = time.time()

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
                      "Test": Test(self)}

        # this is the first page to show
        self.pages["Welcome"].show()
        self.update_clock()


    def update_clock(self):
        # clock 2 will track real time, clock 1 will be manually changed
        self.clock2 = time.time()
        self.diff = self.clock2 - self.clock1
        int_diff = int(self.diff)
        self.timer.set(f"{int_diff // 600}{(int_diff // 60) % 10}:{(int_diff // 10) % 6}{int_diff % 10}")
        # Updates the clock every 100 ms
        self.root.after(100, self.update_clock)


    def update_window_size(self, frame):
        self.root.update()
        height = frame.winfo_reqheight()
        width = frame.winfo_reqwidth()
        self.root.geometry(f'{width + 20}x{height}')

    def run(self):
        self.root.mainloop()
