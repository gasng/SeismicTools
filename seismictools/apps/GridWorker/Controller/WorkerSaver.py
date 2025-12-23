from PyQt5 import QtWidgets
from seismictools.apps.GridWorker.Calculate.Saver.PoligonSaver import save_grd_file
from seismictools.apps.GridWorker.Calculate.Data.PolygonMaska import create_masked_array


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
            Создаёт маскированный массив, где только выделенные полигоны
            содержат исходные значения, а всё остальное заменено на NaN

            parent_widget (QWidget): Родительский виджет для диалогов ошибок
            selected_objects (list): Список выделенных объектов
            file_path (str): Путь для сохранения GRD-файла

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

    def get_save_path(self, parent):
        """
            Функция открывает диалог выбора пути
            parent (QWidget): Родительский виджет
        """
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent, "Сохранить выделенные объекты", "", "GRD Files (*.grd)"
        )
        return path + '.grd' if path and not path.endswith('.grd') else path

    def show_error(self, parent, message):
        """
            Функция отображает модальное окно ошибки
            parent (QWidget): Родительский виджет
            message (str): Текст сообщения об ошибке
        """
        QtWidgets.QMessageBox.critical(parent, "Ошибка", message)