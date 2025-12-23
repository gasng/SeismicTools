import numpy as np
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

        if self.offsets is None or len(self.offsets) != nx:
            raise ValueError("offsets must be array of length nx")

        for j, v in enumerate(velocities):
            t_vals = np.sqrt(times[:, None] ** 2 + (self.offsets[None, :] / v) ** 2)
            amplitudes = np.zeros_like(t_vals)
            for i in range(nx):

                amplitudes[:, i] = np.interp(
                    t_vals[:, i],
                    times,
                    self.data[:, i],
                    left=0.0,
                    right=0.0
                )

            spectrum[:, j] = np.sum(amplitudes, axis=1)


        self.spectrum = spectrum
        print("hhhh", spectrum.shape)
        return spectrum