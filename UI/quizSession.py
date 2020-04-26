from tkinter import *
from datetime import datetime
from Quiz.multiplechoice import Multiplechoice
from multiprocessing import Queue
from random import shuffle, sample
from collections import namedtuple
from Quiz.statistics import Statistics

Vars = namedtuple("Vars", ["q_num", "prompt", "choices"])

class QuizSession():
    def __init__(self, *, vars):
        self.time = 0
        self.correct_questions = 0
        self.incorrect_questions = 0
        self.skipped_qs = 0
        self.abandoned_qs = 0
        self.history = []
        self.questions = Queue()
        self.vars = vars

    def fetch_questions(self):
        for question in Multiplechoice.get_quiz_questions():
            self.questions.put(Question(*question))
        return self

    def start_question(self):
        q = self.questions.get().start_q(self.vars)
        self.history.append(q)
        self.vars.q_num.set(f"Question {len(self.history)}:")

    def skip(self):
        self.skipped_qs += 1
        self.time += self.history[-1].skip().get_time()

    def abandon(self):
        self.abandoned_qs += 1
        self.time += self.history[-1].abandon().get_time()

    def answer(self, i):
        if self.history[-1].give_answer(self.vars.choices[i].get()).status == "correct":
            self.correct_questions += 1
            self.time += self.history[-1].get_time()
            return True
        else:
            self.incorrect_questions += 1
            self.time += self.history[-1].get_time()
            return False

    def is_finished(self):
        return self.questions.empty()

    def ongoing_question(self):
        return self.history[-1].status == "ongoing"

class Question():
    def __init__(self, id, prompt, correct, incorrect1, incorrect2, incorrect3):
        self.id = id
        self.prompt = prompt
        # first choice is the correct choice
        self.choices = [correct, incorrect1, incorrect2, incorrect3]
        self.status = "ongoing"
        self.answer = None
        self.started_at = None
        self.stopped_at = None

    def start_q(self, vars):
        self.started_at = datetime.now()
        vars.prompt.set(self.prompt)
        for i, choice in enumerate(sample(self.choices, 4)):
            vars.choices[i].set(choice)
        return self

    def give_answer(self, answer):
        self.answer = answer
        if self.answer == self.choices[0]:
            self.status = "correct"
        else:
            self.status = "incorrect"

        self.save_stats()
        return self

    def skip(self):
        self.save_stats()
        self.status = "skipped"
        return self

    def abandon(self):
        self.save_stats()
        self.status = "abandoned"
        return self

    def get_time(self):
        try: return round((self.stopped_at - self.started_at).total_seconds(), 2)
        except: return 0

    def save_stats(self):
        self.stopped_at = datetime.now()
        Statistics.save_answer_stats(id=self.id, quiz_format="Multi-Choice",
            status=self.status, time=self.get_time(), created_at=self.stopped_at)
