from PySide6.QtCore import QRunnable, Slot, QObject, Signal
from seismictools.apps.FK_analysis.Calculate.MathFK import inverse_fk
import numpy as np


class FkInverseSignals(QObject):
    result = Signal(object)
    error = Signal(str)
    message = Signal(str)


class FkInverseWorker(QRunnable):
    def __init__(self, fk_spectrum: np.ndarray):
        super().__init__()
        self.fk_spectrum = fk_spectrum
        self.signals = FkInverseSignals()

    @Slot()
    def run(self):
        try:
            result_data = inverse_fk(self.fk_spectrum)
            self.signals.message.emit("Обратное FK-преобразование выполнено")
            self.signals.result.emit(result_data)
        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)