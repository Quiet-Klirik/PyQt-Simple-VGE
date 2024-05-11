import pathlib

from PySide6.QtCore import QSettings

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
config = QSettings("config.ini", QSettings.Format.IniFormat)


LOCALIZATION_DIR = BASE_DIR / "localizations"
DEFAULT_LANGUAGE = "en_US"
