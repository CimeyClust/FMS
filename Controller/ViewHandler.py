from Controller import Controller
from View import Views
from View.Views import View


class ViewHandler:
    def __init__(self, startView: View, control: Controller, values: list):
        self.currentView = startView

        self.initiateView(startView, control, values)

    def initiateView(self, view: View, control: Controller, values: list):
        # Kill old view
        self.currentView.killView()

        # Set the new currentView
        self.currentView = view

        print(str(view))
        self.currentView.initView(control, values)

