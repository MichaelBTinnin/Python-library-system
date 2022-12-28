import sqlite3
import uuid
from datetime import datetime

class CustomerDatabase:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS ___customers (unique_id text, card_number text, name text, title text, isbn text, check_out_time text, check_in_time text, status text)")
        self.conn.commit()

    def insert(self, card_number, customer_name, title, isbn):
        unique_id = str(uuid.uuid1())
        check_out_time = str(datetime.today().strftime('%Y-%m-%d'))
        check_in_time = 'N/A'
        status = 'checked_out'
        self.cur.execute("INSERT INTO ___customers VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)", ( unique_id, card_number, customer_name, title, isbn, check_out_time, check_in_time, status))
        self.conn.commit()

    def update(self, check_in_time, unique_id):
        self.cur.execute("UPDATE ___customers SET check_in_time = ? WHERE unique_id = ?" , ( check_in_time, unique_id))
        self.conn.commit()

    def _update(self, unique_id):
        self.cur.execute("UPDATE ___customers SET status = ? WHERE unique_id = ?", ( "ckecked_in", unique_id, ))
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM ___customers")
        rows = self.cur.fetchall()
        return rows
