import sqlite3

DATA_BASE = "users_books.db"

def init_connection_to_sql():
    connection = sqlite3.connect(DATA_BASE)
    cursor = connection.cursor()
    return cursor, connection

def push_author_data(author, table_name, column_name):
    cursor, connection = init_connection_to_sql()
    for name in author:
        if not check_if_data_exists_in_table(cursor, table_name, column_name, name):
            cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (?)", (name,))
            connection.close()
            print(f"{author} added to {table_name}")
            return True
        else:
            print("author already in db")
            connection.close()
            return False

def push_book_data(book_name, isbn_number, publication_year, format, date_read, table_name, column_name):
    cursor, connection = init_connection_to_sql()
    if not check_if_data_exists_in_table(cursor, table_name, column_name, isbn_number):
        cursor.execute(f"INSERT INTO {table_name} (book_name, isbn, publication_year, format, date_read) VALUES (?, ?, ?, ?, ?)", (book_name, isbn_number, publication_year, format, date_read))
        connection.close()
        print(f"{book_name} added to {table_name}")
        return True
    else:
        connection.close()
        return False

def push_authors_books_data(author_name, isbn, table_name):
    cursor, connection = init_connection_to_sql()
    # get id's
    author_id = cursor.execute("SELECT author_id FROM authors WHERE author_name = ?", author_name)
    book_id = cursor.execute("SELECT book_id FROM books WHERE isbn = ?", isbn)
    author_id_fetch = cursor.fetchone(author_id)
    book_id_fetch = cursor.fetchone(book_id)
    cursor.execute(f"INSERT INTO {table_name} (author_id, book_id) VALUES (?, ?)", (author_id_fetch, book_id_fetch))
    connection.close()
    print(f"{book_id_fetch} and {author_id_fetch} added to {table_name}")

# data_name is what we are getting from the api query (EX: WHERE isbn = isbn)
def check_if_data_exists_in_table(cursor, table_name, column_name, data_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = ?", (data_name,))
    count = cursor.fetchone()[0]
    return count