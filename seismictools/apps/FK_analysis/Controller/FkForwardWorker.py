from PySide6.QtCore import QRunnable, Slot, QObject, Signal
from seismictools.apps.FK_analysis.Calculate.MathFK import forward_fk
import numpy as np


class FkForwardSignals(QObject):
    result = Signal(object)
    error = Signal(str)
    message = Signal(str)


class FkForwardWorker(QRunnable):
    def __init__(self, data: np.ndarray):
        super().__init__()
        self.data = data
        self.signals = FkForwardSignals()

    @Slot()
    def run(self):
        try:
            fk_spectrum = forward_fk(self.data)
            self.signals.message.emit("FK-спектр рассчитан")
            self.signals.result.emit(fk_spectrum)
        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)