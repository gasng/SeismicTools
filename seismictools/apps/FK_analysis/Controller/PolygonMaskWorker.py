from PySide6.QtCore import QRunnable, Slot, QObject, Signal
import numpy as np

class PolygonMaskSignals(QObject):
    result = Signal(object)
    error = Signal(str)

class PolygonMaskWorker(QRunnable):
    def __init__(self, polygon_points: list, shape: tuple, kx_axis: np.ndarray, freq_axis: np.ndarray):
        super().__init__()
        self.polygon_points = polygon_points
        self.shape = shape
        self.kx_axis = kx_axis
        self.freq_axis = freq_axis
        self.signals = PolygonMaskSignals()

    @Slot()
    def run(self):
        try:
            mask = self._create_mask(self.polygon_points, self.shape, self.kx_axis, self.freq_axis)
            self.signals.result.emit(mask)
        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)

    def _create_mask(self, points, shape, kx_axis, freq_axis):
        h, w = shape
        KX, FREQ = np.meshgrid(kx_axis, freq_axis)
        x_flat = KX.ravel()
        y_flat = FREQ.ravel()

        poly = np.array(points)
        n = len(poly)
        inside = np.zeros_like(x_flat, dtype=bool)

        j = n - 1
        for i in range(n):
            xi, yi = poly[i]
            xj, yj = poly[j]
            intersect = ((yi > y_flat) != (yj > y_flat)) & \
                        (x_flat < (xj - xi) * (y_flat - yi) / (yj - yi) + xi)
            inside ^= intersect
            j = i

        return inside.reshape(h, w)

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