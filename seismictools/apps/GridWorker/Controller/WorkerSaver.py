from PyQt5 import QtWidgets
from ..Calculate.Saver.PoligonSaver import save_grd_file
from ..Calculate.Data.PolygonUtils import create_masked_array
import os

class WorkerSaver:
    def __init__(self, original_array, metadata=None):
        self.original_array = original_array
        self.metadata = metadata or {
            'xllcorner': 0.0,
            'yllcorner': 0.0,
            'cellsize': 1.0
        }

    def save_selected_objects(self, parent_widget, selected_objects, file_path):
        """
            Функция сохраняет выделенные объекты в GRD-файл

        """
        if self.original_array is None:
            self.show_error(parent_widget, "Нет загруженной карты")
            return False

        if not selected_objects:
            self.show_error(parent_widget, "Нет отмеченных объектов")
            return False

        try:
            # Извлекаем полигоны
            polygons = [obj['polygon'] for obj in selected_objects]

            # Создаём маскированный массив
            masked_array = create_masked_array(self.original_array, polygons)

            if masked_array is None:
                self.show_error(parent_widget, "Ошибка создания массива")
                return False

            # Сохраняем файл
            save_grd_file(file_path, masked_array, self.metadata)
            return True

        except Exception as e:
            self.show_error(parent_widget, f"Ошибка сохранения:\n{str(e)}")
            return False

    def get_save_path(self, parent) -> str:
        """
            Функция открывает диалог выбора пути
        """
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent, "Сохранить выделенные объекты", "", "GRD Files (*.grd)"
        )
        return path + '.grd' if path and not path.endswith('.grd') else path

    def show_error(self, parent, message):
        """
            Функция для вывода ошибки
        """
        QtWidgets.QMessageBox.critical(parent, "Ошибка", message)

