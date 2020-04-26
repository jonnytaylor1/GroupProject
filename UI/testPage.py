from tkinter import *
from UI import *
from UI.hoverButton import HoverOptionMenu
from UI.quizSession import QuizSession
from datetime import datetime
import time


class Test(Page):

    def __init__(self, mainUI):
        super().__init__(mainUI)

    def show(self):
        super().show()
        Button(self, text="Hello there").pack(fill=BOTH, expand=1)

    def click(self):
        self.hb["state"] = DISABLED
        self.hb["bg"] = "green"