import sqlite3
from write_to_sql import push_book_data, push_author_data, push_authors_books_data

DATA_BASE = "users_books.db"

AUTHOR_TABLE_NAME = "authors"
AUTHOR_NAME_COLUMN = "author_name"
AUTHOR_ID_COLUMN_NAME = "author_id"

AUTHOR_BOOKS_TABLE_NAME = "authors_books"

BOOK_TABLE_NAME = "books"
BOOK_NAME_COLUMN = "book_name"
BOOK_ISBN_COLUMN = "isbn"
BOOK_ID_COLUMN_NAME = "book_id"
BOOK_PUBLICATION_YEAR_COLUMN_NAME = "publication_year"
BOOK_FORMAT_COLUMN_NAME = "format"
BOOK_DATE_READ_COLUMN_NAME = "date_read"
BOOK_CATEGORIES_COLUMN_NAME = "categories"

def init_connection_to_sql():
    return sqlite3.connect(DATA_BASE)

def add_book_manually():
    connection = init_connection_to_sql()
    book_name = input("Book name: \n")
    authors = input("Authors (Dan Brown, Neil Gaiman): \n")
    isbn = input("Isbn: \n")
    publication_year = input("Publication year (mm/dd/yyyy): \n")
    format = input("Format (Digital, BOOK): \n")
    date_read = input("Date read (mm/dd/yyyy, NULL): \n")
    categories = input("Categories (Fiction, Nonfiction): \n")
    push_author_data(authors, AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, connection)
    push_book_data(book_name, isbn, publication_year, format, date_read, categories, BOOK_TABLE_NAME, BOOK_NAME_COLUMN, BOOK_ISBN_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, connection)
    push_authors_books_data(authors, isbn, AUTHOR_BOOKS_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_ID_COLUMN_NAME, AUTHOR_TABLE_NAME, BOOK_TABLE_NAME, connection)

def add_read_date_to_book():
    connection = init_connection_to_sql()
    cursor = connection.cursor()
    date_read = input("Date read (mm/dd/yyyy): \n")
    isbn = input("Isbn: ")
    cursor.execute(f"UPDATE {BOOK_TABLE_NAME} SET {BOOK_DATE_READ_COLUMN_NAME} = ? WHERE {BOOK_ISBN_COLUMN} = ?", (date_read, isbn,))

def add_column_to_table():
    pass

def update_data_in_table():
    pass

def remove_data_from_table():
    pass

def filter_by_category():
    pass

def filter_by_author():
    pass
