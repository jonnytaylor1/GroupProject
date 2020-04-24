from tkinter import *

class BetterEntry(Entry):
    def __init__(self, *args, bgText, **kwargs):
        Entry.__init__(self, *args, fg="grey", **kwargs)
        self.bgText = bgText
        self.insert(END, self.bgText)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<ButtonRelease-1>", self.on_focus_in)
        self.bind("<KeyRelease>", self.on_typing)
        self.placeholder = True

    def on_focus_in(self, e):
        if self.placeholder:
            self.icursor(0)

    def on_typing(self, e):
        if self.placeholder and self.index(INSERT) > 0:
            self.delete(self.index(INSERT), END)
            self["fg"] = "black"
            self.placeholder = False
        elif not len(self.get()) > 0 and not self.placeholder:
            self.insert(END, self.bgText)
            self["fg"] = "grey"
            self.placeholder = True
            self.icursor(0)

    def get(self):
        if self.placeholder:
            return ""
        else:
            return super().get()

class BetterText(Text):
    def __init__(self, *args, bgText, **kwargs):
        Text.__init__(self, *args, fg="grey", **kwargs)
        self.bgText = bgText
        self.insert(END, self.bgText)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<ButtonRelease-1>", self.on_focus_in)
        self.bind("<KeyRelease>", self.on_typing)
        self.placeholder = True

    def on_focus_in(self, e):
        if self.placeholder:
            self.mark_set("insert", "1.0")

    def on_typing(self, e):
        if self.placeholder and self.index(INSERT) != "1.0":
            index = self.index(INSERT)
            self.delete(index, END)
            if index[0] != "1":
                self.insert(END, "\n")
            self["fg"] = "black"
            self.placeholder = False
        elif not len(self.get("1.0", END)) > 1 and not self.placeholder:
            self.insert(END, self.bgText)
            self["fg"] = "grey"
            self.placeholder = True
            self.mark_set("insert", "1.0")

    def get(self, *args):
        if self.placeholder:
            return ""
        else:

            return super().get(*args)
