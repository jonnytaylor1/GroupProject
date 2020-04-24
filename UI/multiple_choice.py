from tkinter import *
import time
import tkinter.messagebox
from Quiz.multiplechoice import Multiplechoice
from Quiz.statistics import Statistics
from UI import *


class MultipleChoice(Page):
    def __init__(self, mainUI):
        super().__init__(mainUI)
        self.create_questions()

    def show(self):
        super().show()
        self.mainUI.root.geometry("750x500")
        # get data on questions from the model
        self.qIter = Multiplechoice.get_multiplechoice_qs(True)
        # initialize the stats for the quiz at the start
        self.stats = {"total_time": 0,
                      "correct_qs": 0,
                      "incorrect_qs": 0,
                      "skipped_qs": 0,
                      "qs": []}
        self.num = 0
        self.load_questions()

    #  update stats when you skip a question
    def skip_q(self):
        self.stats["skipped_qs"] += 1
        self.stats["total_time"] += self.mainUI.diff
        self.stats["qs"].append({"status": "skipped",
                                 "q_id":self.q_id,
                                 "time": self.mainUI.diff,
                                 "answer": None})
        Statistics.create_answer_stats({"id": self.q_id, "time": int(self.mainUI.diff * 10), "status": "skipped", "quiz_format": "Multi-Choice"})
        # load next question
        self.load_questions()

    # create question form for the multiple choice
    def create_questions(self):
        self.autoresize_grid(rows=8, columns=3)

        self.q_num = GridLabel(self, text="Question 1: ", pos=(0, 0, NSEW), cspan=3)
        self.q_text = GridLabel(self, text="Answer A is correct? ", pos=(1, 0, NSEW), cspan=3)
        self.l_timer = GridLabel(self, text="Time Elapsed:", pos=(2, 0, NSEW))
        self.timer = GridLabel(self, textvariable=self.mainUI.timer, pos=(2, 1, NSEW))
        self.choices = []
        self.b_next = HoverButton(self, text="Skip", command=self.skip_q, pos=(3, 0, NSEW))
        self.b_restart = HoverButton(self, text="Restart", command=self.show, pos=(3, 1, NSEW))
        self.b_end = HoverButton(self, text="End Quiz", command=self.end_quiz, pos=(3, 2, NSEW))
        for i, answer in enumerate(list("abcd")):
            b = HoverButton(self, text=answer, font=("MS", 8, "bold"), pos=(4+i, 0, NSEW), cspan=3)
            self.choices.append(b)

    def early_restart(self):
        self.stats["total_time"] += self.mainUI.diff
        Statistics.create_answer_stats({"id": self.q_id, "time": int(self.mainUI.diff * 10), "status": "abandoned", "quiz_format": "Multi-Choice"})
        self.show()

    # record as abandoned question when you end quiz prematurely
    def end_quiz(self):
        self.stats["total_time"] += self.mainUI.diff
        Statistics.create_answer_stats({"id": self.q_id, "time": int(self.mainUI.diff * 10), "status": "abandoned", "quiz_format": "Multi-Choice"})
        # show final statistics for the quiz
        self.go_to("EndScreen")(self.stats)

    # reset everything and load next question
    def load_questions(self):
        try:
            self.q_id, q_text, choices, correct = next(self.qIter)
            for choice in self.choices:
                choice["state"] = NORMAL
            self.b_next["command"] = self.skip_q
            self.b_next["text"] = "Skip"
            self.b_end.grid(row=3, column=2, sticky=NSEW)

            self.mainUI.clock1 = time.time()
            self.mainUI.timer.set("00:00")
            self.timer.grid(row=2, column=1, sticky=NSEW)
            self.l_timer.grid(row=2, column=0, sticky=NSEW)
            self.num += 1
            self.q_num["text"] = f"Question {self.num}:"
            self.q_text["text"] = q_text
            for button, choice in zip(self.choices, choices):
                button["text"] = choice
                button["command"] = lambda button=button, correct = correct: self.check_answer(button, correct)
        except StopIteration:
            tkinter.messagebox.showinfo("Well Done!", "the test is complete!")
            self.go_to("EndScreen")(self.stats)
    # compare the answer to the correct one

    def check_answer(self, button, correct):
        for choice in self.choices:
            # lock ability to choose another answer
            choice["state"] = DISABLED
        if button["text"] == correct:
            button["bg"] = "green"
            self.stats["correct_qs"] += 1
            self.stats["qs"].append({"status": "correct",
                                    "q_id": self.q_id,
                                    "time": self.mainUI.diff,
                                     "answer": button["text"]})
            Statistics.create_answer_stats({"id": self.q_id, "time": int(self.mainUI.diff * 10), "status": "correct", "quiz_format": "Multi-Choice"})

        else:
            button["bg"] = "red"
            self.stats["incorrect_qs"] += 1
            self.stats["qs"].append({"status": "incorrect",
                                    "q_id": self.q_id,
                                    "time": self.mainUI.diff,
                                     "answer": button["text"]})
            Statistics.create_answer_stats({"id": self.q_id, "time": int(self.mainUI.diff * 10), "status": "incorrect", "quiz_format": "Multi-Choice"})
        self.stats["total_time"] += self.mainUI.diff
        self.timer.grid_remove()
        self.l_timer.grid_remove()
        self.b_end.grid_remove()
        self.b_next["text"] = "Next Question"
        self.b_next["command"] = self.load_questions
