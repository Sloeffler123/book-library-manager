from sql_commands import init_connection_to_sql
from write_to_sql import push_author_data, push_book_data, push_authors_books_data
from barcode import scan_code
from google_api import get_book_data

AUTHOR_TABLE_NAME = "authors"
AUTHOR_NAME_COLUMN = "author_name"
AUTHOR_ID_COLUMN_NAME = "author_id"

AUTHOR_BOOKS_TABLE_NAME = "authors_books"

BOOK_TABLE_NAME = "books"
BOOKS_NAME_COLUMN = "book_name"
BOOK_ISBN_COLUMN = "isbn"
BOOK_ID_COLUMN_NAME = "book_id"
BOOK_PUBLICATION_YEAR_COLUMN_NAME = "publication_year"
BOOK_FORMAT_COLUMN_NAME = "format"
BOOK_DATE_READ_COLUMN_NAME = "date_read"
BOOK_CATEGORIES_COLUMN_NAME = "categories"

def main():
    connection = init_connection_to_sql()
    isbn_13 = scan_code()
    book_name, author, publication_year, format, categories = get_book_data(isbn_13)
    push_author_data(author, AUTHOR_TABLE_NAME, AUTHOR_NAME_COLUMN, connection)
    push_book_data(book_name, isbn_13, publication_year, format, "NULL", categories, BOOK_TABLE_NAME, BOOKS_NAME_COLUMN, BOOK_ISBN_COLUMN, BOOK_PUBLICATION_YEAR_COLUMN_NAME, BOOK_FORMAT_COLUMN_NAME, BOOK_DATE_READ_COLUMN_NAME, BOOK_CATEGORIES_COLUMN_NAME, connection)
    push_authors_books_data(author, isbn_13, AUTHOR_BOOKS_TABLE_NAME, AUTHOR_NAME_COLUMN, AUTHOR_ID_COLUMN_NAME, BOOK_ISBN_COLUMN, BOOK_ID_COLUMN_NAME, AUTHOR_TABLE_NAME, BOOK_TABLE_NAME, connection)
    connection.close()
main()

