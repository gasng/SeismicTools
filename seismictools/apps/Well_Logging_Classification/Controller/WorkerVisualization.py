# WorkerVisualisation.py
import logging
import numpy as np
from PySide6.QtCore import QObject, Signal, QRunnable, Slot

logger = logging.getLogger(__name__)


class WorkerVisualisationSignals(QObject):
    """Сигналы для WorkerVisualisation"""
    finished = Signal(dict)        # Результат: {'x_data': ..., 'y_data': ..., 'title': ...}
    error = Signal(str)            # Ошибка
    progress = Signal(int)         # Прогресс
    message = Signal(str)          # Сообщения
    started = Signal()             # Начало работы


class WorkerVisualisation(QRunnable):
    """Воркер для подготовки данных визуализации"""
    
    def __init__(self, well_data, x_curve_name, y_curve_name):
        super().__init__()
        self.well_data = well_data
        self.x_curve_name = x_curve_name
        self.y_curve_name = y_curve_name
        self.signals = WorkerVisualisationSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        """Подготовка данных для визуализации в фоновом потоке"""
        try:
            self.signals.started.emit()
            self.signals.message.emit("Подготовка данных для визуализации...")
            self.signals.progress.emit(10)
            
            # Получаем данные кривых
            x_data = self.well_data.get_curve(self.x_curve_name)
            y_data = self.well_data.get_curve(self.y_curve_name)

            if x_data is None:
                raise ValueError(f"Кривая '{self.x_curve_name}' не найдена")
            if y_data is None:
                raise ValueError(f"Кривая '{self.y_curve_name}' не найдена")
            
            self.signals.progress.emit(30)
            
            # Очистка данных от NaN и бесконечных значений
            valid_mask = np.isfinite(x_data) & np.isfinite(y_data)
            x_clean = x_data[valid_mask]
            y_clean = y_data[valid_mask]
            
            self.signals.progress.emit(70)
            
            if len(x_clean) == 0 or len(y_clean) == 0:
                raise ValueError("Нет валидных данных для визуализации после очистки")
            
            # Подготовка результата
            result = {
                'x_data': x_clean,
                'y_data': y_clean,
                'x_name': self.x_curve_name,
                'y_name': self.y_curve_name,
                'title': f"Кросс-плот: {self.x_curve_name} vs {self.y_curve_name}",
                'num_points': len(x_clean),
                'x_min': float(np.min(x_clean)),
                'x_max': float(np.max(x_clean)),
                'y_min': float(np.min(y_clean)),
                'y_max': float(np.max(y_clean))
            }
            
            self.signals.message.emit(f"Подготовлено {len(x_clean)} точек для визуализации")
            self.signals.progress.emit(100)
            self.signals.finished.emit(result)
            
        except Exception as e:
            error_msg = f"Ошибка при подготовке визуализации: {str(e)}"
            logger.error(error_msg)
            self.signals.error.emit(error_msg)