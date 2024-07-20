from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsLineItem

from core.generics import VGEGraphicsTool


class SelectionTool(VGEGraphicsTool):
    pass


class GeometryTool(VGEGraphicsTool):
    def __init__(self):
        super().__init__()
        self.graphics_item: QGraphicsItem = QGraphicsLineItem()

        self.current_instance = None
        self.start_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = self.view.mapToScene(self.view.cursor_pos)
            self.current_instance = QGraphicsLineItem()
            pen = QPen(Qt.black, 2)
            self.current_instance.setPen(pen)
            self.current_instance.setLine(
                self.start_point.x(), self.start_point.y(),
                self.start_point.x(), self.start_point.y()
            )
            self.view.scene().addItem(self.current_instance)

    def mouseMoveEvent(self, event):
        if self.current_instance:
            end_point = self.view.mapToScene(self.view.cursor_pos)
            self.current_instance.setLine(
                self.start_point.x(), self.start_point.y(),
                end_point.x(), end_point.y()
            )

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.current_instance = None
