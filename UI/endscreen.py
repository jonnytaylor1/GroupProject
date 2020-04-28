from tkinter import *
from collections import namedtuple
from UI.page import Page
from UI.easyGrid import EasyGrid
from UI.usefulLabel import GridLabel
from UI.hoverButton import HoverButton

class Stats:
    def __init__(self):
        self.incorrect_qs = 0
        self.correct_qs = 0
        self.skipped_qs = 0
        self.history = []


class EndScreen(Page):

    def __init__(self, mainUI):
        super().__init__(mainUI)
        Stats = namedtuple("Stats", ["incorrect_qs", "correct_qs", "skipped_qs",
                                     "total_qs", "total_time"])
        self.stats = Stats(StringVar(), StringVar(), StringVar(), StringVar(), StringVar())
    # fill statistics for the quiz

    def show(self, session):
        super().show()
        self.mainUI.root.geometry("1000x500")
        self.stats.incorrect_qs.set(session.incorrect_questions)
        self.stats.correct_qs.set(session.correct_questions)
        self.stats.skipped_qs.set(session.skipped_qs)
        self.stats.total_qs.set(len(session.history))
        self.stats.total_time.set(f"{round(session.time, 2)}s")
        self.h_result.set(history=session.history)

    def create(self):
        self.autoresize_grid(rows=10, columns=3)

        GridLabel(self, text="Incorrect Answers:", pos=(0, 0))
        GridLabel(self, text="Correct Answers:", pos=(1, 0))
        GridLabel(self, text="Skipped Answers:", pos=(2, 0))
        GridLabel(self, text="Total Questions:", pos=(3, 0))
        GridLabel(self, text="Total Time Spent:", pos=(4, 0))

        self.l_incorrect_answers = GridLabel(self, textvariable=self.stats.incorrect_qs, pos=(0, 1))
        self.l_correct_answers = GridLabel(self, textvariable=self.stats.correct_qs, pos=(1, 1))
        self.l_skipped_answers = GridLabel(self, textvariable=self.stats.skipped_qs, pos=(2, 1))
        self.l_total_answers = GridLabel(self, textvariable=self.stats.total_qs, pos=(3, 1))
        self.l_total_time = GridLabel(self, textvariable=self.stats.total_time, pos=(4, 1))

        HoverButton(self, text="Menu", command=self.go_to("Welcome"), pos=(5, 0, NSEW), cspan=2)
        HoverButton(self, text="Restart", command=lambda: self.mainUI.prev_page.show(), pos=(6, 0, NSEW), cspan=2)

        self.h_result = HistoryResult(self, pos=(0, 2))

class HistoryResult(EasyGrid, Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.rows = []

    def set(self, *, history):
        for i, q in enumerate(history):
            try: l = self.rows[i]
            except:
                l = GridLabel(self, anchor=W,  justify='right', pos=(i, 0, W), wraplength=350)
                self.rows.append(l)
            text = f"{i + 1}. {q.prompt} "
            if q.status == "correct":
                l.configure(fg="green")
                text += f"{q.choices[0]}."
            elif q.status == "incorrect":
                l.configure(fg="red")
                text += f"{q.answer}. (Correct: {q.choices[0]})"
            elif q.status == "skipped" or "abandoned":
                l.configure(fg="grey")
                text += f"Skipped. (Correct: {q.choices[0]})"
            text += f" Time spent: {q.get_time()}s"
            l.configure(text=text)