import numpy as np

def read_grd_file(file_path):
    """
    Функция чтения .grd файла и преобразование его в numpy массив.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Извлекаем размеры массива из второй строки
    dims = lines[1].strip().split()
    n_rows = int(dims[1])
    n_cols = int(dims[0])

    # Извлекаем числовые данные, начиная с 6-й строки (после заголовков)
    data_lines = lines[5:]

    # Преобразуем все строки в список чисел
    data = []
    for line in data_lines:
        data.extend([float(x) for x in line.strip().split()])

    # Преобразуем полученный список в numpy массив и изменим форму на (n_rows, n_cols)
    data_array = np.array(data).reshape(n_rows, n_cols)
    data_array[np.where(data_array > 1e5)] = np.nan
    return data_array

