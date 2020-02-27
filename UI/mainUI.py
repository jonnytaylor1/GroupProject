from tkinter import *
from UI import *
import time

class MainUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("Quiz")
        self.root.geometry("1000x500")
        self.timer = StringVar()
        self.clock1 = time.time()
        self.pages = {"Welcome": Welcome(self),
                      "Settings": Settings(self),
                      "MultipleChoice": MultipleChoice(self),
                      "EndScreen": EndScreen(self)}
        self.curr_window = self.pages["Welcome"]
        self.update_clock()

    def update_clock(self):
        self.clock2 = time.time()
        self.diff = self.clock2 - self.clock1
        int_diff = int(self.diff)
        self.timer.set(f"{int_diff // 600}{(int_diff // 60) % 10}:{(int_diff // 10) % 6}{int_diff % 10}")
        self.root.after(100, self.update_clock)

    def run(self):
        self.curr_window.grid()
        self.root.mainloop()





