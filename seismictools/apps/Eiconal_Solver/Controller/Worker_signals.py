from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):
    error = Signal(str)
    progress = Signal(int)
    message = Signal(str)
    result = Signal(object)
