from data.connection import Connection
from Quiz.multiplechoice import Multiplechoice
from random import shuffle

class Hangman():
    def __init__(self):
        pass

    def get_question():
        m = Multiplechoice()
        shuffle(m.qbank)
        return m.qbank[0]


    def get_hangman_qs(random = False):
        bank = []
        with Connection() as con:
            with con:
                for row in con.execute('''
                            SELECT
                            id,
                            question,
                            correct,
                            incorrect1,
                            incorrect2,
                            incorrect3
                            FROM questions
                            INNER JOIN packages
                            ON questions.package_id = packages.package_id
                            WHERE packages.quiz_format = 'Quiz 2'
                '''):
                    print(row[0])
                    bank.append(
                        {"id": row[0], "text": row[1], "correct": row[2], "incorrect": [row[3], row[4], row[5]]})
        if random:
            shuffle(bank)
        for question in bank:
            choices = [question["correct"]] + question["incorrect"]
            shuffle(choices)
            yield (question["id"], question["text"], choices, question["correct"])
