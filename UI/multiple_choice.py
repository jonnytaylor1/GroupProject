from tkinter import *
import random
import tkinter.messagebox
from Quiz.multiplechoice import Multiplechoice
class MultipleChoice(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()
        self.qIter = Multiplechoice().get_questions()
        self.num = 0
        self.create_questions()


    def create_questions(self):
        self.q_num = Label(self, text = "Question 1: ", font = ("MS", 8, "bold"))
        self.q_num.grid(row = 2, column = 4, columnspan = 4)
        self.q_text = Label(self, text="Answer A is correct? ", font=("MS", 8, "bold"))
        self.q_text.grid(row=3, column=4, columnspan=4)
        self.choices = []
        for i, answer in enumerate(list("abcd")):
            b = Button(self, text = answer, font=("MS", 8, "bold"))
            b.grid(row = 6 + i, column=5, columnspan=2)
            self.choices.append(b)
        try:
            self.load_questions()
        except StopIteration:
            pass
    def load_questions(self):
        try:
            q_text, choices, correct = next(self.qIter)
            self.num += 1
            self.q_num["text"] = f"Question {self.num}:"
            self.q_text["text"] = q_text
            for button, choice in zip(self.choices, choices):
                button["text"] = choice
                button["command"] = lambda x=choice, correct = correct: self.check_answer(x, correct)
        except StopIteration:
            tkinter.messagebox.showinfo("Well Done!", "the test is complete!")
            self.parent.parent.destroy()
    def check_answer(self, choice, correct):
        tkinter.messagebox.showinfo("Answer submitted",
                                    f"{choice} is correct!" if choice == correct else f"Sorry, the correct answer is {correct}")
        self.load_questions()
