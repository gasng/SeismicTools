from PyQt5 import QtWidgets, QtCore
from ..Settings.SettingsWidget import Ui_GridWorkerWindow
from seismictools.apps.GridWorker.Calculate.Reader.GrdReader import read_grd_file
from seismictools.apps.GridWorker.Calculate.Data.PoligonData import PointManager
from seismictools.apps.GridWorker.Calculate.Data.GridData import MapRenderer
import numpy as np
import pyqtgraph as pg

pg.setConfigOption('imageAxisOrder', 'row-major')
class ViewWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GridWorkerWindow()
        self.ui.setupUi(self)

        # Заменяем QGraphicsView на PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')

        # Заменяем виджет в layout
        self.ui.horizontalLayout.replaceWidget(self.ui.label_map, self.plot_widget)
        self.ui.label_map.deleteLater()
        self.ui.label_map = self.plot_widget

        self.ui.pushButton_load.clicked.connect(self.load_file)
        self.ui.pushButton_clear.clicked.connect(self.clear_file)

        # Инициализируем менеджер точек
        self.map_renderer = MapRenderer(self.plot_widget)
        self.point_manager = PointManager(self.plot_widget)

        # Подключение строки состояния для постоянных сообщений
        self.status_label = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.status_label)
        self.point_manager = PointManager(self.plot_widget)
        self.point_manager.status_message.connect(self.update_status)

        self.grid_data = None

    def update_status(self, message: str):
        """
            Функция, принимающая информацию о сообщениях, передаваемых в StatusBar
        """
        self.status_label.setText(message)

    def load_file(self):
        """
            Функция загрузки пути до файла через кнопку "Загрузить" и отрисовки карты
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите файл карты",
            "",
            "GRD Files (*.grd);;All Files (*)"
        )
        if file_path:
            self.ui.lineEdit_filePath.setText(file_path)
            try:
                self.grid_data = read_grd_file(file_path)
                self.map_renderer.display_heatmap(self.grid_data)
                self.status_label.setText(f"Файл загружен. Размер массива: {self.grid_data.shape}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self.status_label.setText(f"Ошибка. Не удалось загрузить файл:\n{str(e)}")
                )
                self.grid_data = None
        else:
            self.status_label.setText("Файл не выбран")

    def clear_file(self):
        """
            Функция очистки строки, отображающей путь до файла, удаление отрисованной карты и выделенных полигонов, через кнопку "Очистить"
        """
        self.ui.lineEdit_filePath.clear()
        self.grid_data = None
        self.map_renderer.clear()  # Очищаем карту
        self.point_manager.clear_points()  # Очищаем точки
        self.status_label.setText("Файл удален, карта очищена")
