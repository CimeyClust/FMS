from tkinter import *
from tkinter.ttk import *

# Each View (different Window) should have one own class.
# By instantiating the class of the view, the old view should close and the new one should appear


# The main class every other view is inheriting from
class View:
    def initView(self, *callbacks):
        pass

    def killView(self):
        pass


class MainView(View):
    def initView(self, *callbacks):
        pass

    # Hide the current view and disable it
    def killView(self):
        print("Killed MainView. Window is empty.")
