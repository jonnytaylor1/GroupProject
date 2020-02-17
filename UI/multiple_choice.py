from tkinter import *
import random
import tkinter.messagebox
from Quiz.multiplechoice import Multiplechoice
class MultipleChoice(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent.root)
        self.num = 0

    def show(self):
        self.grid()
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
            self.qIter
        except AttributeError:
            self.qIter = Multiplechoice().get_questions()
        try:
            q_text, choices, correct = next(self.qIter)
            self.num += 1
            self.q_num["text"] = f"Question {self.num}:"
            self.q_text["text"] = q_text
            for button, choice in zip(self.choices, choices):
                button["text"] = choice
                button["command"] = lambda button=button, correct = correct: self.check_answer(button, correct)
        except StopIteration:
            tkinter.messagebox.showinfo("Well Done!", "the test is complete!")
            self.parent.root.destroy()
    def check_answer(self, button, correct):
        if button["text"] == correct:
            button["bg"] = "green"
        else:
            button["bg"] = "red"
        tkinter.messagebox.showinfo("Answer submitted",
                                    f"{button['text']} is correct!" if button["text"] == correct else f"Sorry, the correct answer is {correct}")
        button["bg"] = "SystemButtonFace"
        self.load_questions()


