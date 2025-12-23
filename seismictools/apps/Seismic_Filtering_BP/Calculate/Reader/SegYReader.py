import numpy as np
import segyio as sio
from dataclasses import dataclass

@dataclass
class SegYData:
    data: np.ndarray
    dt : float

class ReaderDataSeicmic:
    """
    Класс для чтения сейсмических данных из файла формата SEG-Y.
    Не хранит данные после чтения — только предоставляет метод для загрузки.
    """
    @staticmethod
    def read_segy(filepath):
        seg_file = sio.open(filepath, ignore_geometry=True)
        gather = np.array([seg_file.trace[i] for i in range(seg_file.tracecount)])

        #Пытаюсь вытащить частоту дискритизации из .sgy файла....
        dt_for_fs = seg_file.bin[sio.BinField.Interval]

        conver_to_sec = 1e-9

        if dt_for_fs == 0:
            dt_for_fs = conver_to_sec
        return SegYData(data=gather, dt=dt_for_fs)



