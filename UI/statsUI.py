from tkinter import *
from tkinter.ttk import Treeview, Notebook, Separator, Style
from collections import namedtuple

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from typing import List

from UI import *

# this function returns a list of named tuples that have question info and statistics
from Quiz.statistics import Statistics as StatDB

StatsCol = namedtuple("StatsCol", ["name", "heading", "type", "width", "anchor"])


class StatsData:
    data = [data for data in StatDB().get_overall_stats()]
    dates = {q.created_at.date().isoformat(): q.created_at.date() for q in data}

    @classmethod
    def available_dates(cls):
        dates_list = list(cls.dates.keys())
        dates_list.sort(reverse=True)
        return dates_list

    @classmethod
    def packages_for_date(cls, date):
        packages_list = list({q.package_name for q in cls.data if q.created_at.date() == date})
        packages_list.sort()
        return packages_list

    @classmethod
    def quizzes_for_package(cls, package, date):
        quiz_list = list({q.quiz for q in cls.get_data_for_date(date) if q.package_name == package})
        quiz_list.sort()
        return quiz_list


    @classmethod
    def get_data(cls, date, package, quiz):
        return [q for q in cls.get_data_for_date(date) if q.package_name == package and q.quiz == quiz]

    @classmethod
    def get_data_for_date(cls, date):
        for q in cls.data:
            print(f"{q.created_at.date()} - {date}")
        return [q for q in cls.data if q.created_at.date() == date]


class StatsTable(Treeview):
    """Using a tree view with no children in the tree allows us to fake a table"""

    def __init__(self, parent, date, package, quiz, **kwargs):
        super().__init__(parent, **kwargs)
        self.date = date
        self.package = package
        self.table_columns = [StatsCol("number", "#", int, 25, E),
                              StatsCol("question", "Question", str, 350, W),
                              StatsCol("count", "Shown", int, 100, E),
                              StatsCol("time", "Mean Time", float, 125, E),
                              StatsCol("correct", "Accuracy", float, 125, E),
                              StatsCol("skipped", "Skipped", float, 125, E),
                              StatsCol("abandoned", "Abandoned", int, 125, E)]
        self.create_table()

        self.data = StatsData.get_data(self.date, self.package, quiz)
        self.insert_data()
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

    def insert_data(self):
        for item in self.data:
            total_times_shown = item.successes + item.failures + item.skips + item.abandons
            self.insert("", 0, text=f"{item.q_id}",
                        values=[f"{item.q_id}",
                                f"{item.text}",
                                f"{total_times_shown}",
                                f"{sum(item.times) / len(item.times):.3f} s",
                                f"{(item.successes / total_times_shown) * 100:.1f}%",
                                f"{(item.skips / total_times_shown) * 100:.1f}%",
                                f"{(item.abandons / total_times_shown) * 100:.1f}%"])

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

    def update_data(self, quiz):
        # https://stackoverflow.com/questions/22812134/how-to-clear-an-entire-treeview-with-tkinter
        self.delete(*self.get_children())
        self.data = StatsData.get_data(self.date, self.package, quiz)
        self.insert_data()


