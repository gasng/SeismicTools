import sys
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from seismictools.apps.FK_analysis.UI.SettingsWidget_ui import  Ui_MainWindow

class FK_filter(QtWidgets.QMainWindow):
    def __init__(self):
        super(FK_filter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.SeismicDataBtn.clicked.connect(self.get_filepath)

    def get_filepath(self):

        lw_items = [self.ui.SeismicDataLW.item(i).text() for i in range(self.ui.SeismicDataLW.count())]
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Дай файл",
                                                   "")
        lw_items.append(file_path)
        lw_items = list(set(lw_items))
        self.ui.SeismicDataLW.clear()
        for item in lw_items:
            self.ui.SeismicDataLW.addItem(item)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FK_filter()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()