from PySide6.QtCore import QRunnable, Slot
from ..Calculate.Reader.Model_reader import ModelReader
from .Worker_signals import WorkerSignals

class ReaderWorker(QRunnable):


    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(f"Загрузка модели из {self.path}")
            model = ModelReader.read(self.path)
            self.signals.message.emit("Модель успешно загружена.")
            self.signals.result.emit(model.model)

        except Exception as e:
            self.signals.error.emit(str(e))
            self.signals.result.emit(None)