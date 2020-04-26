from tkinter import *
import time
from UI.hoverButton import HoverButton
import tkinter.messagebox
from Quiz.multiplechoice import Multiplechoice
from Quiz.statistics import Statistics
from UI import *
from UI.quizSession import Vars, QuizSession
from collections import namedtuple



class MultipleChoice(Page):
    def __init__(self, mainUI):
        super().__init__(mainUI)
        self.vars = Vars(StringVar(), StringVar(), [StringVar(), StringVar(), StringVar(), StringVar()])

    def show(self):
        super().show()
        self.mainUI.root.geometry("750x500")
        # get data on questions from the model
        # initialize the stats for the quiz at the start
        self.session = QuizSession(vars=self.vars).fetch_questions()
        self.before_question()

    # reset everything and load next question
    def before_question(self):
        self.mainUI.clock1 = time.time()
        self.mainUI.timer.set("00:00")
        self.timer.show()
        self.l_timer.show()
        self.b_skip.configure(text="Skip")
        if not self.session.is_finished():
            self.session.start_question()
            for choice in self.choices:
                choice.configure(state=NORMAL, bg="#e8e6e6")
        else:
            self.go_to("EndScreen")(self.session)

    def create(self):
        self.autoresize_grid(rows=8, columns=3)
        GridLabel(self, textvariable=self.vars.q_num, pos=(0, 0, NSEW), cspan=3)
        GridLabel(self, textvariable=self.vars.prompt, pos=(1, 0, NSEW), cspan=3)
        self.l_timer = GridLabel(self, text="Time Elapsed:", pos=(2, 0, NSEW))
        self.timer = GridLabel(self, textvariable=self.mainUI.timer, pos=(2, 1, NSEW))
        self.b_skip = HoverButton(self, text="Skip", command=self.next_q, pos=(3, 0, NSEW))
        self.b_restart = HoverButton(self, text="Restart", command=self.restart, pos=(3, 1, NSEW))
        self.b_end = HoverButton(self, text="End Quiz", command=self.end_quiz, pos=(3, 2, NSEW))
        self.choices = []
        for i in range(4):
            b = HoverButton(self, textvariable=self.vars.choices[i], command=lambda i=i: self.answer(i), pos=(4+i, 0, NSEW), cspan=3)
            self.choices.append(b)

    def answer(self, i):

        for choice in self.choices:
            # lock ability to choose another answer
            choice.configure(state=DISABLED)
        self.choices[i].configure(bg="green" if self.session.answer(i) else "red")
        self.timer.hide()
        self.l_timer.hide()
        self.b_skip.configure(text="Next")
            # if not self.session.is_finished():
            # else:

    def next_q(self):
        if self.session.ongoing_question(): self.session.skip()
        self.before_question()

    def restart(self):
        if self.session.ongoing_question(): self.session.abandon()
        self.show()

    # record as abandoned question when you end quiz prematurely
    def end_quiz(self):
        if self.session.ongoing_question(): self.session.abandon()
        # show final statistics for the quiz
        self.go_to("EndScreen")(self.session)

# Generate the end screen frame


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

        HoverButton(self, text="Menu", command=self.go_to("Welcome"), pos=(5, 0, NSEW))
        HoverButton(self, text="Restart", command=self.go_to("MultipleChoice"), pos=(5, 1, NSEW))

        self.h_result = HistoryResult(self, pos=(0, 2))

class HistoryResult(EasyGrid, Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.rows = []

    def set(self, *, history):
        for i, q in enumerate(history):
            try: l = self.rows[i]
            except:
                l = GridLabel(self, anchor='w', justify='left', pos=(i, 0))
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