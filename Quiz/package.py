
from data.connection import Connection

class Package():
    def __init__(self):
        self.ensure_table_exists()
        self.package_bank = []
        self.load_packages()



    def ensure_table_exists(self):
        with Connection() as con:
            with con:
                con.execute(
                    "CREATE TABLE IF NOT EXISTS packages (package_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, quiz_format text UNIQUE)")



    def load_packages(self):
        with Connection() as con:
            for package_id, name, quiz_format in con.execute("SELECT * from packages"):
                self.package_bank.append({"name": name, "package_id": package_id, "quiz_format": quiz_format})


    def add_package(name):
        with Connection() as con:
            with con:
                return con.execute("INSERT INTO packages(name) values (?)", (name,)).lastrowid


    def delete_package(package_id):
        with Connection() as con:
            with con:
                con.execute('''DELETE 
                FROM questions
                WHERE questions.package_id = ?''', (str(package_id),))
                con.execute("DELETE from packages WHERE package_id = ?", (str(package_id),))

    def get_package(package_id):
        with Connection() as con:
            with con:
                return con.execute("SELECT package_id, name, quiz_format FROM packages WHERE package_id = ?", (str(package_id),)).fetchone()

    def save_package(package_id, name, quiz_format):
        with Connection() as con:
            with con:
                con.execute("UPDATE packages SET name = ?, quiz_format = ? WHERE package_id = ?", (name, quiz_format, str(package_id)))

    def search_format(package_id):
         with Connection() as con:
            with con:
                return con.execute("SELECT package_id, name, quiz_format FROM packages WHERE package_id = ?", (str(package_id))).fetchone()