class PackageView(Frame):
    """This class provides the view for an individual quiz inside each tab"""
    stats_table_row_number = 5

    def __init__(self, parent, date, package, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.quiz_to_view = StringVar()
        self.quiz_to_view.set(StatsData.quizzes_for_package(package, date)[0])
        self.quiz_to_view.trace("w", self.update_table)
        self.choose_quiz_label = Label(self, text="Quiz Type:")
        self.choose_quiz_label.grid(row=1, column=1, sticky="e")
        initial_column=2
        for i, quiz_type in enumerate(StatsData.quizzes_for_package(package, date)):
            button = Radiobutton(self, text=quiz_type, variable=self.quiz_to_view,
                                          value=quiz_type)
            button.grid(row=1, column=initial_column+i, sticky="e")

        self.table_scrollbar = Scrollbar(self)
        self.stats_table = StatsTable(self, date, package, self.quiz_to_view.get(),
                                      height=self.stats_table_row_number, yscrollcommand=self.table_scrollbar.set)
        self.table_scrollbar.config(command=self.stats_table.yview)

        # FIXME: padding
        self.stats_table.grid(row=2, column=1, columnspan=4, padx=(50, 0), pady=(10, 5))
        self.table_scrollbar.grid(row=2, column=5, sticky="ns", padx=(0, 50), pady=(10, 5))

        # graph lives in a Figure
        self.fig = Figure(figsize=(4, 2), dpi=100)

        # Figures are drawn on Canvases
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        # Canvases can be added to the grid
        # FIXME: padding
        self.canvas.get_tk_widget().grid(row=4, column=1, columnspan=1, pady=(5, 10))
        self.update_table()

    def update_table(self, *args):
        self.stats_table.update_data(self.quiz_to_view.get())
        self.update_graph()

    def update_graph(self):
        self.fig.clear()
        self.bar_chart = self.fig.add_subplot(xlabel="Question Number", ylabel="Test", frame_on="false")
        x = [i.q_id for i in self.stats_table.data]
        y = [i.abandons for i in self.stats_table.data]
        self.bar_chart.bar(x, y)
        self.canvas.draw()


class BottomButtons(Frame):
    """This class provides the buttons that sit at the bottom of the page"""

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.button = Button(self, text="Export as CSV")
        self.button.grid(row=3, column=0, sticky="e")
        self.button_two = Button(self, text="Export HTML report")
        self.button_two.grid(row=3, column=1, sticky="w")


class Statistics(Page):
    """This class provides the statistics view, in table and graphical form"""

    def __init__(self, mainUI):
        super().__init__(mainUI)
        self.columnconfigure(0, weight=1)
        self.back_button = Button(self, text="< Back", command=lambda: self.go_to("Welcome")())
        self.back_button.grid(row=1, padx=(10, 0), pady=(10, 5), sticky="w")

        self.choose_date_label = Label(self, text="View statistics from event on: ")
        self.choose_date_label.grid(row=1, column=1)
        self.date_to_view = StringVar(name="date")

        self.choose_date_menu = OptionMenu(self, self.date_to_view, *StatsData.available_dates())
        self.date_to_view.set(StatsData.available_dates()[0])
        self.choose_date_menu.grid(row=1, column=2)
        self.date_to_view.trace("w", self.update_ui)
        # hide border
        # https://groups.google.com/forum/#!topic/comp.lang.tcl/8a6e4tfWJvo
        s = Style(self)
        s.configure('flat.TNotebook', borderwidth=0)
        self.tabbed_section = Notebook(self, style="flat.TNotebook")
        # create frames for tabs
        # self.quiz_one = QuizView(self.tabbed_section, 1, borderwidth=0, highlightthickness=0)
        # self.quiz_two = QuizView(self.tabbed_section, 2)
        # # attach tabs
        # self.tabbed_section.add(self.quiz_one, text="Multi-Choice")
        # self.tabbed_section.add(self.quiz_two, text="Hangman")
        #
        # # FIXME: padding
        self.tabbed_section.grid(row=2, columnspan="3", padx=20, sticky="n")
        #
        self.buttons = BottomButtons(self)
        self.buttons.grid(row=3, columnspan="3", sticky="n")
        self.update_ui()

    def update_ui(self, *args):
        new_date = StatsData.dates[self.date_to_view.get()]
        print(f"date = {new_date}")
        print(StatsData.packages_for_date(new_date))
        for tab in self.tabbed_section.tabs():
            self.tabbed_section.forget(tab)

        for package in StatsData.packages_for_date(new_date):
            test_tab = PackageView(self.tabbed_section, new_date, package)
            self.tabbed_section.add(test_tab, text=package)
