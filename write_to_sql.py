import sqlite3

def push_author_data(author, author_table_name, author_column_name, connection_to_db):
    cursor = connection_to_db.cursor()
    for name in author:
        try:
            cursor.execute(f"INSERT INTO {author_table_name} ({author_column_name}) VALUES (?)", (name,))
            connection_to_db.commit()
            print(f"{name} added to {author_table_name}")
            return True
        except sqlite3.IntegrityError:
            print("author already in db")
            return False

def push_book_data(book_name, isbn_number, publication_year, format, date_read,categories, books_table_name, book_column_name, isbn_colomn_name, publication_year_coulumn_name, format_column_name, date_read_column_name, categories_column_name, connection_to_db):
    cursor = connection_to_db.cursor()
    try:
        cursor.execute(f"INSERT INTO {books_table_name} ({book_column_name}, {isbn_colomn_name}, {publication_year_coulumn_name}, {format_column_name}, {date_read_column_name}, {categories_column_name}) VALUES (?, ?, ?, ?, ?, ?)", (book_name, isbn_number, publication_year, format, date_read, categories,))
        connection_to_db.commit()
        print(f"{book_name} added to {books_table_name}")
        return True
    except sqlite3.IntegrityError:
        print(f"{book_name} already in db")
        return False

def push_authors_books_data(author_name_list, isbn, table_name, author_name_column, author_id_column, book_isbn_column, book_id_column, authors_table, book_table, connection_to_db):
    cursor = connection_to_db.cursor()
    for name in author_name_list:
        cursor.execute(f"SELECT {author_id_column} FROM {authors_table} WHERE {author_name_column} = ?", (name,))
        author_id = cursor.fetchone()[0]
        cursor.execute(f"SELECT {book_id_column} FROM {book_table} WHERE    {book_isbn_column} = ?", (isbn,))
        book_id = cursor.fetchone()[0]
        try:
            cursor.execute(f"INSERT INTO {table_name} ({author_id_column}, {book_id_column}) VALUES (?, ?)",  (author_id, book_id,))
            print(f"{book_id} and {author_id} added to {table_name}")
            connection_to_db.commit()
        except sqlite3.IntegrityError:
            print("Author_id and book_id already exist")