from tkinter import *
import time
import tkinter.messagebox
from Quiz.hangman import Hangman as HangmanDB
from UI.page import Page
from UI.usefulLabel import GridLabel
from UI.hoverButton import HoverButton
from UI.components.timerlabel import TimerLabel
from Quiz.statistics import Statistics
from datetime import datetime
from UI.quizSession import create_vars, QuizSession, Question
from UI.components.image import Image
from UI.endscreen import Stats, EndScreen
from Quiz.questions import QuestionDB

class Hangman(Page):
        # root.tag_raise(canvas)
    def create(self):
        self.autoresize_grid(rows=4, columns=3)
        self.grid_columnconfigure(0, weight=0)

        self.upperFrame = Frame(self)
        self.upperFrame.grid(row=0, column=0, columnspan=3)
        self.vars = create_vars()
        self.question = GridLabel(self.upperFrame, textvariable=self.vars.q_num, pos=(0, 0))
        self.question_label = GridLabel(self.upperFrame, pos=(1, 0), textvariable=self.vars.prompt, wraplength=350)
        GridLabel(self.upperFrame, text="Time Elapsed ", pos=(0, 1))
        self.timer = TimerLabel(self.upperFrame, mainUI=self.mainUI, pos=(0, 2))  #takes a string variable created in main UI, it tracks the timer.


        #### LEFT FRAME #####
        self.left_frame = Frame(self)
        self.left_frame.grid(row=1, rowspan=2, column=0)

        #THIS creates a place for the image, but it is empty, when refresh is run, we implement the initial image.
        self.hangman_image = Image(self.left_frame)
        self.hangman_image.pack()

        # INCORRECT LABEL##
        self.incorrect_letter_space = []
        self.incorrectFrame = Frame(self.left_frame)
        self.incorrectFrame.pack()
        GridLabel(self.incorrectFrame, text="Incorrect Letters: ").pack()
        self.incorrect_letters = Frame(self.incorrectFrame)
        self.incorrect_letters.pack()
        for i in range(6):
            incorrect = StringVar()
            incorrect.set("_")
            GridLabel(self.incorrect_letters, textvariable=incorrect, pos=(0, i))
            self.incorrect_letter_space.append(incorrect)


        self.mainFrame = Frame(self)
        self.mainFrame.grid(row=1, column=1, columnspan=2, rowspan=2, sticky=NSEW)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid_rowconfigure(1, weight=1)
        self.correctUnderscore = StringVar()
        self.correctLetters = GridLabel(self.mainFrame, textvariable=self.correctUnderscore, pos=(0, 0, NSEW)) #Because the variable constantly changes, Label updates accordingly.

        self.keyboard = Frame(self.mainFrame)
        self.keyboard.grid(row=1, column=0, sticky=NSEW, columnspan=2, pady=45, padx=10)

        self.buttons = []
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            row = i // 8
            column = i % 8 + 3 * (i // 24)
            self.keyboard.grid_rowconfigure(row, weight=1)
            self.keyboard.grid_columnconfigure(column, weight=1)
            b = HoverButton(self.keyboard, text=letter, command=lambda x=i: self.click_letter(x), pos=(i // 8, i % 8 + 3 * (i // 24), NSEW))
            b.grid(pady=7, padx=2)
            self.buttons.append(b)

        self.footer = Frame(self)
        self.footer.grid(row=3, column=0, columnspan=3, sticky=NSEW)
        self.skip_button = HoverButton(self.footer, text="Skip", command=self.skip_q) #everything with self.... in order to be able to reuse later.
        self.skip_button.pack(fill=BOTH, expand=1, side=LEFT)
        self.restart_button = HoverButton(self.footer, text="Restart", command=self.restart_quiz) #runs refresh() no parenthesis though, otherwise runs immediatley not when pressed
        self.restart_button.pack(fill=BOTH, expand=1, side=LEFT)
        self.end_quiz_button = HoverButton(self.footer, text="End Quiz", command=self.end_quiz)
        self.end_quiz_button.pack(fill=BOTH, expand=1, side=LEFT)


    def next_q(self):
        if self.session.is_finished():
            self.go_to("EndScreen")(self.session)
        else:
            self.session.start_question()
        self.lives = 6
        self.question_obj = self.session.get_q()
        self.corr = self.session.get_q().get_correct()

        #
        # ################# CORRECT LETTERS #########################
        self.underscores = ["_"] * len(self.corr)
        self.correctUnderscore.set(self.underscores) #each time update the uderscore variable, we need to do .set()
        for under in self.incorrect_letter_space:
            under.set("_")

        ###IMAGE ####
        self.hangman_image.set(path=f"./src/image{6-self.lives}.png")
        #refresh the skip button back to its original text value "Skip button" not "next question button"
        self.skip_button.configure(text="Skip")
        self.end_quiz_button.pack()
        self.restart_button.pack()
        self.timer.start() #Unfreezes the timer

        for button in self.buttons: button.configure(state=NORMAL) #UNFREEZE BUTTONS

    def show(self):
        super().show()
        self.session = QuizSession(vars=self.vars, type="Hangman").fetch_questions()
        # self.questions = HangmanDB.get_hangman_qs(True)  # randomly retrieve Hangman QUestions from the backend
        self.next_q()

    def click_letter(self, i):
        guessed_letter = self.buttons[i]["text"].lower()

        self.buttons[i].configure(state=DISABLED)
        ##### iF CORRECT LETTER #####
        if guessed_letter in self.corr.lower():
            for index, letter in enumerate(self.corr):
                if letter.lower() == guessed_letter:
                    self.underscores[index] = letter.upper() #match index positions, assign our letter from the correct answer in the correct letters field.
            self.correctUnderscore.set(self.underscores) # after done looping, update the label all at once.
        else:

            #List comprehention: #checks if the letter in incorrect space is an underscore, if yes, then the incorrectly chosen letter is popullated in the space.
            #Version 1[letter for letter in self.incorrect_letter_space if letter.get() == "_"][0].set(guessed_letter.upper())

            #Version 2
            self.incorrect_letter_space[-self.lives].set(guessed_letter.upper())
            self.lives -= 1
            self.hangman_image.set(path=f"./src/image{6-self.lives}.png")
        answer = "".join(self.underscores).upper().replace("_"," ")
        self.vars.choices[0].set(answer)
        if self.lives == 0 or self.corr.upper() == answer: #Making sure that the answer of the question is equal to our list of correct LETTERS
        #the correct letters are inside a lsit, which we concatinate into a single string with an underscore in the middle, then repalce the underscore with a sapce to match the answer.
            for button in self.buttons:
                button.configure(state=DISABLED)
            self.session.answer()
            self.skip_button.configure(text="Next Question")
            self.end_quiz_button.hide()
            self.restart_button.hide()
            self.timer.pause()

#######################_____________________________   S T A T I S T I C S __________________________##########################

    def restart_quiz(self):
        self.session.abandon()
        self.show() #loads the page again.

    def end_quiz(self):
        self.session.abandon()
        self.go_to("EndScreen")(self.session)

    def skip_q(self):
        if self.session.ongoing_question():
            self.session.skip()
        self.next_q()
