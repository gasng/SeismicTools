from PySide6.QtCore import QRunnable
from seismictools.apps.NMO_Worker.Calculate.Correction import Correction
from seismictools.apps.NMO_Worker.Controller.ReaderWorker import WorkerSignals

class CorrectionWorker(QRunnable):
    def __init__(self, data, law, offsets, dt):
        super().__init__()
        self.data = data
        self.law = law
        self.offsets = offsets
        self.dt = dt
        self.signals = WorkerSignals()

    def run(self):
        try:
            self.signals.message.emit("Начало расчёта поправок...")
            correction_obj = Correction(self.data, self.law, self.offsets, self.dt)
            correction = correction_obj.calculate_correction()
            self.signals.message.emit('Поправки завершены')
            self.signals.result.emit(correction)
        except Exception as e:
            self.signals.error.emit(str(e))