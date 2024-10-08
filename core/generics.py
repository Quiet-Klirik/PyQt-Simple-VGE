from abc import ABC
from enum import Enum
from math import log2, log10

from PySide6.QtCore import Qt, QLine, QPoint, QLineF, QPointF
from PySide6.QtGui import QPen, QPainter, QColor, QFont, QMouseEvent
from PySide6.QtWidgets import QMainWindow, QGraphicsView

from core.settings import config, DefaultSettings
from core.utils import frange


class WindowUI:
    def __init__(self, window: QMainWindow):
        self.window = window
        self.tr = self.window.tr


class VGEGraphicsTool(ABC):
    def __init__(self):
        self.view: VGEGraphicsView | None = None

    def setParentView(self, view):
        self.view = view

    def mousePressEvent(self, event: QMouseEvent):
        pass

    def mouseMoveEvent(self, event: QMouseEvent):
        pass

    def mouseReleaseEvent(self, event: QMouseEvent):
        pass


class VGEGraphicsView(QGraphicsView):
    class GridStepRateData:
        last_visible_range = None
        last_steps: tuple[int, int] = None

    class GridStepRate(Enum):
        Binary = 2
        Decimal = 10

        def get_steps(self, visible_range: int | float) -> tuple[int, int]:
            """Returns (big_step, small_step)"""
            data = VGEGraphicsView.GridStepRateData
            if visible_range == data.last_visible_range:
                return data.last_steps
            steps = self._get_steps(visible_range, self)
            data.last_visible_range = visible_range
            data.last_steps = steps
            return steps

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

        @staticmethod
        def get_last_steps():
            return VGEGraphicsView.GridStepRateData.last_steps

    class Colors:
        Background: QColor = QColor(230, 230, 230)
        SceneRect: QColor = Qt.white
        Grid: QColor = QColor(230, 230, 230)
        Cursor: QColor = QColor(0, 0, 225)
        Ruler: QColor = QColor(220, 220, 220)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_button = Qt.RightButton

        self.grid_step_rate: VGEGraphicsView.GridStepRate = (
            getattr(VGEGraphicsView.GridStepRate, config.value(
                "grid_step_rate", DefaultSettings.GRID_STEP_RATE)
                    )
        )
        self.draw_grid: bool = config.value(
            "draw_grid", DefaultSettings.DRAW_GRID
        )

        self.ruler_width: int = 18
        self.draw_ruler: bool = config.value(
            "draw_ruler", DefaultSettings.DRAW_RULER
        )

        self.setMouseTracking(True)
        self._drag_start_pos = None
        self.cursor_pos = None
        self.fit_cursor_into_grid: bool = config.value(
            "fit_cursor_into_grid", DefaultSettings.FIT_CURSOR_INTO_GRID
        )

        self.active_graphic_tool: VGEGraphicsTool = VGEGraphicsTool()

    def _draw_grid(self, painter):
        viewport_rect = self.viewport().rect()

        top_left = self.mapToScene(viewport_rect.topLeft())
        bottom_right = self.mapToScene(viewport_rect.bottomRight())
        scale = self.transform().m11()
        visible_range = min(
            bottom_right.x() - top_left.x(), bottom_right.y() - top_left.y()
        )

        big_step, small_step = self.grid_step_rate.get_steps(visible_range)

        if big_step > 10**8:
            return

        pen = QPen(self.Colors.Grid)
        pen.setWidth(0.1)
        painter.setPen(pen)

        range_start = (
            (top_left / big_step).toPoint() + QPoint(-1, -1)
        ) * big_step
        range_end = (
            (bottom_right / big_step).toPoint() + QPoint(1, 1)
        ) * big_step
        painter.drawLines([
            QLine(x, int(top_left.y()), x, int(bottom_right.y()) + 1)
            for x in range(int(range_start.x()), int(range_end.x()), small_step)
        ]+[
            QLine(int(top_left.x()), y, int(bottom_right.x()) + 1, y)
            for y in range(int(range_start.y()), int(range_end.y()), small_step)
        ])

        if scale <= 6:
            pen.setWidth(
                1 if scale > 3
                else 2 if scale > 1
                else 3 // scale
            )
            painter.setPen(pen)
            painter.drawLines([
                QLine(x, int(top_left.y()), x, int(bottom_right.y()) + 1)
                for x in range(int(range_start.x()), int(range_end.x()), big_step)
            ]+[
                QLine(int(top_left.x()), y, int(bottom_right.x()) + 1, y)
                for y in range(int(range_start.y()), int(range_end.y()), big_step)
            ])

        if self.cursor_pos:
            painter = QPainter(self.viewport())
            pen = QPen(self.Colors.Cursor)
            pen.setWidth(0.1)
            painter.setPen(pen)

            cursor_pos = self.cursor_pos
            painter.drawLines([
                QLineF(cursor_pos.x() - 5, cursor_pos.y(),
                       cursor_pos.x() + 5, cursor_pos.y()),
                QLineF(cursor_pos.x(), cursor_pos.y() - 5,
                       cursor_pos.x(), cursor_pos.y() + 5)
            ])

    def _draw_ruler(self):
        viewport_rect = self.viewport().rect()
        painter = QPainter(self.viewport())
        pen = QPen(Qt.black)
        pen.setWidth(0.1)
        painter.setPen(pen)

        top_left = viewport_rect.topLeft()
        bottom_right = viewport_rect.bottomRight()

        size = bottom_right - top_left

        painter.fillRect(
            top_left.x(), self.ruler_width,
            self.ruler_width, size.y(),
            self.Colors.Ruler
        )
        painter.fillRect(
            self.ruler_width, top_left.y(),
            size.x(), self.ruler_width,
            self.Colors.Ruler
        )
        painter.drawLine(
            self.ruler_width, self.ruler_width,
            self.ruler_width, bottom_right.y()
        )
        painter.drawLine(
            self.ruler_width, self.ruler_width,
            bottom_right.x(), self.ruler_width
        )

        scene_top_left = self.mapToScene(top_left)
        scene_bottom_right = self.mapToScene(bottom_right)
        scale = self.transform().m11()
        visible_range = min(
            scene_bottom_right.x() - scene_top_left.x(),
            scene_bottom_right.y() - scene_top_left.y()
        )
        big_step, small_step = self.grid_step_rate.get_steps(visible_range)

        if big_step > 10**8:
            return

        scene_range_start = (
            (scene_top_left / big_step).toPoint() + QPoint(-1, -1)
        ) * big_step
        scene_range_end = (
            (scene_bottom_right / big_step).toPoint() + QPoint(1, 1)
        ) * big_step

        range_start = self.mapFromScene(scene_range_start)
        range_end = self.mapFromScene(scene_range_end)
        big_step, small_step = big_step * scale, small_step * scale

        painter.drawLines(
            [
                QLineF(x, self.ruler_width * 0.75, x, self.ruler_width)
                for x in frange(range_start.x(), range_end.x(), small_step)
            ]+[
                QLineF(self.ruler_width * 0.75, y, self.ruler_width, y)
                for y in frange(range_start.y(), range_end.y(), small_step)
            ]+[
                QLineF(x, self.ruler_width / 4, x, self.ruler_width)
                for x in frange(range_start.x(), range_end.x(), big_step)
            ]+[
                QLineF(self.ruler_width / 4, y, self.ruler_width, y)
                for y in frange(range_start.y(), range_end.y(), big_step)
            ]
        )

        if self.cursor_pos:
            cursor_pen = QPen(self.Colors.Cursor)
            cursor_pen.setWidth(2)
            painter.setPen(cursor_pen)
            painter.drawLines([
                QLineF(self.ruler_width / 2, self.cursor_pos.y(),
                       self.ruler_width, self.cursor_pos.y()),
                QLineF(self.cursor_pos.x(), self.ruler_width / 2,
                       self.cursor_pos.x(), self.ruler_width)
            ])
            painter.setPen(pen)

        painter.setFont(QFont("Arial", self.ruler_width // 2))
        for x, scene_x in zip(
            frange(range_start.x(), range_end.x(), big_step),
            range(
                scene_range_start.x(),
                scene_range_end.x(),
                int(big_step / scale)
            )
        ):
            painter.drawText(
                QPointF(x + 2, self.ruler_width * 0.65),
                str(scene_x)
            )

        painter.rotate(-90)
        for y, scene_y in zip(
            frange(range_start.y(), range_end.y(), big_step),
            range(
                scene_range_start.y(),
                scene_range_end.y(),
                int(big_step / scale)
            )
        ):
            painter.drawText(
                QPointF(-y + 2, self.ruler_width * 0.65),
                str(scene_y)
            )
        painter.rotate(90)

        painter.eraseRect(
            top_left.x(), top_left.y(),
            self.ruler_width + 1, self.ruler_width + 1
        )

        painter.drawText(
            QPointF(self.ruler_width * 0.2, self.ruler_width * 0.7),
            "px"
        )

    def drawBackground(self, painter, rect) -> None:
        super().drawBackground(painter, rect)
        painter.fillRect(rect, self.Colors.Background)
        scene_rect = self.sceneRect()
        painter.fillRect(scene_rect, self.Colors.SceneRect)

        if self.draw_grid:
            self._draw_grid(painter)

    def drawForeground(self, painter, rect) -> None:
        super().drawForeground(painter, rect)
        if self.draw_ruler:
            self._draw_ruler()

    def setDragButton(self, button: Qt.MouseButton):
        self.drag_button = button

    def setActiveGraphicTool(self, tool: VGEGraphicsTool):
        if self.active_graphic_tool:
            self.active_graphic_tool.setParentView(None)
        self.active_graphic_tool = tool
        tool.setParentView(self)

    def mousePressEvent(self, event: QMouseEvent):
        if (
                self.dragMode() == self.DragMode.RubberBandDrag
                and event.button() == self.drag_button
        ):
            self._drag_start_pos = event.pos()

        self.active_graphic_tool.mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & self.drag_button:
            delta = event.pos() - self._drag_start_pos
            horizontal_scrollbar = self.horizontalScrollBar()
            vertical_scrollbar = self.verticalScrollBar()
            horizontal_scrollbar.setValue(
                horizontal_scrollbar.value() - delta.x()
            )
            vertical_scrollbar.setValue(
                vertical_scrollbar.value() - delta.y()
            )
            self._drag_start_pos = event.pos()
        else:
            super().mouseMoveEvent(event)

        if self.cursor_pos:
            if self.draw_ruler or self.draw_grid:
                self.cursor_pos = event.pos()
                last_steps = self.GridStepRate.get_last_steps()
                if self.draw_grid and self.fit_cursor_into_grid and last_steps:
                    scene_cords = self.mapToScene(event.pos())
                    _, small_step = last_steps
                    self.cursor_pos = self.mapFromScene(
                        (
                                (scene_cords.x() + small_step/2)
                                // small_step * small_step
                        ),
                        (
                                (scene_cords.y() + small_step/2)
                                // small_step * small_step
                        )
                    )
                self.viewport().update()
        else:
            self.cursor_pos = event.pos()

        self.active_graphic_tool.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.active_graphic_tool.mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(1.1, 1.1)
        else:
            self.scale(0.9, 0.9)
        event.accept()
