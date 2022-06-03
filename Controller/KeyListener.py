import asyncio

from pynput.keyboard import Key, Listener

from Controller.CallbackRegister import Callback


class KeyListener:
    def __init__(self, control):
        self.control = control

        # Collect events until released
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        return False

    def on_release(self, key):
        if key == Key.delete:
            self.control.handleCallback(Callback.BOOK_DELETE)
        return False
