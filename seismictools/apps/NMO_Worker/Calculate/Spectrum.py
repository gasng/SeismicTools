import numpy as np
from scipy.interpolate import interp1d
from dataclasses import dataclass
def t_theor(t0, offsets, v):
    return np.sqrt(t0 ** 2 + (offsets / v) ** 2)
class Spectrum():
    def __init__(self, data, offsets, dt):
        self.data = data
        self.offsets = offsets
        self.dt = dt
        self.spectrum = None

    def calculate_spectrum(self):
        print("Тип offsets:", type(self.offsets))
        print("Мин/макс offsets:", self.offsets.min(), self.offsets.max())
        print(self.dt)
        nt, nx = self.data.shape
        times = np.arange(nt) * (self.dt)
        velocities = np.arange(100, 2500, 10)  # (nv,)
        nv = len(velocities)
        spectrum = np.zeros((nt, nv))
        print(len(self.offsets), nx)

        # Предварительно проверим данные
        if self.offsets is None or len(self.offsets) != nx:
            raise ValueError("offsets must be array of length nx")

        # Векторизованный расчёт
        for j, v in enumerate(velocities):
            # Вычисляем все времена сразу: (nt, nx)
            t_vals = np.sqrt(times[:, None] ** 2 + (self.offsets[None, :] / v) ** 2)

            # Для каждой трассы интерполируем амплитуды вдоль t_vals[:, i]
            amplitudes = np.zeros_like(t_vals)
            for i in range(nx):
                # np.interp работает быстро и векторизовано
                amplitudes[:, i] = np.interp(
                    t_vals[:, i],
                    times,
                    self.data[:, i],
                    left=0.0,
                    right=0.0
                )

            # Суммируем по трассам → (nt,)
            spectrum[:, j] = np.sum(amplitudes, axis=1)

            # Опционально: отправлять прогресс (если сигналы доступны)
            # if j % 10 == 0: print(f"Скорость {v} м/с готова")

        self.spectrum = spectrum
        print("hhhh", spectrum.shape)
        return spectrum