from data.connection import Connection

class Statistics():
    def __init__(self):
        self.ensure_table_exists()

    # auto-creates the table if it does not exist
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
