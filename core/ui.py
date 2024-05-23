from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QLabel,
    QFrame,
    QVBoxLayout,
    QStatusBar,
    QWidget,
    QHBoxLayout,
    QSizePolicy, QGraphicsScene,
)

from core import generics
from core.generics import VGEGraphicsView


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
        self.menubar__view_menu__ruler_action = QAction("Ruler", self.window)
        self.menubar__view_menu.addAction(self.menubar__view_menu__ruler_action)
        self.menubar__view_menu__ruler_action.setCheckable(True)

        # Instruments Panel
        self.toolbar = QToolBar()
        self.window.addToolBar(self.toolbar)

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
        self.work_area.setObjectName("work-area")
        self.properties_panel.setObjectName("properties_panel")
        self.statusbar.setObjectName("statusbar")

        self.window.setStyleSheet("""
            #toolbar {
                background-color: lightgray;
                border-right: 0.5px solid gray
            }

            #work-area {
                border: none;
            }

            #properties_panel {
                background-color: lightgray;
                border-left: 0.5px solid gray
            }

            #statusbar {
                border-top: 0.5px solid gray;
            }
        """)

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
