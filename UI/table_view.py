from tkinter import *
from UI import EasyGrid

class TableView(Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.parent = parent
        self.root = root
        self.scrollbar = Scrollbar(self.root, orient="vertical")
        self.scrollbar.grid_forget()
        self.columns = 0
        self.prop_names = []
        self.headings = []
        self.headingsFrame = Frame(self)
        self.headingsFrame.pack(fill=X)
        self.canvas = Canvas(self, width=500, height=200, scrollregion=(0, 0, 500, 200),
                             yscrollcommand=self.scrollbar.set)
        self.canvas.pack(fill=BOTH, expand=1)
        self.scrollbar["command"] = self.canvas.yview
        self.windowFrame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.windowFrame, anchor=NW)
        self.cell_constructors = []

    def start(self):
        self.root.bind("<Configure>", self.autoresizer)

    def end(self):
        self.root.unbind("<Configure>")
        self.scrollbar.grid_forget()

    def autoresizer(self, e):
        if (e.widget == self.root):
            w_height = self.windowFrame.winfo_reqheight()
            if (w_height > self.canvas.winfo_height()) and w_height > 200:
                self.scrollbar.grid(row=0, column=1, sticky=NSEW)
                self.canvas["scrollregion"] = (0, 0, 0, w_height)
            else:
                self.scrollbar.grid_forget()

    def add_column(self, *, title=None, h_constructor=None, cell_constructor=None, property=""):
        try:
            heading = h_constructor(self.headingsFrame)
        except:
            heading = Label(self.headingsFrame, text=title)
        self.headings.append(Cell(heading, row=0, column=self.columns))
        if cell_constructor:
            self.cell_constructors.append(cell_constructor)
        else:
            self.cell_constructors.append(lambda f, id: Label(f))
        self.prop_names.append(property)
        self.columns += 1
        return self

    def cell(self, *, row, column):
        self._curr_cell = self.matrix[row][column]
        return self

    def get_cell(self, *, row, column):
        return self.matrix[row][column]

    def set_cell(self, *, row, column, func):
        self.matrix[row][column].contents = func(self.windowFrame)
        self.refresh()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.display_data()
        self.refresh()

    def display_data(self):
        self.matrix = []
        self.windowFrame.destroy()
        self.windowFrame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.windowFrame, anchor=NW)
        self.start()

        for row_i, row in enumerate(self._data):
            dis_row = []
            self.matrix.append(dis_row)
            for i, prop in enumerate(self.prop_names):
                tkinter_obj = self.cell_constructors[i](self.windowFrame, row_i)
                c = Cell(tkinter_obj, column=i, row=row_i)
                try:
                    c.contents["text"] = row[prop]
                except:
                    pass
                dis_row.append(c)
        self.refresh()

    def update_column_width(self):
        self.root.update()
        for col_i in range(self.columns):
            width = 0
            for row in self.matrix:
                width = max(row[col_i].contents.winfo_reqwidth(), width)
            width = max(width, self.headings[col_i].contents.winfo_reqwidth())
            self.headingsFrame.grid_columnconfigure(col_i, minsize=width)
            self.windowFrame.grid_columnconfigure(col_i, minsize=width)

    def refresh(self):
        self.update_column_width()

class Cell:
    def __init__(self, contents, *, column=None, row=None):
        self._contents = contents
        try:
            self.column = column
            self.row = row
            self.unhide()
        except:
            pass

    def hide(self):
        self._contents.grid_forget()

    def unhide(self):
        self._contents.grid(row=self.row, column=self.column)

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, new_contents):
        try:
            self.hide()
        except:
            pass
        self._contents = new_contents
        try:
            self.unhide()
        except:
            pass