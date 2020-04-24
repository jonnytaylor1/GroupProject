from tkinter import *

class Page(Frame):
    def __init__(self, mainUI):
        super().__init__(mainUI.root)
        self.mainUI = mainUI
        self.created = False

    def show(self):
        try:
            self.mainUI.curr_page.grid_forget()
            self.mainUI.prev_page = self.mainUI.curr_page
        except: pass
        self.mainUI.curr_page = self
        self.grid(row=0, column=0, sticky=NSEW)
        self.created = True
        try:
            self.create()
        except: pass
        return self

    def go_to(self, page):
        return self.mainUI.pages[page].show

    def autoresize_grid(self, *, rows, columns):
        for row in range(rows):
            Grid.rowconfigure(self, row, weight=1)
        for column in range(columns):
            Grid.columnconfigure(self, column, weight=1)


