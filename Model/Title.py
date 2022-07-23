from Model.Subject import Subject

titles = []


class Title:
    def __init__(self, id: int, title: str, isbn: str, author: str, subject: Subject, temporary: bool = False):
        self.id = id
        self.title = title
        self.isbn = isbn
        self.author = author
        self.subject = subject

        if not temporary:
            titles.append(self)


def getTitle(id: int):
    for title in titles:
        if title.id == id:
            return title
    return None


def getTitleByNameAndISBN(name: str, isbn: str):
    for title in titles:
        if title.title == name and str(title.isbn) == str(isbn):
            return title
    return None
