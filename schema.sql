CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    isbn TEXT UNIQUE,
    publication_year TEXT,
    format TEXT,
    date_read TEXT DEFAULT NULL,
    categories TEXT
);

CREATE TABLE IF NOT EXISTS authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL COLLATE NOCASE,
    CONSTRAINT unique_name UNIQUE (author_name COLLATE NOCASE)
);

CREATE TABLE IF NOT EXISTS authors_books (
    author_id INTEGER,
    book_id INTEGER,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY(author_id) REFERENCES authors(author_id),
    FOREIGN KEY(book_id) REFERENCES books(book_id)
)