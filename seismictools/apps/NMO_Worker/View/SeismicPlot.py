import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class GatherPlotWidget(QWidget):
    def __init__(self, data, dt=0.002):
        super().__init__()
        self.data = data
        self.dt = dt
        self.plot_widget = None
        self.image_item = None
        self.scatter_plot_item = None
        self.scatter_data_x = []
        self.scatter_data_y = []
        self.__plot_data()
        #self.__apply_2d_agc()

    #def __apply_2d_agc(self, time_window=0.1, trace_window=5, dt=0.004):

        #nt, nx = self.data.shape
        #time_half = int(time_window / dt / 2)
        #trace_half = int(trace_window / 2)

        #data_agc = np.zeros_like(self.data)

        #for i in range(nt):
            #for j in range(nx):
                # Окно по времени
                #t1 = max(0, i - time_half)
                #t2 = min(nt, i + time_half + 1)
                # Окно по трассам
                #x1 = max(0, j - trace_half)
                #x2 = min(nx, j + trace_half + 1)

                # RMS в прямоугольном окне
                #window_data = self.data[t1:t2, x1:x2]
                #rms = np.sqrt(np.mean(window_data ** 2) + 1e-12)

                # Нормализация
                #data_agc[i, j] = self.data[i, j] / rms

        #self.data = data_agc
        #return self.data

    def __plot_data(self):
        if self.plot_widget:
            self.layout().removeWidget(self.plot_widget)
            self.plot_widget.deleteLater()

        self.plot_widget = pg.PlotWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        nt, nx = self.data.shape
        t_max = nt * self.dt  # или 0.004 * nt, если dt не передано

        self.image_item = pg.ImageItem(image=self.data.T)
        self.image_item.setRect(QtCore.QRectF(0, 0, nx, t_max))

        self.plot_widget.addItem(self.image_item)

        # Настройка осей
        x_axis = self.plot_widget.getAxis('bottom')
        y_axis = self.plot_widget.getAxis('left')

        x_axis.setLabel('Трасса')
        y_axis.setLabel('Время, с')

        self.plot_widget.getViewBox().invertY(True)

        # Устанавливаем диапазон
        self.plot_widget.setXRange(0, nx)
        self.plot_widget.setYRange(t_max, 0)  # от max к min (вверх-вниз)


class SpectrumPlotWidget(QWidget):
    def __init__(self, data, dt=0.002):
        super().__init__()
        self.data = np.array(data)  # (nt, nv)
        self.dt = dt
        self.velocities = np.arange(100, 2500, 10)  # массив скоростей, если есть
        self.plot_widget = None
        self.image_item = None
        self.scatter_plot_item = None
        self.scatter_data_x = []
        self.scatter_data_y = []
        self.__plot_data()

    def __plot_data(self):
        if self.plot_widget:
            self.layout().removeWidget(self.plot_widget)
            self.plot_widget.deleteLater()

        self.plot_widget = pg.PlotWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        nt, nv = self.data.shape
        t_max = nt * self.dt
        vel_min, vel_max = self.velocities[0], self.velocities[-1]

        # Создаём изображение и задаём его геометрию в физических координатах
        minl, maxl = np.percentile(self.data, [90,100])
        self.image_item = pg.ImageItem(image=self.data.T, levels=(minl, maxl))
        self.image_item.setRect(QtCore.QRectF(vel_min, 0, vel_max - vel_min, t_max))

        pos = [0.0, 0.5, 1.0]
        color = [
            (0, 0, 139),
            (255, 255, 255),
            (128, 0, 0)
        ]
        cmap = pg.ColorMap(pos, color)
        self.image_item.setLookupTable(cmap.getLookupTable())

        self.plot_widget.addItem(self.image_item)

        # Настраиваем оси
        self.plot_widget.setLabel('bottom', 'Скорость, м/с')
        self.plot_widget.setLabel('left', 'Время, с')
        self.plot_widget.setLimits(xMin=vel_min, xMax=vel_max, yMin=0, yMax=t_max)

    def add_pick(self, x, y):
        """
        Добавляет точку (x, y) на график.
        :param x: скорость (м/с)
        :param y: время (с)
        """
        self.scatter_data_x.append(x)
        self.scatter_data_y.append(y)

        if self.scatter_plot_item is None:
            # Создаём ScatterPlotItem, если ещё не создан
            self.scatter_plot_item = pg.ScatterPlotItem(
                symbol='o',
                size=8,
                pen=pg.mkPen(color='yellow', width=2),
                brush=pg.mkBrush(color=(255, 0, 0, 150))  # полупрозрачный красный
            )
            self.plot_widget.addItem(self.scatter_plot_item)

        # Обновляем данные
        self.scatter_plot_item.setData(x=self.scatter_data_x, y=self.scatter_data_y)

