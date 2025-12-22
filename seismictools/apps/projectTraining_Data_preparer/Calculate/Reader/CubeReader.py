import segyio
import numpy as np

def read_segy_cube(filename):
    try:
        # Читаем куб
        cube = segyio.tools.cube(filename)

        # Получаем координаты
        with segyio.open(filename, "r") as f:
            inlines = f.ilines
            xlines = f.xlines
            samples = f.samples

            # Проверяем совпадение размеров
            if cube.shape[0] != len(inlines) or cube.shape[1] != len(xlines) or cube.shape[2] != len(samples):
                raise ValueError("Размеры куба не совпадают с метаданными")

        inline_range = (inlines[0], inlines[-1])
        xline_range = (xlines[0], xlines[-1])
        time_range = (samples[0], samples[-1])

        return cube.astype(np.float32), inline_range, xline_range, time_range

    except Exception as e:
        raise ValueError(f"Ошибка при чтении SEGY-файла: {e}")