from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from core.settings import (
    config,
    LOCALIZATION_DIR,
    DEFAULT_LANGUAGE
)


def set_language(translator: QTranslator, language: str):
    localization_path = LOCALIZATION_DIR / f"{language}.qm"
    translator.load(str(localization_path))
    print(localization_path)
    QApplication.instance().installTranslator(translator)


def load_language(translator: QTranslator):
    language = config.value("language", DEFAULT_LANGUAGE)
    set_language(translator, language)
