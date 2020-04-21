from tkinter import *
import time
import tkinter.messagebox
from PIL import Image, ImageTk


class Hangman(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent.root)

        # root.tag_raise(canvas)

        Label(self, text = "Question 1: ").grid(row=1, column=5)
        Label(self, text = "What does the fox say? ").grid(row=2, column=5)
        Label(self, text = "Time Elapsed ").grid(row=2, column=6)
        Label(self, text = "00:00").grid(row=2, column=7)

        self.correctLetters = Entry(self)
        self.correctLetters.grid(row=4, column=7, columnspan=8)

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            Button(self, text = letter).grid(row=5 + i // 8, column = 7 + i % 8 + 3 * (i // 24))
            Label(self, text = "").grid(row=9, column=7)
            Button(self, text = "Skip").grid(row=10, column =7, columnspan=2, sticky=E)
            Button(self, text = "Restart").grid(row=10, column =9, columnspan=3)
            Button(self, text = "End Quiz", command=lambda x=self: self.go_to_welcome()).grid(row=10, column =12, columnspan=3, sticky = W)

        # image = PhotoImage(file="image1.png")

        image = Image.open("./src/image1.png")
        image = image.resize((200, 200))
        imagetk = ImageTk.PhotoImage(image)
        canvas = Label(self, image=imagetk)
        canvas.image = imagetk
        canvas.grid(row=4, column=1, rowspan=11, columnspan = 5)


    def go_to_welcome(self):
        self.grid_forget()
        self.parent.pages["Welcome"].show()



        # imagetk = ImageTk.PhotoImage(image)
        # imagesprite = canvas.create_image(0,0,image=imagetk, anchor = NW)









#Main
