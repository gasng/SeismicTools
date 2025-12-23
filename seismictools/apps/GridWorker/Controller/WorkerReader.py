from seismictools.apps.GridWorker.Calculate.Reader.GrdReader import read_grd_file
import numpy as np
class WorkerReader:
    def __init__(self):
        self.data = None
        self.file_path = None

    def load_file(self, file_path: str):
        """
            Загружает .grd файл.
            file_path: путь к файлу
            return: True — успех, False — ошибка
        """
        try:
            self.data = read_grd_file(file_path)
            self.file_path = file_path
            return True
        except Exception as e:
            print(f"Ошибка в WorkerReader: {e}")
            return False

    def get_data(self):
        """
            Функция возвращает загруженные данные
        """
        return self.data

    def is_loaded(self):
        """
            Фунция проверяет, загружены ли данные
        """
        return self.data is not None

