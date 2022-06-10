###########################################################################
#
# Controller.py
# Program made by Jan, Sinan and Leon for the FMS project.
#
###########################################################################

import datetime
import sys
import tkinter
import traceback

from mysql.connector import DatabaseError

from Controller.CallbackRegister import Callback
from Controller.ViewHandler import ViewHandler
from Controller.ViewRegister import ViewRegister
from Model import Book, Subject, Student
from Model.MySQLModel import MySQLModel
from Model.SQLiteModel import SQLiteModel
from Model import Title
import unittest


class Controller:
    def __init__(self, args=None):
        if args is None:
            args = []
        self.sqliteModel = SQLiteModel()
        # Create test database input at beginning
        # self.createTestDatabaseInput()

        # Register listener for book deletion
        # asyncio.run(KeyListener.registerTask())

        # Load access data for the Remote Database
        with SQLiteModel() as db:
            self.host = db.getConnectionHost(1)[0]
            self.user = db.getConnectionUser(1)[0]
            self.password = db.getConnectionPassword(1)[0]
            self.database = db.getConnectionDatabase(1)[0]

        print(self.host)
        print(self.user)
        print(self.password)
        print(self.database)
        if self.host is None or self.user is None or self.password is None or self.database is None:
            with SQLiteModel() as db:
                db.insertEmptyConnection(1)
            self.mainView = ViewRegister.MAIN_VIEW.value()
            self.viewHandler = ViewHandler(self.mainView, self, (self.getBooks(), self.getAllSubjectNames, True))
            return

        # Load data
        try:
            self.loadSubjects()
            self.loadTitles()
            self.loadStudents()
            self.loadBooks()
        except DatabaseError as error:
            print(traceback.format_exc())
            if self.host is None or self.user is None or self.password is None or self.database is None:
                with SQLiteModel() as db:
                    db.insertEmptyConnection(1)
            self.mainView = ViewRegister.MAIN_VIEW.value()
            self.viewHandler = ViewHandler(self.mainView, self, (self.getBooks(), self.getAllSubjectNames, True))
            return

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
        self.viewHandler = ViewHandler(self.mainView, self, (self.getBooks(), self.getAllSubjectNames, False))

    """
    Loads every subject into it's own initiation of the Subject-Class
    """

    def loadSubjects(self):
        with MySQLModel(self.host, self.user, self.password, self.database) as db:
            for subjectID in db.getSubjectIDs():
                Subject.Subject(
                    subjectID[0],
                    db.getSubjectName(subjectID[0])[0]
                )

    """
    Loads every title into it's own initiation of the Title-Class
    """

    def loadTitles(self):
        with MySQLModel(self.host, self.user, self.password, self.database) as db:
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
        with MySQLModel(self.host, self.user, self.password, self.database) as db:
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
        with MySQLModel(self.host, self.user, self.password, self.database) as db:
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

    def getBookAmount(self, title: Title.Title):
        amount = 0
        for currentBook in Book.books:
            if currentBook.title == title:
                amount += 1
        return amount

    def reloadTable(self):
        if self.mainView.radio_var.get() == 0:
            self.mainView.reloadTable(self.getBooks())
        elif self.mainView.radio_var.get() == 1:
            self.mainView.reloadTable(self.getBooks(False))
        elif self.mainView.radio_var.get() == 2:
            self.mainView.reloadTable(self.getBooks(True))

    """
    Handles the callbacks of the view
    """

    def handleCallback(self, callbackType: Callback, *values):
        if callbackType == Callback.ADD_DB_CONNECTION:
            with SQLiteModel() as db:
                try:
                    db.updateConnection(1, values[0].get(), values[1].get(), values[2].get(), values[3].get())
                except DatabaseError as error:

                    print(error)
            self.mainView.connectionwindow.after(100, self.mainView.connectionwindow.destroy)
            Controller()
        elif callbackType == Callback.ADD_SUBJECT:
            with MySQLModel(self.host, self.user, self.password, self.database) as db:
                subjectID = db.insertFachbereich(values[0].get())
                Subject.Subject(int(subjectID[0]), values[0].get())
                self.mainView.updateSubjects(self.getAllSubjectNames())
            values[0].delete(0, 'end')

        elif callbackType == Callback.DELETE_SUBJECT:
            try:
                subject = Subject.getSubjectByName(values[0])

                # Delete books and titles, which belong to this subject
                removedBooks = []
                for i in range(0, len(Book.books)):
                    book = Book.books[i]
                    if book.title.subject == subject:
                        with MySQLModel(self.host, self.user, self.password, self.database) as db:
                            db.deleteRow("EXEMPLAR", "ExemplarID", book.id)
                        removedBooks.append(book)

                [Book.books.remove(book) for book in removedBooks]

                for title in Title.titles:
                    if title.subject.id == subject.id:
                        MySQLModel(self.host, self.user, self.password, self.database).deleteRow("TITEL", "TitelID", title.id)
                        Title.titles.remove(title)

                with MySQLModel(self.host, self.user, self.password, self.database) as db:
                    db.deleteRow("FACHBEREICH", "FachbereichsID", subject.id)
                    Subject.subjects.remove(Subject.getSubjectByName(values[0]))
                    self.mainView.updateSubjects(self.getAllSubjectNames())

                self.reloadTable()
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
            with MySQLModel(self.host, self.user, self.password, self.database) as db:
                db.generateQRCode(bookID)

        elif callbackType == Callback.BORROW_BOOK:
            with MySQLModel(self.host, self.user, self.password, self.database) as db:
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

            self.mainView.leasingwindow.after(100, self.mainView.leasingwindow.destroy)
            self.mainView.trigger1 = False

            curItemID = values[3].focus()
            curItem = values[3].item(curItemID)
            isBorrowed = curItem.get("values")

            # self.mainView.reloadLeasingReturnButton(isBorrowed)

            self.reloadTable()

        elif callbackType == Callback.RETURN_BOOK:
            with MySQLModel(self.host, self.user, self.password, self.database) as db:
                curItemID = values[0].focus()
                curItem = values[0].item(curItemID)
                nValues = curItem.get("values")
                try: studentName = nValues[4].split(" ")[0]
                except IndexError: return
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

            self.reloadTable()

        elif callbackType == Callback.SEARCH:
            content = values[0].get()
            if content == "Suchen":
                return

            matchedBooks = []

            for book in Book.books:
                if book.student is None:
                    if content.isnumeric():
                        if 1000 < int(content):
                            if content in book.title.title or content in book.title.author or content in book.title.isbn \
                                    or int(content) == book.id:
                                matchedBooks.append(book)
                        elif int(content) == book.id:
                            matchedBooks.append(book)
                    else:
                        if content in book.title.title or content in book.title.author or content in book.title.isbn:
                            matchedBooks.append(book)
                else:
                    if content.isnumeric():
                        if 1000 < int(content):
                            if content in book.title.title or content in book.student.surname or \
                                    content in book.student.name or content in book.student.schoolClass or \
                                    content in book.title.author or content in book.title.isbn or int(content) == book.id:
                                matchedBooks.append(book)
                        else:
                            if int(content) == book.id:
                                matchedBooks.append(book)
                    else:
                        if content in book.title.title or content in book.student.surname or \
                                content in book.student.name or content in book.student.schoolClass or \
                                content in book.title.author or content in book.title.isbn:
                            matchedBooks.append(book)

            self.mainView.reloadTable(matchedBooks)

        elif callbackType == Callback.TITLE_CREATE:
            print("Test")
            subject = Subject.getSubjectByName(values[0].get())
            titleName = values[1].get()
            isbn = values[2].get()
            author = values[3].get()
            amount = values[4].get()

            # Check if the amount number by the user is really a number
            if amount.isnumeric():
                amount = int(amount)

                if amount > 10000:
                    return
            else:
                return

            books = []
            with MySQLModel(self.host, self.user, self.password, self.database) as db:
                titleID = db.insertTitel(subject.id, titleName, author, isbn)[0]
                title = Title.Title(titleID, titleName, isbn, author, subject)

                # Create all the books, given in amount
                for bookIndex in range(0, amount):
                    note = (str(bookIndex) + str(title.id))
                    bookID = db.insertExemplar(titleID, "")[-1][0]
                    Book.Book(bookID, False, title)

            self.reloadTable()

            values[1].delete(0, 'end')
            values[2].delete(0, 'end')
            values[3].delete(0, 'end')
            values[4].delete(0, 'end')

        elif callbackType == Callback.TITLE_EDIT_INIT:
            curItemID = values[0].focus()
            curItem = values[0].item(curItemID)
            try: bookID = int(curItem.get("text"))
            except: return

            # Get the amount of all books with the same title
            book = Book.getBook(bookID)
            amount = self.getBookAmount(book.title)

            self.mainView.edit(amount, self.getAllSubjectNames())

        elif callbackType == Callback.BOOK_DELETE:
            curItemID = values[0].focus()
            curItem = values[0].item(curItemID)
            try:
                bookID = int(curItem.get("text"))
            except:
                return

            with MySQLModel(self.host, self.user, self.password, self.database) as db:
                db.deleteRow("EXEMPLAR", "ExemplarID", bookID)
                Book.books.remove(Book.getBook(bookID))

            self.reloadTable()

            # Set focus back
            newIndex = (int(curItemID) - 1)
            values[0].focus_set()
            if Book.getBook(newIndex) is None:
                newIndex = (int(curItemID) + 1)

            if not Book.getBook(newIndex) is None:
                try: values[0].selection_set(newIndex)
                except: return
                values[0].focus(newIndex)

        elif callbackType == Callback.TITLE_EDIT:
            curItemID = self.mainView.trv.focus()
            curItem = self.mainView.trv.item(curItemID)

            subject = Subject.getSubjectByName(values[0].get())
            if subject is None: return

            titleNameBefore = curItem.get("values")[0]
            titleName = values[1].get()
            isbnBefore = curItem.get("values")[1]
            isbn = values[2].get()
            author = values[3].get()
            amount = values[4].get()

            # Check if the amount number by the user is really a number
            if amount.isnumeric():
                amount = int(amount)
            else:
                return

            with MySQLModel(self.host, self.user, self.password, self.database) as db:
                oldTitle = Title.getTitleByNameAndISBN(titleNameBefore, isbnBefore)

                # Update database
                db.updateTitle(oldTitle.id, titleName, isbn, author, subject.id)

                # Update title instances
                oldTitle.title = titleName
                oldTitle.isbn = isbn
                oldTitle.author = author
                oldTitle.subject = subject

                currentAmount = self.getBookAmount(oldTitle)
                if amount < 0:
                    return

                if currentAmount > amount:
                    # Search all books, with a lower in priority, which can be deleted
                    bookPrio1 = []
                    for book in Book.books:
                        if book.borrowed:
                            bookPrio1.append(book)

                    bookPrio2 = []
                    for book in Book.books:
                        if not book.borrowed:
                            bookPrio2.append(book)

                    for newBookNumber in range(0, ((amount - currentAmount) * (-1))):
                        # bookID = db.insertExemplar(oldTitle.id, str(newBookNumber))[-1]
                        # Book.Book(bookID, False, oldTitle)
                        if not bookPrio1 == []:
                            db.deleteRow("EXEMPLAR", "ExemplarID", bookPrio1[-1].id)
                            Book.books.remove(bookPrio1[-1])
                            bookPrio1.remove(bookPrio1[-1])
                        else:
                            db.deleteRow("EXEMPLAR", "ExemplarID", bookPrio2[-1].id)
                            Book.books.remove(bookPrio2[-1])
                            bookPrio2.remove(bookPrio2[-1])

                if currentAmount < amount:
                    for newBookNumber in range(0, (amount - currentAmount)):
                        bookID = db.insertExemplar(oldTitle.id, "")[-1][0]
                        Book.Book(bookID, False, oldTitle)

            self.reloadTable()

            self.mainView.editwindow.after(100, self.mainView.editwindow.destroy)
            self.mainView.trigger1 = False

    def createTestDatabaseInput(self):
        with MySQLModel(self.host, self.user, self.password, self.database) as db:
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
