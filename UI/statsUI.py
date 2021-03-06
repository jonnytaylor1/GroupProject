from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Treeview, Notebook, Style
from collections import namedtuple

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import csv as csv
from typing import List

from UI import *

# this function returns a list of named tuples that have question info and statistics
from Quiz.statistics import Statistics as StatDB

StatsCol = namedtuple("StatsCol", ["name", "heading", "type", "width", "anchor"])

def total_times_shown(question):
    return question.successes + question.failures + question.skips + question.abandons


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
            total_times = total_times_shown(item)
            self.insert("", 0, text=f"{item.q_id}",
                        values=[f"{item.q_id}",
                                f"{item.text}",
                                f"{total_times}",
                                f"{sum(item.times) / len(item.times):.3f} s",
                                f"{(item.successes / total_times) * 100:.1f}%",
                                f"{(item.skips / total_times) * 100:.1f}%",
                                f"{(item.abandons / total_times) * 100:.1f}%"])
        self.sort_column(self.table_columns[0], False)

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
        self.stats_table.grid(row=2, column=1, columnspan=4, padx=(50, 0), pady=(10, 20))
        self.table_scrollbar.grid(row=2, column=5, sticky="ns", padx=(0, 50), pady=(10, 20))

        # graph lives in a Figure
        self.fig = Figure(figsize=(10, 3), dpi=100)
        # Figures are drawn on Canvases
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        # Canvases can be added to the grid
        # FIXME: padding
        self.canvas.get_tk_widget().grid(row=4, column=1, columnspan=5, pady=(5, 10))
        self.update_table()

    def update_table(self, *args):
        self.stats_table.update_data(self.quiz_to_view.get())
        self.update_graph()

    def update_graph(self):
        self.fig.clear()
        plots = []
        for i in range(0, 3):
            plots.append(self.fig.add_subplot(1, 3, i+1))
            plots[i].spines['right'].set_visible(False)
            plots[i].spines['top'].set_visible(False)
        times_x = [j.q_id for j in self.stats_table.data]
        times_y = [j.times for j in self.stats_table.data]
        boxplot = plots[0].boxplot(times_y, showfliers=False, positions=times_x, patch_artist=True)
        plots[0].set_ylabel("Time to answer (s)")
        colors = ['pink', 'lightblue', 'lightgreen']
        for patch in boxplot['boxes']:
            patch.set_facecolor("deepskyblue")
        success_x = [j.q_id for j in self.stats_table.data]
        success_y = [(j.successes / total_times_shown(j)) * 100 for j in self.stats_table.data]
        plots[1].bar(success_x, success_y, color="mediumseagreen", label="accuracy")
        plots[1].set_xticks(success_x)
        plots[1].set_ylabel("% answered accurately")
        plots[1].legend()
        skip_x = [j.q_id for j in self.stats_table.data]
        skip_y = [(j.skips / total_times_shown(j)) * 100 for j in self.stats_table.data]
        abandon_y = [(j.abandons / total_times_shown(j)) * 100 for j in self.stats_table.data]
        plots[2].bar(skip_x, skip_y, label="skipped")
        plots[2].bar(skip_x, abandon_y, bottom=skip_y, label="abandoned")
        plots[2].set_xticks(skip_x)
        plots[2].set_ylabel("% skipped/abandoned")
        plots[2].legend()
        self.fig.tight_layout()
        self.canvas.draw()


class BottomButtons(Frame):
    """This class provides the buttons that sit at the bottom of the page"""

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

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

        # # FIXME: padding
        self.tabbed_section.grid(row=2, columnspan="3", padx=20, sticky="n")
        #
        self.button = Button(self, text="Export event statistics as CSV", command=self.csv_export)
        self.button.grid(row=3, columnspan="3", pady=10, sticky="n")
        self.update_ui()

    def update_ui(self, *args):
        new_date = StatsData.dates[self.date_to_view.get()]
        for tab in self.tabbed_section.tabs():
            self.tabbed_section.forget(tab)

        for package in StatsData.packages_for_date(new_date):
            test_tab = PackageView(self.tabbed_section, new_date, package)
            self.tabbed_section.add(test_tab, text=package)


    def csv_export(self):
        date = StatsData.dates[self.date_to_view.get()]

        file_path = filedialog.asksaveasfilename(filetypes=(("CSV", ".csv"),), initialfile=date)

        # code taken from https://docs.python.org/3/library/csv.html
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(("package name", "quiz", "question id", "question text",
                                    "total times shown", "successful answers", "skips", "abandons"))
                for package in StatsData.packages_for_date(date):
                    for quiz in StatsData.quizzes_for_package(package, date):
                        for q in StatsData.get_data(date, package, quiz):
                            csvwriter.writerow((q.package_name, q.quiz, q.q_id, q.text,
                                                total_times_shown(q), q.successes, q.skips, q.abandons))
