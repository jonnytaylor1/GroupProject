from tkinter import *
from UI import *
from Quiz.questions import QuestionDB

# This is a start page for the program
class Welcome(Page):

    def create(self):
        # Creating the grid
        self.autoresize_grid(rows=6, columns=1)

        b_font = ("MS", 14, "bold")
        GridLabel(self, text="Welcome!", font=("MS", 22, "bold"), pos=(0, 0, NSEW))

        #Button goes to multiplechoice quiz
        self.multiple_choice_button = HoverButton(self, text="Start multiplechoice quiz", font=b_font, pos=(1, 0, NSEW), command=self.go_to("MultipleChoice"))

        #J Goes to packages menu
        self.packages_button = HoverButton(self, text="Packages menu", font=b_font, pos=(4, 0, NSEW), command=self.go_to("PackageMenu"))

        #Button goes to statistics
        self.stats_button = HoverButton(self, text="View Statistics", font=b_font, pos=(3, 0, NSEW), command=self.go_to("Statistics"))

        #Button goes to hangman
        self.hangman_button = HoverButton(self, text="Start a game of hangman", font=b_font, pos=(2, 0, NSEW), command=self.go_to("Hangman"))

        #Button that controls settings
        self.settings = HoverButton(self, text="Settings Menu", font=b_font, pos=(5, 0, NSEW), command=self.go_to("SettingsMenu"))



        #Button goes to a test area for debugging
        # HoverButton(self, text="Test", font=b_font, pos=(5, 0, NSEW), command=self.go_to("Test"))

    def show(self):
        super().show()
        self.mainUI.root.geometry("500x500") # decides the size of the window

        if len(QuestionDB.get_quiz_questions(quiz="Hangman")) == 0:
            self.hangman_button.configure(state=DISABLED)
        else:
            self.hangman_button.configure(state=NORMAL)
        if len(QuestionDB.get_quiz_questions(quiz="Multi-Choice")) == 0:
            self.multiple_choice_button.configure(state=DISABLED)
        else:
            self.multiple_choice_button.configure(state=NORMAL)


        if self.mainUI.is_student:
            self.packages_button.hide()
            self.stats_button.hide()
            self.settings.hide()
        else:
            self.packages_button.show()
            self.stats_button.show()
            self.settings.show()
