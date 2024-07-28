from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtWidgets import (
    QGraphicsLineItem,
    QGraphicsRectItem,
    QGraphicsPolygonItem,
    QGraphicsEllipseItem
)


class VGEGraphicsItemMixin:
    def __init__(self, start_point: QPoint | QPointF, scene):
        super().__init__()
        self.start_point = start_point
        self.points: list = [start_point, ]
        scene.addItem(self)

    def add_point(self, point: QPoint | QPointF):
        self.points.append(point)

    def update_last_point(self, point: QPoint | QPointF):
        pass

    def mouse_release_action(self, event, tool):
        if event.button() == Qt.LeftButton:
            tool.current_instance = None


class VGEGraphicsLineItem(VGEGraphicsItemMixin, QGraphicsLineItem):
    def __init__(self, start_point, scene):
        super().__init__(start_point, scene)
        self.setLine(
            start_point.x(), start_point.y(),
            start_point.x(), start_point.y() - 1
        )

    def update_last_point(self, point: QPoint | QPointF):
        start_point = self.start_point
        if point == start_point:
            point.setY(point.y() - 1)
        self.setLine(start_point.x(), start_point.y(), point.x(), point.y())


class VGEGraphicsRectItem(VGEGraphicsItemMixin, QGraphicsRectItem):
    def __init__(self, start_point, scene):
        super().__init__(start_point, scene)
        self.setRect(start_point.x(), start_point.y(), 1, 1)

    def update_last_point(self, point: QPoint | QPointF):
        start_point = self.start_point
        if point == start_point:
            point.setY(point.y() - 1)
        width = point.x() - start_point.x()
        height = point.y() - start_point.y()
        self.setRect(start_point.x(), start_point.y(), width, height)


class VGEGraphicsPolygonItem(VGEGraphicsItemMixin, QGraphicsPolygonItem):
    def __init__(self, start_point, scene):
        super().__init__(start_point, scene)
        self.setPolygon([
            *self.points,
            QPointF(start_point.x(), start_point.y() - 1),
        ])

    def update_last_point(self, point: QPoint | QPointF):
        if point in self.points:
            point.setY(point.y() - 1)
        self.setPolygon([
            *self.points,
            QPointF(point.x(), point.y()),
        ])

    def mouse_release_action(self, event, tool):
        if event.button() == Qt.MiddleButton:
            self.setPolygon(self.points)
            tool.current_instance = None


class VGEGraphicsEllipseItem(VGEGraphicsItemMixin, QGraphicsEllipseItem):
    def __init__(self, start_point, scene):
        super().__init__(start_point, scene)
        self.setRect(start_point.x(), start_point.y(), 1, 1)

    def update_last_point(self, point: QPoint | QPointF):
        start_point = self.start_point
        if point == start_point:
            point.setY(point.y() - 1)
        width = point.x() - start_point.x()
        height = point.y() - start_point.y()
        self.setRect(start_point.x(), start_point.y(), width, height)
