from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QActionGroup
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QLabel,
    QFrame,
    QVBoxLayout,
    QStatusBar,
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QGraphicsScene,
    QToolButton,
    QButtonGroup,
    QMenu,
)

from core import generics
from core.generics import VGEGraphicsView
from core.graphics.graphics_tools import SelectionTool, GeometryTool
from core.settings import config, DefaultSettings, Assets


class RootWindow(generics.WindowUI):
    def __init__(self, window: QMainWindow):
        super().__init__(window)

        # MenuBar
        self.menubar = self.window.menuBar()
        self.menubar__file_menu = self.menubar.addMenu("File")

        self.menubar__file_menu__open_action = QAction("Open", self.window)
        self.menubar__file_menu.addAction(self.menubar__file_menu__open_action)
        self.menubar__file_menu__save_action = QAction("Save", self.window)
        self.menubar__file_menu.addAction(self.menubar__file_menu__save_action)
        self.menubar__file_menu__export_action = QAction("Export", self.window)
        self.menubar__file_menu.addAction(self.menubar__file_menu__export_action)

        self.menubar__view_menu = self.menubar.addMenu("View")

        self.menubar__view_menu__grid_action = QAction("Grid", self.window)
        self.menubar__view_menu.addAction(self.menubar__view_menu__grid_action)
        self.menubar__view_menu__grid_action.setCheckable(True)
        self.menubar__view_menu__grid_action.setChecked(
            config.value("draw_grid", DefaultSettings.DRAW_GRID)
        )
        self.menubar__view_menu__ruler_action = QAction("Ruler", self.window)
        self.menubar__view_menu.addAction(self.menubar__view_menu__ruler_action)
        self.menubar__view_menu__ruler_action.setCheckable(True)
        self.menubar__view_menu__ruler_action.setChecked(
            config.value("draw_ruler", DefaultSettings.DRAW_RULER)
        )

        # Instruments Panel
        self.toolbar = QToolBar()
        self.window.addToolBar(self.toolbar)

        self.toolbar__container = QWidget()
        self.toolbar__layout_v = QVBoxLayout()

        self.toolbar__selection_tool_button = QToolButton()
        self.toolbar__selection_tool_button_action = QAction(
            QIcon(Assets.SELECTION_TOOl_ICON), "Selection tool", self.window
        )
        self.toolbar__selection_tool_button_action.setCheckable(True)

        self.toolbar__selection_tool_button.setDefaultAction(
            self.toolbar__selection_tool_button_action
        )

        self.toolbar__geometry_tool_button = QToolButton()
        self.toolbar__geometry_tool_button_action = QAction(
            QIcon(Assets.GEOMETRY_TOOL_LINE_ICON), "Geometry tool", self.window
        )
        self.toolbar__geometry_tool_button_action.setCheckable(True)

        self.toolbar__geometry_tool_button.setDefaultAction(
            self.toolbar__geometry_tool_button_action
        )

        self.toolbar__geometry_tool_menu = QMenu()

        self.toolbar__geometry_tool_menu__line_action = QAction(
            QIcon(Assets.GEOMETRY_TOOL_LINE_ICON), "Line", self.window
        )
        self.toolbar__geometry_tool_menu__line_action.setCheckable(True)
        self.toolbar__geometry_tool_menu__line_action.setChecked(True)
        self.toolbar__geometry_tool_menu__rectangle_action = QAction(
            QIcon(Assets.GEOMETRY_TOOL_RECTANGLE_ICON), "Rectangle", self.window
        )
        self.toolbar__geometry_tool_menu__rectangle_action.setCheckable(True)
        self.toolbar__geometry_tool_menu__polygon_action = QAction(
            QIcon(Assets.GEOMETRY_TOOL_POLYGON_ICON), "Polygon", self.window
        )
        self.toolbar__geometry_tool_menu__polygon_action.setCheckable(True)
        self.toolbar__geometry_tool_menu__ellipse_action = QAction(
            QIcon(Assets.GEOMETRY_TOOL_ELLIPSE_ICON), "Ellipse", self.window
        )
        self.toolbar__geometry_tool_menu__ellipse_action.setCheckable(True)

        self.toolbar__geometry_tool_menu.addActions([
            self.toolbar__geometry_tool_menu__line_action,
            self.toolbar__geometry_tool_menu__rectangle_action,
            self.toolbar__geometry_tool_menu__polygon_action,
            self.toolbar__geometry_tool_menu__ellipse_action,
        ])

        self.toolbar__geometry_tool__action_group = QActionGroup(self.window)
        self.toolbar__geometry_tool__action_group.setExclusive(True)
        self.toolbar__geometry_tool__action_group.addAction(
            self.toolbar__geometry_tool_menu__line_action
        )
        self.toolbar__geometry_tool__action_group.addAction(
            self.toolbar__geometry_tool_menu__rectangle_action
        )
        self.toolbar__geometry_tool__action_group.addAction(
            self.toolbar__geometry_tool_menu__polygon_action
        )
        self.toolbar__geometry_tool__action_group.addAction(
            self.toolbar__geometry_tool_menu__ellipse_action
        )

        self.toolbar__geometry_tool_button.setMenu(
            self.toolbar__geometry_tool_menu
        )
        self.toolbar__geometry_tool_button.setPopupMode(
            QToolButton.MenuButtonPopup
        )

        self.toolbar__button_group = QButtonGroup(self.window)
        self.toolbar__button_group.setExclusive(True)
        self.toolbar__button_group.addButton(self.toolbar__selection_tool_button)
        self.toolbar__button_group.addButton(self.toolbar__geometry_tool_button)

        self.toolbar__tool_instances = {
            "Selection tool": SelectionTool(),
            "Geometry tool": GeometryTool(),
        }

        self.toolbar__layout_v.addWidget(self.toolbar__selection_tool_button)
        self.toolbar__layout_v.addWidget(self.toolbar__geometry_tool_button)
        self.toolbar__container.setLayout(self.toolbar__layout_v)
        self.toolbar.addWidget(self.toolbar__container)

        # Work area
        self.work_area = VGEGraphicsView(self.window)
        self.graphics_scene = QGraphicsScene(self.work_area)
        self.work_area.setScene(self.graphics_scene)
        self.work_area.setDragMode(VGEGraphicsView.RubberBandDrag)

        self.graphics_scene.setSceneRect(0, 0, 1000, 1000)

        # Properties Panel
        self.properties_panel = QFrame()
        self.properties_layout = QVBoxLayout(self.properties_panel)
        self.properties_label = QLabel("Properties Panel")
        self.properties_label.setAlignment(Qt.AlignCenter)
        self.properties_layout.addWidget(self.properties_label)

        # StatusBar
        self.statusbar = QStatusBar()

        # Compounding widgets
        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.work_area)
        self.main_layout.addWidget(self.properties_panel)

        self.window.setStatusBar(self.statusbar)

        self.setup()

    def setup(self):
        self.setup_styles()
        self.setup_sizes()
        self.setup_texts()
        self.setup_images()
        self.setup_tooltips()

    def setup_styles(self):
        self.toolbar.setObjectName("toolbar")
        self.toolbar__selection_tool_button.setObjectName("toolbar-item")
        self.toolbar__geometry_tool_button.setObjectName("toolbar-item")
        self.work_area.setObjectName("work-area")
        self.properties_panel.setObjectName("properties-panel")
        self.statusbar.setObjectName("statusbar")

        self.window.setStyleSheet("""
            #toolbar {
                background-color: lightgray;
                border-right: 0.5px solid gray
            }
            
            #toolbar-item {
                padding: 5px;
                background-color: #f0f0f0;
                border: 1px solid #bbb;
            }
            
            #toolbar-item:hover {
                background-color: #eaeaea;
            }
            
            #toolbar-item:checked {
                background-color: #e0e0e0;
                border-color: #888;
            }

            #toolbar-item::menu-button {
                height: 12%;
                width: 12%;
                subcontrol-position: bottom right;
                border: none;
            }

            #toolbar-item::menu-arrow {
                image: url("./assets/dropdown.png");
            }

            #work-area {
                border: none;
            }

            #properties-panel {
                background-color: lightgray;
                border-left: 0.5px solid gray
            }

            #statusbar {
                border-top: 0.5px solid gray;
            }
        """)

        self.toolbar__selection_tool_button.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonIconOnly
        )
        self.toolbar__layout_v.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.work_area.setAlignment(Qt.AlignCenter)

        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def setup_sizes(self):
        self.window.setGeometry(100, 100, 800, 600)

        self.toolbar.setFixedWidth(50)
        self.toolbar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.properties_panel.setFixedWidth(250)

    def setup_texts(self):
        self.window.setWindowTitle("Simple VGE ( by Quiet_Klirik )")

        # MenuBar
        self.menubar__file_menu.setTitle(self.tr("File"))

        self.menubar__file_menu__open_action.setText(self.tr("Open"))
        self.menubar__file_menu__save_action.setText(self.tr("Save"))
        self.menubar__file_menu__export_action.setText(self.tr("Export"))

        self.menubar__view_menu.setTitle(self.tr("View"))

        self.menubar__view_menu__grid_action.setText(self.tr("Grid"))
        self.menubar__view_menu__ruler_action.setText(self.tr("Ruler"))

    def setup_images(self):
        pass

    def setup_tooltips(self):
        pass
