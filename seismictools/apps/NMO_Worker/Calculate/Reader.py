import segyio as sio
import numpy as np
from dataclasses import dataclass

@dataclass
class SegYData:
    def __init__(self, data, receiver_x=None, offsets=None, dt=None):
        self.data = data
        self.receiver_x = receiver_x
        self.offsets = offsets
        self.dt = dt

class SegYReader:
    @staticmethod
    def read(filepath, dx=30.0):
        with sio.open(filepath, "r", strict=False) as seg_file:
            print(filepath)
            if filepath == "C:/Users/seshu/Downloads/Telegram Desktop/CPD.segy":
                gather = np.array([seg_file.trace[i] for i in range(seg_file.tracecount)])
            else:
                gather = np.array([seg_file.trace[i] for i in range(seg_file.tracecount)]).T
            nx = gather.shape[1]

            dt =  0.002

            if filepath == "C:/Users/seshu/Downloads/Telegram Desktop/CPD.segy":
                receiver_x = np.arange(nx) * dx
                offsets = receiver_x

            else:
            # Приёмники: [-L, ..., -dx, 0, dx, ..., L]
                if nx % 2 == 1:
                    # Нечётное число трасс, есть трасса под источником
                    receiver_x = np.arange(-(nx // 2), nx // 2 + 1) * dx
                    offsets = receiver_x
                else:
                     #Чётное число, симметрия между двумя центральными
                    receiver_x = (np.arange(nx) - (nx - 1) / 2) * dx
                    offsets = receiver_x

            #print("Первые 5 выносов:", offsets[:5])
            #print("Последние 5 выносов:", offsets[-5:])
    # @staticmethod
    # def read(filepath, dx=30.0):
    #     with sio.open(filepath, "r", strict=False) as seg_file:
    #         gather = np.stack([seg_file.trace[i] for i in range(seg_file.tracecount)]).T
    #
    #         source_x = []
    #         group_x = []
    #         for i in range(seg_file.tracecount):
    #             header = seg_file.header[i]
    #             src_x = header[sio.TraceField.SourceX]
    #             grp_x = header[sio.TraceField.GroupX]
    #             source_x.append(src_x)
    #             group_x.append(grp_x)
    #
    #         source_x = np.array(source_x)
    #         group_x = np.array(group_x)
    #
    #         offsets = np.abs(group_x - source_x)
    #
    #         dt = seg_file.bin[sio.BinField.Interval] / 1_000_000.0  # микросек → сек

            return SegYData(
                data=gather,
                offsets=offsets,
                dt=dt
            )