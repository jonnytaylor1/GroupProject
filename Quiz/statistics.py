from data.connection import Connection
from collections import namedtuple

class Statistics():
    def __init__(self):
        self.ensure_table_exists()
        self.q_bank = []

    # auto-creates the table if it does not exist
    def ensure_table_exists(self):
        with Connection() as con:
            con.execute('''
            CREATE TABLE IF NOT EXISTS statistics(
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            quiz_format INTEGER,
            corrects INTEGER,
            incorrects INTEGER,
            skips INTEGER,
            time INTEGER,
            FOREIGN KEY(question_id) REFERENCES questions(id)
            )''')

    # creates a new stats entry for a new question and sets all values to 0
    def create_stats(id):
        with Connection() as con:
            with con:
                for format in range(1,3):
                    con.execute('''
                    INSERT INTO statistics
                    (question_id, quiz_format, corrects, incorrects, skips, time)
                    VALUES
                    (?, ?, 0, 0, 0, 0)
                    ''', (id, str(format)))

    # returns stats for a question id
    # time is represented by 10^(-1) seconds
    def get_stats(id, quiz):
        with Connection() as con:
            with con:
                return con.execute('''
                SELECT question_id,
                quiz_format,
                corrects,
                incorrects,
                skips,
                time
                FROM statistics
                WHERE question_id = ?
                AND quiz_format = ?
                ''', (str(id), str(quiz))).fetchone()

    # increments existing stats by this amount
    def increment_stats(obj):
        new_obj = {}
        new_obj["id"], new_obj["quiz_format"], new_obj["corrects"], new_obj["incorrects"], new_obj["skips"], new_obj["time"] = Statistics.get_stats(obj["id"], obj["quiz_format"])
        for attr in ["corrects", "incorrects", "skips", "time"]:
            try:
                new_obj[attr] += obj[attr]
            except KeyError:
                pass
        print(new_obj)

        Statistics.update_stats(new_obj)

    # replaces old values with new values
    def update_stats(obj):
        obj = {k: str(v) for k, v in obj.items()}
        with Connection() as con:
            with con:
                con.execute('''
                UPDATE statistics
                SET corrects = ?,
                incorrects = ?,
                skips = ?,
                time = ?
                WHERE question_id = ?
                AND quiz_format = ?
                ''', (obj["corrects"],
                      obj["incorrects"],
                      obj["skips"],
                      obj["time"],
                      obj["id"],
                      obj["quiz_format"]))

    def load_stats(self):
        Question = namedtuple("Question",
                              ["q_id", "text", "correct", "in1", "in2", "in3", "corrects", "incorrects", "skips", "total_time", "quiz"])
        with Connection() as con:
            with con:
                for i, row in enumerate(con.execute('''
                SELECT questions.id,
                question,
                correct,
                incorrect1,
                incorrect2,
                incorrect3,
                corrects,
                incorrects,
                skips,
                time,
                statistics.quiz_format
                FROM ((questions
                INNER JOIN statistics
                ON questions.id = statistics.question_id)
                INNER JOIN packages
                ON questions.package_id = packages.package_id)
                ''')):
                    print(*row)
                    self.q_bank.append(Question(*row))

    def get_overall_stats(self):
        self.load_stats()
        return self.q_bank