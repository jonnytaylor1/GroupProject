from tkinter import *
import sqlite3
from tkinter import messagebox
from Quiz.package import Package
from UI import *
from Quiz.packageHelper import check_for_numbers


class PackageMenu(Page):

    def create(self):
        self.table = TableView(self, self.mainUI.root)
        self.table.pack(fill=BOTH, expand=1)
        self.table.add_column(title="Package Name", property="name")
        def drop_constructor(f, row_id):
            format_selected = StringVar()
            choices = ['None', 'Multi-Choice', 'Hangman']
            format_selected.set(self.table.data[row_id]["quiz_format"])
            format_selector = OptionMenu(f, format_selected, *choices, command=lambda value=format_selected.get(),
                                                                                      package_id = self.table.data[row_id]["package_id"]: self.assign_format(package_id, value))
            format_selector.configure(bg="#e8e6e6", fg="#000000", activebackground="#a6a6a6", activeforeground="#ffffff")
            return format_selector
        self.table.add_column(title="Quiz Format", cell_constructor=drop_constructor, property="quiz_format")
        self.table.add_column(
            cell_constructor=lambda f, id: HoverButton(f, text="Edit Package Name",
                                                       command=lambda row_id=id: self.edit_p(row_id))
        )
        self.table.add_column(
            cell_constructor=lambda f, id: HoverButton(f, text="Edit Package Questions",
                                                       command=lambda package_id = self.table.data[id]["package_id"]: self.go_to("Settings")(package_id) )
        )
        self.table.add_column(
            cell_constructor=lambda f, id: HoverButton(f, text="Delete",
                                                       command=lambda package_id=self.table.data[id]["package_id"]: self.del_p(package_id))
        )

        self.footer = Frame(self)
        self.footer.pack(fill=X)
        self.add_new_package_b = HoverButton(self.footer, text="Add new Package", command=self.create_p_form)
        self.add_new_package_b.grid(row=0, column=2, sticky=E)
        HoverButton(self.footer, text="Back - Main Menu", command=self.go_to("Welcome")).grid(row=0, column=0, sticky=W)
        self.footer.grid_columnconfigure(1, weight=2)

        # left for debugging purposes
        # Button(self.subFrame, text="Refresh", command=self.refresh).grid(row=4, column=4, sticky = SE)

    # Updates the table with the format selected for the package (error handling: quiz format is unique and so only one package
    # can be "Multi-Choice" and one package can be "Hangman", all other packages quiz format are set to null in the table

    def assign_format(self, package_id, value):
        package_id, name, quiz_format = Package.get_package(package_id)

        if value == "Hangman":
            if check_for_numbers(package_id=package_id):
                messagebox.showinfo("Alert",
                                    "Cannot assign a package with numbers to Hangman")
            else:
                try:
                    Package.save_package(package_id, name, value)
                except sqlite3.IntegrityError:
                    messagebox.showinfo("Alert",
                                        "You can only assign one question package to a quiz at a time. Please unassign a question package before continuing")
        elif value == "Multi-Choice":
            try:
                Package.save_package(package_id, name, value)
            except sqlite3.IntegrityError:
                messagebox.showinfo("Alert", "You can only assign one question package to a quiz at a time. Please unassign a question package before continuing")
        else:
            Package.save_package(package_id, name, None)
        self.show()

    # Creates an entry so that the user can save a new package
    def create_p_form(self):
        # self.add_new_package_b.destroy()
        self.formFrame = Frame(self.footer)
        self.formFrame.grid(row=0, column=1)
        self.package_name = BetterEntry(self.formFrame, bgText="Enter Package Name", pos=(0, 1, W))
        self.add_new_package_b.configure(command=self.send_p_data, text="Create")
        self.mainUI.root.update()

    # Adds the new package to the database (Error handling: ensures that the package name is unique and is not blank)
    def send_p_data(self):
        if self.package_name.get() == "" or self.package_name.placeholder:
            messagebox.showinfo("Alert", "Blank package name has not been saved. You must enter a package name before saving")
        else:
            try:
                Package.add_package(self.package_name.get().rstrip())
            except sqlite3.IntegrityError:
                messagebox.showinfo("Alert", "There is already a package with this name, please choose a different name")
        self.show()
        self.formFrame.grid_forget()
        self.add_new_package_b.configure(command=self.create_p_form, text="Add new Package")

    # Deletes the package
    def del_p(self, i):
        confirmMessage = messagebox.askquestion ('Delete Package','Are you sure you want to delete this package, all questions inside the package will also be deleted',icon = 'warning')
        if confirmMessage == "yes":
            Package.delete_package(i)
        self.show()

    # Allows the user to edit an existing package
    def edit_p(self, row_id):
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

            except sqlite3.IntegrityError:
                messagebox.showinfo("Alert", "There is already a package with this name, please choose a different name")
        self.show()

    def before_showing(self):
        self.table.data = Package().package_bank

    def before_leaving(self):
        super().before_leaving()
        self.table.end()

