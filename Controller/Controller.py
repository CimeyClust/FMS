from Controller.ViewHandler import ViewHandler
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
        # Use self.callbackHandler.initiateView() to set a new view and kill the old one
        self.callbackHandler = ViewHandler(MainView())
