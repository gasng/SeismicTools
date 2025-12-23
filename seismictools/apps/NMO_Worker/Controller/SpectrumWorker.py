from PySide6.QtCore import QRunnable
from seismictools.apps.NMO_Worker.Calculate.Spectrum import Spectrum
from seismictools.apps.NMO_Worker.Controller.ReaderWorker import WorkerSignals

class SpectrumWorker(QRunnable):
    def __init__(self, data, offsets, dt):
        print("SpectrumWorker: data.shape =", data.shape)
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()
        self.offsets = offsets
        self.dt = dt

    def run(self):
        try:
            self.signals.message.emit("Начало расчёта спектра...")
            spectrum_obj = Spectrum(self.data, self.offsets, self.dt)
            spectrum = spectrum_obj.calculate_spectrum()
            self.signals.message.emit('Спектр построен')
            self.signals.result.emit(spectrum)
        except Exception as e:
            self.signals.error.emit(str(e))