from tkinter import *
from UI import *
from Quiz.multiplechoice import Multiplechoice
# create Settings UI for the quiz
class Settings(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.subFrame = Frame(self)
        self.subFrame.grid()

    # list questions imported from the Multiple choice model
    def list_qs(self):
        self.subFrame = Frame(self)
        self.subFrame.grid(row = 0, column = 0, sticky=NSEW)

        self.table = TableView(self.subFrame, self.parent.root)
        self.table.grid()

        self.table.add_column(
            h_constructor=lambda f: Label(f, text="Question Prompt"),
            cell_constructor=lambda f, id: Label(f),
            property="text"
        )
        self.table.add_column(
            h_constructor=lambda f: Label(f, text="Answer"),
            cell_constructor=lambda f, id: Label(f),
            property="correct"
        )
        self.table.add_column(
            h_constructor=lambda f: Label(f, text="Incorrect choice 1"),
            cell_constructor=lambda f, id: Label(f),
            property="in1"
        )
        self.table.add_column(
            h_constructor=lambda f: Label(f, text="Incorrect choice 2"),
            cell_constructor=lambda f, id: Label(f),
            property="in2"
        )
        self.table.add_column(
            h_constructor=lambda f: Label(f, text="Incorrect choice 3"),
            cell_constructor=lambda f, id: Label(f),
            property="in3"
        )
        self.table.add_column(
            h_constructor=lambda f: Label(f),
            cell_constructor=lambda f, id: Button(f, text="Edit", command=lambda id=id: self.edit_form(id)),
            property=""
        )
        self.table.add_column(
            h_constructor=lambda f: Label(f),
            cell_constructor=lambda f, row: Button(f, text="Delete", command=lambda row=row: self.del_q(row)),
            property=""
        )

        self.table.data = Multiplechoice(self.package_id, True).qbank

        self.footer = Frame(self.subFrame)
        self.footer.grid(row=1, column=0, sticky=NSEW)

        Button(self.footer, text="Back - Package Menu", command=self.go_package_menu).grid(row=0, column=0, sticky=W)
        self.footer.grid_columnconfigure(2, weight=2)
        self.b_add = Button(self.footer, text="Add new Question", command=self.new_q_form)
        self.b_add.grid(row=0, column=2, sticky=E)


#J Go back to package menu
    def go_package_menu(self):
        self.grid_forget()
        self.table.scrollbar.grid_forget()
        self.parent.pages["PackageMenu"].show()

    def save_q(self):
        Multiplechoice.save_question(self.question["id"], self.question["text"].get("1.0", END).rstrip(), self.question["correct"].get(),
                                     self.question["in1"].get(), self.question["in2"].get(), self.question["in3"].get())
        self.refresh()

    # send edit form to the database

    # delete a question in the database
    def del_q(self, i):
        confirm_message = messagebox.askquestion ('Delete Question','Are you sure you want to delete this question?',icon = 'warning')
        if confirm_message == "yes":
            Multiplechoice.delete_question(i)
        self.refresh()


    #  create a new form for the next question
    def new_q_form(self):
        # self.b_add.destroy()
        self.refresh()
        self.formFrame = Frame(self.footer)
        self.formFrame.grid(column=1, row=0)

        # self.b_add["state"] = "disabled"
        self.question = {"correct": StringVar(), "incorrect": [StringVar(), StringVar(), StringVar()]}

        self.question["text"] = Text(self.formFrame, width = 30, height = 2)
        self.question["text"].grid(row = 0, column = 0)

        c_entry = Entry(self.formFrame, textvariable=self.question["correct"])
        c_entry.grid(row=0, column=1)

        for i in range(3):
            entry = Entry(self.formFrame, textvariable=self.question["incorrect"][i])
            entry.grid(row=0, column=2 + i)

        self.b_add["command"] = self.send_q_data
        self.b_add["text"] = "Save"

        self.parent.update_window_size(self)



    def edit_form(self, row_id):

        self.question = {"correct": StringVar(), "in1": StringVar(), "in2": StringVar(), "in3": StringVar()}

        for i in range(self.table.columns):
            property = self.table.prop_names[i]
            if len(property) > 0:
                if property == "text":
                    def constructor(frame):
                        self.question["text"] = Text(frame, width=30, height=2)
                        return self.question["text"]
                else:
                    def constructor(frame):
                        return Entry(frame, textvariable=self.question[property])

                self.table.set_cell(row=row_id, column=i, func=constructor)
            else:
                for row in range(len(self.table.data)):
                    self.table.get_cell(row=row, column=i).hide()
        self.table.set_cell(row=row_id, column=5, func=lambda f: Button(f, text="Save", command=self.save_q))


        self.question["id"], text, correct, inc1, inc2, inc3 = Multiplechoice.get_question(self.table.data[row_id]["id"])

        self.question["text"].insert(END, text)
        self.question["correct"].set(correct)
        self.question["in1"].set(inc1)
        self.question["in2"].set(inc2)
        self.question["in3"].set(inc3)

        self.parent.update_window_size(self)



    def refresh(self):
        try:
            self.subFrame.destroy()
            self.table.scrollbar.destroy()
        except:
            pass
        self.list_qs()
        self.parent.update_window_size(self)

    # create a new question in the database

    def send_q_data(self):
        in_choices = [el.get() for el in self.question["incorrect"]]
        q = {"text": self.question["text"].get("1.0", END).rstrip(), "correct": self.question["correct"].get(), "incorrect": in_choices, "package_id": self.package_id}
        Multiplechoice.add_question(q)
        self.refresh()


    def show(self, package_id):
        self.package_id = package_id
        self.grid(column=0, row=0, sticky=NSEW)
        self.refresh()


