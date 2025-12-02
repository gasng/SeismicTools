import segyio as sio
import numpy as np
from dataclasses import dataclass

@dataclass
class SegYData:
    data: np.ndarray


class SegYReader:
    @staticmethod
    def read(filepath):
        seg_file = sio.open(filepath, ignore_geometry=True)
        gather = np.array([seg_file.trace[i] for i in range(seg_file.tracecount)])
        return SegYData(data=gather)
