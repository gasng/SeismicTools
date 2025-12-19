import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject, Signal
import numpy as np
class PlotClickedSignal(QObject):
    clicked = Signal(float, float)  # x (время), y (амплитуда)
import colorcet
from seismictools.apps.First_Break_Picker.Calculate.Data.SeismicData import SegYData
from seismictools.apps.First_Break_Picker.Calculate.Data.SeismicPicks import Picks_data
from seismictools.apps.First_Break_Picker.Controller.WorkerReader import WorkerSignals




class ViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        self.SGYdata : SegYData = None
        self.image_item = None
        #self.histogram = None
        self.plot()
        self.signals = WorkerSignals()
        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClicked)

    def mouseClicked(self, event):
        if self.SGYdata is None or self.image_item is None:
            return
        try:
            position = event.scenePos()
            view_position = self.plot_widget.plotItem.vb.mapSceneToView(position)
            x, y = view_position.x(), view_position.y()
            trace_idx = int(round(x))
            time_idx = int(round(y))
            if (0 <= trace_idx < self.SGYdata.data.shape[1] and
                    0 <= time_idx < self.SGYdata.data.shape[0]):

                # Визуальный маркер
                if hasattr(self, 'pick_marker'):
                    self.plot_widget.removeItem(self.pick_marker)
                self.pick_marker = pg.ScatterPlotItem(
                    x=[trace_idx], y=[time_idx], size=5,
                    pen=pg.mkPen('y', width=2), brush=None
                )
                self.plot_widget.addItem(self.pick_marker)
                self.signals.result.emit(Picks_data(station = trace_idx, time = time_idx))


        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)


    def getData(self, data : SegYData):
        try:
            self.SGYdata = data
            raw_data = data.data
            # Нормализация
            gather_normalized = np.zeros_like(raw_data, dtype=np.float32)
            for i in range(gather_normalized.shape[1]):
                trace = raw_data[:, i]
                norm = np.max(np.abs(trace))
                if norm != 0:
                    gather_normalized[:, i] = trace / norm
            self.SGYdata = SegYData(data=gather_normalized)
            self.plot()
        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)

    def plot(self):
        try:
            #Для первого запуска, пока данные не переданы
            if self.SGYdata is None:
                return None
            #Для последующих запусков,чтоб прочистить картинку
            if self.image_item is not None:
                self.plot_widget.removeItem(self.image_item)
            #if self.histogram is not None:
                #self.plot_widget.removeItem(self.histogram)

            #Формирование изображения
            data = self.SGYdata.data
            self.image_item = pg.ImageItem()
            self.image_item.setImage(data)
            self.plot_widget.addItem(self.image_item)
            #self.plot_widget.addItem(self.histogram)

            colormap = pg.colormap.get('seismic', source='matplotlib')
            self.image_item.setLookupTable(colormap.getLookupTable())

            # Настраиваем оси
            self.plot_widget.setLabel('bottom', 'Номер трассы')
            self.plot_widget.setLabel('left', 'Время (отсчёты)')
            self.plot_widget.setTitle("Тепловая карта сейсмограммы")

        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)

    def clear(self):
        try:
            if self.image_item is not None:
                self.plot_widget.removeItem(self.image_item)
            self.SGYdata: SegYData = None
        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)

