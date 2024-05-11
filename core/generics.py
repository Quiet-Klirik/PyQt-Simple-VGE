from PySide6.QtWidgets import QMainWindow


class WindowUI:
    def __init__(self, window: QMainWindow):
        self.window = window
        self.tr = self.window.tr
