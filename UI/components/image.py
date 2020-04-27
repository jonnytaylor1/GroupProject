from tkinter import *
from UI.easyGrid import EasyGrid
from PIL import Image as ImagePIL
from PIL import ImageTk
# from PIL import Image, ImageTk

class Image(EasyGrid, Label):

    def set(self, *, path, fit_size=(200, 200)):
        image = ImagePIL.open(path)
        image = image.resize(fit_size)
        imagetk = ImageTk.PhotoImage(image)
        self.configure(image=imagetk) # this actually puts image into the space.
        self.image = imagetk

