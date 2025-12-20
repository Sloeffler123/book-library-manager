import sqlite3

DATA_BASE = "users_books.db"

def init_connection_to_sql():
    connection = sqlite3.connect(DATA_BASE)
    cursor = connection.cursor()
    return cursor, connection

def test():
    cursor, conn = init_connection_to_sql()
    cursor.execute(f"SELECT * FROM authors")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
def push_author_data(author, author_table_name, author_column_name):
    cursor, connection = init_connection_to_sql()
    for name in author:
        if not check_if_data_exists_in_table(cursor, author_table_name, author_column_name, name):
            cursor.execute(f"INSERT INTO {author_table_name} ({author_column_name}) VALUES ?", (name,))
            connection.commit()
            connection.close()
            print(f"{name} added to {author_table_name}")
            return True
        else:
            print("author already in db")
            connection.close()
            return False

def push_book_data(book_name, isbn_number, publication_year, format, date_read, books_table_name, column_isbn_name, book_column_name, isbn_colomn_name, publication_year_coulumn_name, format_column_name, date_read_column_name):
    cursor, connection = init_connection_to_sql()
    if not check_if_data_exists_in_table(cursor, books_table_name, column_isbn_name, isbn_number):
        cursor.execute(f"INSERT INTO {books_table_name} ({book_column_name}, {isbn_colomn_name}, {publication_year_coulumn_name}, {format_column_name}, {date_read_column_name}) VALUES (?, ?, ?, ?, ?)", (book_name, isbn_number, publication_year, format, date_read,))
        connection.commit()
        connection.close()
        print(f"{book_name} added to {books_table_name}")
        return True
    else:
        print(f"{book_name} already in db")
        connection.close()
        return False

def push_authors_books_data(author_name_list, isbn, table_name, author_name_column, author_id_column, book_isbn_column, book_id_column, authors_table, book_table):
    cursor, connection = init_connection_to_sql()
    for name in author_name_list:
        cursor.execute(f"SELECT {author_id_column} FROM {authors_table} WHERE   {author_name_column} = ?", (name,))
        author_id = cursor.fetchone()[0]
        cursor.execute(f"SELECT {book_id_column} FROM {book_table} WHERE    {book_isbn_column} = ?", (isbn,))
        book_id = cursor.fetchone()[0]
        if not check_if_bookid_and_authid_exist(cursor, table_name, author_id_column,   book_id_column, author_id, book_id):
            cursor.execute(f"INSERT INTO {table_name} ({author_id_column},  {book_id_column}) VALUES (?, ?)",  (author_id, book_id,))
            print(f"{book_id} and {author_id} added to {table_name}")
            connection.commit()
            connection.close()
        else:
            print("Author_id and book_id already exist")
            connection.close()

def check_if_data_exists_in_table(cursor, table_name, column_name, data_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = ?", (data_name,))
    count = cursor.fetchone()[0]
    print(count)
    return count

def check_if_bookid_and_authid_exist(cursor, table_name, author_id_column, book_id_column, author_id, book_id):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {author_id_column} = ? AND {book_id_column} = ?", (author_id, book_id,))
    count = cursor.fetchone()[0]
    return count
