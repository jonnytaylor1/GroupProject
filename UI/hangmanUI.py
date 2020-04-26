from tkinter import *
import time
import tkinter.messagebox
from PIL import Image, ImageTk
from Quiz.hangman import Hangman as HangmanDB
from UI.page import Page
from UI.usefulLabel import GridLabel
from UI.hoverButton import HoverButton
from UI.components.timerlabel import TimerLabel
from Quiz.statistics import Statistics
from datetime import datetime
from UI.quizSession import Vars

class Hangman(Page):
        # root.tag_raise(canvas)
    def create(self):

        self.question = GridLabel(self, text = "Question 1: ", pos=(1, 5))
        self.question_label = GridLabel(self, text = "What does the fox say? ", pos=(2, 5))
        GridLabel(self, text = "Time Elapsed ", pos=(2, 6))
        self.timer = TimerLabel(self, mainUI=self.mainUI, pos=(2, 7))  #takes a string variable created in main UI, it tracks the timer.

        self.correctUnderscore = StringVar()
        self.correctLetters = GridLabel(self, textvariable=self.correctUnderscore, pos=(4, 7), cspan=8) #Because the variable constantly changes, Label updates accordingly.

        self.buttons= []
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            b = HoverButton(self, text=letter, command=lambda x=i: self.click_letter(x), pos=(5 + i // 8, 7 + i % 8 + 3 * (i // 24)))
            self.buttons.append(b)

        GridLabel(self, text = "", pos=(9, 7))

        self.skip_button = HoverButton(self, text="Skip", command=self.skip_q, pos=(10, 7, E), cspan=2) #everything with self.... in order to be able to reuse later.
        self.restart_button = HoverButton(self, text="Restart", command=self.restart_quiz, pos=(10, 9), cspan=3) #runs refresh() no parenthesis though, otherwise runs immediatley not when pressed

        self.end_quiz_button = HoverButton(self, text="End Quiz", command=self.end_quiz, pos=(10, 12, W), cspan=3)
        # image = PhotoImage(file="image1.png")

        #INCORRECT LABEL##
        GridLabel(self, text="        ", pos=(4, 17))
        GridLabel(self, text="Incorrect Letters: ", pos=(3, 18), cspan=6)
        #THIS creates a place for the image, but it is empty, when refresh is run, we implement the initial image.
        self.canvas = GridLabel(self, pos=(4, 1), rspan=11, cspan=5)

    def next_q(self):
        try:
            self.questionID, self.question_label["text"], _, self.correctAnswer = next(self.questions) #create variables, which asks Database for next question, the database is going to provide
            #data as a tuple, and we unpack it into the empty variables. ",_," means like an empty variable, which dont want to use it.
        except StopIteration:
            self.go_to("Welcome")()
        self.lives = 6

        ################# CORRECT LETTERS #########################
        self.underscores = ["_"] * len(self.correctAnswer)
        self.correctUnderscore.set(self.underscores) #each time update the uderscore variable, we need to do .set()

        self.incorrect_letter_space = []
        for i in range(6):
            incorrect = StringVar()
            incorrect.set("_")
            GridLabel(self, textvariable=incorrect, pos=(4, 18+i))
            self.incorrect_letter_space.append(incorrect)

        ###IMAGE ####
        image = Image.open(f"./src/image{6-self.lives}.png")
        image = image.resize((200, 200))
        imagetk = ImageTk.PhotoImage(image)
        self.canvas["image"] = imagetk # this actually puts image into the space.

        self.canvas.image = imagetk #This solves the problem of disappearing image, saves a refrence to the actual image.

        #refresh the skip button back to its original text value "Skip button" not "next question button"
        self.skip_button.configure(text="Skip")
        self.skip_button.grid(columnspan=2) # fixes layout issue
        self.end_quiz_button.show()
        self.restart_button.show()
        self.timer.start() #Unfreezes the timer

        for button in self.buttons: button.configure(state=NORMAL) #UNFREEZE BUTTONS

    def show(self):
        super().show()
        self.questions = HangmanDB.get_hangman_qs(True)  # randomly retrieve Hangman QUestions from the backend
        self.next_q()

    def click_letter(self, i):
        guessed_letter = self.buttons[i]["text"].lower()
        self.buttons[i].configure(state=DISABLED)
        ##### iF CORRECT LETTER #####
        if guessed_letter in self.correctAnswer.lower():
            for index, letter in enumerate(self.correctAnswer):
                if letter.lower() == guessed_letter:
                    self.underscores[index] = letter.upper() #match index positions, assign our letter from the correct answer in the correct letters field.
            self.correctUnderscore.set(self.underscores) # after done looping, update the label all at once.
        else:

            #List comprehention: #checks if the letter in incorrect space is an underscore, if yes, then the incorrectly chosen letter is popullated in the space.
            #Version 1[letter for letter in self.incorrect_letter_space if letter.get() == "_"][0].set(guessed_letter.upper())

            #Version 2
            self.incorrect_letter_space[-self.lives].set(guessed_letter.upper())
            self.lives -= 1
            image = Image.open(f"./src/image{6-self.lives}.png")
            image = image.resize((200, 200))
            imagetk = ImageTk.PhotoImage(image)
            self.canvas["image"] = imagetk
            self.canvas.image = imagetk
        if self.lives == 0 or self.correctAnswer.lower() == "".join(self.underscores).lower().replace("_"," "): #Making sure that the answer of the question is equal to our list of correct LETTERS
        #the correct letters are inside a lsit, which we concatinate into a single string with an underscore in the middle, then repalce the underscore with a sapce to match the answer.
            for button in self.buttons:
                button.configure(state=DISABLED)

            self.skip_button.configure(text="Next Question")
            self.skip_button.grid(columnspan=8) # fixes layout issue
            self.end_quiz_button.hide()
            self.restart_button.hide()
            self.timer.pause()
            self.is_done = True

#######################_____________________________   S T A T I S T I C S __________________________##########################

            #WHEN ANSWERED:
            Statistics.save_answer_stats(
                id=self.questionID,
                quiz_format="Hangman",
                status="incorrect" if self.lives==0 else "correct", # pass in either correct or incorrect status
                time=self.timer.time, #self.timer.time returns the time displayed on the timer.
                created_at=datetime.now(),
            )


    def restart_quiz(self):
        Statistics.save_answer_stats(
            id=self.questionID,
            quiz_format="Hangman",
            status="abandoned",
            time=self.timer.time, #self.timer.time returns the time displayed on the timer.
            created_at=datetime.now(),
        )
        self.show() #loads the page again.

    def end_quiz(self):
        Statistics.save_answer_stats(
            id=self.questionID,
            quiz_format="Hangman",
            status="abandoned",
            time=self.timer.time, #self.timer.time returns the time displayed on the timer.
            created_at=datetime.now(),
        )
        self.go_to("Welcome")()

    def skip_q(self):
        Statistics.save_answer_stats(
         id=self.questionID,
         quiz_format="Hangman",
         status="skipped", # pass in either correct or incorrect status
         time=self.timer.time, #self.timer.time returns the time displayed on the timer.
         created_at=datetime.now(),
         )
        self.next_q()
