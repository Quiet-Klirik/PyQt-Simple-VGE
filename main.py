import sys

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication, QMainWindow

from core import ui, utils


class RootWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UI = ui.RootWindow(self)

    def setup_connections(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    utils.load_language(translator)
    window = RootWindow()
    window.show()
    sys.exit(app.exec())
