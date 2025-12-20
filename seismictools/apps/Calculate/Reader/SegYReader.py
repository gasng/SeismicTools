import numpy as np
import segyio as sio
from dataclasses import dataclass

@dataclass
class SegYData:
    data: np.ndarray

class ReaderDataSeicmic:
    """
    Класс для чтения сейсмических данных из файла формата SEG-Y.
    Не хранит данные после чтения — только предоставляет метод для загрузки.
    """
    @staticmethod
    def read_segy(filepath):
        seg_file = sio.open(filepath, ignore_geometry=True)
        gather = np.array([seg_file.trace[i] for i in range(seg_file.tracecount)])
        return SegYData(data=gather)