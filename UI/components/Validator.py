from tkinter import *


def field_checker(*args, f_commiter):
    for arg in args:
        if len(arg) == 0:
            messagebox.showinfo("Alert", "Blank value cannot be saved. You must enter a valid value before saving")
            return None
    else:
        f_commiter()