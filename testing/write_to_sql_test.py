import pytest
import sqlite3
from pathlib import Path
from sql_files.write_to_sql import push_author_data, push_book_data, push_authors_books_data
from constants import AUTHOR_TABLE_NAME, AUTHOR_BOOKS_TABLE_NAME, BOOK_TABLE_NAME, AUTHOR_NAME_COLUMN

SCHEMA_PATH = Path(__file__).parent.parent / "schema.sql"

@pytest.fixture
def db_connection():
    connection = sqlite3.connect(":memory:")
    schema_sql = SCHEMA_PATH.read_text()
    connection.executescript(schema_sql)
    yield connection
    connection.close()

def test_push_author_data(db_connection):
    cursor = db_connection.cursor()
    push_author_data(["Tom Clancy"], db_connection)
    cursor.execute(f"SELECT {AUTHOR_NAME_COLUMN} FROM {AUTHOR_TABLE_NAME} WHERE {AUTHOR_NAME_COLUMN} = ?", ("Tom Clancy",))
    result = cursor.fetchone()
    assert result[0] == "Tom Clancy"

def test_push_book_data(db_connection):
    cursor = db_connection.cursor()
    data = [(1, "Patriot Games", "9780425134351", "1992-05-01", "BOOK", "NULL", "Fiction")]
    push_book_data(data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], db_connection)
    cursor.execute(f"SELECT * FROM {BOOK_TABLE_NAME}")
    result = cursor.fetchall()
    assert result == data

def test_push_authors_books_data(db_connection):
    cursor = db_connection.cursor()
    data = [(1, "Patriot Games", "9780425134351", "1992-05-01", "BOOK", "NULL", "Fiction")]
    push_author_data(["Tom Clancy"], db_connection)
    push_book_data(data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], db_connection)
    push_authors_books_data(["Tom Clancy"], "9780425134351", db_connection)
    cursor.execute(f"SELECT * FROM {AUTHOR_BOOKS_TABLE_NAME}")
    result = cursor.fetchall()
    assert result == [(1, 1)]