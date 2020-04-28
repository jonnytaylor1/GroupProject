from tkinter import *
from UI.page import Page
from UI.hoverButton import HoverButton
from UI.usefulLabel import GridLabel

class UserTypePage(Page):

    def create(self):
        self.autoresize_grid(rows=2, columns=2)

        GridLabel(self, text="Please choose your account type", font=("MS", 22, "bold"), pos=(0,0, NSEW), cspan=2)

        HoverButton(self, text="Student", pos=(1, 0, NSEW), font=("MS", 14, "bold"), command=self.get_student_ver)
        HoverButton(self, text="Teacher", pos=(1, 1, NSEW), font=("MS", 14, "bold"), command=self.go_to("Login"))

    def get_student_ver(self):
        self.mainUI.is_student = True
        self.go_to("Welcome")()


