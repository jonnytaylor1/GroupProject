from data.connection import Connection

# def save_stats()

class Statistics():
    def __init__(self):
        self.ensure_table_exists()

    def ensure_table_exists():
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

    def create_stats(id):
        with Connection() as con:
            with con:
                con.execute('''
                INSERT INTO statistics
                (question_id, corrects, incorrects, skips, time)
                VALUES
                (?, 0, 0, 0, 0)
                ''', (id, ))

    def get_stats(id):
        with Connection() as con:
            with con:
                return con.execute('''
                SELECT *
                FROM statistics
                WHERE question_id = ?
                ''', (str(id),)).fetchone()

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
