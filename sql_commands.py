import sqlite3
DATA_BASE = "users_books.db"

def init_connection_to_sql():
    return sqlite3.connect(DATA_BASE)
