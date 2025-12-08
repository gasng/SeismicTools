from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from seismictools.apps.FK_analysis.Calculate.Reader import SegYReader


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    message = Signal(str)
    result = Signal(object)


class WorkerReader(QRunnable):
    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            segy_data = SegYReader.read(filepath=self.filepath)
            self.signals.message.emit("Файл прочитан")
            self.signals.result.emit(segy_data)
            self.signals.finished.emit()
        except Exception as e:
            error_msg = str(e) if str(e) else "Неизвестная ошибка при чтении файла"
            self.signals.error.emit(error_msg)
            self.signals.result.emit(None)
            self.signals.finished.emit()