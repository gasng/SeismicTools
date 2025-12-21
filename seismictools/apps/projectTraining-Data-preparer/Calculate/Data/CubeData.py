import numpy as np

class CubeData:
    def __init__(self):
        self.data = None  # 3D array: [inline, xline, time]
        self.inline_range = None
        self.xline_range = None
        self.time_range = None
        self.filename = None

    def set_data(self, data, inline_range, xline_range, time_range, filename=""):
        self.data = data
        self.inline_range = inline_range
        self.xline_range = xline_range
        self.time_range = time_range
        self.filename = filename

    def get_slice(self, time_index):
        #Получить временной срез по индексу времени
        if self.data is not None and time_index < self.data.shape[2]:
            return self.data[:, :, time_index]
        return None

    def get_trace(self, inline_idx, xline_idx):
        #Получить трассу по индексам inline/xline
        if self.data is not None:
            return self.data[inline_idx, xline_idx, :]
        return None

    def get_coordinates(self, inline_idx, xline_idx):
        #Получить физические координаты (Inline, Xline)
        inline_val = self.inline_range[0] + inline_idx * (self.inline_range[1] - self.inline_range[0]) / (self.data.shape[0] - 1)
        xline_val = self.xline_range[0] + xline_idx * (self.xline_range[1] - self.xline_range[0]) / (self.data.shape[1] - 1)
        return inline_val, xline_val

    def get_time_value(self, time_idx):
        #Получить значение времени в мс по индексу
        dt = (self.time_range[1] - self.time_range[0]) / (self.data.shape[2] - 1)
        return self.time_range[0] + time_idx * dt

    def shape(self):
        return self.data.shape if self.data is not None else (0, 0, 0)