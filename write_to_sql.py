import sqlite3

def push_author_data(author, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    if not check_if_author_exists(cursor, author):
        cursor.execute(f"INSERT INTO authors (author_name) VALUES ('{author}')")
        connection.close()
        return True
    else:
        connection.close()
        return False

def check_if_author_exists(cursor, author_name):
    count = cursor.execute(f"SELECT COUNT(*) FROM authors WHERE author_name = '{author_name}'")
    return count

def push_book_data(book_name, isbn_number, publication_year, format, date_read, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    if not check_if_book_exists(cursor, isbn_number):
        cursor.execute(f"INSTER INTO books (book_name, isbn, publication_year, format, date_read) VALUES ('{book_name}, {isbn_number}, {publication_year}, {format}, {date_read}')")
        connection.close()
        return True
    else:
        connection.close()
        return False

def check_if_book_exists(cursor, isbn_number):
    count = cursor.execute(f"SELECT COUNT(*) FROM books WHERE isbn = '{isbn_number}'")
    return count

