from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene


class WindowUI:
    def __init__(self, window: QMainWindow):
        self.window = window
        self.tr = self.window.tr


class VGEGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_button = Qt.RightButton

        self.setMouseTracking(True)
        self.last_pos = None

    def setDragButton(self, button: Qt.MouseButton):
        self.drag_button = button

    def mousePressEvent(self, event):
        if (
                self.dragMode() == self.DragMode.RubberBandDrag
                and event.button() == self.drag_button
        ):
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & self.drag_button:
            delta = event.pos() - self.last_pos
            horizontal_scrollbar = self.horizontalScrollBar()
            vertical_scrollbar = self.verticalScrollBar()
            horizontal_scrollbar.setValue(
                horizontal_scrollbar.value() - delta.x()
            )
            vertical_scrollbar.setValue(
                vertical_scrollbar.value() - delta.y()
            )
            self.last_pos = event.pos()
        else:
            super().mouseMoveEvent(event)


class VGEGraphicsScene(QGraphicsScene):
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        painter.fillRect(rect, Qt.lightGray)
        scene_rect = self.sceneRect()
        painter.fillRect(scene_rect, Qt.white)
