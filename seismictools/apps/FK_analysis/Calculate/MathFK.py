import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift


def forward_fk(data: np.ndarray) -> np.ndarray:
    """
    Выполняет 2D FFT: время в частоту, трассы в волновое число (k).
    Возвращает FK-спектр.

    :param data: Массив [трассы, время]
    :return: FK-спектр
    """
    if data.ndim != 2:
        raise ValueError("Данные должны быть 2D (трассы и время)")

    fk = fft2(data)
    fk_shifted = fftshift(fk)

    return fk_shifted

def inverse_fk(fk_spectrum: np.ndarray):
    """
    Выполняет 2D IFFT: частоту во время, волновое число (k) в трассы.
    Возвращает изначальный сигнал.

    :param fk_spectrum: Массив [значение k, значение частоты]
    :return: Изначальный сигнал
    """

    if fk_spectrum.ndim != 2:
        raise ValueError("FK-спектр должен быть 2D")

    fk_unshifted = ifftshift(fk_spectrum)
    data = ifft2(fk_unshifted)

    return np.real(data)