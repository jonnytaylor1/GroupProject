from tkinter import *
from tkinter.ttk import Treeview, Notebook, Separator, Style
from collections import namedtuple

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from typing import List

# this function returns a list of named tuples that have question info and statistics
from Quiz.statistics import Statistics as StatDB

StatsCol = namedtuple("StatsCol", ["name", "heading", "type", "width", "anchor"])


class StatsTable(Treeview):
    """Using a tree view with no children in the tree allows us to fake a table"""

    def __init__(self, parent, quiz, **kwargs):
        super().__init__(parent, **kwargs)

        self.table_columns = [StatsCol("number", "#", int, 25, E),
                              StatsCol("question", "Question", str, 350, W),
                              StatsCol("count", "Count", int, 100, E),
                              StatsCol("time", "Mean Time", float, 125, E),
                              StatsCol("correct", "Accuracy", float, 125, E),
                              StatsCol("abandoned", "Abandoned", int, 125, E)]
        self.create_table()

        # no db yet so invent some data
        #if you want to show only stats for questions that are currently loaded into the quiz check if currently assigned like below:
        self.data = [data for data in StatDB().get_overall_stats_old() if data.quiz == quiz and data.currently_assigned]
        self.insert_data(self.data)

        # initial sort by question number after creation, just in case
        self.sort_column(self.table_columns[0], False)

    def create_table(self):
        """Creates the table and sets up the headings. Should only run once"""

        # make individual items in the table unselectable - unless we can think of a use for selection?
        self.configure(selectmode="none")

        self["columns"] = [col.name for col in self.table_columns]

        for col in self.table_columns:
            self.heading(col.name, text=col.heading,
                         command=lambda col=col: self.sort_column(col, False))
            self.column(col.name, width=col.width, anchor=col.anchor)
        # hide the first column which has no heading and is pretty useless
        self["show"] = "headings"

    def insert_data(self, data):
        # FIXME: Dummy data

        for item in data:
            self.insert("", 0, text=f"{item.q_id}",
                        values=[f"{item.q_id}",
                                f"{item.text}",
                                f"{item.successes + item.failures + item.skips + item.abandons}",
                                f"{item.total_time}s",
                                f"{item.successes}%",
                                f"{item.abandons}%"])

    # https://stackoverflow.com/questions/46618459/tkinter-treeview-column-sorting
    def sort_column(self, sort_col, reverse):
        l = [(self.set(k, sort_col.name), k) for k in self.get_children('')]
        l.sort(key=lambda x: sort_col.type(x[0].strip('%s')), reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)

        sort_indicator = "↓"
        if reverse:
            sort_indicator = "↑"

        # reverse sort next time
        for col in self.table_columns:
            if col.name == sort_col.name:
                self.heading(col.name, text=f"{col.heading} {sort_indicator}",
                             command=lambda col=col: self.sort_column(col, not reverse))
            else:
                self.heading(col.name, text=col.heading,
                             command=lambda col=col: self.sort_column(col, False))


class QuizView(Frame):
    """This class provides the view for an individual quiz inside each tab"""

    def __init__(self, parent, quiz, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        stats_table_row_number = 7

        self.table_scrollbar = Scrollbar(self)
        self.stats_table = StatsTable(self, quiz,
                                      height=stats_table_row_number, yscrollcommand=self.table_scrollbar.set)
        self.table_scrollbar.config(command=self.stats_table.yview)

        self.data = self.stats_table.data

        # FIXME: padding
        self.stats_table.grid(row=2, column=1, columnspan=3, padx=(50, 0), pady=(10, 5))
        self.table_scrollbar.grid(row=2, column=4, sticky="ns", padx=(0, 50), pady=(10, 5))

        # self.separator = Separator(self)
        # self.separator.grid(row=3, column=1, columnspan=3, sticky="we")

        # FIXME: fake graph
        # graph lives in a Figure
        self.fig = Figure(figsize=(5, 2), dpi=100)
        self.bar_chart = self.fig.add_subplot(111)

        self.bar_chart.bar([i.q_id for i in self.data], [i.total_time for i in self.data])

        # Figures are drawn on Canvases
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        # Canvases can be added to the grid
        # FIXME: padding
        self.canvas.get_tk_widget().grid(row=4, column=1, columnspan=1, pady=(5, 10))


class BottomButtons(Frame):
    """This class provides the buttons that sit at the bottom of the page"""

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.button = Button(self, text="Export as CSV")
        self.button.grid(row=3, column=0, sticky="e")
        self.button_two = Button(self, text="Export HTML report")
        self.button_two.grid(row=3, column=1, sticky="w")


class Statistics(Frame):
    """This class provides the statistics view, in table and graphical form"""

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.back_button = Button(self, text="< Back", command=self.back)
        self.back_button.grid(row=1, padx=(10, 0), pady=(10, 5), sticky="w")

        # hide border
        # https://groups.google.com/forum/#!topic/comp.lang.tcl/8a6e4tfWJvo
        s = Style(self)
        s.configure('flat.TNotebook', borderwidth=0)
        self.tabbed_section = Notebook(self, style="flat.TNotebook")
        # create frames for tabs
        self.quiz_one = QuizView(self.tabbed_section, 1, borderwidth=0, highlightthickness=0)
        self.quiz_two = QuizView(self.tabbed_section, 2)
        # attach tabs
        self.tabbed_section.add(self.quiz_one, text="Multi-Choice")
        self.tabbed_section.add(self.quiz_two, text="Hangman")

        # FIXME: padding
        self.tabbed_section.grid(row=2, padx=20, sticky="n")

        self.buttons = BottomButtons(self)
        self.buttons.grid(row=3, sticky="n")

    def back(self):
        self.grid_forget()
        self.parent.pages["Welcome"].show()
