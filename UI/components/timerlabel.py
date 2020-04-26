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
        self.diff = self.mainUI.clock - self.start_time
        secs = self.diff.seconds % 60
        mins = self.diff.seconds // 60
        self.displayed_time.set(f"{mins if mins > 9 else '0' + str(mins)}:{secs if secs > 9 else '0' + str(secs)}.{str(self.diff.microseconds)[0]}")

    def pause(self):
        self.mainUI.listeners.remove(self.update)

    def refresh(self):
        self.displayed_time.set("0")
