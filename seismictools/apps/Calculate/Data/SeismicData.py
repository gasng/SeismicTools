import segyio
import os

class DataSeismic:
    def __init__(self):
        """
        Создаём пустой объект для загрузки сейсмических данных.
        """
        self.data = None
        self.file_path = None

    def load_segy(self, file_path):
        """
        Создаем функцию, для загрузки файла из путя, который предоставит пользователь
        приложения.
        Дополнительно, проверяем на наличие всех ошибок, в плане наличие файла, его чтения и т.п.
        На выход идет только путь к файлу с данными, на выход получаем данные, загруженные в наше
        приложение.
        """
        self.file_path = file_path

        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found:", file_path)

        try:
            self.data = segyio.tools.cube(file_path)

        except OSError as exc:
            raise OSError("The SEGY file cannot be read or is corrupted:", exc)
        except ValueError as exc:
            raise ValueError("It is not possible to upload data as a 3D cube:", exc)

        return self.data