import segyio as sio
import numpy as np
from dataclasses import dataclass
from seismictools.apps.First_Break_Picker.Calculate.Data.SeismicData import SegYData


class SegYReader:
    @staticmethod
    def read(filepath: str) -> SegYData:
        try:
            with sio.open(filepath, ignore_geometry=True) as f:
                tracecount = f.tracecount
                samples = f.samples / 1000
                dt = samples[1]
                gather = np.zeros((len(samples), tracecount))

                for i, trace in enumerate(f.trace):
                    gather[:, i] = trace
            return SegYData(data=gather)



        except Exception as e:
            raise RuntimeError(f"Ошибка при чтении {filepath}: {str(e)}")