from View import Views
from View.Views import View, MainView


class ViewHandler:
    def __init__(self, startView: View, *callbacks: classmethod, values: list):
        # Set the new currentView and instantiate it
        self.currentView = startView
        self.currentView.initView()

    def initiateView(self, view: View, *callbacks: classmethod, values: list):
        # Kill old view
        self.currentView.killView()

        # Set the new currentView and instantiate it
        self.currentView = view
        self.currentView.initView(callbacks, values)

