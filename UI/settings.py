from tkinter import *
from Quiz.multiplechoice import Multiplechoice

class Settings(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()
        self.create_q_form()


    def create_q_form(self):
        self.question = {"text": StringVar(), "correct": StringVar(), "incorrect": [StringVar(), StringVar(), StringVar()]}
        l = Label(self, text = "Add new question", font = ("MS", 8, "bold"))
        l.grid(row = 2, column = 2, columnspan = 4)

        q_label = Label(self, text = "Question prompt", font = ("MS", 8, "bold"))
        q_label.grid(row = 3, column = 1)
        self.question["text"] = Text(self, width = 70, height = 5)
        self.question["text"].grid(row = 3, column = 2)

        c_label = Label(self, text = "Correct answer", font = ("MS", 8, "bold"))
        c_label.grid(row = 4, column = 1)
        c_entry = Entry(self, textvariable = self.question["correct"])
        c_entry.grid(row = 4, column = 2)

        for i in range(3):
            label = Label(self, text = f"incorrect choice {i+1}", font = ("MS", 8, "bold"))
            label.grid(row = 5 + i, column = 1)
            entry = Entry(self, textvariable = self.question["incorrect"][i])
            entry.grid(row = 5 + i, column = 2)

        b = Button(self, text = "Save", font = ("MS", 8, "bold"))
        b.grid(row = 10, column = 2, columnspan = 2)
        b["command"] = self.send_q_data

    def send_q_data(self):
        in_choices = list(map( lambda el: el.get(), self.question["incorrect"]))
        q = {"text": self.question["text"].get("1.0", END), "correct": self.question["correct"].get(), "incorrect": in_choices}
        print(q)
        Multiplechoice().add_question(q)
