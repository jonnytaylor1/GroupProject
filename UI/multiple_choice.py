from tkinter import *
import time
import tkinter.messagebox
from Quiz.multiplechoice import Multiplechoice
from Quiz.statistics import Statistics
class MultipleChoice(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent.root)
        self.create_questions()

    def show(self):
        self.grid()
        # get data on questions from the model
        self.qIter = Multiplechoice().get_questions(True)
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
        self.stats["total_time"] += self.parent.diff
        self.stats["qs"].append({"status": "skipped",
                                 "q_id":self.q_id,
                                 "time": self.parent.diff,
                                 "answer": None})
        Statistics.increment_stats({"id": self.q_id, "time": int(self.parent.diff), "skips": 1})
        # load next question
        self.load_questions()

    # create question form for the multiple choice
    def create_questions(self):
        self.q_num = Label(self, text = "Question 1: ", font = ("MS", 8, "bold"))
        self.q_num.grid(row = 2, column = 4)
        self.q_text = Label(self, text="Answer A is correct? ", font=("MS", 8, "bold"))
        self.q_text.grid(row=3, column=4)
        self.l_timer = Label(self, text = "Time Elapsed:")
        self.l_timer.grid(row=3, column=5)
        self.timer = Label(self, textvariable=self.parent.timer)
        self.timer.grid(row=3, column=6)
        self.choices = []
        self.b_next = Button(self, text="Skip?", command=self.skip_q)
        self.b_next.grid(row=7, column=6)
        self.b_restart = Button(self, text="Restart", command=self.show)
        self.b_restart.grid(row=7, column=7)
        self.b_end = Button(self, text="End Quiz", command=self.end_quiz)
        self.b_end.grid(row=7, column=8)
        for i, answer in enumerate(list("abcd")):
            b = Button(self, text = answer, font=("MS", 8, "bold"))
            b.grid(row = 6 + i, column=5)
            self.choices.append(b)

    # record as skipped question when you end quiz prematurely
    def end_quiz(self):
        self.grid_remove()
        self.stats["skipped_qs"] += 1
        self.stats["total_time"] += self.parent.diff
        Statistics.increment_stats({"id": self.q_id, "time": int(self.parent.diff), "skips": 1})
        # show final statistics for the quiz
        self.parent.pages["EndScreen"].show(self.stats)

    # reset everything and load next question
    def load_questions(self):
        try:
            self.q_id, q_text, choices, correct = next(self.qIter)
            for choice in self.choices:
                choice["bg"] = "grey"
                choice["state"] = NORMAL
            self.b_next["command"] = self.skip_q
            self.b_next["text"] = "Skip?"
            self.b_end.grid()
            self.timer.grid()
            self.parent.clock1 = time.time()
            self.parent.timer.set("00:00")
            self.timer.grid()
            self.l_timer.grid()
            self.num += 1
            self.q_num["text"] = f"Question {self.num}:"
            self.q_text["text"] = q_text
            for button, choice in zip(self.choices, choices):
                button["text"] = choice
                button["command"] = lambda button=button, correct = correct: self.check_answer(button, correct)
        except StopIteration:
            tkinter.messagebox.showinfo("Well Done!", "the test is complete!")
            self.grid_remove()
            self.parent.pages["EndScreen"].show(self.stats)
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
                                    "time": self.parent.diff,
                                     "answer": button["text"]})
            Statistics.increment_stats({"id": self.q_id, "time": int(self.parent.diff), "corrects": 1})

        else:
            button["bg"] = "red"
            self.stats["incorrect_qs"] += 1
            self.stats["qs"].append({"status": "incorrect",
                                    "q_id": self.q_id,
                                    "time": self.parent.diff,
                                     "answer": button["text"]})
            Statistics.increment_stats({"id": self.q_id, "time": int(self.parent.diff), "incorrects": 1})
        for choice in self.choices:
            choice["state"] = DISABLED
        self.stats["total_time"] += self.parent.diff
        self.timer.grid_remove()
        self.l_timer.grid_remove()
        self.b_end.grid_remove()
        self.b_next["text"] = "Next Question"
        self.b_next["command"] = self.load_questions
# Generate the end screen frame
class EndScreen(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.create_stat_page()
    # fill statistics for the quiz
    def show(self, stats):
        self.grid()
        total = stats["incorrect_qs"] + stats["correct_qs"] + stats["skipped_qs"]
        self.l_incorrect_answers["text"] = stats["incorrect_qs"]
        self.l_correct_answers["text"] = stats["correct_qs"]
        self.l_skipped_answers["text"] = stats["skipped_qs"]
        self.l_total_answers["text"] = total
        time = int(stats["total_time"])
        self.l_total_time["text"] = f"{time // 600}{(time // 60) % 10}:{(time // 10) % 6}{time % 10}"
        self.subFrame = Frame(self)
        self.subFrame.grid(column=3, row=2, rowspan=10)

        for i,q in enumerate(stats["qs"]):
            id, question, corr, inc1, inc2, inc3 = Multiplechoice.get_question(q["q_id"])
            text = f"{i + 1}. {question} {q['answer'] if q['answer'] else 'Skipped'}."
            l = Label(self.subFrame)
            l.grid(row=1 + i, column=1)
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

    def go_menu(self):
        self.subFrame.destroy()
        self.grid_remove()
        self.parent.pages["Welcome"].grid()
    #  restart the quiz
    def restart(self):
        self.subFrame.destroy()
        self.grid_remove()
        self.parent.pages["MultipleChoice"].show()
    # create form for the stats to fill
    def create_stat_page(self):
        Label(self, text = "Incorrect Answers:").grid(row=2, column=1)
        Label(self, text = "Correct Answers:").grid(row=3, column=1)
        Label(self, text = "Skipped Answers:").grid(row=4, column=1)
        Label(self, text = "Total Questions:").grid(row=5, column=1)
        Label(self, text = "Total Time Spent:").grid(row=6, column=1)

        self.l_incorrect_answers = Label(self, text = "Incorrect Answers")
        self.l_incorrect_answers.grid(row=2, column=2)
        self.l_correct_answers = Label(self, text = "Correct Answers")
        self.l_correct_answers.grid(row=3, column=2)
        self.l_skipped_answers = Label(self, text = "Skipped Answers")
        self.l_skipped_answers.grid(row=4, column=2)
        self.l_total_answers = Label(self, text = "Total Answers")
        self.l_total_answers.grid(row=5, column=2)
        self.l_total_time = Label(self, text = "Total Time Spent")
        self.l_total_time.grid(row=6, column=2)




        Button(self, text="Menu", command=self.go_menu).grid(row=7, column=1)
        Button(self, text="Restart", command=self.restart).grid(row=7, column=2)
