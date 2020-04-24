from tkinter import *
from UI import *

class HoverButton(EasyGrid, Button):
    def __init__(self, *args, bg="#e8e6e6", fg="#000000", bg_hover="#a6a6a6", fg_hover="#ffffff", **kwargs):
        super().__init__(*args, **kwargs)
        self.bg = bg
        self.fg = fg
        self.bg_hover = bg_hover
        self.fg_hover = fg_hover
        self.add_hover_effect()

    # applies event listeners to check for mouse entering and exiting the bounds of the button
    def add_hover_effect(self):
        self.bind("<Enter>", lambda event, h=self: h.configure(bg=self.bg_hover, fg=self.fg_hover))
        self.bind("<Leave>", lambda event, h=self: h.configure(bg=self.bg, fg=self.fg))

    # removes event listeners and restore initial colors
    def remove_hover_effect(self):
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.configure(bg=self.bg, fg=self.fg)

    def configure(self, cnf=None, **kw):
        try:
            if kw["state"] == DISABLED:
                self.remove_hover_effect()
            elif kw["state"] == NORMAL:
                self.add_hover_effect()
        except: pass

        return super().configure(cnf=cnf, **kw)

    def __setitem__(self, key, value):
        if key == "state":
            if value == DISABLED:
                self.remove_hover_effect()
            elif value == NORMAL:
                self.add_hover_effect()

        return super().__setitem__(key, value)


class HoverOptionMenu(EasyGrid, OptionMenu):
    def __init__(self, *args, bg="#e8e6e6", fg="#000000", bg_hover="#a6a6a6", fg_hover="#ffffff", **kwargs):
        super().__init__(*args, **kwargs)
        self.bg = bg
        self.fg = fg
        self.bg_hover = bg_hover
        self.fg_hover = fg_hover
        self.add_hover_effect()

    # applies event listeners to check for mouse entering and exiting the bounds of the button
    def add_hover_effect(self):
        self.bind("<Enter>", lambda event, h=self: h.configure(bg=self.bg_hover, fg=self.fg_hover))
        self.bind("<Leave>", lambda event, h=self: h.configure(bg=self.bg, fg=self.fg))

    # removes event listeners and restore initial colors
    def remove_hover_effect(self):
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.configure(bg=self.bg, fg=self.fg)

    def configure(self, cnf=None, **kw):
        try:
            if kw["state"] == DISABLED:
                self.remove_hover_effect()
            elif kw["state"] == NORMAL:
                self.add_hover_effect()
        except: pass

        return super().configure(cnf=cnf, **kw)

    def __setitem__(self, key, value):
        if key == "state":
            if value == DISABLED:
                self.remove_hover_effect()
            elif value == NORMAL:
                self.add_hover_effect()

        return super().__setitem__(key, value)
