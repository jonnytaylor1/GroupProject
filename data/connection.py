from sqlite3 import connect

# Creates a connection object that automaticallly commiits and rolls back transactions
class Connection(object):
    # before doing anything else connect to the database and return the connection object for later use
    def __enter__(self):
        self.con = connect("./data/questions.db")
        return self.con
    # finally, after everything else, close the connection object
    def __exit__(self, type, value, traceback):
        self.con.close
