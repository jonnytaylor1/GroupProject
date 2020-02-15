from random import shuffle
from data.connection import Connection


class Multiplechoice():
    def __init__(self):
        self.qbank = []
        self.ensure_table_exists()
        self.load_questions()

    def load_questions(self):
        with Connection() as con:
            for id, question_text, correct, b, c, d in con.execute("SELECT * from questions"):
                self.qbank.append({"text": question_text, "correct": correct, "incorrect": [b,c,d], "id": id})

    def ensure_table_exists(self):
        with Connection() as con:
            con.execute(
                "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, correct TEXT, incorrect1 TEXT, incorrect2 TEXT, incorrect3 TEXT)")

    def add_question(self, q):
        b, c, d = q["incorrect"]
        with Connection() as con:
            with con:
                con.execute("INSERT INTO questions(question, correct, incorrect1, incorrect2, incorrect3) values (?,?,?,?,?)", (q["text"], q["correct"], b, c, d))

    def get_questions(self):
        for question in self.qbank:
            choices = [question["correct"]] + question["incorrect"]
            shuffle(choices)
            yield (question["text"], choices, question["correct"])

    def run(self):
        for (question, choices, correct) in self.get_questions():
            print(question)
            print("Choices are: ")
            for i, choice in enumerate(choices):
                print(f"{i + 1}. {choice}")
            ans = input("Select Answer: ")
            print("correct" if correct == ans.upper() else f"{ans} is incorrect. Correct is {correct}")


def get_question(id):
    with Connection() as con:
        with con:
            return con.execute("SELECT id, question, correct, incorrect1, incorrect2, incorrect3 from questions WHERE id = ?", str(id)).fetchone()
def save_question(id, question, correct, inc1, inc2, inc3):
    with Connection() as con:
        with con:
            con.execute("UPDATE questions SET question = ?, correct = ?, incorrect1 = ?, incorrect2 = ?, incorrect3 = ? WHERE id = ?", (question, correct, inc1, inc2, inc3, str(id)))