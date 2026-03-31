from sql_files.sql_commands import init_connection_to_sql
from sql_files.write_to_sql import push_author_data, push_book_data, push_authors_books_data
from barcode import scan_code
from api_files.google_api import get_book_data

def main():
    connection = init_connection_to_sql()
    isbn_13 = scan_code()
    book_name, author, publication_year, format, categories = get_book_data(isbn_13)
    push_author_data(author, connection)
    push_book_data(book_name, isbn_13, publication_year, format, "NULL", categories, connection)
    push_authors_books_data(author, isbn_13, connection)
    connection.close()
