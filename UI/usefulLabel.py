from tkinter import *

class GridLabel(Label):
    def __init__(self, *args, row=None, column=None, sticky=None, pos=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pos:
            try: sticky = pos[2]
            except: pass
            self.grid(row=pos[0], column=pos[1], sticky=sticky)
        else:
            self.grid(row=row, column=column, sticky=sticky)