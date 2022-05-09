books = []

class Book:
    def __init__(self, id: int, borrowed: bool):
        self.id = id
        self.borrowed = borrowed

        books.append(self)


def getBook(id: int):
    for book in books:
        if book.id == id:
            return book
    return None
