from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore
import pyqtgraph as pg

class PointManager(QObject):
    def __init__(self, plot_widget):
        super().__init__()
        self.plot_widget = plot_widget
        self.points = []  # [(x, y), ...]
        self.scatter_plot = None
        self.line_plot = None  # Линия между точками
        self.is_polygon_closed = False  # Флаг замкнутого полигона

        self.plot_widget.scene().sigMouseClicked.connect(self._on_click)

    # Сигналы
    status_message = pyqtSignal(str)
    polygon_completed = pyqtSignal()

    def _on_click(self, event):
        """
            Функция обработки кликов: одиночного и двойного
        """
        if event.button() != QtCore.Qt.LeftButton:
            return

        # Если полигон уже замкнут — сброс
        if self.is_polygon_closed:
            self.clear_points()
            self.is_polygon_closed = False

        pos = event.scenePos()
        if not self.plot_widget.viewRect().contains(pos):
            return

        view_box = self.plot_widget.getViewBox()
        if not view_box:
            return

        if event.double():
            # Двойной клик - замкнуть полигон полигон
            self.close_polygon()
        else:
            # Одиночный клик - добавить или удалить точку
            image_pos = view_box.mapSceneToView(pos)
            x, y = image_pos.x(), image_pos.y()
            point_index = self._find_closest_point(pos, view_box, threshold=10)
            if point_index is not None:
                self.remove_point(point_index)
            else:
                self.add_point(x, y)

    def _find_closest_point(self, click_pos, view_box, threshold=10):
        """
            Функция поиска ближайшей точки
        """
        if not self.points:
            return None
        closest_index = None
        min_dist_px = float('inf')
        for i, (px, py) in enumerate(self.points):
            point_px = view_box.mapViewToScene(QtCore.QPointF(px, py))
            dist_px = ((click_pos.x() - point_px.x())**2 +
                       (click_pos.y() - point_px.y())**2)**0.5
            if dist_px < min_dist_px:
                min_dist_px = dist_px
                closest_index = i
        return closest_index if min_dist_px <= threshold else None

    def add_point(self, x, y):
        """
            Фунция добавления точки и обновления линии
        """
        self.points.append((x, y))
        self._update_plot()
        self.status_message.emit(f"Точка добавлена: ({x:.1f}, {y:.1f})")

    def remove_point(self, index):
        """
            Функция удаления точки и обновления линии
        """
        if 0 <= index < len(self.points):
            del self.points[index]
            self._update_plot()

    def close_polygon(self):
        """
            Функция, замыкающая полигон
        """
        if len(self.points) < 3:
            return  # Нужно минимум 3 точки

        self.is_polygon_closed = True
        self._update_plot()
        self.status_message.emit(f"Полигон замкнут. Вершин: {len(self.points)}")
        self.polygon_completed.emit()

    def _update_plot(self):
        """
            Функция обновления точки и линии
        """
        if not self.points:
            self._clear_plot_items()
            return

        x = [p[0] for p in self.points]
        y = [p[1] for p in self.points]

        # Обновление точек
        if self.scatter_plot is None:
            self.scatter_plot = pg.ScatterPlotItem(
                size=10,
                brush=pg.mkBrush(0, 0, 0, 200),
                symbol='o'
            )
            self.plot_widget.addItem(self.scatter_plot)
        self.scatter_plot.setData(x=x, y=y)

        # Обновляем линию
        if self.line_plot is None:
            self.line_plot = pg.PlotDataItem(
                pen=pg.mkPen(color=(0, 0, 0), width=2)
            )
            self.plot_widget.addItem(self.line_plot)

        # Если полигон замкнут — добавляем первую точку в конец
        if self.is_polygon_closed:
            x_closed = x + [x[0]]
            y_closed = y + [y[0]]
            self.line_plot.setData(x=x_closed, y=y_closed)
        else:
            self.line_plot.setData(x=x, y=y)

    def _clear_plot_items(self):
        """
            Функция удаления всех графических элементов
        """
        if self.scatter_plot:
            self.plot_widget.removeItem(self.scatter_plot)
            self.scatter_plot = None
        if self.line_plot:
            self.plot_widget.removeItem(self.line_plot)
            self.line_plot = None

    def clear_points(self):
        """
            Фунция полной очистки
        """
        self.points = []
        self.is_polygon_closed = False
        self._clear_plot_items()

    def get_polygon(self):
        """
            Фунция возвращает координаты полигона или None
        """
        if self.is_polygon_closed and len(self.points) >= 3:
            return self.points.copy()
        return None


