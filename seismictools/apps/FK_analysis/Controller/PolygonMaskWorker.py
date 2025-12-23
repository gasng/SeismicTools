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