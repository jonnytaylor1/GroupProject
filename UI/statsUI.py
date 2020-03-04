from tkinter import *
from tkinter.ttk import Treeview, Notebook, Separator
from collections import namedtuple

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from typing import List

QuestionStats = namedtuple("QuestionStatistic", ["q_number", "time", "pc_correct", "pc_abandon"])


class StatsTable(Treeview):
    """Using a tree view with no children in the tree allows us to fake a table"""

    def __init__(self, parent, quiz, **kwargs):
        super().__init__(parent, **kwargs)

        self.create_table()

        # no db yet so invent some data
        if quiz==1:
            self.dummy_data = [QuestionStats(1, 20, 70, 30),
                               QuestionStats(2, 50, 50, 9),
                               QuestionStats(4, 40, 30, 5),
                               QuestionStats(5, 10, 60, 10),
                               QuestionStats(6, 90, 10, 90),
                               QuestionStats(10, 15, 40, 4)]
        else:
            self.dummy_data = [QuestionStats(1, 60, 34, 10),
                               QuestionStats(2, 20, 56, 7),
                               QuestionStats(4, 30, 45, 3),
                               QuestionStats(5, 70, 76, 50),
                               QuestionStats(6, 10, 67, 7),
                               QuestionStats(10, 50, 34, 6)]

        self.insert_data(self.dummy_data)

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

    def insert_data(self, data: List[QuestionStats]):
        # FIXME: Dummy datL

        for item in data:
            self.insert("", 0, text=f"{item.q_number}",
                        values=[f"Question {item.q_number}",
                                f"{item.time}s", f"{item.pc_correct}%", f"{item.pc_abandon}%"])

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


class QuizView(Frame):
    """This class provides the view for an individual quiz inside each tab"""
    def __init__(self, parent, quiz, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        stats_table_row_number = 7

        self.table_scrollbar = Scrollbar(self)
        self.stats_table = StatsTable(self, quiz, height=stats_table_row_number, yscrollcommand=self.table_scrollbar.set)
        self.table_scrollbar.config(command=self.stats_table.yview)

        self.data = self.stats_table.dummy_data

        self.stats_table.grid(row=2, column=1, columnspan=2)
        self.table_scrollbar.grid(row=2, column=3, sticky="ns")

        self.separator = Separator(self)
        self.separator.grid(row=3, column=1, columnspan=3, sticky="we")

        self.extra_text = Label(self, text="We can say something here \n about best/worst\n questions")
        self.extra_text.grid(row=4, column=1)

        # FIXME: fake graph
        # graph lives in a Figure
        self.fig = Figure(figsize=(5, 2), dpi=100)
        self.bar_chart = self.fig.add_subplot(111)

        self.bar_chart.bar([i.q_number for i in self.data], [i.time for i in self.data])

        # Figures are drawn on Canvases
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        # Canvases can be added to the grid
        # FIXME: padding
        self.canvas.get_tk_widget().grid(row=4, column=2, pady=10)




class Statistics(Frame):
    """This class provides the statistics view, in table and graphical form"""

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent

        self.hello_world = Label(self, text="Hello World! \n This is where the statistics will be")
        self.hello_world.grid(row=1, column=1, columnspan=2)

        self.tabbed_section = Notebook(self)
        # create frames for tabs
        self.quiz_one = QuizView(self.tabbed_section, 1)
        self.quiz_two = QuizView(self.tabbed_section, 2)
        # attach tabs
        self.tabbed_section.add(self.quiz_one, text="Quiz 1")
        self.tabbed_section.add(self.quiz_two, text="Quiz 2")

        # FIXME: padding
        self.tabbed_section.grid(row=2, column=1, columnspan=2, padx=10)

        self.button = Button(self, text="This button does nothing")
        self.button.grid(row=3, column=1, sticky="e")
        self.button_two = Button(self, text="This button also does nothing")
        self.button_two.grid(row=3, column=2, sticky="w")