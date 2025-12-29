import sqlite3
import pytest
from google_api import get_book_data
from write_to_sql import push_author_data, push_authors_books_data, push_book_data
from pathlib import Path
from sql_commands import add_book_manually, add_read_date_to_book, add_column_to_table, update_data_in_table, remove_data_from_table, filter_data_by_book_name_and_author
from constants import AUTHOR_BOOKS_TABLE_NAME, AUTHOR_ID_COLUMN_NAME, AUTHOR_NAME_COLUMN, AUTHOR_TABLE_NAME, BOOK_CATEGORIES_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_NAME_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_TABLE_NAME, AUTHOR_BOOKS_AUTHOR_ID, AUTHOR_BOOKS_BOOK_ID

SCHEMA_PATH = Path(__file__).parent.parent / "schema.sql"

@pytest.fixture
def db_connection():
    connection = sqlite3.connect(":memory:")
    schema_sql = SCHEMA_PATH.read_text()
    connection.executescript(schema_sql)
    yield connection
    connection.close()

def test_add_book_manually(db_connection):
    data_books = [(1, "Patriot Games", "9780425134351", "1992-05-01", "BOOK", "NULL", "Fiction")]
    data_authors = [(1, "Tom Clancy")]
    data_authors_books = [(1, 1)]
    cursor = db_connection.cursor()
    add_book_manually(db_connection)
    cursor.execute(f"SELECT * FROM {BOOK_TABLE_NAME}")
    book_result = cursor.fetchall()
    cursor.execute(f"SELECT * FROM {AUTHOR_TABLE_NAME}")
    author_result = cursor.fetchall()
    cursor.execute(f"SELECT * FROM {AUTHOR_BOOKS_TABLE_NAME}")
    author_books_result = cursor.fetchall()
    assert book_result == data_books
    assert author_result == data_authors
    assert author_books_result == data_authors_books

def test_add_book_manually_multiple_authors(db_connection):
    data_books = [(1, "Patriot Games", "9780425134351", "1992-05-01", "BOOK", "NULL", "Fiction")]
    data_authors = [(1, "Tom Clancy"), (2, "Sam Fisher")]
    data_authors_books = [(1, 1), (2, 1)]
    cursor = db_connection.cursor()
    add_book_manually(db_connection)
    cursor.execute(f"SELECT * FROM {BOOK_TABLE_NAME}")
    book_result = cursor.fetchall()
    cursor.execute(f"SELECT * FROM {AUTHOR_TABLE_NAME}")
    author_result = cursor.fetchall()
    cursor.execute(f"SELECT * FROM {AUTHOR_BOOKS_TABLE_NAME}")
    author_books_result = cursor.fetchall()
    assert book_result == data_books
    assert author_result == data_authors
    assert author_books_result == data_authors_books

def test_add_read_date_to_book(db_connection):
    data = ["2002"]
    add_book_data_helper(db_connection)
    cursor = db_connection.cursor()
    add_read_date_to_book(db_connection)
    cursor.execute(f"SELECT {BOOK_DATE_READ_COLUMN_NAME} FROM books")
    result = cursor.fetchone()
    assert result[0] == data[0]

def test_add_column_to_table(db_connection):
    add_book_data_helper(db_connection)
    cursor = db_connection.cursor()
    new_table = ["Rating"]
    add_column_to_table(BOOK_TABLE_NAME, new_table[0], db_connection)
    cursor.execute("SELECT name FROM pragma_table_info('books') WHERE name = 'Rating'")
    result = cursor.fetchone()
    assert result[0] == new_table[0]

def test_update_data_in_table(db_connection):
    add_book_data_helper(db_connection)
    cursor = db_connection.cursor()
    new_data = ["Tom Clancy"]
    data_to_replace = ["Dan Brown"]
    update_data_in_table(AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, data_to_replace[0], new_data[0], db_connection)
    cursor.execute(f"SELECT {AUTHOR_NAME_COLUMN} FROM {AUTHOR_TABLE_NAME}")
    result = cursor.fetchone()
    assert result[0] == new_data[0]

def test_remove_data_from_table(db_connection):
    add_book_data_helper(db_connection)
    cursor = db_connection.cursor()
    data_to_remove = ["Angels and Demons"]
    remove_data_from_table(BOOK_TABLE_NAME, BOOK_NAME_COLUMN, data_to_remove[0], db_connection)
    result = cursor.fetchone()
    assert result == None

def test_filter_data(db_connection):
    add_book_data_helper(db_connection)
    data = ("Angels and Demons", "Dan Brown")
    filtered_data = filter_data_by_book_name_and_author(BOOK_TABLE_NAME, AUTHOR_TABLE_NAME, BOOK_NAME_COLUMN, AUTHOR_NAME_COLUMN, AUTHOR_BOOKS_TABLE_NAME, BOOK_ID_COLUMN_NAME, AUTHOR_ID_COLUMN_NAME, AUTHOR_BOOKS_BOOK_ID, AUTHOR_BOOKS_AUTHOR_ID, db_connection)
    assert filtered_data[0] == data

def add_book_data_helper(db_connection):
    book_name, author, publication_year, format, categories = get_book_data("9780552150736")
    push_author_data(author, AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, db_connection)
    push_book_data(book_name, "9780552150736", publication_year, format, "NULL", categories, BOOK_TABLE_NAME, BOOK_NAME_COLUMN, BOOK_ISBN_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, db_connection)
    push_authors_books_data(author, "9780552150736", AUTHOR_BOOKS_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_ID_COLUMN_NAME, AUTHOR_TABLE_NAME, BOOK_TABLE_NAME, db_connection)