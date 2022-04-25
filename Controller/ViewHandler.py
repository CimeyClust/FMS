from View import Views
from View.Views import View


class ViewHandler:
    def __init__(self, startView: View):
        self.currentView = startView

    def initiateView(self, view: View):
        # Kill old view
        self.currentView.killView()

        # Set the new currentView
        self.currentView = view

