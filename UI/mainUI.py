from tkinter import *
from UI.welcome import Welcome

class MainUI(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()


root = Tk()
root.title("Quiz")
root.geometry("1000x500")
m = MainUI(root)
Welcome(m)
def run():
    root.mainloop()
