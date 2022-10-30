from book_manager import Book
from db import DB as db


def add_book(title):
        book = Book(title=title)
        db.session.add(book)
        db.session.commit()

def one_book_by_title(title):
    pass

def create():
    db.create_all()
    db.commit()

def all_books():
    return Book.query.all()
