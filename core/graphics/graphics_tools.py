from PySide6.QtCore import Qt
from PySide6.QtGui import QPen

from core.generics import VGEGraphicsTool
from core.graphics.graphics_items import (
    VGEGraphicsLineItem,
    VGEGraphicsRectItem,
    VGEGraphicsPolygonItem,
    VGEGraphicsEllipseItem
)


class SelectionTool(VGEGraphicsTool):
    pass


class GeometryTool(VGEGraphicsTool):
    graphics_items_classes = {
        "line": VGEGraphicsLineItem,
        "rectangle": VGEGraphicsRectItem,
        "polygon": VGEGraphicsPolygonItem,
        "ellipse": VGEGraphicsEllipseItem,
    }

    def __init__(self):
        super().__init__()

        self.geometry_type = VGEGraphicsLineItem

        self.current_instance = None
        self.start_point = None

    def set_geometry_type(self, type_: str):
        """
        type_ in ["line", "rectangle", "polygon", "ellipse"]
        """
        self.geometry_type = self.graphics_items_classes.get(
            type_.lower(), VGEGraphicsLineItem
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = self.view.mapToScene(self.view.cursor_pos)
            if not self.current_instance:
                self.current_instance = self.geometry_type(
                    point, self.view.scene()
                )
                pen = QPen(Qt.black, 2)
                self.current_instance.setPen(pen)
            else:
                self.current_instance.add_point(point)

    def mouseMoveEvent(self, event):
        if self.current_instance:
            end_point = self.view.mapToScene(self.view.cursor_pos)
            self.current_instance.update_last_point(end_point)

    def mouseReleaseEvent(self, event):
        if self.current_instance:
            self.current_instance.mouse_release_action(event, self)
