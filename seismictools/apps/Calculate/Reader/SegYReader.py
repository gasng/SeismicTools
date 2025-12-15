import os
import segyio

class DataSeismic:
    """
    Класс для чтения сейсмических данных из файла формата SEG-Y.
    Не хранит данные после чтения — только предоставляет метод для загрузки.
    """
    @staticmethod
    def load_segy(file_path):
        """
        Параметры: file_path (str) - путь к файлу SEG-Y
        Возвращает: numpy.ndarray - 3D-массив данных (iline, xline, time/depth)
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found:", file_path)
        try:
            # Открываем и читаем наши данные
            data = segyio.tools.cube(file_path)
            return data
        except OSError as exc:
            raise OSError("The SEG-Y file cannot be read or is corrupted:", exc) from exc
        except ValueError as exc:
            raise ValueError("Failed to load data as a 3D cube (check file structure):", exc) from exc