from tkinter import *
from UI import *
from Quiz.multiplechoice import Multiplechoice
# create Settings UI for the quiz
class Settings(Page):
    def __init__(self, mainUI):
        super().__init__(mainUI)

    # list questions imported from the Multiple choice model
    def list_qs(self):
        self.subFrame = Frame(self)
        self.subFrame.grid(row = 0, column = 0, sticky=NSEW)

        self.table = TableView(self.subFrame, self.mainUI.root).show()

        self.table.add_column(title="Question Prompt", property="text")
        self.table.add_column(title="Answer", property="correct")
        self.table.add_column(title="Incorrect choice 1", property="in1")
        self.table.add_column(title="Incorrect choice 2", property="in2")
        self.table.add_column(title="Incorrect choice 3", property="in3")
        self.table.add_column(
            cell_constructor=lambda f, row: HoverButton(f, text="Edit", command=lambda row=row: self.edit_form(row))
        )
        self.table.add_column(
            cell_constructor=lambda f, row: HoverButton(f, text="Delete", command=lambda row=row: self.del_q(row))
        )

        self.table.data = Multiplechoice(self.package_id, True).qbank

        self.footer = Frame(self.subFrame)
        self.footer.grid(row=1, column=0, sticky=NSEW)

        HoverButton(self.footer, text="Back - Package Menu", command=self.go_package_menu, pos=(0, 0, W))
        self.footer.grid_columnconfigure(2, weight=2)
        self.b_add = HoverButton(self.footer, text="Add new Question", command=self.new_q_form, pos=(0, 2, E))


#J Go back to package menu
    def go_package_menu(self):
        self.table.scrollbar.grid_forget()
        self.go_to("PackageMenu")()

    def save_q(self):
        Multiplechoice.save_question(self.question["id"], self.question["text"].get("1.0", END).rstrip(), self.question["correct"].get(),
                                     self.question["in1"].get(), self.question["in2"].get(), self.question["in3"].get())
        self.refresh()

    # send edit form to the database

    # delete a question in the database
    def del_q(self, row_id):
        confirm_message = messagebox.askquestion ('Delete Question','Are you sure you want to delete this question?',icon = 'warning')
        if confirm_message == "yes":
            Multiplechoice.delete_question(self.table.data[row_id]["id"])
        self.refresh()

    class NewQuestionForm(EasyGrid, Frame):

        def __init__(self, root, page, *args, **kwargs):
            super().__init__(root, *args, **kwargs)
            self.page = page
            self.question = {"incorrect": []}
            self.prompt = BetterText(self, width=30, height=2, bgText="Enter Question Prompt", pos=(0, 0))
            self.correct = BetterEntry(self, bgText="Enter The Answer", pos=(0, 1))
            self.incorrect1 = BetterEntry(self, bgText=f"Enter Wrong Choice 1", pos=(0, 2))
            self.incorrect2 = BetterEntry(self, bgText=f"Enter Wrong Choice 2", pos=(0, 3))
            self.incorrect3 = BetterEntry(self, bgText=f"Enter Wrong Choice 3", pos=(0, 4))

        # create a new question in the database
        def send_q_data(self):
            Multiplechoice.create_question(prompt=self.prompt.get("1.0", END).rstrip(),
                                           answer=self.correct.get(), incorrect1=self.incorrect1.get(),
                                           incorrect2=self.incorrect2.get(), incorrect3=self.incorrect3.get(),
                                           package_id=self.page.package_id)


    #  create a new form for the next question
    def new_q_form(self):
        self.refresh()
        self.new_question_form = self.NewQuestionForm(self.footer, self, pos=(0, 1))
        def save_b_handler():
            self.new_question_form.send_q_data()
            self.refresh()
        self.b_add["command"] = save_b_handler
        self.b_add["text"] = "Create"
        self.mainUI.update_window_size(self)




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
        self.table.set_cell(row=row_id, column=5, func=lambda f: HoverButton(f, text="Save", command=self.save_q))


        self.question["id"], text, correct, inc1, inc2, inc3 = Multiplechoice.get_question(self.table.data[row_id]["id"])

        self.question["text"].insert(END, text)
        self.question["correct"].set(correct)
        self.question["in1"].set(inc1)
        self.question["in2"].set(inc2)
        self.question["in3"].set(inc3)

        self.mainUI.update_window_size(self)

    def refresh(self):
        try:
            self.subFrame.destroy()
            self.table.scrollbar.destroy()
        except:
            pass
        self.list_qs()
        self.mainUI.update_window_size(self)

    def show(self, package_id):
        super().show()
        self.package_id = package_id
        self.refresh()


