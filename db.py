import sqlite3
from sqlite3 import Connection

conn: Connection = sqlite3.connect('FEEDBACK.db')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE feedback_data(name TEXT, email TEXT,phone INTEGER, gender TEXT,course TEXT,rate INTEGER)')
    return True


create_table()
print("successfully created")
