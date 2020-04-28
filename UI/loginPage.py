from tkinter import *
from UI.page import Page
from UI.betterEntry import BetterEntry
from UI.hoverButton import HoverButton
from Quiz.password import PasswordDB

class LoginPage(Page):
    def create(self):
        self.autoresize_grid(rows=7, columns=6)
        self.password = BetterEntry(self, bgText="enter password", pos=(3,2, NSEW), font=("MS", 14, "bold"))
        HoverButton(self, command=self.check_password, pos=(3,3, NSEW), text="login", font=("MS", 14, "bold"))

    def check_password(self):
        if PasswordDB.get_password() == self.password.get():
            self.mainUI.is_student = False
            self.go_to("Welcome")()
        else:
            messagebox.showinfo("Alert", "Password is incorrect")

