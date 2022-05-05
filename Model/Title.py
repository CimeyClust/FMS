from Model.Subject import Subject

titles = []

class Title:
    def __init__(self, id: int, title: str, isbn: str, author: str, subject: Subject):
        self.id = id
        self.title = title
        self.isbn = isbn
        self.author = author
        self.subject = subject

        titles.append(self)
