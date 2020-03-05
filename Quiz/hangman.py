from data.connection import Connection
from Quiz.multiplechoice import Multiplechoice
from random import shuffle

class Hangman():
    def __init__(self):
        pass

    def get_question(self):
        m = Multiplechoice()
        shuffle(m.qbank)
        return m.qbank[0]
