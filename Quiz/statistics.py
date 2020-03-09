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
                con.execute('''
                INSERT INTO statistics
                (question_id, corrects, incorrects, skips, time)
                VALUES
                (?, 0, 0, 0, 0)
                ''', (id, ))

    # returns stats for a question id
    # time is represented by 10^(-1) seconds
    def get_stats(id):
        with Connection() as con:
            with con:
                return con.execute('''
                SELECT *
                FROM statistics
                WHERE question_id = ?
                ''', (str(id),)).fetchone()

    # increments existing stats by this amount
    def increment_stats(obj):
        new_obj = {}
        id, new_obj["id"], new_obj["corrects"], new_obj["incorrects"], new_obj["skips"], new_obj["time"] = Statistics.get_stats(obj["id"])
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
                ''', (obj["corrects"],
                      obj["incorrects"],
                      obj["skips"],
                      obj["time"],
                      obj["id"]))

    def load_stats(self):
        counter = 0
        Question = namedtuple("Question",
                              ["q_number", "text", "correct", "in1", "in2", "in3", "pc_correct", "pc_abandon", "time"])
        with Connection() as con:
            with con:
                for id, q_text, correct, in1, in2, in3, stat_id, q_id, corrects, incorrects, skips, time in con.execute('''
                SELECT * 
                FROM questions
                INNER JOIN statistics
                ON questions.id = statistics.question_id
                '''):
                    counter += 1
                    answered = corrects + incorrects
                    abandons = "N/A" if answered + skips <= 0 else round(skips * 100 / (answered + skips))
                    accuracy = "N/A" if answered <= 0 else round(corrects * 100 / answered)
                    mean_time = "N/A" if answered <= 0 else round(time / (10 * answered))

                    self.q_bank.append(Question(counter, q_text, correct, in1, in2, in3, accuracy, abandons, mean_time))

    def get_overall_stats(self):
        self.load_stats()
        return self.q_bank