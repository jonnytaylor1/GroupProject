from data.connection import Connection
from collections import namedtuple
import datetime
from functools import reduce

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
            quiz_format TEXT,
            corrects INTEGER,
            incorrects INTEGER,
            skips INTEGER,
            time INTEGER,
            abandons INTEGER,
            FOREIGN KEY(question_id) REFERENCES questions(id)
            )''')

        with Connection() as con:
            con.execute('''
            CREATE TABLE IF NOT EXISTS answer_stats(
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            quiz_format TEXT,
            status TEXT,
            time INTEGER,
            created_at TIMESTAMP,
            FOREIGN KEY(question_id) REFERENCES questions(id)
            )''')

    # Save stats for a single unique answer from the user
    def create_answer_stats(obj):
        with Connection() as con:
            with con:
                con.execute('''
                INSERT INTO answer_stats
                (question_id, quiz_format, status, time, created_at)
                VALUES
                (?, ?, ?, ?, ?)
                ''', (obj["id"], obj["quiz_format"], obj["status"], obj["time"], datetime.datetime.now()))

    def save_answer_stats(*, id, quiz_format, status, time, created_at):
        with Connection() as con:
            with con:
                con.execute('''
                INSERT INTO answer_stats
                (question_id, quiz_format, status, time, created_at)
                VALUES
                (?, ?, ?, ?, ?)
                ''', (str(id), quiz_format, status, str(time), created_at))


    # def update_answer_stats(obj):
    #     with Connection() as con:
    #         with con:
    #             con.execute('''
    #             INSERT INTO answer_stats
    #             (question_id, quiz_format, is_correct, is_abandoned, time_spent, time_stamp)
    #             VALUES
    #             ()
    #             ''')

    # creates a new stats entry for a new question and sets all values to 0
    def create_stats(id):
        with Connection() as con:
            with con:
                for format in ["Multi-Choice", "Hangman"]:
                    con.execute('''
                    INSERT INTO statistics
                    (question_id, quiz_format, corrects, incorrects, skips, abandons, time)
                    VALUES
                    (?, ?, 0, 0, 0, 0, 0)
                    ''', (id, format))

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
                time,
                abandons
                FROM statistics
                WHERE question_id = ?
                AND quiz_format = ?
                ''', (str(id), str(quiz))).fetchone()


    def get_answer_stats(id):
        with Connection() as con:
            with con:
                return con.execute('''
                SELECT questions.id,
                quiz_format,
                status,
                question,
                correct,
                incorrect1,
                incorrect2,
                incorrect3,
                time,
                created_at
                FROM (answer_stats
                INNER JOIN questions
                ON answer_stats.question_id = questions.id)
                WHERE question_id = ?
                ''', (str(id))).fetchall()

    # increments existing stats by this amount
    def increment_stats(obj):
        new_obj = {}
        new_obj["id"], new_obj["quiz_format"], new_obj["corrects"], new_obj["incorrects"], new_obj["skips"], new_obj["time"], new_obj["abandons"] = Statistics.get_stats(obj["id"], obj["quiz_format"])
        for attr in ["corrects", "incorrects", "skips", "time", "abandons"]:
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
                time = ?,
                abandons = ?
                WHERE question_id = ?
                AND quiz_format = ?
                ''', (obj["corrects"],
                      obj["incorrects"],
                      obj["skips"],
                      obj["time"],
                      obj["abandons"],
                      obj["id"],
                      obj["quiz_format"]))

    def load_stats(self):
        Question = namedtuple("Question",
                              ["currently_assigned", "q_id", "text", "correct", "in1", "in2", "in3", "successes", "failures", "skips", "abandons", "total_time", "quiz"])
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
                abandons,
                time,
                statistics.quiz_format,
                packages.quiz_format
                FROM ((questions
                INNER JOIN statistics
                ON questions.id = statistics.question_id)
                INNER JOIN packages
                ON questions.package_id = packages.package_id)
                ''')):
                    q = Question(row[-1] == row[-2], *row[:-1])
                    self.q_bank.append(q)
                    print(q)


    def load_stats2(self):
        Question = namedtuple("Question",
                              ["currently_assigned", "q_id", "text", "correct", "in1", "in2", "in3", "time", "status", "created_at", "package_id", "package_name", "quiz" ])
        with Connection() as con:
            with con:
                for i, row in enumerate(con.execute('''
                SELECT questions.id,
                question,
                correct,
                incorrect1,
                incorrect2,
                incorrect3,
                time,
                status,
                created_at,
                questions.package_id,
                packages.name,
                answer_stats.quiz_format,
                packages.quiz_format
                FROM ((answer_stats
                INNER JOIN questions
                ON answer_stats.question_id = questions.id)
                INNER JOIN packages
                ON questions.package_id = packages.package_id)
                ''')):
                    self.q_bank.append(Question(row[-1] == row[-2],*row[:-1]))


    def get_overall_stats_old(self):
        self.load_stats()
        return self.q_bank

    def get_overall_stats(self):
        self.load_stats2()
        Question = namedtuple("Question",
                              ["currently_assigned", "q_id", "text", "correct", "in1", "in2", "in3", "times", "successes", "failures", "skips", "abandons",
                               "created_at", "package_id", "package_name", "quiz"])
        def data_reducer(acc, q):
            for y in acc:
                if(q.q_id == y[1] and q.quiz == y[-1]):
                    y[7].append(q.time)
                    if q.status == "correct":
                        y[8] += 1
                    elif q.status == "incorrect":
                        y[9] += 1
                    elif q.status == "skipped":
                        y[10] += 1
                    elif q.status == "abandoned":
                        y[11] += 1
                    return acc
            acc.append([*q[:7], [q.time], 0, 0, 0, 0, *q[9:]])
            return acc

        result = []

        for q in reduce(data_reducer, self.q_bank, []):
            result.append(Question(*q))

        return result