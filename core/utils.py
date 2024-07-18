from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from core.settings import (
    config,
    LOCALIZATION_DIR,
    DefaultSettings
)


def set_language(translator: QTranslator, language: str):
    localization_path = LOCALIZATION_DIR / f"{language}.qm"
    translator.load(str(localization_path))
    QApplication.instance().installTranslator(translator)


def load_language(translator: QTranslator):
    language = config.value("language", DefaultSettings.LANGUAGE)
    set_language(translator, language)


def frange(start: float, stop: float, step: float = 0.1):
    while start < stop:
        yield start
        start += step
