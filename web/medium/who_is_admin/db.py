import sqlite3

from flask import g

DATABASE = "app.db"


def setup_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    with open("setup.sql", "r") as f:
        cursor.executescript(f.read())


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
