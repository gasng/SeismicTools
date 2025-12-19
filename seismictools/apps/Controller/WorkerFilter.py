from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from seismictools.apps.Calculate.Processing.Filter import BandPassFilter

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
    def __init__(self, data, low_freq, high_freq, fs, order=4):
        super().__init__()
        self.data = data
        self.low_freq = low_freq
        self.high_freq = high_freq
        self.fs = fs
        self.order = order
        self.signals = WorkerSignals()

    def run(self):
        """
        Проходит по всем трассам (iline, xline), применяет полосовой фильтр
        к каждому одномерному временному разрезу и собирает результат в новый куб.
        """
        try:
            bp_filter = BandPassFilter(
                type_filter='bandpass',
                freq=(self.low_freq, self.high_freq),
                fs=self.fs,
                order=self.order
            )
            # Тут будем хранить наш результат
            filtered_data = np.zeros_like(self.data, dtype=np.float64)

            # Ищем общее количество трасс для расчёта прогресса
            n_ilines, n_xlines, n_samples = self.data.shape
            total_traces = n_ilines * n_xlines
            processed = 0
            for i in range(n_ilines):
                for j in range(n_xlines):
                    # Сделаем временной разрез
                    trace = self.data[i, j, :]
                    filtered_trace = bp_filter.filter(trace)
                    filtered_data[i, j, :] = filtered_trace

                    # Обновляем прогресс (взял для примера в 100 трасс)
                    processed += 1
                    if processed % 100 == 0 or processed == total_traces:
                        progress_percent = int(processed / total_traces * 100)
                        self.signals.progress.emit(progress_percent)

            msg = 'Filtering complete: ' + total_traces + ' traces processed'
            self.signals.message.emit(msg)
            self.signals.result.emit(filtered_data)

        except Exception as exc:
            error_msg = "Filtering error: " + str(exc)
            self.signals.error.emit(error_msg)
            self.signals.result.emit(None)
        finally:
            self.signals.finished.emit()