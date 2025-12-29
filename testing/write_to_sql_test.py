import pytest
import sqlite3
from pathlib import Path
from write_to_sql import push_author_data, push_book_data, push_authors_books_data
from constants import AUTHOR_BOOKS_TABLE_NAME, AUTHOR_ID_COLUMN_NAME, AUTHOR_NAME_COLUMN, AUTHOR_TABLE_NAME, BOOK_CATEGORIES_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_NAME_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_TABLE_NAME

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
    push_author_data(["Tom Clancy"], AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, db_connection)
    cursor.execute(f"SELECT author_name FROM authors WHERE author_name = ?", ("Tom Clancy",))
    result = cursor.fetchone()
    assert result[0] == "Tom Clancy"

def test_push_book_data(db_connection):
    cursor = db_connection.cursor()
    data = [(1, "Patriot Games", "9780425134351", "1992-05-01", "BOOK", "NULL", "Fiction")]
    push_book_data(data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], BOOK_TABLE_NAME, BOOK_NAME_COLUMN, BOOK_ISBN_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, db_connection)
    cursor.execute(f"SELECT * FROM books")
    result = cursor.fetchall()
    assert result == data

def test_push_authors_books_data(db_connection):
    cursor = db_connection.cursor()
    data = [(1, "Patriot Games", "9780425134351", "1992-05-01", "BOOK", "NULL", "Fiction")]
    push_author_data(["Tom Clancy"], AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, db_connection)
    push_book_data(data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], BOOK_TABLE_NAME, BOOK_NAME_COLUMN, BOOK_ISBN_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, db_connection)
    push_authors_books_data(["Tom Clancy"], "9780425134351", AUTHOR_BOOKS_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_ID_COLUMN_NAME, AUTHOR_TABLE_NAME, BOOK_TABLE_NAME, db_connection)
    cursor.execute(f"SELECT * FROM authors_books")
    result = cursor.fetchall()
    assert result == [(1, 1)]