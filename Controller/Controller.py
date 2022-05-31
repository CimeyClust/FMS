import datetime
import time
import tkinter

from Controller.CallbackRegister import Callback
from Controller.ViewHandler import ViewHandler
from Controller.ViewRegister import ViewRegister
from Model import Book, Subject, Student
from Model.SQLiteModel import SQLiteModel
from Model import Title
import unittest


class Controller(unittest.TestCase):
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
        self.mainView = ViewRegister.MAIN_VIEW.value()
        self.viewHandler = ViewHandler(self.mainView, self, (self.getBooks(), self.getAllSubjectNames()))

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
                        Title.getTitle(db.getBookTitleID(bookID[0])[0]),
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
                Subject.Subject(int(subjectID[0]), values[0].get())
                self.mainView.updateSubjects(self.getAllSubjectNames())
            values[0].delete(0, 'end')

        elif callbackType == Callback.DELETE_SUBJECT:
            try:
                with SQLiteModel() as db:
                    print(values[0])
                    db.deleteRow("FACHBEREICH", "FachbereichsID", Subject.getSubjectByName(values[0]).id)
                    Subject.subjects.remove(Subject.getSubjectByName(values[0]))
                    self.mainView.updateSubjects(self.getAllSubjectNames())
            except:
                pass

        elif callbackType == Callback.RELOAD_TABLE:
            if values[0] == "all":
                self.mainView.reloadTable(self.getBooks())
            elif values[0] == "available":
                self.mainView.reloadTable(self.getBooks(False))
            elif values[0] == "unavailable":
                self.mainView.reloadTable(self.getBooks(True))

        elif callbackType == Callback.CREATE_QRCODE:
            curItemID = values[0].focus()
            curItem = values[0].item(curItemID)
            bookID = curItem.get("text")
            with SQLiteModel() as db:
                db.generateQRCode(bookID)

        elif callbackType == Callback.BORROW_BOOK:
            with SQLiteModel() as db:
                student = Student.getStudentByAttributes(values[0], values[1], values[2])
                if student is None:
                    studentID = db.insertSchueler(values[0], values[1], values[2])[0]
                    student = Student.Student(studentID, values[0], values[1], values[2])

                curItemID = values[3].focus()
                curItem = values[3].item(curItemID)
                bookID = curItem.get("text")
                book = Book.getBook(bookID)

                book.student = student
                book.borrowed = True

                db.insertAusleihe(
                    student.id,
                    bookID,
                    datetime.date.today()
                )

            # Change button back to "Rückgabe"
            self.mainView.checkbox_button_2.configure(
                fg_color="#ff5e5e",
                hover_color="#c94949",
                state=tkinter.NORMAL,
                text="Zurückgeben",
                command=lambda: self.mainView.control.handleCallback(Callback.RETURN_BOOK, self.mainView.trv)
            )

            self.mainView.editwindow.destroy()

            curItemID = values[3].focus()
            curItem = values[3].item(curItemID)
            isBorrowed = curItem.get("values")
            self.mainView.reloadLeasingReturnButton(isBorrowed)

            if self.mainView.radio_var.get() == 0:
                self.mainView.reloadTable(self.getBooks())
            elif self.mainView.radio_var.get() == 1:
                self.mainView.reloadTable(self.getBooks(False))
            elif self.mainView.radio_var.get() == 2:
                self.mainView.reloadTable(self.getBooks(True))

        elif callbackType == Callback.RETURN_BOOK:
            with SQLiteModel() as db:
                curItemID = values[0].focus()
                curItem = values[0].item(curItemID)
                nValues = curItem.get("values")
                studentName = nValues[4].split(" ")[0]
                studentSurname = nValues[4].split(" ")[1]

                student = Student.getStudentByAttributes(studentName, studentSurname)

                if student is None:
                    return

                curItemID = values[0].focus()
                curItem = values[0].item(curItemID)
                bookID = curItem.get("text")
                book = Book.getBook(bookID)

                borrowID = db.getAusleiheID(student.id, bookID)[0]
                db.deleteRow("AUSLEIHE", "VorgangsID", borrowID)

                book.student = None
                book.borrowed = False

                # Change button back to "Ausleihen"
                self.mainView.checkbox_button_2.configure(
                    fg_color="#38FF88",
                    hover_color="#30d973",
                    state=tkinter.NORMAL,
                    text="Ausleihen",
                    command=self.mainView.leasing
                )

            if self.mainView.radio_var.get() == 0:
                self.mainView.reloadTable(self.getBooks())
            elif self.mainView.radio_var.get() == 1:
                self.mainView.reloadTable(self.getBooks(False))
            elif self.mainView.radio_var.get() == 2:
                self.mainView.reloadTable(self.getBooks(True))

        elif callbackType == Callback.SEARCH:
            content = values[0].get()
            matchedBooks = []

            for book in Book.books:
                if book.student is None:
                    if content in book.title.title or content in book.title.author or content in book.title.isbn:
                        matchedBooks.append(book)
                else:
                    if content.isnumeric():
                        if content in book.title.title or content in book.student.surname or \
                                content in book.student.name or content in book.student.schoolClass or \
                                content in book.title.author or content in book.title.isbn or int(content) == book.id:
                            matchedBooks.append(book)
                    else:
                        print(book.student.name)
                        print(content in book.student.surname)
                        if content in book.title.title or content in book.student.surname or \
                                content in book.student.name or content in book.student.schoolClass or \
                                content in book.title.author or content in book.title.isbn:
                            matchedBooks.append(book)

            self.mainView.reloadTable(matchedBooks)

    def createTestDatabaseInput(self):
        with SQLiteModel() as db:
            db.insertSchueler("Yassin", "Starzetz", "10.11")
            db.insertSchueler("Luis", "Hamann", "10.11")
            db.insertSchueler("Leon", "Martin", "10.11")
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
            db.insertAusleihe(1, 1, datetime.date.today())
            db.insertAusleihe(2, 3, datetime.date.today())
            db.insertAusleihe(3, 4, datetime.date.today())
            # db.dumpTable(['SCHÜLER', 'AUSLEIHE', 'EXEMPLAR', 'TITEL', 'FACHWERK'])
