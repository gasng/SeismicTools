import numpy as np

class WorkerVisualization:

    def __init__(self, cube_data):
        self.cube_data = cube_data

    def get_slice_data(self, time_index):
        #Возвращает временной срез и заголовок
        slice_data = self.cube_data.get_slice(time_index)
        if slice_data is not None:
            time_ms = self.cube_data.get_time_value(time_index)
            title = f"Временной срез: {time_ms:.0f} мс"
            return slice_data, title
        return None, ""

    def get_trace_data(self, inline_idx, xline_idx):
        #Возвращает трассу, её номер и координаты
        trace_data = self.cube_data.get_trace(inline_idx, xline_idx)
        if trace_data is not None:
            coords = self.cube_data.get_coordinates(inline_idx, xline_idx)
            trace_id = f"{inline_idx}_{xline_idx}"
            return trace_data, trace_id, coords
        return None, None, None