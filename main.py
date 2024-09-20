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
            self.tool_chosen
        )

        self.UI.toolbar__geometry_tool_button_action.changed.connect(
            self.tool_chosen
        )

        self.UI.toolbar__geometry_tool_menu__line_action.changed.connect(
            self.geometry_tool_change_geometry
        )
        self.UI.toolbar__geometry_tool_menu__rectangle_action.changed.connect(
            self.geometry_tool_change_geometry
        )
        self.UI.toolbar__geometry_tool_menu__polygon_action.changed.connect(
            self.geometry_tool_change_geometry
        )
        self.UI.toolbar__geometry_tool_menu__ellipse_action.changed.connect(
            self.geometry_tool_change_geometry
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
    def tool_chosen(self):
        tool_action = self.sender()
        if not tool_action.isChecked():
            return
        self.UI.work_area.setActiveGraphicTool(
            self.UI.toolbar__tool_instances[tool_action.text()]
        )

    @Slot()
    def geometry_tool_change_geometry(self):
        action = self.sender()
        if not action.isChecked():
            return
        if not self.UI.toolbar__geometry_tool_button_action.isChecked():
            self.UI.toolbar__geometry_tool_button_action.setChecked(True)
        self.UI.toolbar__tool_instances["Geometry tool"].set_geometry_type(
            action.text()
        )
        self.UI.toolbar__geometry_tool_button_action.setIcon(action.icon())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    utils.load_language(translator)
    window = RootWindow()
    window.show()
    sys.exit(app.exec())
