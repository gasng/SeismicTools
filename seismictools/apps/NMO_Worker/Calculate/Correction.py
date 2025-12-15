import numpy as np
from scipy.interpolate import interp1d

class Correction:
    def __init__(self, data, law, offsets, dt):
        """
        :param data:    ndarray (nt, nx) — исходный gather
        :param law:     ndarray (nt,)   — скоростной закон v(t0)
        :param offsets: ndarray (nx,)   — выносы (в метрах)
        :param dt:      float           — шаг по времени (в секундах)
        """
        self.data = data
        self.law = law
        self.offsets = offsets
        self.dt = dt

    def calculate_correction(self):
        nt, nx = self.data.shape
        times = np.arange(nt) * self.dt  # (nt,)

        # Результирующий массив — NMO-скорректированный gather
        corrected = np.zeros_like(self.data)

        # Создаём интерполяторы для каждой трассы
        interpolators = []
        for i in range(nx):
            # Интерполяция по времени: избегаем выхода за границы → fill_value=0
            f = interp1d(times, self.data[:, i], kind='linear',
                         fill_value=0.0, bounds_error=False)
            interpolators.append(f)

        # Для каждой точки t0 и каждой трассы — применяем NMO
        for i, t0 in enumerate(times):
            if t0 <= 0:
                continue  # пропускаем t0 = 0
            v = self.law[i]  # скорость для данного t0
            if v <= 0:
                continue  # избегаем деления на ноль

            # Теоретическое время на каждой трассе для этого (t0, v)
            t_src = np.sqrt(t0**2 + (self.offsets / v)**2)  # (nx,)

            # Берём амплитуды из исходных трасс в этих временах
            for j in range(nx):
                corrected[i, j] = interpolators[j](t_src[j])

        return corrected
