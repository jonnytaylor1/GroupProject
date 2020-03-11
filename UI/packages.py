from tkinter import *
import sqlite3
from tkinter import messagebox
from Quiz.package import Package


class PackageMenu(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.list_packages()

    def list_packages(self):
        h_row = 1
        h_font = ("MS", 10, "bold")
        self.subFrame = Frame(self)
        self.subFrame.grid()
        Label(self.subFrame, text="Package Name", font = h_font).grid(row=h_row, column=2)
        Label(self.subFrame, text="Quiz Format", font = h_font).grid(row=h_row, column=4)

        row = 1
        self.rows = []
        for i, p in enumerate(Package().package_bank):
            row += 1
            l_name = Label(self.subFrame, text=p["name"])
            l_name.grid(row=row, column=2)
            b_edit = Button(self.subFrame, text="Edit Package Name")
            b_edit.grid(row=row, column=7)
            b_edit["command"] = lambda row=row, package_id = p["package_id"]: self.edit_p(row, package_id)
            b_edit_questions = Button(self.subFrame, text="Edit Package Questions")
            b_edit_questions.grid(row=row, column=8)
            b_edit_questions["command"] = lambda package_id = p["package_id"]: self.go_to_package_questions(package_id)

            # Dropdown menu for quiz format
            format_selected = StringVar()
            choices = ['None', 'Quiz 1','Quiz 2']
            # Unpacks package info
            if p["quiz_format"] == "Quiz 1" or "Quiz 2":
                format_selected.set(p["quiz_format"])
            else:
                format_selected.set("None")
            # When the dropdown menu is selected the command method is triggered
            format_dropdown = OptionMenu(self.subFrame, format_selected, *choices, command=lambda value=format_selected.get(), package_id = p["package_id"]: self.assign_format(package_id, value))
            format_dropdown.grid(row=row, column=4)
            Button(self.subFrame, text="Delete", command=lambda package_id=p["package_id"]: self.del_p(package_id)).grid(row=row, column=10)
            self.rows.append([l_name])
        self.add_new_package_b = Button(self.subFrame, text="Add new Package", command=lambda: self.create_p_form(row + 1))
        self.add_new_package_b.grid(row = row + 1, column = 3)
        Button(self.subFrame, text="Back - Main Menu", command = self.go_menu).grid(row=row + 2, column=3)
        # left for debugging purposes
        Button(self.subFrame, text="Refresh", command=self.refresh).grid(row=row + 3, column=3)

# Updates the table with the format selected for the package (error handling: quiz format is unique and so only one package
# can be "Quiz 1" and one package can be "Quiz 2", all other packages quiz format are set to null in the table

    def assign_format(self, package_id, value):
        package_id, name, quiz_format = Package.get_package(package_id)
        if value == "Quiz 1" or value == "Quiz 2":
            try:
                Package.save_package(package_id, name, value)
            except sqlite3.IntegrityError:
                self.refresh()
                messagebox.showinfo("Alert", "You can only assign one question package to a quiz at a time. Please unassign a question package before continuing")
        else:
            Package.save_package(package_id, name, None)

# Creates an entry so that the user can save a new package
    def create_p_form(self, new_row):
        self.add_new_package_b.destroy()

        self.package_name = Entry(self.subFrame)
        self.package_name.grid(row = new_row, column = 2)

        self.b = Button(self.subFrame, text = "Save", font = ("MS", 8, "bold"))
        self.b.grid(row = new_row, column = 3)
        self.b["command"] = self.send_p_data

# Adds the new package to the database (Error handling: ensures that the package name is unique and is not blank)
    def send_p_data(self):
        if self.package_name.get() == "":
            messagebox.showinfo("Alert", "Blank package name has not been saved. You must enter a package name before saving")
        else:
            try:
                p = {"name": self.package_name.get().rstrip()}
                Package.add_package(p)
                self.refresh()
            except sqlite3.IntegrityError:
                messagebox.showinfo("Alert", "There is already a package with this name, please choose a different name")



# Goes back to the main menu
    def go_menu(self):
        self.grid_forget()
        self.parent.pages["Welcome"].grid()

    def refresh(self):
        self.subFrame.destroy()
        self.list_packages()

# Deletes the package
    def del_p(self, i):
        Package.delete_package(i)
        self.refresh()

# Allows the user to edit an existing package
    def edit_p(self, row, package_id):
        for label in self.rows[row - 2]:
            label.grid_remove()
        self.create_p_form(row)
        package_id, name, quiz_format = Package.get_package(package_id)
        self.package_name.insert(END, name)
        self.b["command"] = lambda: self.save_p(package_id)

# Updates the package records (error handling: ensures that the package name is unique and is not empty)
    def save_p(self, package_id):
        package_id, name, quiz_format = Package.get_package(package_id)
        if self.package_name.get() == "":
            messagebox.showinfo("Alert", "Blank package name has not been saved. You must enter a package name before saving")
        else:
            try:
                Package.save_package(package_id, self.package_name.get().rstrip(), quiz_format)
                self.refresh()

            except sqlite3.IntegrityError:
                messagebox.showinfo("Alert", "There is already a package with this name, please choose a different name")


# Will eventually go to the packages questions
    def go_to_package_questions(self, package_id):
        self.grid_forget()
        self.parent.pages["Settings"].show(package_id)

