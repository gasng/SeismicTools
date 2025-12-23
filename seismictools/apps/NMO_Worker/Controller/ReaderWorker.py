from PySide6.QtCore import QObject, Signal, QRunnable
from seismictools.apps.NMO_Worker.Calculate.Reader import SegYReader
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    message = Signal(str)
    result = Signal(object)


class WorkerReader(QRunnable):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.signals = WorkerSignals()

    def run(self):
        try:
            segy_data = SegYReader().read(filepath=self.filepath)
            self.signals.message.emit('Файл прочитан')
            self.signals.result.emit(segy_data)
        except Exception as e:
            self.signals.error.emit(str(e))