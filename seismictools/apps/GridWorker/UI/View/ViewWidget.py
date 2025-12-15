from PyQt5 import QtWidgets, QtCore
from ..Settings.SettingsWidget import Ui_GridWorkerWindow
from seismictools.apps.GridWorker.Calculate.Reader.GrdReader import read_grd_file
import numpy as np
import pyqtgraph as pg

pg.setConfigOption('imageAxisOrder', 'row-major')
class ViewWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GridWorkerWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_load.clicked.connect(self.load_file)
        self.ui.pushButton_clear.clicked.connect(self.clear_file)

        # Заменяем QGraphicsView на PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setAspectLocked(False)
        self.plot_widget.invertY(True)

        # Создаём ImageItem
        self.image_item = pg.ImageItem()
        self.plot_widget.addItem(self.image_item)

        # Заменяем виджет в layout
        self.ui.horizontalLayout.replaceWidget(self.ui.label_map, self.plot_widget)
        self.ui.label_map.deleteLater()
        self.ui.label_map = self.plot_widget

        self.grid_data = None

    def load_file(self):
        """
            Функция загрузки пути до файла через кнопку "Загрузить"
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
                print(f"Файл загружен. Размер массива: {self.grid_data.shape}")
                self.display_heatmap()
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}"
                )
                self.grid_data = None
        else:
            print("Файл не выбран")

    def display_heatmap(self):
        """
            Отображает grid_data в виде карты
        """
        if self.grid_data is None:
            return
        self.image_item.setImage(self.grid_data)
        self.image_item.setLookupTable(pg.colormap.get('viridis').getLookupTable())
        self.plot_widget.autoRange()

    def clear_file(self):
        """
            Функция очистки строки, отображающей путь до файла через кнопку "Очистить"
        """
        self.ui.lineEdit_filePath.clear()
        self.grid_data = None

        if hasattr(self, 'image_item') and self.image_item is not None:
            self.image_item.clear()

        print("Данные и поле для карты очищены")


