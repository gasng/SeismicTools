from PySide6.QtCore import QRunnable, Slot, QObject, Signal
import numpy as np

class PolygonMaskSignals(QObject):
    result = Signal(object)
    error = Signal(str)

class PolygonMaskWorker(QRunnable):
    def __init__(self, polygon_points: list, shape: tuple):
        """
        :param polygon_points: список [(x, y), ...] в координатах графика
        :param shape: (h, w) — размер FK-спектра
        """
        super().__init__()
        self.polygon_points = polygon_points
        self.shape = shape
        self.signals = PolygonMaskSignals()

    @Slot()
    def run(self):
        try:
            mask = self._create_mask(self.polygon_points, self.shape)
            self.signals.result.emit(mask)
        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)

    def _create_mask(self, points, shape):
        h, w = shape
        mask = np.zeros((h, w), dtype=bool)

        # Преобразуем точки в целочисленные индексы
        poly_x = []
        poly_y = []
        for (x, y) in points:
            xi = int(np.clip(x, 0, w - 1))
            yi = int(np.clip(y, 0, h - 1))
            poly_x.append(xi)
            poly_y.append(yi)

        # Ray casting
        for y in range(h):
            for x in range(w):
                mask[y, x] = self._point_in_polygon(x, y, poly_x, poly_y)
        return mask

    def _point_in_polygon(self, x, y, poly_x, poly_y):
        n = len(poly_x)
        inside = False
        p1x, p1y = poly_x[0], poly_y[0]
        for i in range(1, n + 1):
            p2x, p2y = poly_x[i % n], poly_y[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside