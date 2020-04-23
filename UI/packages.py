from tkinter import *
import sqlite3
from tkinter import messagebox
from Quiz.package import Package
from UI import *


class PackageMenu(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.root)
        self.parent = parent
        self.subFrame = Frame(self)
        self.subFrame.grid()

    def list_packages(self):
        self.subFrame = Frame(self)
        self.subFrame.grid(row = 0, column = 0, sticky=NSEW)

        self.table = TableView(self.subFrame, self.parent.root)
        self.table.grid()

        self.table.add_column(
            h_constructor=lambda f: Label(f, text="Package Name"),
            cell_constructor=lambda f, id: Label(f),
            property="name"
        )
        def drop_constructor(f, row_id):
            format_selected = StringVar()
            choices = ['None', 'Multi-Choice', 'Hangman']
            format_selected.set(self.table.data[row_id]["quiz_format"])
            format_selector = OptionMenu(f, format_selected, *choices, command=lambda value=format_selected.get(), package_id = self.table.data[row_id]["package_id"]: self.assign_format(package_id, value))
            # format_selector["command"] = lambda value=format_selected.get(), package_id = self.table.data[row_id]["package_id"]: self.assign_format(package_id, value)
            return format_selector

        self.table.add_column(
            h_constructor=lambda f: Label(f, text="Quiz Format"),
            cell_constructor=drop_constructor,
            property="quiz_format"
        )

        self.table.add_column(
            cell_constructor=lambda f, id: Button(f, text="Edit Package Name", command=lambda row_id=id: self.edit_p(row_id))
        )

        self.table.add_column(
            cell_constructor=lambda f, id: Button(f, text="Edit Package Questions", command=lambda package_id = self.table.data[id]["package_id"]: self.go_to_package_questions(package_id) )
        )

        self.table.add_column(
            cell_constructor=lambda f, id: Button(f, text="Delete", command=lambda package_id=self.table.data[id]["package_id"]: self.del_p(package_id))
        )

        self.table.data = Package().package_bank


        self.footer = Frame(self.subFrame)
        self.footer.grid(row=1, column=0, sticky=NSEW)

        self.add_new_package_b = Button(self.footer, text="Add new Package", command=self.create_p_form)
        self.add_new_package_b.grid(row = 0, column = 2, sticky = E)
        Button(self.footer, text="Back - Main Menu", command = self.go_menu).grid(row=0, column=0, sticky = W)
        self.footer.grid_columnconfigure(1, weight=2)

        # left for debugging purposes
        # Button(self.subFrame, text="Refresh", command=self.refresh).grid(row=4, column=4, sticky = SE)





# Updates the table with the format selected for the package (error handling: quiz format is unique and so only one package
# can be "Multi-Choice" and one package can be "Hangman", all other packages quiz format are set to null in the table

    def assign_format(self, package_id, value):
        package_id, name, quiz_format = Package.get_package(package_id)
        if value == "Multi-Choice" or value == "Hangman":
            try:
                Package.save_package(package_id, name, value)
            except sqlite3.IntegrityError:
                self.refresh()
                messagebox.showinfo("Alert", "You can only assign one question package to a quiz at a time. Please unassign a question package before continuing")
        else:
            Package.save_package(package_id, name, None)

# Creates an entry so that the user can save a new package
    def create_p_form(self):
        # self.add_new_package_b.destroy()
        self.refresh()

        self.formFrame = Frame(self.footer)
        self.formFrame.grid(row=0, column=1)


        Label(self.formFrame, text = "New Package Name").grid(row = 0, column = 0, sticky = E)

        self.package_name = Entry(self.formFrame)
        self.package_name.grid(row = 0, column = 1, sticky = W)

        self.add_new_package_b["command"] = self.send_p_data
        self.add_new_package_b["text"] = "Create"

        self.parent.root.update()

# Adds the new package to the database (Error handling: ensures that the package name is unique and is not blank)
    def send_p_data(self):
        if self.package_name.get() == "":
            messagebox.showinfo("Alert", "Blank package name has not been saved. You must enter a package name before saving")
        else:
            try:
                Package.add_package(self.package_name.get().rstrip())
                self.refresh()
            except sqlite3.IntegrityError:
                messagebox.showinfo("Alert", "There is already a package with this name, please choose a different name")



# Goes back to the main menu
    def go_menu(self):
        self.grid_forget()
        self.table.scrollbar.grid_forget()
        self.parent.pages["Welcome"].show()

    def refresh(self):
        try:
            self.subFrame.destroy()
        except:
            pass
        self.list_packages()
        self.parent.update_window_size(self)

# Deletes the package
    def del_p(self, i):
        confirmMessage = messagebox.askquestion ('Delete Package','Are you sure you want to delete this package, all questions inside the package will also be deleted',icon = 'warning')
        if confirmMessage == "yes":
            Package.delete_package(i)
        self.refresh()

# Allows the user to edit an existing package
    def edit_p(self, row_id):
        self.refresh()
        package_id = self.table.data[row_id]["package_id"]
        package_id, name, _ = Package.get_package(package_id)
        def constructor(frame):
            self.package_name = Entry(frame)
            self.package_name.insert(END, name)
            return self.package_name
        self.table.set_cell(row=row_id, column=0, func=constructor)

        for row_i, row in enumerate(self.table.data):
            self.table.get_cell(column=1, row=row_i).contents["state"] = "disabled"
            for i in range(3):
                self.table.get_cell(column=2 + i, row=row_i).hide()

        self.table.set_cell(row=row_id, column=2, func=lambda f: Button(f, text="Save", command=lambda: self.save_p(package_id)))

# Updates the package records (error handling: ensures that the package name is unique and is not empty)
    def save_p(self, package_id):
        package_id, _, quiz_format = Package.get_package(package_id)
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
        self.table.scrollbar.grid_forget()
        self.parent.pages["Settings"].show(package_id)

    def show(self):
        self.grid(column=0, row=0, sticky=NSEW)
        self.refresh()


