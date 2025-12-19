import sys
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog, QLayout, QLayoutItem, QWidget

from seismictools.apps.example.Controller.ExampleWorker import WorkerReader
from seismictools.apps.example.UI.ExampleWidget_ui import  Ui_ExampleWidget
from seismictools.apps.example.View.SeismicPlot import GatherPlotWidget


class Example(QtWidgets.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.threadpool = QtCore.QThreadPool()
        self.worker_reader = None

        self.ui = Ui_ExampleWidget()
        self.ui.setupUi(self)
        self.ui.SeismicDataBtn.clicked.connect(self.get_filepath)
        self.ui.RunBtn.clicked.connect(self.load_data)

    def get_filepath(self):

        lw_items = [self.ui.SeismicDataLW.item(i).text() for i in range(self.ui.SeismicDataLW.count())]
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Дай файл",
                                                   "",
                                                   "*.sgy")
        lw_items.append(file_path)
        lw_items = list(set(lw_items))
        self.ui.SeismicDataLW.clear()
        for item in lw_items:
            self.ui.SeismicDataLW.addItem(item)

    def load_data(self):
        filepath = self.ui.SeismicDataLW.currentItem().text()
        self.worker_reader = WorkerReader(filepath=filepath)
        self.worker_reader.signals.result.connect(self.show_data)
        self.worker_reader.signals.message.connect(self.print_message)
        self.worker_reader.signals.error.connect(self.print_error)
        self.threadpool.start(self.worker_reader)

    def print_message(self, string):
        self.ui.MessageLine.setText(string)

    def print_error(self, string):
        self.ui.MessageLine.setText(string)

    def clear_layout(self, layout: QLayout):
        """
        Clears all widgets and sub-layouts from a given QLayout.
        """
        if layout is None:
            return

        while layout.count():
            item: QLayoutItem = layout.takeAt(0)
            if item.widget() is not None:
                widget: QWidget = item.widget()
                widget.deleteLater()  # Schedule widget for deletion
            elif item.layout() is not None:
                self.clear_layout(item.layout())  # Recursively clear sub-layouts
            del item  # Delete the layout item itself

    def show_data(self, result):
        self.clear_layout(self.ui.plotLayout)
        my_plot_widget = GatherPlotWidget(result.data)
        self.ui.plotLayout.addWidget(my_plot_widget)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Example()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()