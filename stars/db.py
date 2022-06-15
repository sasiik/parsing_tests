import sqlite3

connection = None


def get_connection():
    global connection
    if connection is None:
        connection = sqlite3.connect('database.db')
    return connection


def init_db(force: bool = True):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS stars')

    c.execute('''
        CREATE TABLE IF NOT EXISTS stars (
            id           INTEGER PRIMARY KEY,
            star         TEXT NOT NULL,
            planetcount  TEXT NOT NULL,
            ra           TEXT NOT NULL,
            dec          TEXT NOT NULL,
            raddist      TEXT NOT NULL
        )
    ''')

    conn.commit()


def add_message(star: str, planetcount: str, ra: str, dec: str, raddist: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO stars (star, planetcount, ra, dec, raddist) VALUES (?, ?, ?, ?, ?)',
        (star, planetcount, ra, dec, raddist))
    conn.commit()


if __name__ == '__main__':
    init_db()
