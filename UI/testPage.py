from tkinter import *
from UI import *



class Test(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent

    def show_table(self):
        self.table = TableView(self)
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text="Hello there"),
            cell_constructor=lambda fr, id: Label(fr),
            property="name"
        )
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text="Column 2"),
            cell_constructor=lambda fr, id: Label(fr),
            property="age"
        )
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text="Column 2"),
            cell_constructor=lambda fr, id: Label(fr),
            property="age"
        )
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text="Column 2"),
            cell_constructor=lambda fr, id: Label(fr),
            property="age"
        )
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text="Column 2"),
            cell_constructor=lambda fr, id: Label(fr),
            property="age"
        )
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text="Column 2"),
            cell_constructor=lambda fr, id: Label(fr),
            property="age"
        )
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text="Column 2"),
            cell_constructor=lambda fr, id: Label(fr),
            property="age"
        )
        self.table.add_column(
            h_constructor=lambda fr: Label(fr, text=""),
            cell_constructor=lambda fr, id: Button(fr, text="Save"),
            property="svButton"
        )
        self.table.data = [
            {"name": "Alex", "age": 24, "id": 1},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Alex", "age": 24, "id": 1},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Alex", "age": 24, "id": 1},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "Patrick", "age": 30, "id": 2},
            {"name": "lkasdfklsadflkj;sadfkj;l", "age": 30, "id": 2},
        ]
        self.table.grid()

        self.table.set_cell(func=lambda fr: Label(fr, text="hacked"), row=1, column=1)


    def show(self):
        self.grid()
        self.show_table()

