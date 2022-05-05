from Controller.ViewHandler import ViewHandler
from Controller.ViewRegister import ViewRegister
from Model.Book import Book
from Model.Model import Model
from View.Views import View, MainView


class Controller:
    def __init__(self):
        mainView = MainView()

        # Model
        self.model = Model()

        # CallbackHandler
        # Load the main view, which enable the window
        # A new view will be instantiated every time it switches
        # Use self.viewHandler.initiateView() to set a new view and kill the old one
        # Set Main windows on startup
        self.viewHandler = ViewHandler(ViewRegister.MAIN_VIEW.value)

    '''
    Loads every subject into it's own initiation of the Subject-Class
    '''
    def loadSubjects(self):
        pass

    '''
    Loads every title into it's own initiation of the Title-Class
    '''
    def loadTitles(self):
        pass

    ''''
    Loads every book into it's own initiation of the Title-Class
    '''
    def loadBooks(self):
        pass

    '''
    Return all books if onlyBorrowed = false
    If onlyBorrowed = true, only already borrowed books will be returned
    '''
    def getAllBooks(self, onlyBorrowed: bool):
        exampleBooks: list[Book] = []

        return exampleBooks