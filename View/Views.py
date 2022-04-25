from tkinter import *
from tkinter.ttk import *

# Each View (different Window) should have one own class.
# By instantiating the class of the view, the old view should close and the new one should appear


# The main class every other view is inheriting from
class View:
    def killView(self):
        pass


class MainView(View):
    def __init__(self):
        # Enable the view and show it in the window
        pass

    # Hide the current view and disable it
    def killView(self):
        print("Test")
