from Controller.CallbackRegister import Callback
from Controller.ViewHandler import ViewHandler
from Controller.ViewRegister import ViewRegister
from Model import Book, Subject, Student
from Model.SQLiteModel import SQLiteModel
from Model import Title
from View.Views import View, MainView


class Controller:
    def __init__(self):
        mainView = MainView()

        # Model
        self.model = SQLiteModel()

        # CallbackHandler
        # Load the main view, which enable the window
        # A new view will be instantiated every time it switches

        # Use self.callbackHandler.initiateView() to set a new view and kill the old one

        # Use self.viewHandler.initiateView() to set a new view and kill the old one
        # Set Main windows on startup
        self.viewHandler = ViewHandler(ViewRegister.MAIN_VIEW.value, self, self.getBooks())


    """
    Loads every subject into it's own initiation of the Subject-Class
    """
    def loadSubjects(self):
        with SQLiteModel() as db:
            for subjectID in db.getSubjectIDs():
                Subject.Subject(
                    subjectID[0],
                    db.getSubjectName(subjectID[0])[0]
                )

    """
    Loads every title into it's own initiation of the Title-Class
    """
    def loadTitles(self):
        with SQLiteModel() as db:
            for titleID in db.getTitleIDs():
                Title.Title(
                    titleID[0],
                    db.getTitleTitle(titleID[0])[0],
                    db.getTitleISBN(titleID[0])[0],
                    db.getTitleAuthor(titleID[0])[0],
                    Subject.getSubject(db.getTitleSubjectID(titleID[0])[0])
                )

    """
    Loads every student into it's own initiation of the Student-Class
    """

    def loadStudents(self):
        with SQLiteModel() as db:
            for studentID in db.getStudentIDs():
                Student.Student(
                    studentID[0],
                    db.getStudentSurName(studentID[0])[0],
                    db.getStudentLastName(studentID[0])[0],
                    db.getStudentSchoolClass(studentID[0])[0]
                )

    """
    Loads every book into it's own initiation of the Book-Class
    """
    def loadBooks(self):
        with SQLiteModel() as db:
            for bookID in db.getBookIDs():
                if db.isBookBorrowed(bookID[0]):
                    Book.Book(
                        bookID[0],
                        db.isBookBorrowed(bookID[0]),
                        Title.getTitle(db.getBookTitleID(bookID[0])[0]),
                        Student.getStudent(db.getBookStudentID(bookID[0])[0])
                    )
                else:
                    Book.Book(
                        bookID[0],
                        db.isBookBorrowed(bookID[0]),
                        Title.getTitle(db.getBookTitleID(bookID[0])[0])
                    )

    """
    Just return no borrowed books onlyBorrowed = false
    If onlyBorrowed = true, only already borrowed books will be returned
    Return all books if onlyBorrowed is not given
    """
    def getBooks(self, onlyBorrowed: bool = None):
        Book.Book(1, False, Title.Title(1, "Test1", "ISBN1", "Ich", Subject.Subject(1, "Mathe")))
        Book.Book(2, False, Title.Title(2, "Test2", "ISBN2", "Ich", Subject.Subject(2, "Deutsch")))
        Book.Book(3, False, Title.Title(3, "Test3", "ISBN3", "Ich", Subject.Subject(3, "Englisch")))
        Book.Book(4, False, Title.Title(4, "Test4", "ISBN4", "Ich", Subject.Subject(4, "Sport")))

        borrowedBooks = []
        if onlyBorrowed is None:
            return Book.books

        if onlyBorrowed:
            for book in Book.books:
                if book.borrowed:
                    borrowedBooks.append(book)
        else:
            for book in Book.books:
                if not book.borrowed:
                    borrowedBooks.append(book)
        return borrowedBooks

    """
    Handles the callbacks of the view
    """
    def handleCallback(self, callbackType: Callback):
        if callbackType == Callback.ADD_TITLE_BUTTON:
            pass
        elif callbackType == Callback.ADD_BOOKS_BUTTON:
            pass
        elif callbackType == Callback.CREATE_QR_CODE_BUTTON:
            pass
