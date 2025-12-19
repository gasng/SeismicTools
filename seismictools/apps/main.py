import sys
import pyqtgraph as pg
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QStatusBar
from PySide6.QtCore import Qt, QObject, Signal, Slot, QThreadPool

from seismictools.apps.UI.UI_Designer.Designer_Apps_ui import Ui_MainWindow
from seismictools.apps.Controller.WorkerReader import WorkerReader
from seismictools.apps.Controller.WorkerFilter import WorkerFilter
from seismictools.apps.UI.ViewWidgets.PlotWidgets import SeismicPlotWidget

class BandPassApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(BandPassApp, self).__init__()
        self.threadpool = QThreadPool()
        self.setupUi(self)

        self.ui = Ui_MainWindow()

        self.lineEdit.setReadOnly(True)

        self.pushButton_load.clicked.connect(self.load_file)
        self.pushButton_clear.clicked.connect(self.clear_all)
        self.pushButton_apply.clicked.connect(self.apply_filter)
        self.pushButton_reset.clicked.connect(self.reset_plot)

        self.original_data = None

        self.statusBar: QStatusBar = self.statusBar

    def connect_buttons(self):
        """Подключение кнопок"""
        self.pushButton_load.clicked.connect(self.load_file)
        self.pushButton_clear.clicked.connect(self.clear_all)
        self.pushButton_apply.clicked.connect(self.apply_filter)
        self.pushButton_reset.clicked.connect(self.reset_plot)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите SEGY файл", "", "SEGY Files (*.sgy *.segy)"
        )
        if not file_path:
            return

        self.statusBar.showMessage("Загрузка файла...", 0)
        worker = WorkerReader(file_path)
        worker.signals.result.connect(self.on_load_success)
        worker.signals.error.connect(self.on_load_error)
        worker.signals.message.connect(self.on_load_message)
        QThreadPool.globalInstance().start(worker)

    def on_load_message(self, msg):
        self.statusBar.showMessage(msg, 4000)

    def on_load_success(self, data, file_path):
        self.original_data = data
        self.lineEdit.setText(file_path.split("/")[-1])
        self.update_plot()

    def on_load_error(self, error_msg):
        self.statusBar.showMessage(f"Ошибка: {error_msg}", 6000)
        QMessageBox.critical(self, "Ошибка", error_msg)

    def apply_filter(self):
        if self.original_data is None:
            self.statusBar.showMessage("Сначала загрузите файл!", 3000)
            return

        # Получаем параметры из UI
        filter_type = self.comboBox.currentText()
        order = self.spinBox.value()
        freq_min = int(self.lineEdit_2.text()) if self.lineEdit_2.text() else 10
        freq_max = int(self.lineEdit_3.text()) if self.lineEdit_3.text() else 50

        if filter_type == "bandpass" and freq_min >= freq_max:
            self.statusBar.showMessage("Ошибка: min < max", 5000)
            return

        worker = WorkerFilter(
            data=self.original_data,
            low_freq=freq_min,
            high_freq=freq_max,
            fs=1000,
            order=order
        )
        worker.signals.result.connect(self.on_filter_success)
        worker.signals.error.connect(self.on_filter_error)
        worker.signals.message.connect(self.on_filter_message)
        QThreadPool.globalInstance().start(worker)

    def on_filter_message(self, msg):
        self.statusBar.showMessage(msg, 4000)

    def on_filter_success(self, filtered_data):
        self.filtered_data = filtered_data
        self.update_plot()

    def on_filter_error(self, error_msg):
        self.statusBar.showMessage(f"Ошибка: {error_msg}", 6000)
        QMessageBox.critical(self, "Ошибка", error_msg)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def update_plot(self):
        from seismictools.apps.UI.ViewWidgets.PlotWidgets import SeismicPlotWidget
        self.clear_layout(self.plotLayout)
        plot_widget = SeismicPlotWidget(self.original_data, self.filtered_data)
        self.plotLayout.addWidget(plot_widget)

    def clear_all(self):
        self.original_data = None
        self.filtered_data = None
        self.lineEdit.setText("")
        self.update_plot()

    def reset_plot(self):
        self.filtered_data = None
        self.update_plot()
        self.statusBar.showMessage("Фильтр сброшен", 3000)

def main():
    app = QApplication(sys.argv)
    window = BandPassApp()
    window.show()
    return app.exec()

if __name__ == "__main__":
    main()