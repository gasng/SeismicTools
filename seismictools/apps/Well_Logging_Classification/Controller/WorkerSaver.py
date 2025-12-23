# Controller/WorkerSaver.py
import logging
from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from seismictools.apps.Well_Logging_Classification.Calculate.Saver.WellLogSaver import WellLogSaver

logger = logging.getLogger(__name__)

class WorkerSaverSignals(QObject):
    finished = Signal(bool)
    error = Signal(str)
    progress = Signal(int)
    message = Signal(str)
    started = Signal()

class WorkerSaver(QRunnable):
    def __init__(self, filepath, well_data):
        super().__init__()
        self.filepath = filepath
        self.well_data = well_data
        self.signals = WorkerSaverSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        try:
            self.signals.started.emit()
            self.signals.message.emit("Сохранение файла...")
            self.signals.progress.emit(10)
            
            # Добавляем кривые классов если есть
            labels = self.well_data.class_labels
            if labels is not None:
                for class_id in self.well_data.class_names:
                    if class_id != 0:
                        class_name = self.well_data.get_class_name(class_id)
                        curve_name = f"CLASS_{class_id:02d}_{class_name}"
                        class_data = (labels == class_id).astype(float)
                        self.well_data.add_curve(curve_name, class_data)
                self.signals.progress.emit(50)
            
            # Сохраняем
            success = WellLogSaver.save_las_file(self.filepath, self.well_data)
            self.signals.progress.emit(100)
            self.signals.finished.emit(success)
            
        except Exception as e:
            self.signals.error.emit(str(e))