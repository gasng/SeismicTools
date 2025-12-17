import segyio as sio
import numpy as np
from dataclasses import dataclass

@dataclass
class SegYData:
    data: np.ndarray
    dt: float
    dx: float


class SegYReader:
    @staticmethod
    def read(filepath):
        """
        Метод для чтения segy файлов

        :param filepath: Путь до файла
        :return: Объект класса SegYData. Внутри - трассы и шаги дискретизации по x и t.
        """
        seg_file = sio.open(filepath, ignore_geometry=True)
        gather = np.array([seg_file.trace[i] for i in range(seg_file.tracecount)])

        dt_microsec = seg_file.bin[sio.BinField.Interval]
        dt_sec = dt_microsec / 1e6
        if dt_sec == 0:
            dt_sec = 0.001

        # Читаем dx (расстояние между трассами)
        if len(seg_file.header) > 0:
            x0 = seg_file.header[0][sio.TraceField.GroupX]
            if len(seg_file.header) > 1:
                x1 = seg_file.header[1][sio.TraceField.GroupX]
                dx = abs(x1 - x0)
            else:
                dx = 1.0
        else:
            dx = 1.0

        if dx == 0:
            dx = 1.0
        return SegYData(data=gather, dt=dt_sec, dx=dx)