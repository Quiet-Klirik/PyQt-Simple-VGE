from enum import Enum
from math import log2, log10

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
            self.scale(1.1, 1.1)
        else:
            self.scale(0.9, 0.9)
        event.accept()


class VGEGraphicsScene(QGraphicsScene):
    class GridStepRate(Enum):
        Binary = 2
        Decimal = 10

        def get_steps(self, visible_range: int | float) -> tuple[int, int]:
            """Returns (big_step, small_step)"""
            return self._get_steps(visible_range, self)

        @classmethod
        def _get_steps(cls, visible_range, rate):
            return(
                cls.get_binary_steps(visible_range) if rate == cls.Binary
                else cls.get_decimal_steps(visible_range) if rate == cls.Decimal

                else cls.get_binary_steps(visible_range)
            )

        @staticmethod
        def get_binary_steps(visible_range):
            big_step = 2**(max(2, int(log2(visible_range) - 2.5)))
            small_step = big_step // 4
            return big_step, small_step

        @staticmethod
        def get_decimal_steps(visible_range):
            log_10 = log10(visible_range)
            log_frac_part = log_10 % 1
            big_step = 10**(max(1, int(log_10)))
            step_divider = (
                20 if log_frac_part < 0.25 and big_step != 10
                else 10 if log_frac_part < 0.65
                else 5
            ) if visible_range > 10 else 10
            small_step = big_step // step_divider
            return big_step, small_step

    grid_step_rate: GridStepRate = GridStepRate.Binary
    draw_grid: bool = False

    def _draw_grid(self, painter, _):
        view = self.views()[0]
        viewport_rect = view.viewport().rect()

        top_left = view.mapToScene(viewport_rect.topLeft())
        top_right = view.mapToScene(viewport_rect.topRight())
        bottom_left = view.mapToScene(viewport_rect.bottomLeft())
        bottom_right = view.mapToScene(viewport_rect.bottomRight())
        scale = view.transform().m11()
        visible_range = min(
            top_right.x() - top_left.x(), bottom_left.y() - top_left.y()
        )
        big_step, small_step = self.grid_step_rate.get_steps(visible_range)

        pen = QPen(Qt.lightGray)
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
