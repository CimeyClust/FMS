from Controller.ViewHandler import ViewHandler
from Controller.ViewRegister import ViewRegister
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

    def getTitles(self):
        examples = []

        return  examples