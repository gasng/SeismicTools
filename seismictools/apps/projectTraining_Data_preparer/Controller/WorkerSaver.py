from PySide6.QtCore import QObject, Signal
import numpy as np

class WorkerSaver(QObject):
    saved = Signal(str)
    error = Signal(str)

    def __init__(self, traces, output_path):
        super().__init__()
        self.traces = traces
        self.output_path = output_path

    def run(self):
        try:
            if not self.traces:
                raise ValueError("Нет трасс для сохранения")

            #Определяем размеры
            n_traces = len(self.traces)
            n_samples = len(self.traces[0].data)

            #Подготавливаем массивы
            data_array = np.zeros((n_traces, n_samples), dtype=np.float32)
            labels_array = np.zeros(n_traces, dtype=np.int32)
            coords_array = np.zeros((n_traces, 2), dtype=np.float32)

            #Заполняем
            for i, trace in enumerate(self.traces):
                data_array[i, :] = trace.data
                labels_array[i] = trace.class_label
                coords_array[i, :] = trace.coordinates

            #Сохраняем в формат .npz
            np.savez_compressed(
                self.output_path,
                data=data_array,
                labels=labels_array,
                coordinates=coords_array
            )

            self.saved.emit(self.output_path)

        except Exception as e:
            self.error.emit(f"Ошибка при сохранении:\n{str(e)}")