from tkinter import *
from tkinter.ttk import Treeview


class StatsTable(Treeview):
    """Using a tree view with no children in the tree allows us to fake a table"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_table()

        self.insert_data()

        # initial sort by question number after creation, just in case
        self.sort_column("name", float, False)

    def create_table(self):
        """Creates the table and sets up the headings. Should only run once"""

        # make individual items in the table unselectable - unless we can think of a use for selection?
        self.configure(selectmode="none")

        self["columns"] = ["name", "time", "correct", "abandoned"]

        self.heading("name", text="Question Number", command=lambda: self.sort_column("name", float, False))
        self.heading("time", text="mean time", command=lambda: self.sort_column("time", float, False))
        self.heading("correct", text="% correct", command=lambda: self.sort_column("correct", float, False))
        self.heading("abandoned", text="% abandoned", command=lambda: self.sort_column("abandoned", float, False))

        # hide the first column which has no heading and is pretty useless
        self["show"] = "headings"

    def insert_data(self):
        # FIXME: Dummy data
        self.insert("", 0, text="Question 1", values=["Question 1", "20s", "70%", "30%"])
        self.insert("", 1, text="Question 2", values=["Question 2", "50s", "50%", "9%"])
        self.insert("", 1, text="Question 3", values=["Question 3", "30s", "20%", "3%"])
        self.insert("", 1, text="Question 4", values=["Question 4", "40s", "30%", "5%"])
        self.insert("", 1, text="Question 5", values=["Question 5", "10s", "60%", "10%"])
        self.insert("", 1, text="Question 6", values=["Question 6", "90s", "10%", "90%"])
        self.insert("", 1, text="Question 10", values=["Question 10", "15s", "40%", "4%"])

    # https://stackoverflow.com/questions/46618459/tkinter-treeview-column-sorting
    def sort_column(self, col, key, reverse):
        l = [(self.set(k, col), k) for k in self.get_children('')]
        l.sort(key=lambda x: key(x[0].strip('%Question')), reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)

        # reverse sort next time
        # TODO: Look at this, should it change other cols sorts as well?
        self.heading(col, command=lambda: self.sort_column(col, key, not reverse))


class Statistics(Frame):
    """This class provides the statistics view, in table or graphical form"""
    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent

        hello_world = Label(self, text="Hello World! \n This is where the statistics will be")
        hello_world.grid(row=1, column=1)

        stats_table = StatsTable(self)
        stats_table.grid(row=2, column=1)
