from Controller.ViewHandler import ViewHandler
from Controller.ViewRegister import ViewRegister
from Model import Book, Student, Subject, Title
from Model.Model import Model
from View.Views import View, MainView
from pythonlangutil.overload import Overload, signature


class Controller:
    """
    Init the controller
    """
    def __init__(self):
        mainView = MainView()

        # Model
        self.model = Model()

        # Load all subjects into instances
        self.loadSubjects()

        # Load all titles into instances with also a subject instance
        self.loadTitles()

        # Load all book instances (Exemplare) at least
        self.loadBooks()

        # CallbackHandler
        # Load the main view, which enable the window
        # A new view will be instantiated every time it switches
        # Use self.viewHandler.initiateView() to set a new view and kill the old one
        # Set Main windows on startup
        self.viewHandler = ViewHandler(ViewRegister.MAIN_VIEW.value)

    """
    Loads every subject into it's own initiation of the Subject-Class
    """
    def loadSubjects(self):
        with Model() as db:
            for subjectID in db.getSubjectIDs():
                Subject.Subject(
                    subjectID,
                    db.getSubjectName(subjectID)
                )

    """
    Loads every title into it's own initiation of the Title-Class
    """
    def loadTitles(self):
        with Model() as db:
            for titleID in db.getTitleIDs():
                Title.Title(
                    titleID,
                    db.getTitleTitle(titleID),
                    db.getTitleISBN(titleID),
                    db.getTitleAuthor(titleID),
                    Subject.getSubject(db.getTitleSubjectID(titleID))
                )

    """
    Loads every student into it's own initiation of the Student-Class
    """

    def loadStudents(self):
        with Model() as db:
            for studentID in db.getStudentIDs():
                Student.Student(
                    studentID,
                    db.getStudentSurName(studentID),
                    db.getStudenLastName(studentID),
                    db.getStudentSchoolClass(studentID)
                )

    """
    Loads every book into it's own initiation of the Book-Class
    """
    def loadBooks(self):
        with Model() as db:
            for bookID in db.getBookIDs():
                if db.isBookBorrowed():
                    Book.Book(
                        bookID,
                        db.isBookBorrowed(bookID),
                        Title.getTitle(db.getBookTitleID()),
                        Student.getStudent(db.getBookStudentID())
                    )
                else:
                    Book.Book(
                        bookID,
                        db.isBookBorrowed(bookID),
                        Title.getTitle(db.getBookTitleID())
                    )

    """
    Just return no borrowed books onlyBorrowed = false
    If onlyBorrowed = true, only already borrowed books will be returned
    """
    def getBooks(self, onlyBorrowed: bool):
        borrowedBooks = []
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
    Return all books, ignoring the borrowed state
    """
    @Overload
    def getBooks(self):
        return Book.books
