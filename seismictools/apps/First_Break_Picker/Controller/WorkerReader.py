from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from seismictools.apps.First_Break_Picker.Calculate.Reader.SegYReader import  SegYReader

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

    @Slot()
    def run(self):
        try:
            segy_data = SegYReader().read(filepath=self.filepath)
            self.signals.message.emit('Файл прочитан')
            self.signals.result.emit(segy_data)
        except Exception as e:
            self.signals.error.emit(e.args[0])
            self.signals.result.emit(None)