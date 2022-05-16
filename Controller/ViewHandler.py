from View import Views
from View.Views import View


class ViewHandler:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self, startView: View):
=======
=======
>>>>>>> Stashed changes
    def __init__(self, startView: View, *callbacks: classmethod, values: list):
        # Set the new currentView and instantiate it
>>>>>>> Stashed changes
        self.currentView = startView

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def initiateView(self, view: View):
=======
    def initiateView(self, view: View, *callbacks: classmethod, values: list):
>>>>>>> Stashed changes
=======
    def initiateView(self, view: View, *callbacks: classmethod, values: list):
>>>>>>> Stashed changes
        # Kill old view
        self.currentView.killView()

        # Set the new currentView
        self.currentView = view
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
        self.currentView.initView(callbacks, values)
>>>>>>> Stashed changes
=======
        self.currentView.initView(callbacks, values)
>>>>>>> Stashed changes

