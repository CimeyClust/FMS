from Model.Title import Title
from Model.Student import Student

books = []

class Book:
    def __init__(self, id: int, borrowed: bool, title: Title, user: Student = None):
        self.id = id
        self.borrowed = borrowed
        self.title = title
        self.user = user

        books.append(self)


def getBook(id: int):
    for book in books:
        if book.id == id:
            return book
    return None
