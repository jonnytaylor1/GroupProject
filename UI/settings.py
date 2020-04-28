from tkinter import *
from UI import *
from Quiz.multiplechoice import Multiplechoice
from UI.components.Validator import field_checker
# create Settings UI for the quiz
class Settings(Page):

    # list questions imported from the Multiple choice model
    def create(self):
        super().create()
        self.table = TableView(self, self.mainUI.root)
        self.table.pack(fill=BOTH, expand=1)

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

        self.footer = Frame(self)
        self.footer.pack(fill=X)

        HoverButton(self.footer, text="Back - Package Menu", command=self.go_to("PackageMenu"), pos=(0, 0, W))
        self.footer.grid_columnconfigure(2, weight=2)
        self.b_add = HoverButton(self.footer, text="Add new Question", command=self.new_q_form, pos=(0, 2, E))


    def save_q(self):
        id = self.question["id"]
        prompt = self.question["text"].get("1.0", END).rstrip()
        correct = self.question["correct"].get()
        in1 = self.question["in1"].get()
        in2 = self.question["in2"].get()
        in3 = self.question["in3"].get()

        field_checker(prompt, correct, in1, in2, in3, f_commiter=lambda: Multiplechoice.save_question(id, prompt, correct, in1, in2, in3))
        self.show()

    # send edit form to the database

    # delete a question in the database
    def del_q(self, row_id):
        confirm_message = messagebox.askquestion ('Delete Question','Are you sure you want to delete this question?',icon = 'warning')
        if confirm_message == "yes":
            Multiplechoice.delete_question(self.table.data[row_id]["id"])
        self.show()

    class NewQuestionForm(EasyGrid, Frame):

        def __init__(self, root, page, *args, **kwargs):
            super().__init__(root, *args, **kwargs)
            self.page = page
            self.root = root
            self.question = {"incorrect": []}
            self.prompt = BetterText(self, width=30, height=2, bgText="Enter Question Prompt", pos=(0, 0))
            self.correct = BetterEntry(self, bgText="Enter The Answer", pos=(0, 1))
            self.incorrect1 = BetterEntry(self, bgText=f"Enter Wrong Choice 1", pos=(0, 2))
            self.incorrect2 = BetterEntry(self, bgText=f"Enter Wrong Choice 2", pos=(0, 3))
            self.incorrect3 = BetterEntry(self, bgText=f"Enter Wrong Choice 3", pos=(0, 4))

        # create a new question in the database
        def send_q_data(self):
            prompt = self.prompt.get("1.0", END).rstrip()
            answer = self.correct.get()
            in1 = self.incorrect1.get()
            in2 = self.incorrect2.get()
            in3 = self.incorrect3.get()
            p_id=self.page.package_id

            field_checker(prompt, answer, in1, in2, in3, f_commiter=lambda:
                            Multiplechoice.create_question(prompt=prompt, answer=answer, incorrect1=in1,
                                           incorrect2=in2, incorrect3=in3, package_id=p_id)
                          )


            self.grid_forget()
            self.page.b_add.configure(text="Add new Question", command=self.page.new_q_form)
            self.page.show()

    #  create a new form for the next question
    def new_q_form(self):
        self.show()
        self.new_question_form = self.NewQuestionForm(self.footer, self, pos=(0, 1))
        def save_b_handler():
            self.new_question_form.send_q_data()
            self.show()
        self.b_add.configure(command=save_b_handler, text="Create")
        self.mainUI.update_window_size()

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

        self.mainUI.update_window_size()



    def before_showing(self, package_id=None):
        if package_id: self.package_id = package_id
        self.table.data = Multiplechoice(self.package_id, True).qbank

    def before_leaving(self):
        super().before_leaving()
        self.table.end()
        self.new_question_form.grid_forget()
        self.b_add.configure(text="Add new Question", command=self.new_q_form)
