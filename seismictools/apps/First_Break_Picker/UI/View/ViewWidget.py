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
    pick_added = Signal(int, float, str)  # trace, time, type
    pick_removed = Signal(int, str)
    picks_interpolated = Signal(str, list)  # trace, type


class ViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        self.SGYdata: SegYData = None
        self.image_item = None
        self.signals = WorkerSignals()
        self.pickSignal = PickSignal()

        self.Pick_type: str = 'First_Break'
        self.picks = {}
        self.last_pick = None
        self.pick_markers = {}
        self.pick_curves = {}

        self.plot_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClicked)
        view_box = self.plot_widget.getViewBox()
        if view_box is not None:
            view_box.setMouseMode(view_box.PanMode)
            view_box.setMenuEnabled(False)
        self.plot_widget.setBackground('transparent')
        self.plot()

    ######################################
    # ЗАГРУЗКА И ОТОБРАЖЕНИЕ ДАННЫХ
    ######################################

    def getData(self, data):
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
            # Для первого запуска, пока данные не переданы
            if self.SGYdata is None:
                return None
            # Для последующих запусков,чтоб прочистить картинку
            if self.image_item is not None:
                self.plot_widget.removeItem(self.image_item)

            # Формирование изображения
            data = self.SGYdata.data
            self.image_item = pg.ImageItem()
            self.image_item.setImage(data[::-1].T)
            self.plot_widget.addItem(self.image_item)

            #Ограничение обзора
            view_box = self.plot_widget.getViewBox()
            if view_box is not None:
                x_min, x_max = 0, data.shape[1]  # Границы по трассам (X)
                y_min, y_max = 0, data.shape[0]  # Границы по времени (Y)

                view_box.setLimits(
                    xMin=x_min, xMax=x_max,
                    yMin=y_min, yMax=y_max,
                    minXRange=1,  # Минимум 1 трасса при увеличении
                    maxXRange=x_max,  # Максимум все трассы при уменьшении
                    minYRange=1,  # Минимум 1 отсчёт
                    maxYRange=y_max  # Максимум всё время
                )

            colormap = pg.colormap.get('seismic', source='matplotlib')
            self.image_item.setLookupTable(colormap.getLookupTable())

            # Настраиваем оси
            self.plot_widget.setLabel('bottom', 'Trace number')
            self.plot_widget.setLabel('left', 'Time (отсчёты)')
            self.plot_widget.setTitle("Seismogram Heat map")


        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)

    def change_display_mode(self, display_mode):
        if self.SGYdata is None or self.image_item is None:
            return

        if self.image_item is None:
            return
        colormap = pg.colormap.get(display_mode)
        self.image_item.setLookupTable(colormap.getLookupTable())

    def clear(self):
        try:
            if self.image_item is not None:
                self.plot_widget.removeItem(self.image_item)
            self.SGYdata: SegYData = None
        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)

    ######################################
    # УПРАВЛЕНИЕ ТИПАМИ ПИКОВ
    ######################################

    def set_pick_type(self, pick_type: str):
        self.Pick_type = pick_type
        self.last_pick = None

    ######################################
    # ИНТЕРАКТИВНОСТЬ: КЛИКИ И ПИКИ
    ######################################

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

            # Проверка границ трассы
            if not (0 <= trace_idx < self.SGYdata.data.shape[1]):
                return

            # === Обработка ПРАВОГО клика: удаление пика ===
            if event.button() == QtCore.Qt.MouseButton.RightButton:
                if (self.Pick_type in self.picks and
                        trace_idx in self.picks[self.Pick_type]):
                    self.remove_pick(trace_idx, self.Pick_type)
                return

            # === Обработка ЛЕВОГО клика: добавление пика ===
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                time_idx = int(round(y))
                if not (0 <= time_idx < self.SGYdata.data.shape[0]):
                    return

                current_pick = (trace_idx, time_idx, self.Pick_type)

                # Интерполяция (если включена)
                if (self.last_pick is not None and
                        self.last_pick[2] == self.Pick_type and
                        abs(trace_idx - self.last_pick[0]) > 1):

                    # Удаляем промежуточные пики
                    start = min(trace_idx, self.last_pick[0])
                    end = max(trace_idx, self.last_pick[0])
                    for t in range(start + 1, end):
                        if t in self.picks.get(self.Pick_type, {}):
                            self.remove_pick(t, self.Pick_type)

                    # Интерполируем
                    self._interpolate_picks(self.last_pick, current_pick)

                self.last_pick = current_pick
                self.add_pick(trace_idx, time_idx, self.Pick_type)

        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)

    def add_pick(self, trace_idx: int, time_idx: float, pick_type: str):
        """Добавляет пик с обновлением визуализации"""
        if pick_type not in self.picks:
            self.picks[pick_type] = {}

        # Удаляем существующий пик на этой трассе
        if trace_idx in self.picks[pick_type]:
            self.remove_pick(trace_idx, pick_type)

        # Добавляем новый пик
        self.picks[pick_type][trace_idx] = time_idx
        self._update_pick_visualization(pick_type)

        # Отправляем сигнал (только для ручных пиков)
        self.pickSignal.pick_added.emit(trace_idx, time_idx, pick_type)

    def remove_pick(self, trace_idx: int, pick_type: str):
        """Удалить пик"""
        if pick_type in self.picks and trace_idx in self.picks[pick_type]:
            del self.picks[pick_type][trace_idx]
            self._update_pick_visualization(pick_type)
            self.pickSignal.pick_removed.emit(trace_idx, pick_type)

    def remove_pick_by_data(self, trace_idx: int, pick_type: str):
        """Удаляет пик по данным (вызывается из main.py)"""
        if pick_type in self.picks and trace_idx in self.picks[pick_type]:
            del self.picks[pick_type][trace_idx]
            self._update_pick_visualization(pick_type)
            # Не отправляем сигнал pick_removed, чтобы избежать зацикливания!

    def clear_all_picks(self):
        """Очищает все пики"""
        self.picks.clear()
        # Удаляем визуальные элементы
        for marker in self.pick_markers.values():
            self.plot_widget.removeItem(marker)
        for curve in self.pick_curves.values():
            self.plot_widget.removeItem(curve)
        self.pick_markers.clear()
        self.pick_curves.clear()
        self.last_pick = None

    ######################################
    # ИНТЕРПОЛЯЦИЯ И ВИЗУАЛИЗАЦИЯ ПИКОВ
    ######################################

    def _interpolate_picks(self, start_pick, end_pick):
        try:
            """Интерполирует пики БЕЗ частых перерисовок"""
            start_trace, start_time, pick_type = start_pick
            end_trace, end_time, _ = end_pick

            if start_trace > end_trace:
                start_trace, end_trace = end_trace, start_trace
                start_time, end_time = end_time, start_time

            # Собираем ВСЕ новые пики
            new_picks = {}
            for trace in range(start_trace + 1, end_trace):
                time = start_time + (end_time - start_time) * (trace - start_trace) / (end_trace - start_trace)
                new_picks[trace] = time

            # Удаляем ВСЕ старые промежуточные пики
            if pick_type in self.picks:
                traces_to_remove = [
                    t for t in self.picks[pick_type].keys()
                    if start_trace < t < end_trace
                ]
                for trace in traces_to_remove:
                    del self.picks[pick_type][trace]

            # Добавляем ВСЕ новые пики
            if pick_type not in self.picks:
                self.picks[pick_type] = {}
            self.picks[pick_type].update(new_picks)

            # ОДНА перерисовка
            self._update_pick_visualization(pick_type)

            # ОДИН сигнал со всеми новыми пиками
            self.pickSignal.picks_interpolated.emit(
                pick_type,
                [(trace, time) for trace, time in new_picks.items()]
            )

        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)

    def _update_pick_visualization(self, pick_type: str):
        colors = {
            'First_Break': 'yellow',
            'Refraction': 'purple',
            'Reflection': 'green'
        }
        color = colors.get(pick_type, 'y')

        if pick_type not in self.picks:
            x_coords, y_coords = [], []
        else:
            items = sorted(self.picks[pick_type].items())  # сортируем по трассам
            x_coords = [item[0] for item in items]
            y_coords = [item[1] for item in items]

        # Маркеры
        if pick_type not in self.pick_markers:
            self.pick_markers[pick_type] = pg.ScatterPlotItem(size=5, brush=color)
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