from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from seismictools.apps.Calculate.Reader.SegYReader import ReaderDataSeicmic

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    message = Signal(str)
    result = Signal(object)

class WorkerReader(QRunnable):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.signals = WorkerSignals()

    @Slot()
    def working(self):
        """
        Выполняет чтение сейсмического файла SEG-Y в фоновом потоке.

        В случае успеха:
        - отправляется сообщение об успешной загрузке
        - данные передаются через сигнал result

        В случае ошибки:
        - текст ошибки отправляется через сигнал error
        - result получает значение None
        """
        try:
            reader = ReaderDataSeicmic()
            # Считываем наши данные
            data = reader.read_segy(self.file_path)

            msg = 'The file ' + self.file_path + ' has been read successfully'
            self.signals.message.emit(msg)
            self.signals.result.emit(data)
        except Exception as exc:
            error_msg = str(exc)
            self.signals.error.emit(error_msg)
            self.signals.result.emit(None)
        finally:
            self.signals.finished.emit()