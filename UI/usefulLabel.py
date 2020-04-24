from tkinter import *
from UI.easyGrid import EasyGrid

class GridLabel(EasyGrid, Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)