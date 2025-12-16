import pyqtgraph as pg
import numpy as np

class PolygonSelector:
    def __init__(self, plot_widget: pg.PlotWidget, data_shape: tuple, f_nyquist: float, k_nyquist: float):
        self.plot_widget = plot_widget
        self.data_shape = data_shape
        self.f_nyquist = f_nyquist
        self.k_nyquist = k_nyquist
        self.points = []  # [(x_view, y_view), ...] ← float, координаты графика
        self.scatter = None
        self.polygon_line = None
        self.is_selecting = False
        self.image_item = None


    def start_selection(self):
        self.clear()
        self.points = []
        self.is_selecting = True

    def finish_selection(self):
        self.is_selecting = False
        return len(self.points) >= 3

    def clear(self):
        if self.scatter:
            self.plot_widget.removeItem(self.scatter)
            self.scatter = None
        if self.polygon_line:
            self.plot_widget.removeItem(self.polygon_line)
            self.polygon_line = None
        self.points = []

    def add_point(self, scene_pos):
        view_pos = self.plot_widget.plotItem.vb.mapSceneToView(scene_pos)

        # Если есть ImageItem — используем его для конвертации
        if self.image_item:
            img_pos = self.image_item.mapFromView(view_pos)
            x_phys = img_pos.x()
            y_phys = img_pos.y()

            # Конвертируем в индексы массива
            h, w = self.data_shape
            x_idx = int(np.clip((x_phys + self.k_nyquist) / (2 * self.k_nyquist) * w, 0, w - 1))
            y_idx = int(np.clip((y_phys + self.f_nyquist) / (2 * self.f_nyquist) * h, 0, h - 1))
            self.points.append((x_idx, y_idx))
        else:
            # Без image_item — просто конвертируем координаты графика в индексы
            x_view = view_pos.x()
            y_view = view_pos.y()
            h, w = self.data_shape
            x_idx = int(np.clip(x_view, 0, w - 1))
            y_idx = int(np.clip(y_view, 0, h - 1))
            self.points.append((x_idx, y_idx))

        self._update_visuals()

    def _update_visuals(self):
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]

        if self.scatter is None:
            self.scatter = pg.ScatterPlotItem(size=8, pen='r', brush='r')
            self.plot_widget.addItem(self.scatter)
        self.scatter.setData(x=xs, y=ys)

        if len(self.points) > 1:
            if self.polygon_line is None:
                self.polygon_line = pg.PlotCurveItem(pen=pg.mkPen('g', width=2))
                self.plot_widget.addItem(self.polygon_line)
            if len(self.points) >= 3:
                closed_x = xs + [xs[0]]
                closed_y = ys + [ys[0]]
            else:
                closed_x, closed_y = xs, ys
            self.polygon_line.setData(x=closed_x, y=closed_y)

    def get_points(self):
        return self.points.copy()  # ← возвращаем [(x, y)] в координатах графика