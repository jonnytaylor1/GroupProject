from tkinter import *


class UsefulTable(Frame):
    def __init__(self, parent):
        super().__init__(parent.root)
        self.parent = parent
        self.scrollbar = Scrollbar(self.parent.root, orient="vertical")
        self.scrollbar.grid_forget()
        self.columns = 0
        self.prop_names = []
        self.headings = []
        self.headingsFrame = Frame(self)
        self.headingsFrame.grid(row=0, column=0)
        self.canvas = Canvas(self, width=500, height=200, scrollregion=(0, 0, 500, 200),
                             yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0)
        self.scrollbar["command"] = self.canvas.yview
        self.windowFrame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.windowFrame, anchor=NW)
        self.cell_constructors = []
        self.matrix = []
        self._data = "hoho"

    def add_column(self, *, h_constructor, cell_constructor, property):
        heading = h_constructor(self.headingsFrame)
        self.cell_constructors.append(cell_constructor)
        heading.grid(row=0, column=self.columns)
        self.headings.append(heading)
        self.prop_names.append(property)
        self.columns += 1
        return self

    # @property
    # def data(self):
    #     return self._data
    #
    # @data.setter
    # def data(self, data):
    #     self._data = data*2
    #     print("hello")
    #     self.display_data()
    #     self.refresh()

    def display_data(self):
        print("i am here")
        for row_i, row in enumerate(self._data):
            dis_row = []
            self.matrix.append([dis_row])
            for i, prop in enumerate(self.prop_names):
                cell = self.cell_constructors[i](self.windowFrame, self._data["id"])
                try:
                    cell["text"] = self._data[prop]
                except:
                    pass
                cell.grid(column=i, row=row_i)
                dis_row.append(cell)

    def update_column_width(self):
        self.parent.root.update()
        for col_i in range(self.columns):
            width = 0
            for row in self.matrix:
                width = max(row[col_i].winfo_reqwidth(), width)
            self.headingsFrame.grid_columnconfigure(col_i, minsize=width)
            self.windowFrame.grid_columnconfigure(col_i, minsize=width)

    def refresh(self):
        self.update_column_width()
