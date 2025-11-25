import sys
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from seismictools.apps.example.UI.ExampleWidget_ui import  Ui_ExampleWidget


class Example(QtWidgets.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.ui = Ui_ExampleWidget()
        self.ui.setupUi(self)

        self.ui.SeismicDataBtn.clicked.connect(self.get_filepath)
        self.ui.RunBtn.clicked.connect(self.load_data)

    def get_filepath(self):

        lw_items = [self.ui.SeismicDataLW.item(i).text() for i in range(self.ui.SeismicDataLW.count())]
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Дай файл",
                                                   "",
                                                   "*.npy")
        lw_items.append(file_path)
        lw_items = list(set(lw_items))
        self.ui.SeismicDataLW.clear()
        for item in lw_items:
            self.ui.SeismicDataLW.addItem(item)

    def load_data(self):
        filepath = self.ui.SeismicDataLW.currentItem().text()
        data = np.load(filepath)
        print(data)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Example()
    window.show()

    return app.exec_()

if getattr(sys, 'frozen', False):
    main()