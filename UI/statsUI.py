from tkinter import *
from tkinter.ttk import Treeview
from collections import namedtuple

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

QuestionStatistic = namedtuple("QuestionStatistic", ["q_number", "time", "pc_correct", "pc_abandon"])


class StatsTable(Treeview):
    """Using a tree view with no children in the tree allows us to fake a table"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_table()

        # no db yet so invent some data
        self.dummy_data = [QuestionStatistic("1", "20", "70", "30"),
                           QuestionStatistic("2", "50", "50", "9"),
                           QuestionStatistic("4", "40", "30", "5"),
                           QuestionStatistic("5", "10", "60", "10"),
                           QuestionStatistic("6", "90", "10", "90"),
                           QuestionStatistic("10", "15", "40", "4")]

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

    def insert_data(self, data: QuestionStatistic):
        # FIXME: Dummy data

        for item in data:
            self.insert("", 0, text=item.q_number,
                        values=["Question " + item.q_number,
                                item.time + "s", item.pc_correct + "%", item.pc_abandon + "%"])

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
    """This class provides the statistics view, in table and graphical form"""

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent

        hello_world = Label(self, text="Hello World! \n This is where the statistics will be")
        hello_world.grid(row=1, column=1, columnspan=2)

        stats_table = StatsTable(self)
        stats_table.grid(row=2, column=1, columnspan=2)

        extra_text = Label(self, text="We can say something here \n about best/worst\n questions")
        extra_text.grid(row=3, column=1)

        # FIXME: fake graph
        fig = Figure(figsize=(5, 2), dpi=100)
        bar_chart = fig.add_subplot(111)
        bar_chart.bar([i.q_number for i in stats_table.dummy_data], [i.time for i in stats_table.dummy_data])
        canvas = FigureCanvasTkAgg(fig, master=self) 
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=2)
