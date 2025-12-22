from PySide6.QtCore import QObject, Signal
from seismictools.apps.projectTraining_Data_preparer.Calculate.Reader.CubeReader import read_segy_cube
from seismictools.apps.projectTraining_Data_preparer.Calculate.Data.CubeData import CubeData

class WorkerReader(QObject):
    finished = Signal(object)  # CubeData instance
    error = Signal(str)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        try:
            data, inline_range, xline_range, time_range = read_segy_cube(self.filepath)
            cube = CubeData()
            cube.set_data(data, inline_range, xline_range, time_range, self.filepath)
            self.finished.emit(cube)
        except Exception as e:
            self.error.emit(str(e))