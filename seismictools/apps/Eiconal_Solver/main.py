import sys
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from seismictools.apps.Eiconal_Solver.UI.main_window_ui import Ui_MainWindow


class EikonalSolver(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.UploadButton.clicked.connect(self.select_npy_file)

    def select_npy_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл модели",
            "",  # текущая папка
            "NumPy файлы (*.npy)"
        )

        if file_path:
            self.ui.UploadedFileWidget.clear()
            self.ui.UploadedFileWidget.addItem(file_path)

            self.ui.StatusWidget.addItem(f"Загружен: {file_path}")
            return(file_path)

    def clear_npy_file(self):
        self.ui.UploadedFileWidget.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = EikonalSolver()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()