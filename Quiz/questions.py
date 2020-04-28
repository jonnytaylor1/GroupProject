from random import shuffle, sample
from data.connection import Connection
from Quiz.statistics import Statistics

# Creates a backend model of the questions for the multiple choice quiz
class QuestionDB:
    def __init__(self): pass

    def get_quiz_questions(*, quiz="Multi-Choice"):
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
                            WHERE packages.quiz_format = ?
                ''', (str(quiz),)):
                    bank.append(row)
        return sample(bank, len(bank))


