from PySide6.QtCore import QObject, Signal, QRunnable
from seismictools.apps.Seismic_Filtering_BP.Calculate.Processing.Filter import BandPassFilter

import numpy as np

class WorkerSignals(QObject):
    """
    finished - работа завершена
    error - произошла ошибка (текстовое сообщение)
    progress - прогресс выполнения в процентах [0-100]
    message - какаое-то информационное сообщение
    result - результат (отфильтрованные данные)

    Это сигналы, нужны для обмена данными между фоновым потоком и основным потоком.
    """
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)
    message = Signal(str)
    result = Signal(object)

class WorkerFilter(QRunnable):
    """
    Воркер для применения полосового фильтра к сейсмическим данным в фоновом потоке.
    Обрабатывает трассы по одной, чтобы показывать прогресс и не блокировать окно запуска программы.
    """
    def __init__(self, data, type_filter, low_freq, high_freq, fs, order=4):
        super().__init__()
        self.data = data
        self.type_filter = type_filter
        self.low_freq = low_freq
        self.high_freq = high_freq
        self.fs = fs
        self.order = order
        self.signals = WorkerSignals()

    def run(self):
        """
        Проходит по всем трассам (номер трассы, время).
        Применяет заданный цифровой фильтр (bandpass/lowpass/highpass) ко всем трассам
        во входном массиве self.data и возвращает отфильтрованный результат через сигналы.
        """
        freq = None #изначально ничему не равно, так как получим значение от пользователя
        try:
            try:
                if self.type_filter == 'bandpass':
                    freq = (float(self.low_freq), float(self.high_freq))
                elif self.type_filter == 'lowpass':
                    freq = float(self.high_freq)
                elif self.type_filter == 'highpass':
                    freq = float(self.low_freq)
            except ValueError as exc:
                raise ValueError(f"Invalid frequency value: {exc}")

            bp_filter = BandPassFilter(
                type_filter=self.type_filter,
                freq=freq,
                fs=self.fs,
                order=self.order
            )

            filtered_data = np.zeros_like(self.data, dtype=np.float64) # переменная для хранения результата, должно быть размером с нашим исходным сигналом

            n_traces = self.data.shape[0]

            for i in range(n_traces):
                trace = self.data[i, :]
                filtered_trace = bp_filter.filter(trace)
                filtered_data[i, :] = filtered_trace

                if i % 100 == 99 or i == n_traces - 1: # обновляем прогресс (взял для примера в 100 трасс) - чтобы не перегружать основной поток
                                                       # проще говоря - ограничиваем частоту обновления
                    self.signals.progress.emit(int(100 * (i + 1) / n_traces))

            self.signals.message.emit(f'Filtering complete: {n_traces} traces processed')
            self.signals.result.emit(filtered_data)

        except Exception as exc:
            self.signals.error.emit(f'Filtering error {str(exc)}')
            self.signals.result.emit(None)
        finally:
            self.signals.finished.emit()