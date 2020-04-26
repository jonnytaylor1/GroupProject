from tkinter import *

class Page(Frame):
    def __init__(self, mainUI):
        super().__init__(mainUI.root)
        self.mainUI = mainUI
        self.created = False

    def before_leaving(self):
        self.grid_forget()
        try: self.scrollbar.grid_forget()
        except: pass

    def create(self): pass

    def before_showing(self): pass

    def show(self, *args, **kwargs):
        try:
            self.mainUI.curr_page.before_leaving()
            self.mainUI.prev_page = self.mainUI.curr_page
        except AttributeError: pass
        self.mainUI.curr_page = self
        if not self.created:
            self.created = True
            self.create()
        self.before_showing(*args, **kwargs)
        self.grid(row=0, column=0, sticky=NSEW)
        self.mainUI.update_window_size()
        return self

    def go_to(self, page):
        return self.mainUI.pages[page].show

    def autoresize_grid(self, *, rows, columns):
        for row in range(rows):
            Grid.rowconfigure(self, row, weight=1)
        for column in range(columns):
            Grid.columnconfigure(self, column, weight=1)


