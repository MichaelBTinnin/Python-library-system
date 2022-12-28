import sqlite3

class BooksDatabase:
    def __init__(self, db):
        #video from will said to open and close connection during each action
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS __books ( isbn text, title text, first_name text, last_name text, genre text, publisher text, short_description text, checked_in text)")
        self.conn.commit()


    def insert(self, isbn, title, first_name, last_name, genre, publisher, short_description, checked_in):
        self.cur.execute("INSERT INTO __books VALUES ( ?,?,?,?,?,?,?,?)", ( isbn, title, first_name, last_name, genre, publisher, short_description, checked_in))
        self.conn.commit()


    def fetch(self):
        self.cur.execute("SELECT * FROM __books")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("DELETE FROM __books WHERE isbn=?", (id,))
        self.conn.commit()

    def update(self, isbn, title, first_name, last_name, genre, publisher, short_description, checked_in):
        self.cur.execute("UPDATE __books SET title = ?, first_name = ?, last_name = ?, genre = ?, publisher = ?, short_description = ?, checked_in = ? WHERE isbn = ?", ( title,  first_name, last_name, genre, publisher, short_description, checked_in, isbn ))
        self.conn.commit()


    def _update(self, checked_in, isbn):
        self.cur.execute("UPDATE __books SET checked_in = ? WHERE isbn = ?", ( checked_in, isbn ))
        self.conn.commit()

    def __del__(self):

        self.conn.close()



