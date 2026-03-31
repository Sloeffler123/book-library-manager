import requests

def get_book_data(isbn):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
    data = response.json()
    title = data["items"][0]["volumeInfo"]["title"]
    author = data["items"][0]["volumeInfo"]["authors"]
    publication_year = data["items"][0]["volumeInfo"]["publishedDate"]
    format = data["items"][0]["volumeInfo"]["printType"]
    categories = data["items"][0]["volumeInfo"]["categories"][0]
    return title, author, publication_year, format, categories