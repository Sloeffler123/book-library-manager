import sqlite3
import pandas as pd
from constants import DATA_BASE, AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_BOOKS_TABLE_NAME, AUTHOR_ID_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_NAME_COLUMN,BOOK_PUBLICATION_YEAR_COLUMN_NAME,BOOK_TABLE_NAME, AUTHOR_BOOKS_AUTHOR_ID, AUTHOR_BOOKS_BOOK_ID, BOOK_REVIEW_COLUMN_NAME
from sql_files.write_to_sql import push_book_data, push_author_data, push_authors_books_data

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
    push_author_data(new_author_lst, connection_to_db)
    push_book_data(book_name, isbn, publication_year, format, date_read, categories, connection_to_db)
    push_authors_books_data(new_author_lst, isbn, connection_to_db)

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

def add_column_to_table(new_column_name, connection_to_db):
    cursor = connection_to_db.cursor()
    cursor.execute(f"ALTER TABLE {BOOK_TABLE_NAME} ADD COLUMN {new_column_name}")
    connection_to_db.commit()

def update_data_in_table(table_name, column_to_update, new_value, filter_column, filter_value, connection_to_db):
    cursor = connection_to_db.cursor()
    sql = f"""
        UPDATE {table_name} SET {column_to_update} = ? WHERE {filter_column} = ?
        """
    cursor.execute(sql, (new_value, filter_value))
    connection_to_db.commit()

def remove_data_from_table(table_name, column_name, data_name, connection_to_db):
    cursor = connection_to_db.cursor()
    user_response = input(f"Are you sure you want to delete {data_name} from {table_name} in {column_name}? : (Y or N) ").upper()
    if user_response == "Y":
        cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = ?", (data_name,))
        connection_to_db.commit()

def filter_data_by_book_name_and_author(connection_to_db):
    cursor = connection_to_db.cursor()
    sql = f"""
        SELECT b.{BOOK_NAME_COLUMN}, a.{AUTHOR_NAME_COLUMN} 
        FROM {BOOK_TABLE_NAME} AS b 
        INNER JOIN {AUTHOR_BOOKS_TABLE_NAME} AS ab ON b.{BOOK_ID_COLUMN_NAME} = ab.{AUTHOR_BOOKS_BOOK_ID} 
        INNER JOIN {AUTHOR_TABLE_NAME} AS a ON ab.{AUTHOR_BOOKS_AUTHOR_ID} = a.{AUTHOR_ID_COLUMN_NAME} 
        ORDER BY a.{AUTHOR_NAME_COLUMN}, b.{BOOK_NAME_COLUMN}"""
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        print(i)
    return data

def filter_data_by_category_book_name_and_author_name(db_conneciton):
    cursor = db_conneciton.cursor()
    sql = f"""
        SELECT b.{BOOK_NAME_COLUMN}, a.{AUTHOR_NAME_COLUMN}, b.{BOOK_CATEGORIES_COLUMN_NAME} 
        FROM {BOOK_TABLE_NAME} AS b 
        INNER JOIN {AUTHOR_BOOKS_TABLE_NAME} AS ab ON b.{BOOK_ID_COLUMN_NAME} = ab.{AUTHOR_BOOKS_BOOK_ID} 
        INNER JOIN {AUTHOR_TABLE_NAME} AS a ON ab.{AUTHOR_BOOKS_AUTHOR_ID} = a.{AUTHOR_ID_COLUMN_NAME} 
        ORDER BY b.{BOOK_CATEGORIES_COLUMN_NAME}, a.{AUTHOR_NAME_COLUMN}, b.{BOOK_NAME_COLUMN}"""
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def filter_title_author_review_date_read(db_connection):
    cursor = db_connection.cursor()
    sql = f"""
        SELECT b.{BOOK_NAME_COLUMN}, a.{AUTHOR_NAME_COLUMN}, b.{BOOK_REVIEW_COLUMN_NAME}, b.{BOOK_DATE_READ_COLUMN_NAME}
        FROM {BOOK_TABLE_NAME} AS b 
        INNER JOIN {AUTHOR_BOOKS_TABLE_NAME} AS ab ON b.{BOOK_ID_COLUMN_NAME} = ab.{AUTHOR_BOOKS_BOOK_ID} 
        INNER JOIN {AUTHOR_TABLE_NAME} AS a ON ab.{AUTHOR_BOOKS_AUTHOR_ID} = a.{AUTHOR_ID_COLUMN_NAME} 
        ORDER BY b.{BOOK_NAME_COLUMN}, a.{AUTHOR_NAME_COLUMN}, b.{BOOK_REVIEW_COLUMN_NAME}, b.{BOOK_DATE_READ_COLUMN_NAME}"""
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def export_all_data_to_csv(db_connection):
    cursor = db_connection.cursor()
    sql = f"""
        SELECT b.{BOOK_NAME_COLUMN}, a.{AUTHOR_NAME_COLUMN}, b.{BOOK_CATEGORIES_COLUMN_NAME}, b.{BOOK_FORMAT_COLUMN_NAME}, b.{BOOK_ISBN_COLUMN}, b.{BOOK_PUBLICATION_YEAR_COLUMN_NAME}, b.{BOOK_DATE_READ_COLUMN_NAME}, b.{BOOK_REVIEW_COLUMN_NAME}
        FROM {BOOK_TABLE_NAME} AS b 
        INNER JOIN {AUTHOR_BOOKS_TABLE_NAME} AS ab ON b.{BOOK_ID_COLUMN_NAME} = ab.{AUTHOR_BOOKS_BOOK_ID} 
        INNER JOIN {AUTHOR_TABLE_NAME} AS a ON ab.{AUTHOR_BOOKS_AUTHOR_ID} = a.{AUTHOR_ID_COLUMN_NAME} 
        """
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    df.columns = ["Title", "Author", "Category", "Format", "ISBN", "Publication Year", "Date Read", "Review"]
    df.to_csv("library_book_data.csv", index=False)