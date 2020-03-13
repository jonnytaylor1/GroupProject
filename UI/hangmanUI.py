from tkinter import *
import time
import tkinter.messagebox
from PIL import Image, ImageTk
from Quiz.hangman import Hangman as HangmanDB


class Hangman(Frame):
    def __init__(self, parent):
        self.parent = parent #PARENT IS THE MAIN UI
        Frame.__init__(self, parent.root)


        # root.tag_raise(canvas)

        self.question = Label(self, text = "Question 1: ")
        self.question.grid(row=1, column=5)

        self.question_label = Label(self, text = "What does the fox say? ")
        self.question_label.grid(row=2, column=5)

        Label(self, text = "Time Elapsed ").grid(row=2, column=6)
        self.time = Label(self, textvariable = self.parent.timer)
        self.time.grid(row=2, column=7) #takes a string variable created in main UI, it tracks the timer.



        self.buttons= []
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            b = Button(self, text = letter)
            b["command"] = lambda x=b: self.click_letter(x)
            b.grid(row=5 + i // 8, column = 7 + i % 8 + 3 * (i // 24))
            self.buttons.append(b)

        Label(self, text = "").grid(row=9, column=7)

        self.skip_button = Button(self, text = "Skip") #everything with self.... in order to be able to reuse later.
        self.skip_button.grid(row=10, column =7, columnspan=2, sticky=E)

        self.restart_button = Button(self, text = "Restart", command=self.refresh) #runs refresh() no parenthesis though, otherwise runs immediatley not when pressed
        self.restart_button.grid(row=10, column =9, columnspan=3)

        self.end_quiz_button = Button(self, text = "End Quiz", command=self.go_to_welcome)
        self.end_quiz_button.grid(row=10, column =12, columnspan=3, sticky = W)

        # image = PhotoImage(file="image1.png")

        #INCORRECT LABEL##
        Label(self, text="        ").grid(row=4, column=17)
        Label(self, text="Incorrect Letters: ").grid(row=3, column=18, columnspan=6)

        #THIS creates a place for the image, but it is empty, when refresh is run, we implement the initial image.
        self.canvas = Label(self)
        self.canvas.grid(row=4, column=1, rowspan=11, columnspan = 5)

        self.questions = HangmanDB.get_hangman_qs(True) # randomly retrieve Hangman QUestions from the backend



        self.refresh()


    def refresh(self):
        self.questionID, self.question_label["text"], _, self.correctAnswer = next(self.questions) #create variables, which asks Database for next question, the database is going to provide
        #data as a tuple, and we unpack it into the empty variables. ",_," means like an empty variable, which dont want to use it.

        self.lives = 6
        self.parent.clock1 = time.time() # reset the clock provided from Main UI


        ################# CORRECT LETTERS #########################
        self.underscores = ["_"] * len(self.correctAnswer)
        self.correctUnderscore = StringVar()
        self.correctUnderscore.set(self.underscores) #each time update the uderscore variable, we need to do .set()

        self.correctLetters = Label(self, textvariable=self.correctUnderscore) #Because the variable constantly changes, Label updates accordingly.
        self.correctLetters.grid(row=4, column=7, columnspan=8)



        self.incorrect_letter_space = []
        for i in range(6):
            incorrect = StringVar()
            incorrect.set("_")
            l = Label(self, textvariable = incorrect)
            self.incorrect_letter_space.append(incorrect)
            l.grid(row=4, column=18+i)


        ###IMAGE ####
        image = Image.open(f"./src/image{6-self.lives}.png")
        image = image.resize((200, 200))
        imagetk = ImageTk.PhotoImage(image)
        self.canvas["image"] = imagetk # this actually puts image into the space.

        self.canvas.image = imagetk #This solves the problem of disappearing image, saves a refrence to the actual image.

        #refresh the skip button back to its original text value "Skip button" not "next question button"
        self.skip_button["text"] = "Skip"
        self.skip_button.grid(columnspan=2) # fixes layout issue
        self.end_quiz_button.grid()
        self.restart_button.grid()
        self.time["textvariable"] = self.parent.timer #Unfreezes the timer

        for button in self.buttons: #UNFREEZE BUTTONS
            button["state"] = NORMAL


    def go_to_welcome(self):
        self.grid_forget()
        self.parent.pages["Welcome"].grid()


    def click_letter(self,clicked_button):
        guessed_letter = clicked_button["text"].lower()
        clicked_button["state"] = DISABLED
        ##### iF CORRECT LETTER #####
        if guessed_letter in self.correctAnswer.lower():
            for index,letter in enumerate(self.correctAnswer):
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
            if self.lives == 0:
                for button in self.buttons:
                    button["state"] = DISABLED

                self.skip_button["text"] = "Next Question"
                self.skip_button.grid(columnspan=8) # fixes layout issue
                self.end_quiz_button.grid_forget()
                self.restart_button.grid_forget()
                self.time["textvariable"] = self.parent.timer.get()



        ##### iF INCORRECT LETTER #####





        # imagetk = ImageTk.PhotoImage(image)
        # imagesprite = canvas.create_image(0,0,image=imagetk, anchor = NW)









#Main
