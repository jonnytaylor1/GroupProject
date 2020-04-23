from tkinter import *

class BetterEntry(Entry):
    def __init__(self, *args, bgText, **kwargs):
        Entry.__init__(self, *args, fg="grey", **kwargs)
        self.bgText = bgText
        self.insert(END, self.bgText)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<ButtonRelease-1>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<KeyRelease>", self.on_typing)
        self.bind("<KeyRelease-BackSpace>", self.on_focus_out)
        self.placeholder = True

    def on_focus_in(self, e):
        if self.placeholder:
            self.icursor(0)

    def on_typing(self, e):
        if self.placeholder and self.index(INSERT) > 0:
            self.delete(self.index(INSERT), END)
            self["fg"] = "black"
            self.placeholder = False

    def on_focus_out(self, e):
        if not len(self.get()) > 0:
            self.insert(END, self.bgText)
            self["fg"] = "grey"
            self.placeholder = True
            self.icursor(0)

class BetterText(Text):
    def __init__(self, *args, bgText, **kwargs):
        Text.__init__(self, *args, fg="grey", **kwargs)
        self.bgText = bgText
        self.insert(END, self.bgText)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<ButtonRelease-1>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<KeyRelease>", self.on_typing)
        self.bind("<KeyRelease-BackSpace>", self.on_focus_out)
        self.placeholder = True

    def on_focus_in(self, e):
        if self.placeholder:
            self.mark_set("insert", "1.0")
            print(self.index(CURRENT))

    def on_typing(self, e):
        if self.placeholder and self.index(INSERT) > 0:
            self.delete(self.index(INSERT), END)
            self["fg"] = "black"
            self.placeholder = False

    def on_focus_out(self, e):
        if not len(self.get()) > 0:
            self.insert(END, self.bgText)
            self["fg"] = "grey"
            self.placeholder = True
            self.mark_set("insert", "1.1")