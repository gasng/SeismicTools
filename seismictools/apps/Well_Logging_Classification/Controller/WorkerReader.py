# WorkerReader.py
import logging
import numpy as np
from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from seismictools.apps.Well_Logging_Classification.Calculate.Reader.WellLogReader import WellLogReader

logger = logging.getLogger(__name__)


class WorkerReaderSignals(QObject):
    """Сигналы для WorkerReader"""
    finished = Signal(object)
    error = Signal(str)         
    progress = Signal(int)     
    message = Signal(str)          
    started = Signal()


class WorkerReader(QRunnable):
    """Воркер для загрузки LAS файлов"""
    
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.signals = WorkerReaderSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        """Основной метод выполнения в фоновом потоке"""
        try:
            self.signals.started.emit()
            self.signals.message.emit(f"Загрузка файла: {self.filepath}")
            self.signals.progress.emit(10)
            
            data_dict = WellLogReader.read_las_file(self.filepath)
            
            if data_dict is None:
                raise ValueError(f"Не удалось прочитать файл: {self.filepath}")
            
            self.signals.progress.emit(50)
            
            # Проверяем структуру данных
            if 'curves' not in data_dict:
                raise ValueError("Файл не содержит кривых данных")
            
            curves = data_dict['curves']
            if not curves:
                raise ValueError("Файл не содержит кривых данных")
            
            # Подсчитываем количество точек
            num_points = 0
            for curve_name, curve_data in curves.items():
                if curve_data is not None and hasattr(curve_data, '__len__'):
                    if len(curve_data) > 0:
                        num_points = len(curve_data)
                        break
            
            data_dict['num_points'] = num_points
            
            metadata = data_dict.get('metadata', {})
            
            self.signals.message.emit(
                f"Файл успешно загружен: {len(curves)} кривых, {num_points} точек"
            )
            self.signals.progress.emit(100)
            
            self.signals.finished.emit(data_dict)
            
        except Exception as e:
            error_msg = f"Ошибка при загрузке файла: {str(e)}"
            logger.error(error_msg)
            self.signals.error.emit(error_msg)