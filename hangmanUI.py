from tkinter import *
import time
import tkinter.messagebox
from PIL import ImageTk, Image

class Hangman(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()

        image = PhotoImage(file = "image1.png")
        canvas = Label(self,image = image)
        canvas.grid(row=4,column=1)
        root.tag_raise(canvas)

        Label(self, text = "Question 1: ").grid(row=1, column=5)
        Label(self, text = "What does the fox say? ").grid(row=2, column=5)
        Label(self, text = "Time Elapsed ").grid(row=2, column=6)
        Label(self, text = "00:00").grid(row=2, column=7)

        self.correctLetters = Entry(self)
        self.correctLetters.grid(row=4, column=7, columnspan=4)

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            Button(self, text = letter).grid(row=5 + i // 8, column = 7 + i % 8 + 3 * (i // 24))

            Label(self, text = "").grid(row=9, column=7)
            Button(self, text = "Skip").grid(row=10, column =7, columnspan=2)
            Button(self, text = "Restart").grid(row=10, column =9, columnspan=3)
            Button(self, text = "End Quiz").grid(row=10, column =12, columnspan=3)


        # image = Image.open("image1.png")

        # imagetk = ImageTk.PhotoImage(image)
        # imagesprite = canvas.create_image(0,0,image=imagetk, anchor = NW)









#Main
root = Tk()
root.title("H Quiz")
root.geometry("1000x500")
app = Hangman(root)
app.grid()
root.mainloop()
