import datetime

from Controller.CallbackRegister import Callback
from Controller.ViewHandler import ViewHandler
from Controller.ViewRegister import ViewRegister
from Model import Book, Subject, Student
from Model.SQLiteModel import SQLiteModel
from Model import Title


class Controller:
    def __init__(self, args):
        # Model
        self.model = SQLiteModel()

        # Create test database input at beginning
        # self.createTestDatabaseInput()

        # Load data
        self.loadSubjects()
        self.loadTitles()
        self.loadStudents()
        self.loadBooks()

        # CallbackHandler
        # Load the main view, which enable the window
        # A new view will be instantiated every time it switches

        # Use self.callbackHandler.initiateView() to set a new view and kill the old one

        # Cancel the init of the view, when the code gets tested:
        if len(args) >= 1 and "testing" in args:
            return

        # Use self.viewHandler.initiateView() to set a new view and kill the old one
        # Set Main windows on startup
        self.mainView = ViewRegister.MAIN_VIEW.value
        self.viewHandler = ViewHandler(self.mainView, self, (self.getBooks(), self.getAllSubjectNames()))

    """
    Loads every subject into it's own initiation of the Subject-Class
    """
    def loadSubjects(self):
        with SQLiteModel() as db:
            for subjectID in db.getSubjectIDs():
                print("Subject: " + str(subjectID))
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

    def getAllSubjectNames(self):
        subjectNames = []
        for subject in Subject.subjects:
            subjectNames.append(subject.subjectTitle)

        return subjectNames

    """
    Handles the callbacks of the view
    """
    def handleCallback(self, callbackType: Callback, *values):
        if callbackType == Callback.ADD_SUBJECT:
            with SQLiteModel() as db:
                subjectID = db.insertFachbereich(values[0].get())
                print(Subject.Subject(int(subjectID[0]), values[0].get()).subjectTitle)
            values[0].delete(0, 'end')

        elif callbackType == Callback.DELETE_SUBJECT:
            with SQLiteModel() as db:
                db.deleteRow("FACHBEREICH", Subject.getSubjectByName(values[0]))
                Subject.subjects.remove(Subject.getSubjectByName(values[0]))

        elif callbackType == Callback.RELOAD_TABLE:
            if values[0] == "all":
                self.mainView.reloadTable(self.getBooks())
            elif values[0] == "available":
                self.mainView.reloadTable(self.getBooks(False))
            elif values[0] == "unavailable":
                self.mainView.reloadTable(self.getBooks(True))


    def createTestDatabaseInput(self):
        with SQLiteModel() as db:
            db.insertSchueler("Yassin", "Starzetz", 1011)
            db.insertSchueler("Luis", "Hamann", 1011)
            db.insertSchueler("Leon", "Martin", 1011)
            db.insertFachbereich("Mathe")
            db.insertFachbereich("Englisch")
            db.insertTitel(1, "Math - the Book", "Dr. Bum", "1154848942134")
            db.insertTitel(1, "1 + 1 die Basics", "Smith Johnson", "1157496342456")
            db.insertTitel(2, "learn english", "Erwin Arlert", "1685645422381")
            db.insertExemplar(1, "sieht gut aus")
            db.insertExemplar(2, "bisl zerkratzt")
            db.insertExemplar(2, "Flasche ausgeschüttet")
            db.insertExemplar(3, "wurde aus Versehen verbrannt")
            db.insertExemplar(3, "wurde reingemalt")
            db.insertAusleihe(1, 1, datetime.date.today(), datetime.date(2022, 7, 6))
            db.insertAusleihe(2, 3, datetime.date.today(), datetime.date(2022, 7, 6))
            db.insertAusleihe(3, 4, datetime.date.today(), datetime.date(2022, 7, 6))
            # db.dumpTable(['SCHÜLER', 'AUSLEIHE', 'EXEMPLAR', 'TITEL', 'FACHWERK'])
