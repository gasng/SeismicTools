import sys
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from seismictools.apps.FK_analysis.UI.SettingsWidget_ui import  Ui_FK_Filtration

class FK_filter(QtWidgets.QMainWindow):
    def __init__(self):
        super(FK_filter, self).__init__()
        self.ui = Ui_FK_Filtration()
        self.ui.setupUi(self)
        self.apply_style()

        self.ui.SeismicDataBtn.clicked.connect(self.get_filepath)
        self.ui.DeleteBtn.clicked.connect(self.delete_selected_file)

    def get_filepath(self):

        lw_items = [self.ui.SeismicDataLW.item(i).text() for i in range(self.ui.SeismicDataLW.count())]
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Дай файл",
                                                   "",
                                                   "*.segy *.sgy")
        lw_items.append(file_path)
        lw_items = list(set(lw_items))
        self.ui.SeismicDataLW.clear()
        for item in lw_items:
            self.ui.SeismicDataLW.addItem(item)

    def delete_selected_file(self):
        current_row = self.ui.SeismicDataLW.currentRow()
        if current_row >= 0:
            self.ui.SeismicDataLW.takeItem(current_row)
        else:
            self.ui.ErrorLW.addItem("⚠️ Сначала выберите файл для удаления.")
            self.ui.ErrorLW.scrollToBottom()

    def apply_style(self):
        style = """
            QMainWindow {
                background-color: #0f172a;
            }
            QGroupBox {
                color: #e2e8f0;
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                font-size: 10pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: #60a5fa;
            }
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid #475569;
                padding: 7px 14px;
                border-radius: 6px;
                font-size: 9pt;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #334155;
                border: 1px solid #60a5fa;
            }
            QPushButton:pressed {
                background-color: #0ea5e9;
                color: #0f172a;
                border: 1px solid #0ea5e9;
            }
            QLabel {
                color: #94a3b8;
            }
            QListWidget {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #1d4ed8;
                color: white;
                border-left: 3px solid #60a5fa;
            }
            QStatusBar {
                color: #94a3b8;
                background-color: #1e293b;
                border-top: 1px solid #334155;
            }
        """
        self.setStyleSheet(style)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FK_filter()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()