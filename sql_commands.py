import sqlite3
from constants import DATA_BASE, AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_BOOKS_TABLE_NAME, AUTHOR_ID_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_NAME_COLUMN,BOOK_PUBLICATION_YEAR_COLUMN_NAME,BOOK_TABLE_NAME, AUTHOR_BOOKS_AUTHOR_ID, AUTHOR_BOOKS_BOOK_ID
from write_to_sql import push_book_data, push_author_data, push_authors_books_data

def init_connection_to_sql():
    return sqlite3.connect(DATA_BASE)

def commit_and_close_connection(connection_to_db):
    connection_to_db.commit()
    connection_to_db.close()

def add_book_manually(connection_to_db):
    book_name = input("Book name: \n")
    authors = input("Authors (Dan Brown, Neil Gaiman): \n")
    new_author_lst = check_for_multiple_authors_helper(authors)
    isbn = input("Isbn: \n")
    publication_year = input("Publication year (yyyy/mm/dd): \n")
    format = input("Format (Digital, BOOK): \n")
    date_read = input("Date read (mm/dd/yyyy, NULL): \n")
    categories = input("Categories (Fiction, Nonfiction): \n")
    push_author_data(new_author_lst, AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, connection_to_db)
    push_book_data(book_name, isbn, publication_year, format, date_read, categories, BOOK_TABLE_NAME, BOOK_NAME_COLUMN, BOOK_ISBN_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, connection_to_db)
    push_authors_books_data(new_author_lst, isbn, AUTHOR_BOOKS_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_ID_COLUMN_NAME, AUTHOR_TABLE_NAME, BOOK_TABLE_NAME, connection_to_db)

def check_for_multiple_authors_helper(authors):
    if "," in authors:
        new_lst = []
        for name in authors.split(","):
            new_author = name.strip()
            new_lst.append(new_author)
    else:
        new_lst = [authors]
    return new_lst

def add_read_date_to_book(connection_to_db):
    cursor = connection_to_db.cursor()
    date_read = input("Date read (yyyy/mm/dd): \n")
    user_input_isbn_title = input("ISBN or Title? (I), (T): ").upper().strip()
    if user_input_isbn_title == "I":
        user_input = input("Please enter isbn: ").strip()
        cursor.execute(f"UPDATE {BOOK_TABLE_NAME} SET {BOOK_DATE_READ_COLUMN_NAME} = ? WHERE {BOOK_ISBN_COLUMN} = ?", (date_read, user_input,))
    else:
        user_input = input("Please enter book name: ").strip()
        cursor.execute(f"UPDATE {BOOK_TABLE_NAME} SET {BOOK_DATE_READ_COLUMN_NAME} = ? WHERE {BOOK_NAME_COLUMN} = ?", (date_read, user_input,))
    connection_to_db.commit()

def add_column_to_table(table_name, new_column_name, connection_to_db):
    cursor = connection_to_db.cursor()
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {new_column_name}")
    connection_to_db.commit()

def update_data_in_table(table_name, column_name, data_name_to_replace, new_data_name, connection_to_db):
    cursor = connection_to_db.cursor()
    cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {column_name} = ?", (new_data_name, data_name_to_replace,))
    connection_to_db.commit()

def remove_data_from_table(table_name, column_name, data_name, connection_to_db):
    cursor = connection_to_db.cursor()
    user_response = input(f"Are you sure you want to delete {data_name} from {table_name} in {column_name}? : (Y or N) ").upper()
    if user_response == "Y":
        cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = ?", (data_name,))
        connection_to_db.commit()

def filter_data_by_book_name_and_author(book_table_name, author_table_name, book_column_name, author_column_name, authors_books_table_name, book_id_column, author_id_column, author_books_book_id_column, author_books_author_id_column, connection_to_db):
    cursor = connection_to_db.cursor()
    sql = f"""
        SELECT b.{book_column_name}, a.{author_column_name} 
        FROM {book_table_name} AS b 
        INNER JOIN {authors_books_table_name} AS ab ON b.{book_id_column} = ab.{author_books_book_id_column} 
        INNER JOIN {author_table_name} AS a ON ab.{author_books_author_id_column} = a.{author_id_column} 
        ORDER BY a.{author_column_name}, b.{book_column_name}"""
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        print(i)
    return data

def filter_data_by_category_book_name_and_author_name(book_table_name, author_table_name, author_books_table_name, book_name_column, author_name_column, categories_column, book_id_column, author_id_column, author_books_book_id_column, author_books_author_id_column, db_conneciton):
    cursor = db_conneciton.cursor()
    sql = f"""
        SELECT b.{book_name_column}, a.{author_name_column}, b.{categories_column} 
        FROM {book_table_name} AS b 
        INNER JOIN {author_books_table_name} AS ab ON b.{book_id_column} = ab.{author_books_book_id_column} 
        INNER JOIN {author_table_name} AS a ON ab.{author_books_author_id_column} = a.{author_id_column} 
        ORDER BY b.{categories_column}, a.{author_name_column}, b.{book_name_column}"""
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        print(i)
    return data


# filter_data_by_book_name_and_author(BOOK_TABLE_NAME, AUTHOR_TABLE_NAME, BOOK_NAME_COLUMN, AUTHOR_NAME_COLUMN, AUTHOR_BOOKS_TABLE_NAME, BOOK_ID_COLUMN_NAME, AUTHOR_ID_COLUMN_NAME, AUTHOR_BOOKS_BOOK_ID, AUTHOR_BOOKS_AUTHOR_ID, init_connection_to_sql())

filter_data_by_category_book_name_and_author_name(BOOK_TABLE_NAME, AUTHOR_TABLE_NAME, AUTHOR_BOOKS_TABLE_NAME, BOOK_NAME_COLUMN, AUTHOR_NAME_COLUMN, BOOK_CATEGORIES_COLUMN_NAME, BOOK_ID_COLUMN_NAME, AUTHOR_ID_COLUMN_NAME, AUTHOR_BOOKS_BOOK_ID, AUTHOR_BOOKS_AUTHOR_ID, init_connection_to_sql())