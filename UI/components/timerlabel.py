from tkinter import *
from UI.easyGrid import EasyGrid
from datetime import datetime

class TimerLabel(EasyGrid, Label):
    def __init__(self, *args, mainUI, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainUI = mainUI
        self.displayed_time = StringVar()
        self.displayed_time.set("0")
        self.configure(textvariable=self.displayed_time)

    def start(self):
        self.start_time = datetime.now()
        self.id = self.mainUI.add_listener(self.update)

    def update(self):
        self.time = self.mainUI.clock - self.start_time
        self.displayed_time.set(formatter(self.time))

    def pause(self):
        self.mainUI.listeners.remove(self.update)

    def refresh(self):
        self.displayed_time.set("0")


def formatter(time):
    def form00(val): return str(val) if val > 9 else f"0{val}"
    tenths = str(time.microseconds)[0]
    secs = time.seconds % 60
    mins = time.seconds // 60
    return f"{form00(mins)}:{form00(secs)}.{tenths}"


