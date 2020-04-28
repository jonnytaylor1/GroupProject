from data.connection import Connection

class PasswordDB:
    def ensure_table_exists():
        with Connection() as con:
            con.execute('''
                        CREATE TABLE IF NOT EXISTS passwords(
                        id INTEGER PRIMARY KEY,
                        password TEXT
                        )''')

        with Connection() as con:
            with con:
                con.execute('''
                            INSERT INTO passwords
                            (password)
                            VALUES
                            ('password')
                            ''')

    def set_password(password):
        with Connection() as con:
            with con:
                con.execute('''
                            UPDATE passwords
                            SET password = ?
                            WHERE id = '1'
                            ''', (password, ))

    def get_password():
        with Connection() as con:
            return con.execute('''
                        SELECT password
                        FROM passwords
                        WHERE id = '1'
                        ''').fetchone()[0]
