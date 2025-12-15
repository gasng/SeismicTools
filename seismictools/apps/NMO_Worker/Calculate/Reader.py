import segyio as sio
import numpy as np
from dataclasses import dataclass

@dataclass
class SegYData:
    def __init__(self, data, receiver_x=None, offsets=None, dt=None):
        self.data = data              # (nt, nx)
        self.receiver_x = receiver_x  # (nx,) — x-координаты приёмников
        self.offsets = offsets        # (nx,) — выносы (если источник один — можно вычислить)
        self.dt = dt                  # шаг по времени, сек

class SegYReader:
    @staticmethod
    def read(filepath, dx=30.0):  # dx — расстояние между приёмниками в метрах
        with sio.open(filepath, "r", strict=False) as seg_file:
            # 1. Данные
            gather = np.array([seg_file.trace[i] for i in range(seg_file.tracecount)]).T  # (nt, nx)
            nx = gather.shape[1]

            # 2. Шаг по времени
            dt_micros = seg_file.bin[sio.BinField.Interval]
            dt =  0.002

            # 3. Аппроксимация геометрии: источник в центре
            # Приёмники: [-L, ..., -dx, 0, dx, ..., L]
            if nx % 2 == 1:
                # Нечётное число трасс → есть трасса под источником
                receiver_x = np.arange(-(nx // 2), nx // 2 + 1) * dx
            else:
                # Чётное число → симметрия между двумя центральными
                receiver_x = (np.arange(nx) - (nx - 1) / 2) * dx

            offsets = receiver_x

            # (Опционально: проверим, что offsets симметричны)
            print("Первые 5 выносов:", offsets[:5])
            print("Последние 5 выносов:", offsets[-5:])

            return SegYData(
                data=gather,
                offsets=offsets,
                dt=dt
            )