import numpy as np
from scipy.signal import butter, filtfilt

class BandPassFilter:
    def __init__(self, type_filter, freq, fs, order=4):
        """
        Инициализация полосового фильтра Баттерворта.
        Выбран фильтр Баттерворта, так как он сохраняет форму сигнала
        и рабоате быстрее аналогов (оконный фильтр).
        _____________________________________________
        Параметры:
            type_filter - тип данных "str", значения: 'lowpass', 'highpass' или 'bandpass'
            freq - тип данных "float" или "tuple":
                - для lowpass/highpass будет "float" (выбираем только одну частоту)
                - для bandpass будет "tuple" (low, high) (выбираем диапазон частот)
            fs - тип данных "float": частота дискретизации (Гц)
            order - тип данных "int": порядок фильтра (по умолчанию 4, а затем пользователь сам выбирает)
        """
        self.type_filter = type_filter
        self.freq = freq
        self.fs = fs
        self.order = order

        nyquist = 0.5 * fs #нормируем частоту среза (Nyquist = fs/2)
        try:
            if self.type_filter == 'bandpass':
                low, high = freq
                if low <= 0 or high <= 0:
                    raise ValueError("The frequencies must be positive")
                if low >= high:
                    raise ValueError("low should be < high")
                if high >= nyquist:
                    raise ValueError("Upper frequency >= Nyquist frequency (normalized frequency)")
                Win_num = [low / nyquist, high / nyquist]
                btype = 'band'
            else:
                cutoff = float(freq)
                if cutoff <= 0:
                    raise ValueError("The cutoff frequency should be positive")
                if cutoff >= nyquist:
                    raise ValueError("The cutoff frequency >= Nyquist frequency (normalized frequency)")
                Win_num = cutoff / nyquist
                btype = type_filter

            self.b, self.a = butter(order, Win_num, btype=btype) # noinspection PyUnresolvedReferences
        except (TypeError, ValueError) as exc:
            if type_filter == 'bandpass':
                raise ValueError("For bandpass, specify freq as a pair of numbers: (low, high), for example (10, 60)") from exc
            else:
                raise ValueError(f"For {type_filter}, specify freq as a single number, for example 50.0") from exc

    def apply(self, data):
        if data.ndim != 1:
            raise ValueError("A one-dimensional array is expected")
        if len(data) < self.order * 3:
            raise ValueError("The signal is too short for the specified filter order")
        return filtfilt(self.b, self.a, data)