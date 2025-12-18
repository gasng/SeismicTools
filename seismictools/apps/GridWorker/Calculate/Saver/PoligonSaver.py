import numpy as np
def save_grd_file(file_path: str, data: np.ndarray, metadata: dict = None):
    """
         Функия сохраняет массив данных в формат GRD
    """
    nrows, ncols = data.shape

    # Определяем метаданные
    if metadata is None:
        metadata = {
            'xllcorner': 0.0,
            'yllcorner': 0.0,
            'cellsize': 1.0
        }

    cellsize = metadata.get('cellsize', 1.0)
    xll = metadata.get('xllcorner', 0.0)
    yll = metadata.get('yllcorner', 0.0)

    # Вычисляем верхний правый угол
    xur = xll + ncols * cellsize
    yur = yll + nrows * cellsize

    # Обрабатываем NaN для min/max
    valid_data = data[np.isfinite(data)]
    if len(valid_data) > 0:
        zmin, zmax = np.nanmin(valid_data), np.nanmax(valid_data)
    else:
        zmin, zmax = 0.0, 0.0

    with open(file_path, 'w') as f:
        f.write("DSAA\n")
        f.write(f"{ncols} {nrows}\n")
        f.write(f"{xll} {yll}\n")
        f.write(f"{xur} {yur}\n")
        f.write(f"{zmin} {zmax}\n")

        # Сохраняем данные построчно
        for row in data:
            # Заменяем NaN на очень большое число
            row_str = " ".join([f"{x:.6f}" if np.isfinite(x) else "1e30" for x in row])
            f.write(row_str + "\n")