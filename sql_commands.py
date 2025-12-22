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
    commit_and_close_connection(connection)

def add_column_to_table(table_name, new_column_name, connection_to_db):
    # ALTER TABLE table ADD COLUMN new_column;
    cursor = connection_to_db.cursor()
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {new_column_name}")
    commit_and_close_connection(connection_to_db)

def update_data_in_table(table_name, column_name, data_name_to_replace, new_data_name, connection_to_db):
    # UPDATE table_name SET column_1 = value_1, column_2 = value2
    cursor = connection_to_db.cursor()
    cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {column_name} = ?", (new_data_name, data_name_to_replace,))
    commit_and_close_connection(connection_to_db)
    
def remove_data_from_table(table_name, column_name, data_name, connection_to_db):
    # DELETE FROM table WHERE column_name = data;
    cursor = connection_to_db.cursor()
    user_response = input(f"Are you sure you want to delete {data_name} from {table_name} in {column_name}? : (Y or N) ")
    if user_response:
        cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = ?", (data_name,))
        commit_and_close_connection(connection_to_db)

def filter_by_category():
    pass

def filter_by_author():
    pass

def commit_and_close_connection(connection_to_db):
    connection_to_db.commit()
    connection_to_db.close()
