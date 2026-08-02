# Book Library Manager

A personal library tracker that lets you scan a book's barcode with a webcam, automatically pulls in its metadata, and stores everything in a local database you can browse from a simple web page.

## What it does

- **Scan a barcode** using your webcam — the app reads the ISBN directly off the book's cover (OpenCV + pyzbar)
- **Fetches book details automatically** — title, author(s), publication year, format, and category are pulled from the Google Books API, so you never have to type them in by hand
- **Stores everything in SQLite** with a normalized schema that correctly models many-to-many relationships (a book can have multiple authors, an author can have multiple books)
- **Command-line tools** to add books manually, log the date you finished reading one, update reviews, filter your library by author/category, and export your whole collection to CSV
- **A small FastAPI web page** to view your library — title, author, review, and date read — without touching the database directly

## Why I built it

I wanted a low-friction way to catalog my physical book collection without manually typing in title/author/ISBN for every book — scan the barcode, and the rest fills itself in.

## Tech stack

| Layer | Tools |
|---|---|
| Barcode scanning | OpenCV, pyzbar |
| Metadata | Google Books API |
| Database | SQLite (normalized schema — `books`, `authors`, `authors_books` join table) |
| Backend / API | FastAPI |
| Testing | pytest, with in-memory SQLite fixtures |

## Project structure

```
main.py                 # entry point — scan → fetch → store
barcode.py               # webcam barcode scanning
schema.sql                # database schema (books, authors, authors_books)
constants.py              # table/column name constants
sql_files/
    sql_commands.py        # queries, filters, manual add, CSV export
    write_to_sql.py         # insert/write operations
api_files/
    google_api.py           # Google Books API lookup
    api_helper_funcs.py      # data shaping for the web view
api_code.py               # FastAPI app
*_test.py                 # pytest suites for SQL read/write logic
```

## Testing

The SQL read/write logic is covered by pytest, using an in-memory SQLite database seeded from `schema.sql` for each test — so tests run in isolation and never touch real library data.

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install opencv-python pyzbar requests fastapi jinja2
   ```
2. Run the schema to create your database:
   ```bash
   sqlite3 users_books.db < schema.sql
   ```
3. Scan a book:
   ```bash
   python main.py
   ```
4. (Optional) Launch the web view:
   ```bash
   uvicorn api_code:api --reload
   ```

## Possible next steps

- Defensive handling for books missing fields in the Google Books response (e.g. multiple authors, no categories)
- Move hardcoded config into environment variables
- Add a way to edit/delete entries from the web view instead of just viewing
