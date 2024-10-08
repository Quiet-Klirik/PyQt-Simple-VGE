import pathlib

from PySide6.QtCore import QSettings

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
config = QSettings("config.ini", QSettings.Format.IniFormat)


LOCALIZATION_DIR = BASE_DIR / "localizations"


class DefaultSettings:
    LANGUAGE = "en_US"

    DRAW_GRID = True
    GRID_STEP_RATE = "Decimal"
    FIT_CURSOR_INTO_GRID = True

    DRAW_RULER = True


ASSETS_DIR = BASE_DIR / "assets"


class Assets:
    SELECTION_TOOl_ICON = str(ASSETS_DIR / "cursor.png")
    GEOMETRY_TOOL_LINE_ICON = str(ASSETS_DIR / "line.png")
    GEOMETRY_TOOL_RECTANGLE_ICON = str(ASSETS_DIR / "rectangle.png")
    GEOMETRY_TOOL_POLYGON_ICON = str(ASSETS_DIR / "polygon.png")
    GEOMETRY_TOOL_ELLIPSE_ICON = str(ASSETS_DIR / "ellipse.png")

