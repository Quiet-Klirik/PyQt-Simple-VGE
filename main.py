import sys

from PySide6.QtCore import QTranslator, Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from core import ui, utils


class RootWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UI = ui.RootWindow(self)
        self.setup_connections()

        self.UI.toolbar__selection_tool_button_action.trigger()

    def setup_connections(self):
        self.UI.menubar__view_menu__grid_action.changed.connect(
            self.toggle_grid_display
        )
        self.UI.menubar__view_menu__ruler_action.changed.connect(
            self.toggle_ruler_display
        )

        self.UI.toolbar__selection_tool_button_action.changed.connect(
            self.selection_tool_chosen
        )

        self.UI.toolbar__selection_tool_button_action.changed.connect(
            self.geometry_tool_chosen
        )

    @Slot()
    def toggle_grid_display(self):
        self.UI.work_area.draw_grid = (
            self.UI.menubar__view_menu__grid_action.isChecked()
        )

    @Slot()
    def toggle_ruler_display(self):
        self.UI.work_area.draw_ruler = (
            self.UI.menubar__view_menu__ruler_action.isChecked()
        )

    @Slot()
    def selection_tool_chosen(self):
        if not self.UI.toolbar__selection_tool_button_action.isChecked():
            return
        self.UI.work_area.setActiveGraphicTool(
            self.UI.toolbar__selection_tool_instance
        )

    @Slot()
    def geometry_tool_chosen(self):
        if not self.UI.toolbar__geometry_tool_button_action.isChecked():
            return
        self.UI.work_area.setActiveGraphicTool(
            self.UI.toolbar__geometry_tool_instance
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    utils.load_language(translator)
    window = RootWindow()
    window.show()
    sys.exit(app.exec())
