from Model.Title import Title
from Model.Student import Student

books = []

class Book:
    _highestBookID = float('-inf')

    def __init__(self, id: int, borrowed: bool, title: Title, student: Student = None, temporary: bool = False):
        self.id = id
        self.borrowed = borrowed
        self.title = title
        self.student = student

        if id > Book._highestBookID:
            Book._highestBookID = id

        if not temporary:
            books.append(self)

    @staticmethod
    def getHighestBookID() -> float:
        return Book._highestBookID


def getBook(id: int) -> Book:
    for book in books:
        if book.id == id:
            return book
    return None
