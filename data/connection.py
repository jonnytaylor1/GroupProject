from sqlite3 import connect

class Connection(object):
    def __enter__(self):
        self.con = connect("./data/questions.db")
        return self.con

    def __exit__(self, type, value, traceback):
        self.con.close