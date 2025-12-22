from PySide6.QtCore import QObject, Signal, QRunnable
from seismictools.apps.Seismic_Filtering_BP.Calculate.Reader.SegYReader import ReaderDataSeicmic

class WorkerSignals(QObject):
    """
    finished - работа завершена
    error - произошла ошибка (текстовое сообщение)
    progress - прогресс выполнения в процентах [0-100]
    message - какаое-то информационное сообщение
    result - результат (отфильтрованные данные)

    Это сигналы, нужны для обмена данными между фоновым потоком и основным потоком.
    """
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    message = Signal(str)
    result = Signal(object, str)

class WorkerReader(QRunnable):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.signals = WorkerSignals()

    def run(self):
        """
        Выполняет чтение сейсмического файла SEG-Y в фоновом потоке.
        """
        try:
            # Считываем наши данные
            data = ReaderDataSeicmic.read_segy(self.file_path)

            msg = 'The file ' + self.file_path + ' has been read successfully'
            self.signals.message.emit(msg)
            self.signals.result.emit(data, self.file_path)
        except Exception as exc:
            error_msg = "Error reading the file " + self.file_path + ": " + str(exc)
            self.signals.error.emit(error_msg)
            self.signals.result.emit(None, self.file_path)
        finally:
            self.signals.finished.emit()