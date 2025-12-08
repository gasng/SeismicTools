import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice

from seismictools.apps.GridWorker.UI.Settings.SettingsWidget_ui import GridWorker

def main():
    app = QApplication(sys.argv)
    window = GridWorker()
    window.show()
    sys.exit(app.exec())
