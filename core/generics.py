from enum import Enum
from math import log, log2

from PySide6.QtCore import Qt, QLine, QPoint
from PySide6.QtGui import QPen
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

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(1.1, 1.1)  # Збільшення масштабу
        else:
            self.scale(0.9, 0.9)  # Зменшення масштабу
        event.accept()


class VGEGraphicsScene(QGraphicsScene):
    class GridStepRate(Enum):
        Binary = 2
        Decimal = 5

    grid_step_rate: GridStepRate = GridStepRate.Binary
    draw_grid: bool = False

    def _draw_grid(self, painter, _):
        view = self.views()[0]
        viewport_rect = view.viewport().rect()

        top_left = view.mapToScene(viewport_rect.topLeft())
        top_right = view.mapToScene(viewport_rect.topRight())
        bottom_left = view.mapToScene(viewport_rect.bottomLeft())
        bottom_right = view.mapToScene(viewport_rect.bottomRight())
        visible_range = min(
            top_right.x() - top_left.x(), bottom_left.y() - top_left.y()
        )
        step_rate = self.grid_step_rate
        if step_rate == self.GridStepRate.Binary:
            big_step = 2**(max(2, int(log2(visible_range)) - 2))
            small_step = big_step // 4
        else:
            big_step = 5**(max(1, int(log(visible_range, 5) - 0.5)))
            small_step = big_step // 5

        pen = QPen(Qt.lightGray)
        scale = view.transform().m11()
        pen.setWidth(0.1)
        painter.setPen(pen)

        range_start = (
            (top_left / big_step).toPoint() + QPoint(-1, -1)
        ) * big_step
        range_end = (
            (bottom_right / big_step).toPoint() + QPoint(1, 1)
        ) * big_step
        painter.drawLines([
            QLine(x, int(top_left.y()), x, int(bottom_left.y()) + 1)
            for x in range(int(range_start.x()), int(range_end.x()), small_step)
        ]+[
            QLine(int(top_left.x()), y, int(top_right.x()) + 1, y)
            for y in range(int(range_start.y()), int(range_end.y()), small_step)
        ])

        if scale > 6:
            return

        pen.setWidth(
            1 if scale > 3
            else 2 if scale > 1
            else 3 // scale
        )
        painter.setPen(pen)
        painter.drawLines([
            QLine(x, int(top_left.y()), x, int(bottom_left.y()) + 1)
            for x in range(int(range_start.x()), int(range_end.x()), big_step)
        ]+[
            QLine(int(top_left.x()), y, int(top_right.x()) + 1, y)
            for y in range(int(range_start.y()), int(range_end.y()), big_step)
        ])

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        painter.fillRect(rect, Qt.lightGray)
        scene_rect = self.sceneRect()
        painter.fillRect(scene_rect, Qt.white)

        if self.draw_grid:
            self._draw_grid(painter, rect)
