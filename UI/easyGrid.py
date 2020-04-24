# Add the easy grid as as the first (left-most) inherited class for your tkinter widget to make grid positioning easy.
# Either use your usual keywords (eg. column, row) when creating a widget or use pos keyword to pass a tuple
# (row, column, sticky) eg. (1, 2, E) will position the widget on row 1, column 2 with sticky E
class EasyGrid:
    def __init__(self, *args, row=None, column=None, sticky=None, pos=None, cspan=None, rspan=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._row = row
        self._column = column
        self._cspan = cspan
        self._rspan = rspan
        self._sticky = sticky
        if pos:
            try: self._sticky = pos[2]
            except: pass
            self._row = pos[0]
            self._column = pos[1]
            self.show()
        elif row != None:
            self.show()


    def hide(self):
        self.grid_forget()
        return self

    def show(self):
        self.grid(row=self._row, column=self._column, sticky=self._sticky, columnspan=self._cspan, rowspan=self._rspan)
        return self