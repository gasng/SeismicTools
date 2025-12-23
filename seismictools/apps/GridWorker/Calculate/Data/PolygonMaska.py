import numpy as np
from matplotlib.path import Path


def create_masked_array(original_array, selected_polygons, metadata=None):
    """
        Фунция создаёт маску выделенных полигонов, где только выделенные полигоны
        содержат исходные значения, а всё остальное заменено на NaN
        original_array (numpy.ndarray): Исходный двумерный массив данных
        selected_polygons (list): Список полигонов для маскирования
        metadata (dict): Словарь с метаданными GRD-файла.
    """
    if original_array is None or not selected_polygons:
        return np.full_like(original_array, np.nan) if original_array is not None else None

    nrows, ncols = original_array.shape
    masked_array = np.full_like(original_array, np.nan, dtype=np.float32)

    # Получаем метаданные
    if metadata is None:
        metadata = {'xllcorner': 0.0, 'yllcorner': 0.0, 'cellsize': 1.0}
    xll = metadata['xllcorner']
    yll = metadata['yllcorner']
    cellsize = metadata['cellsize']

    # Генерируем координаты всех пикселей
    y_indices, x_indices = np.meshgrid(np.arange(nrows), np.arange(ncols), indexing='ij')
    points = np.column_stack((x_indices.flatten(), y_indices.flatten()))

    for polygon in selected_polygons:
        if len(polygon) < 3:
            continue

        # Преобразуем координаты полигона в индексы массива
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]

        # Конвертируем в индексы
        col_indices = ((np.array(xs) - xll) / cellsize).astype(int)
        row_indices = ((np.array(ys) - yll) / cellsize).astype(int)

        # Проверяем границы
        valid_mask = (row_indices >= 0) & (row_indices < nrows) & (col_indices >= 0) & (col_indices < ncols)
        if not np.any(valid_mask):
            continue

        # Фильтруем
        col_indices = col_indices[valid_mask]
        row_indices = row_indices[valid_mask]

        if len(col_indices) < 3:
            continue

        # Создаём путь из полигона
        poly_coords = [(col, row) for col, row in zip(col_indices, row_indices)]
        poly_path = Path(poly_coords)

        # Проверяем все точки
        mask_flat = poly_path.contains_points(points)
        mask = mask_flat.reshape(x_indices.shape)

        # Копируем значения
        masked_array[mask] = original_array[mask]

    return masked_array