from UI.page import Page
from UI.betterEntry import BetterEntry
from UI.hoverButton import HoverButton
from tkinter import *
from Quiz.password import PasswordDB

class SettingsPage(Page):
    def create(self):
        font = ("MS", 14, "bold")
        self.autoresize_grid(rows=8, columns=3)
        self.old_pass = BetterEntry(self, bgText="Enter Old Password", font=font, pos=(1, 1, NSEW))
        self.new_pass = BetterEntry(self, bgText="Enter New Password", font=font, pos=(2, 1, NSEW))
        self.new_pass_confirm = BetterEntry(self, bgText="Confirm New Password", font=font, pos=(3, 1, NSEW))
        self.bottomFrame = Frame(self)
        self.bottomFrame.grid(row=7, column=0, columnspan=3, sticky=NSEW)
        HoverButton(self.bottomFrame, text="Change Password", font=font, command=self.change_password).pack(fill=BOTH, expand=1, side=RIGHT)
        HoverButton(self.bottomFrame, text="Main Menu", font=font, command=self.go_to("Welcome")).pack(fill=BOTH, expand=1, side=LEFT)

    def show(self):
        super().show()
        self.old_pass.clear()
        self.new_pass.clear()
        self.new_pass_confirm.clear()

    def change_password(self):
        if PasswordDB.get_password() != self.old_pass.get():
            messagebox.showinfo("Alert", "Password is incorrect")
        elif self.new_pass.get() != self.new_pass_confirm.get():
            messagebox.showinfo("Alert", "New password and confirmation password should match")
        elif len(self.new_pass.get()) < 4:
            messagebox.showinfo("Alert", "Password should be at least 4 characters long")
        else:
            PasswordDB.set_password(self.new_pass.get())
            messagebox.showinfo("Alert", "Password has been changed successfuly")
            self.show()
