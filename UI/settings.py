from tkinter import *
from Quiz.multiplechoice import Multiplechoice, get_question

class Settings(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()
        # self.create_q_form()
        self.list_qs()


    def list_qs(self):
        h_row = 1
        h_font = ("MS", 10, "bold")
        Label(self, text="Question Prompt", font = h_font).grid(row=h_row, column=2)
        Label(self, text="Answer", font = h_font).grid(row=h_row, column=3)
        Label(self, text="Incorrect choice 1", font = h_font).grid(row=h_row, column=4)
        Label(self, text="Incorrect choice 2", font = h_font).grid(row=h_row, column=5)
        Label(self, text="Incorrect choice 3", font = h_font).grid(row=h_row, column=6)
        for i, q in enumerate(Multiplechoice().qbank):
            row = 2 + i
            Label(self, text = q["text"]).grid(row=row, column=2)
            Label(self, text = q["correct"]).grid(row = row, column =3)
            Label(self, text= q["incorrect"][0]).grid(row = row, column = 4)
            Label(self, text = q["incorrect"][1]).grid(row = row, column = 5)
            Label(self, text = q["incorrect"][2]).grid(row = row, column = 6)
            b_edit = Button(self, text = "Edit")
            b_edit.grid(row = row, column = 7)
            b_edit["command"] = lambda i=i: self.edit_q(i)
            Button(self, text="Delete").grid(row=row, column=8)
        self.b_add = Button(self, text = "Add new Question", command= lambda: self.create_q_form(15))
        self.b_add.grid(row = 14, column = 3)

    def save_q(self):
        self.refresh()

    def edit_q(self, i):
        self.create_q_form(i + 2)
        text, correct, inc1, inc2, inc3 = get_question(i+1)
        self.question["text"].insert(END, text)
        self.question["correct"].set(correct)
        self.question["incorrect"][0].set(inc1)
        self.question["incorrect"][1].set(inc2)
        self.question["incorrect"][2].set(inc3)



    def create_q_form(self, new_row):
        self.b_add.destroy()
        self.question = {"correct": StringVar(), "incorrect": [StringVar(), StringVar(), StringVar()]}



        self.question["text"] = Text(self, width = 30, height = 2)
        self.question["text"].grid(row = new_row, column = 2)

        c_entry = Entry(self, textvariable = self.question["correct"])
        c_entry.grid(row = new_row, column = 3)

        for i in range(3):
            entry = Entry(self, textvariable = self.question["incorrect"][i])
            entry.grid(row = new_row, column = 4 + i)

        b = Button(self, text = "Save", font = ("MS", 8, "bold"))
        b.grid(row = new_row, column = 7)
        b["command"] = self.send_q_data
    def refresh(self):
        self.destroy()
        Settings(self.parent)


    def send_q_data(self):
        in_choices = list(map( lambda el: el.get(), self.question["incorrect"]))
        q = {"text": self.question["text"].get("1.0", END), "correct": self.question["correct"].get(), "incorrect": in_choices}
        Multiplechoice().add_question(q)
        self.refresh()



