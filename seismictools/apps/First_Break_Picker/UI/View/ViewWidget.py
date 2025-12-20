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

class PickSignal(QObject):
    pick_added = Signal(int, float, str)    # trace, time, type
    pick_removed = Signal(int, str)         # trace, type


class ViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        self.SGYdata : SegYData = None
        self.image_item = None
        self.signals = WorkerSignals()
        self.pickSignal = PickSignal()

        self.Pick_type : str = 'First_Break'
        self.picks = {

        }
        self.pick_markers = {}  # {тип: ScatterPlotItem}
        self.pick_curves = {}  # {тип: PlotDataItem}

        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClicked)
        self.plot()

    ######################################Интерактивность###############################################################
    def mouseClicked(self, event):
        if self.SGYdata is None or self.image_item is None:
            return

        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return
        try:
            plot_item = self.plot_widget.getPlotItem()
            if plot_item is None or plot_item.vb is None:
                return

            position = event.scenePos()
            view_position = plot_item.vb.mapSceneToView(position)
            x, y = view_position.x(), view_position.y()

            trace_idx = int(round(x))
            time_idx = int(round(y))

            if not (0 <= trace_idx < self.SGYdata.data.shape[1] and
                    0 <= time_idx < self.SGYdata.data.shape[0]):
                return

            # Удаляем существующий пик на этой трассе для этого типа
            if self.Pick_type in self.picks and trace_idx in self.picks[self.Pick_type]:
                self.remove_pick(trace_idx, self.Pick_type)

            # Добавляем новый пик
            if self.Pick_type not in self.picks:
                self.picks[self.Pick_type] = {}
            self.picks[self.Pick_type][trace_idx] = time_idx

            # Обновляем визуализацию
            self._update_pick_visualization(self.Pick_type)

            # Отправляем сигнал
            self.pickSignal.pick_added.emit(trace_idx, time_idx, self.Pick_type)


        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)

    def remove_pick(self, trace_idx: int, pick_type: str):
        """Удалить пик"""
        if pick_type in self.picks and trace_idx in self.picks[pick_type]:
            del self.picks[pick_type][trace_idx]
            self._update_pick_visualization(pick_type)
            self.pickSignal.pick_removed.emit(trace_idx, pick_type)

    def _update_pick_visualization(self, pick_type: str):
        """Обновить маркеры и линии для типа пика"""
        # Цвета по типу
        colors = {
            'First_Break': 'r',
            'Refraction': 'g',
            'Reflection': 'b'
        }
        color = colors.get(pick_type, 'y')

        # Получаем координаты
        if pick_type not in self.picks:
            x_coords, y_coords = [], []
        else:
            items = sorted(self.picks[pick_type].items())  # сортируем по трассам
            x_coords = [item[0] for item in items]
            y_coords = [item[1] for item in items]

        # Маркеры
        if pick_type not in self.pick_markers:
            self.pick_markers[pick_type] = pg.ScatterPlotItem(size=2, brush=color)
            self.plot_widget.addItem(self.pick_markers[pick_type])
        self.pick_markers[pick_type].setData(x=x_coords, y=y_coords)

        # Линии
        if len(x_coords) > 1:
            if pick_type not in self.pick_curves:
                self.pick_curves[pick_type] = self.plot_widget.plot(pen=pg.mkPen(color, width=2))
            self.pick_curves[pick_type].setData(x=x_coords, y=y_coords)
        elif pick_type in self.pick_curves:
            self.plot_widget.removeItem(self.pick_curves[pick_type])
            del self.pick_curves[pick_type]
    ####################################################################################################################
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
            self.image_item.setImage(data[::-1].T)
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

    def set_pick_type(self, pick_type: str):
        self.Pick_type = pick_type

    def clear(self):
        try:
            if self.image_item is not None:
                self.plot_widget.removeItem(self.image_item)
            self.SGYdata: SegYData = None
        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)

