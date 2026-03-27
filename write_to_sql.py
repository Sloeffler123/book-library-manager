import sqlite3
from constants import AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_ID_COLUMN_NAME, AUTHOR_BOOKS_TABLE_NAME, BOOK_TABLE_NAME, BOOK_NAME_COLUMN, BOOK_ISBN_COLUMN, BOOK_ID_COLUMN_NAME, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME

def push_author_data(author, connection_to_db):
    cursor = connection_to_db.cursor()
    any_inserted = False
    for name in author:
        try:
            sql = f"""INSERT INTO {AUTHOR_TABLE_NAME} ({AUTHOR_NAME_COLUMN}) VALUES (?)
            """
            cursor.execute(sql, (name,))
            connection_to_db.commit()
            print(f"{name} added to {AUTHOR_TABLE_NAME}\n")
            any_inserted = True
        except sqlite3.IntegrityError:
            print("author already in db")
    return any_inserted

def push_book_data(book_name, isbn_number, publication_year, format, date_read, categories, connection_to_db):
    cursor = connection_to_db.cursor()
    try:
        sql = f"""INSERT INTO {BOOK_TABLE_NAME} ({BOOK_NAME_COLUMN}, {BOOK_ISBN_COLUMN}, {BOOK_PUBLICATION_YEAR_COLUMN_NAME}, {BOOK_FORMAT_COLUMN_NAME}, {BOOK_DATE_READ_COLUMN_NAME}, {BOOK_CATEGORIES_COLUMN_NAME}) VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (book_name, isbn_number, publication_year, format, date_read, categories))
        connection_to_db.commit()
        print(f"{book_name} added to {BOOK_TABLE_NAME}\n")
        return True
    except sqlite3.IntegrityError:
        print(f"{book_name} already in db")
        return False

def push_authors_books_data(author_name_list, isbn, connection_to_db):
    cursor = connection_to_db.cursor()
    for name in author_name_list:
        sql_string = f"""SELECT {AUTHOR_ID_COLUMN_NAME} FROM {AUTHOR_TABLE_NAME} WHERE {AUTHOR_NAME_COLUMN} = ?
        """
        cursor.execute(sql_string, (name,))
        author_id = cursor.fetchone()[0]
        sql_string_2 = f"""SELECT {BOOK_ID_COLUMN_NAME} FROM {BOOK_TABLE_NAME} WHERE {BOOK_ISBN_COLUMN} = ?"""
        cursor.execute(sql_string_2, (isbn,))
        book_id = cursor.fetchone()[0]
        try:
            sql_string_3 = f"""INSERT INTO {AUTHOR_BOOKS_TABLE_NAME} ({AUTHOR_ID_COLUMN_NAME}, {BOOK_ID_COLUMN_NAME}) VALUES (?, ?)
            """
            cursor.execute(sql_string_3, (author_id, book_id))
            print(f"book {book_id} and author {author_id} added to {AUTHOR_BOOKS_TABLE_NAME}\n")
            connection_to_db.commit()
        except sqlite3.IntegrityError:
            print("Author_id and book_id already exist")