# Generate the end screen frame


class EndScreen(Page):

    def __init__(self, mainUI):
        super().__init__(mainUI)
    # fill statistics for the quiz

    def show(self, stats):
        super().show()
        self.create_stat_page()
        self.mainUI.root.geometry("1000x500")
        self.autoresize_grid(rows=10, columns=3)

        total = stats["incorrect_qs"] + stats["correct_qs"] + stats["skipped_qs"]
        self.l_incorrect_answers["text"] = stats["incorrect_qs"]
        self.l_correct_answers["text"] = stats["correct_qs"]
        self.l_skipped_answers["text"] = stats["skipped_qs"]
        self.l_total_answers["text"] = total
        time = int(stats["total_time"])
        self.l_total_time["text"] = f"{time // 600}{(time // 60) % 10}:{(time // 10) % 6}{time % 10}"

        for i,q in enumerate(stats["qs"]):
            id, question, corr, inc1, inc2, inc3 = Multiplechoice.get_question(q["q_id"])
            text = f"{i + 1}. {question} {q['answer'] if q['answer'] else 'Skipped'}."
            l = GridLabel(self, anchor='w', justify='left', pos=(0 + i, 2))
            if q["status"] == "correct":
                l["fg"] = "green"
            elif q["status"] == "incorrect":
                l["fg"] = "red"
                text += f" (Correct: {corr})"
            elif q["status"] == "skipped":
                l["fg"] = "grey"
            t = int(q['time'])
            time = f"{t // 600}{(t // 60) % 10}:{(t // 10) % 6}{t % 10}"
            text += f" Time spent: {time}"
            l["text"] = text


    # create form for the stats to fill
    def create_stat_page(self):
        GridLabel(self, text="Incorrect Answers:", pos=(0, 0))
        GridLabel(self, text="Correct Answers:", pos=(1, 0))
        GridLabel(self, text="Skipped Answers:", pos=(2, 0))
        GridLabel(self, text="Total Questions:", pos=(3, 0))
        GridLabel(self, text="Total Time Spent:", pos=(4, 0))

        self.l_incorrect_answers = GridLabel(self, text="Incorrect Answers", pos=(0, 1))
        self.l_correct_answers = GridLabel(self, text="Correct Answers", pos=(1, 1))
        self.l_skipped_answers = GridLabel(self, text="Skipped Answers", pos=(2, 1))
        self.l_total_answers = GridLabel(self, text="Total Answers", pos=(3, 1))
        self.l_total_time = GridLabel(self, text="Total Time Spent", pos=(4, 1))

        HoverButton(self, text="Menu", command=self.go_to("Welcome"), pos=(5, 0, NSEW))
        HoverButton(self, text="Restart", command=self.go_to("MultipleChoice"), pos=(5, 1, NSEW))
