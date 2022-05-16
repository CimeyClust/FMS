from View import Views
from View.Views import View


class ViewHandler:
    def __init__(self, startView: View, *callbacks: classmethod, values: list):
        self.currentView = startView


    def initiateView(self, view: View, *callbacks: classmethod, values: list):
        # Kill old view
        self.currentView.killView()

        # Set the new currentView
        self.currentView = view

        self.currentView.initView(callbacks, values)

