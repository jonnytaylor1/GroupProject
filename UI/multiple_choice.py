from tkinter import *
import time
import tkinter.messagebox
from Quiz.multiplechoice import Multiplechoice
class MultipleChoice(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent.root)
        self.create_questions()

    def show(self):
        self.grid()
        self.qIter = Multiplechoice().get_questions(True)
        self.stats = {"total_time": 0,
                      "correct_qs": 0,
                      "incorrect_qs": 0,
                      "skipped_qs": 0}
        self.num = 0
        self.load_questions()

    def skip_q(self):
        self.stats["skipped_qs"] += 1
        self.stats["total_time"] += self.parent.diff
        self.load_questions()

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

    def end_quiz(self):
        self.grid_remove()
        self.stats["skipped_qs"] += 1
        self.stats["total_time"] += self.parent.diff
        self.parent.pages["EndScreen"].show(self.stats)

    def load_questions(self):
        try:
            q_text, choices, correct = next(self.qIter)
            for choice in self.choices:
                choice["bg"] = "SystemButtonFace"
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
    def check_answer(self, button, correct):
        if button["text"] == correct:
            button["bg"] = "green"
            self.stats["correct_qs"] += 1
        else:
            button["bg"] = "red"
            self.stats["incorrect_qs"] += 1
        self.stats["total_time"] += self.parent.diff
        self.timer.grid_remove()
        self.l_timer.grid_remove()
        self.b_end.grid_remove()
        self.b_next["text"] = "Next Question"
        self.b_next["command"] = self.load_questions

class EndScreen(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.create_stat_page()

    def show(self, stats):
        self.grid()
        total = stats["incorrect_qs"] + stats["correct_qs"] + stats["skipped_qs"]
        self.l_incorrect_answers["text"] = stats["incorrect_qs"]
        self.l_correct_answers["text"] = stats["correct_qs"]
        self.l_skipped_answers["text"] = stats["skipped_qs"]
        self.l_total_answers["text"] = total
        time = stats["total_time"]
        self.l_total_time["text"] = f"{time // 600}{(time // 60) % 10}:{(time // 10) % 6}{time % 10}"

    def go_menu(self):
        self.grid_remove()
        self.parent.pages["Welcome"].grid()

    def restart(self):
        self.grid_remove()
        self.parent.pages["MultipleChoice"].show()


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

