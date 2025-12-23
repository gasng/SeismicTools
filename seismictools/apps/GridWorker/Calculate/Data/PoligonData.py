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

        # Для хранения сохранённых полигонов
        self.saved_polygons = []  # Список полигонов: [[(x1,y1), (x2,y2), ...], ...]
        self.saved_polygon_items = []  # Список отображаемых линий на карте

        self.plot_widget.scene().sigMouseClicked.connect(self._on_click)

    # Сигналы
    status_message = pyqtSignal(str)
    polygon_completed = pyqtSignal()

    def _on_click(self, event):
        """
            Функция обработки кликов: одиночного и двойного
            event (QGraphicsSceneMouseEvent): Событие клика мыши
        """
        if event.button() != QtCore.Qt.LeftButton:
            return

        # Если полигон уже замкнут — сбрасываем только текущий
        if self.is_polygon_closed:
            self.clear_current_polygon()

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
            Функция поиска ближайшей точки к указанной позиции клика
            click_pos (QPointF): Позиция клика в координатах сцены
            view_box (ViewBox): ViewBox для преобразования координат
            threshold (int): Максимальное расстояние в пикселях
            для считания точки "близкой". По умолчанию 10.
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
            Функция добавления точки и обновления линии
            x (float): X-координата точки в системе координат данных
            y (float): Y-координата точки в системе координат данных
        """
        self.points.append((x, y))
        self._update_plot()
        self.status_message.emit(f"Точка добавлена: ({x:.1f}, {y:.1f})")

    def remove_point(self, index):
        """
            Функция удаления точки по индексу и обновления линии
            index (int): Индекс удаляемой точки
        """
        if 0 <= index < len(self.points):
            del self.points[index]
            self._update_plot()

    def close_polygon(self):
        """
            Функция, замыкающая полигон
        """
        if len(self.points) < 3:
            return

        self.is_polygon_closed = True
        self._update_plot()
        self.status_message.emit(f"Полигон замкнут. Вершин: {len(self.points)}")
        self.polygon_completed.emit()

    def _update_plot(self):
        """
            Функция обновляет текущий полигон при его изменении
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

    def add_saved_polygon(self, polygon: list, color=(0, 255, 0)):
        """
            Функция добавляет сохранённый полигон на карту
            polygon (list): Список координат полигона
            color (tuple): Цвет линии в формате (R, G, B)
        """
        if len(polygon) < 2:
            return

        if not hasattr(self, 'plot_widget') or not self.plot_widget:
            print("Предупреждение: нет виджета для отрисовки")
            return

        # Замыкаем полигон
        x = [p[0] for p in polygon] + [polygon[0][0]]
        y = [p[1] for p in polygon] + [polygon[0][1]]

        # Создаём линию
        line = pg.PlotDataItem(
            x=x, y=y,
            pen=pg.mkPen(color=color, width=2)
        )

        # Сохраняем данные и отображение
        self.saved_polygons.append(polygon)
        self.saved_polygon_items.append(line)
        self.plot_widget.addItem(line)

    def _clear_plot_items(self):
        """
            Функция удаления графических элементов текущего полигона
        """
        if self.scatter_plot:
            self.plot_widget.removeItem(self.scatter_plot)
            self.scatter_plot = None
        if self.line_plot:
            self.plot_widget.removeItem(self.line_plot)
            self.line_plot = None

    def clear_all(self):
        """
            Фунция полной очистки
        """
        self.clear_current_polygon()
        # Удаляем все сохранённые полигоны с карты
        for item in self.saved_polygon_items:
            self.plot_widget.removeItem(item)
        self.saved_polygons = []
        self.saved_polygon_items = []

    def clear_current_polygon(self):
        """
            Функция очищает только текущий (активный) полигон, сохранённые остаются
        """
        self.points = []
        self.is_polygon_closed = False
        self._clear_plot_items()

    def get_polygon(self):
        """
            Функция возвращает координаты полигона или None
        """
        if self.is_polygon_closed and len(self.points) >= 3:
            return self.points.copy()
        return None


