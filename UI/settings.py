from tkinter import *
from Quiz.multiplechoice import Multiplechoice
# create Settings UI for the quiz
class Settings(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.subFrame = Frame(self)
        self.subFrame.grid()

    # list questions imported from the Multiple choice model
    def list_qs(self, package_id):
        self.package_id = package_id
        self.subFrame = Frame(self)
        self.subFrame.grid()
        h_row = 1
        h_font = ("MS", 10, "bold")
        Label(self.subFrame, text="Question Prompt", font = h_font).grid(row=h_row, column=2)
        Label(self.subFrame, text="Answer", font = h_font).grid(row=h_row, column=3)
        Label(self.subFrame, text="Incorrect choice 1", font = h_font).grid(row=h_row, column=4)
        Label(self.subFrame, text="Incorrect choice 2", font = h_font).grid(row=h_row, column=5)
        Label(self.subFrame, text="Incorrect choice 3", font = h_font).grid(row=h_row, column=6)
        row = 1
        self.rows = []
        for i, q in enumerate(Multiplechoice(package_id).qbank):
            row += 1
            l_text = Label(self.subFrame, text = q["text"])
            l_text.grid(row=row, column=2)
            l_correct = Label(self.subFrame, text = q["correct"])
            l_correct.grid(row = row, column =3)
            inc1 = Label(self.subFrame, text= q["incorrect"][0])
            inc1.grid(row = row, column = 4)
            inc2 = Label(self.subFrame, text = q["incorrect"][1])
            inc2.grid(row = row, column = 5)
            inc3 = Label(self.subFrame, text = q["incorrect"][2])
            inc3.grid(row = row, column = 6)
            b_edit = Button(self.subFrame, text = "Edit")
            b_edit.grid(row = row, column = 7)
            b_edit["command"] = lambda row=row, id = q["id"]: self.edit_q(row, id)
            Button(self.subFrame, text="Delete", command=lambda id = q["id"]: self.del_q(id)).grid(row=row, column=8)
            self.rows.append([l_text, l_correct, inc1, inc2, inc3])
        self.b_add = Button(self.subFrame, text = "Add new Question", command= lambda: self.create_q_form(row + 1))
        self.b_add.grid(row = row + 1, column = 3)
        Button(self.subFrame, text = "Back - Package Menu", command = self.go_package_menu).grid(row = row + 2, column = 3)
        # left for debugging purposes
        Button(self.subFrame, text = "Refresh", command = self.refresh).grid(row = row + 3, column = 3)


#J Go back to package menu
    def go_package_menu(self):
        self.grid_forget()
        self.parent.pages["PackageMenu"].grid()

    def save_q(self):
        in_choices = list(map(lambda el: el.get(), self.question["incorrect"]))
        Multiplechoice.save_question(self.question["id"], self.question["text"].get("1.0", END).rstrip(), self.question["correct"].get(), *in_choices)
        self.refresh()

    # send edit form to the database
    def edit_q(self, row, id):
        for label in self.rows[row - 2]:
            label.grid_remove()
        self.create_q_form(row)
        self.question["id"], text, correct, inc1, inc2, inc3 = Multiplechoice.get_question(id)
        self.question["text"].insert(END, text)
        self.question["correct"].set(correct)
        self.question["incorrect"][0].set(inc1)
        self.question["incorrect"][1].set(inc2)
        self.question["incorrect"][2].set(inc3)
        self.b["command"] = lambda: self.save_q()

    # delete a question in the database
    def del_q(self, i):
        Multiplechoice.delete_question(i)
        self.refresh()


    #  create a new form for the next question
    def create_q_form(self, new_row):
        self.b_add.destroy()
        self.question = {"correct": StringVar(), "incorrect": [StringVar(), StringVar(), StringVar()]}

        self.question["text"] = Text(self.subFrame, width = 30, height = 2)
        self.question["text"].grid(row = new_row, column = 2)

        c_entry = Entry(self.subFrame, textvariable = self.question["correct"])
        c_entry.grid(row = new_row, column = 3)

        for i in range(3):
            entry = Entry(self.subFrame, textvariable = self.question["incorrect"][i])
            entry.grid(row = new_row, column = 4 + i)

        self.b = Button(self.subFrame, text = "Save", font = ("MS", 8, "bold"))
        self.b.grid(row = new_row, column = 7)
        self.b["command"] = self.send_q_data
    def refresh(self):
        self.subFrame.destroy()
        self.list_qs(self.package_id)

    # create a new question in the database
    def send_q_data(self):
        in_choices = list(map( lambda el: el.get(), self.question["incorrect"]))
        q = {"text": self.question["text"].get("1.0", END).rstrip(), "correct": self.question["correct"].get(), "incorrect": in_choices, "package_id": self.package_id}
        Multiplechoice.add_question(q)
        self.refresh()
    def show(self, package_id):
        self.subFrame.destroy()
        self.list_qs(package_id)
        self.grid()
