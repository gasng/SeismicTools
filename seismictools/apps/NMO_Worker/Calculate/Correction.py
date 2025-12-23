import numpy as np
from numba import njit, prange


@njit()
def nmo_correction_numba(data, law, offsets, dt):

    nt, nx = data.shape
    corrected = np.zeros_like(data)
    times = np.arange(nt) * dt

    for i in prange(nt):
        t0 = times[i]
        if t0 <= 0.0:
            continue
        v = law[i]
        if v <= 0.0:
            continue

        t_src = np.sqrt(t0 * t0 + (offsets / v) ** 2)  # (nx,)

        for j in range(nx):
            t = t_src[j]

            if t <= 0.0:
                amp = data[0, j]
            elif t >= times[-1]:
                amp = data[-1, j]
            else:
                idx = int(t / dt)
                if idx >= nt - 1:
                    amp = data[-1, j]
                else:
                    t0_idx = times[idx]
                    t1_idx = times[idx + 1]
                    if t1_idx == t0_idx:
                        amp = data[idx, j]
                    else:
                        w = (t - t0_idx) / (t1_idx - t0_idx)
                        amp = data[idx, j] * (1 - w) + data[idx + 1, j] * w

            corrected[i, j] = amp

    return corrected


class Correction:
    def __init__(self, data, law, offsets, dt):
        self.data = data
        self.law = law
        self.offsets = offsets
        self.dt = dt

    def calculate_correction(self):
        data = np.asarray(self.data, dtype=np.float64)
        law = np.asarray(self.law, dtype=np.float64)
        offsets = np.asarray(self.offsets, dtype=np.float64)
        dt = float(self.dt)

        corrected = nmo_correction_numba(data, law, offsets, dt)
        return corrected