from functions import get_book_information
from dbconn import db

hobbit_bood_data = get_book_information(url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit')

books_col = db["books"]

books_col.insert_many(hobbit_bood_data)