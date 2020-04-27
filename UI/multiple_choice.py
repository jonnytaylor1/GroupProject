from tkinter import *
import time
from UI.hoverButton import HoverButton
import tkinter.messagebox
from Quiz.multiplechoice import Multiplechoice
from Quiz.statistics import Statistics
from UI import *
from UI.quizSession import create_vars, QuizSession
from UI.components.timerlabel import TimerLabel



class MultipleChoice(Page):
    def __init__(self, mainUI):
        super().__init__(mainUI)
        self.vars = create_vars()

    def show(self):
        super().show()
        self.mainUI.root.geometry("750x500")
        # get data on questions from the model
        self.session = QuizSession(vars=self.vars).fetch_questions()
        self.before_question()

    # reset everything and load next question
    def before_question(self):
        self.timer.start()
        self.b_skip.configure(text="Skip")
        if not self.session.is_finished():
            self.session.start_question()
            for choice in self.choices:
                choice.configure(state=NORMAL, bg="#e8e6e6")
        else: self.go_to("EndScreen")(self.session)

    def create(self):
        self.autoresize_grid(rows=8, columns=3)
        GridLabel(self, textvariable=self.vars.q_num, pos=(0, 0, NSEW), cspan=3)
        GridLabel(self, textvariable=self.vars.prompt, pos=(1, 0, NSEW), cspan=3)
        self.l_timer = GridLabel(self, text="Time Elapsed:", pos=(2, 0, NSEW))
        self.timer = TimerLabel(self, mainUI=self.mainUI, pos=(2, 1, NSEW))
        self.b_skip = HoverButton(self, text="Skip", command=self.next_q, pos=(3, 0, NSEW))
        self.b_restart = HoverButton(self, text="Restart", command=self.restart, pos=(3, 1, NSEW))
        self.b_end = HoverButton(self, text="End Quiz", command=self.end_quiz, pos=(3, 2, NSEW))
        self.choices = []
        for i in range(4):
            b = HoverButton(self, textvariable=self.vars.choices[i], command=lambda i=i: self.answer(i), pos=(4+i, 0, NSEW), cspan=3)
            self.choices.append(b)

    def answer(self, i):
        # lock ability to choose another answer
        for choice in self.choices: choice.configure(state=DISABLED)
        self.choices[i].configure(bg="green" if self.session.answer(i) else "red")
        self.timer.pause()
        self.b_skip.configure(text="Next")

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
