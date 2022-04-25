from Controller.ViewHandler import ViewHandler
from Model.Model import Model
from View.Views import View, MainView


class Controller:
    def __init__(self):
        mainView = MainView()

        # Model
        self.model = Model()

        self.getTitles()

    def getTitles(self):
        examples = {
            1: {
                "title": "10 Wege um so schlau zu werden, wie Leon."
            }
        }
        for exampleKey in examples.keys():
            print(examples[exampleKey]["title"])

        # CallbackHandler
        # Load the main view, which enable the window
        # A new view will be instantiated every time it switches
        # Use self.callbackHandler.initiateView() to set a new view and kill the old one
        self.callbackHandler = ViewHandler(MainView())
