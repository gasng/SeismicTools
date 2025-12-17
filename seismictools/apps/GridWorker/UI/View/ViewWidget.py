from PyQt5 import QtWidgets, QtCore
from ..Settings.SettingsWidget import Ui_GridWorkerWindow
from seismictools.apps.GridWorker.Calculate.Reader.GrdReader import read_grd_file
from seismictools.apps.GridWorker.Calculate.Data.PoligonData import PointManager
from seismictools.apps.GridWorker.Calculate.Data.GridData import MapRenderer
from seismictools.apps.GridWorker.Calculate.Data.ObjectList import ObjectListManager
import numpy as np
import pyqtgraph as pg

pg.setConfigOption('imageAxisOrder', 'row-major')
class ViewWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GridWorkerWindow()
        self.ui.setupUi(self)

        # Заменяем QGraphicsView на PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')

        # Заменяем виджет в layout
        self.ui.horizontalLayout.replaceWidget(self.ui.label_map, self.plot_widget)
        self.ui.label_map.deleteLater()
        self.ui.label_map = self.plot_widget

        # Подключение кнопок "Загрузкить", "Очистить" и "Добавить объект"
        self.ui.pushButton_load.clicked.connect(self.load_file)
        self.ui.pushButton_clear.clicked.connect(self.clear_file)
        self.ui.pushButton_addObject.clicked.connect(self.add_object)

        # Подключение контекстного меню для удаления выделенных объектов
        self.ui.listWidget_objects.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.listWidget_objects.customContextMenuRequested.connect(self.show_context_menu)

        # Инициализируем менеджеры точек, отрисовки карты и добавления выделенных объктов
        self.map_renderer = MapRenderer(self.plot_widget)
        self.point_manager = PointManager(self.plot_widget)
        self.object_list_manager = ObjectListManager(self.ui.listWidget_objects)

        # Подключение строки состояния для постоянных сообщений
        self.point_manager = PointManager(self.plot_widget)
        self.status_label = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.status_label)

        # Информация о сообщениях в строку состояния из других файлов
        self.point_manager.status_message.connect(self.update_status)
        self.point_manager.polygon_completed.connect(self.on_polygon_completed)

        self.grid_data = None

    def update_status(self, message: str):
        """
            Функция, принимающая информацию о сообщениях, передаваемых в StatusBar
        """
        self.status_label.setText(message)

    def load_file(self):
        """
            Функция загрузки пути до файла через кнопку "Загрузить" и отрисовки карты
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите файл карты",
            "",
            "GRD Files (*.grd);;All Files (*)"
        )
        if file_path:
            self.ui.lineEdit_filePath.setText(file_path)
            try:
                self.grid_data = read_grd_file(file_path)
                self.map_renderer.display_heatmap(self.grid_data)
                self.status_label.setText(f"Файл загружен. Размер массива: {self.grid_data.shape}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
                self.status_label.setText("Ошибка загрузки")
                self.grid_data = None
        else:
            self.status_label.setText("Файл не выбран")

    def add_object(self):
        """
            Функция обработки кнопки 'Добавить объект'
        """
        # Сбрасываем текущий полигон (если есть)
        self.point_manager.clear_points()

        # Обновляем статус
        self.status_label.setText("Режим выделения: кликайте по карте, двойной клик — завершить")

    def on_polygon_completed(self):
        """
            Функция, вызываемая после замыкания полигона
        """
        polygon = self.point_manager.get_polygon()
        if polygon:
            self.show_polygon_dialog(polygon)

    def show_polygon_dialog(self, polygon):
        """
            Функция ввода имени объекта в диалоговое окно
        """
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Новый объект")
        dialog.setModal(True)
        dialog.resize(300, 150)

        layout = QtWidgets.QVBoxLayout()
        name_label = QtWidgets.QLabel("Имя объекта:")
        name_input = QtWidgets.QLineEdit()
        name_input.setPlaceholderText("Введите название")
        type_label = QtWidgets.QLabel("Тип объекта:")
        type_combo = QtWidgets.QComboBox()
        type_combo.addItems(["channel", "bar", "other"])

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(name_label)
        layout.addWidget(name_input)
        layout.addWidget(type_label)
        layout.addWidget(type_combo)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name = name_input.text().strip()
            obj_type = type_combo.currentText()
            if not name:
                self.status_label.setText("Ошибка: имя не может быть пустым")
                return
            self.add_object_to_list(name, obj_type, polygon)
            self.status_label.setText(f"Объект '{name}' добавлен")
        else:
            # Отмена — сбрасываем полигон
            self.point_manager.clear_points()
            self.status_label.setText("Выделение отменено")

    def add_object_to_list(self, name, obj_type, polygon):
        """
            Функция добавляет объект в список через менеджер
        """
        self.object_list_manager.add_object(name, obj_type, polygon)

    def delete_selected_objects(self):
        """
            Функция удаляет отмеченные объекты
        """
        count = self.object_list_manager.delete_selected()
        if count > 0:
            self.status_label.setText(f"Удалено объектов: {count}")
        else:
            self.status_label.setText("Нет отмеченных объектов для удаления")

    def show_context_menu(self, pos):
        """
            Показывает контекстное меню при правом клике на списке объектов
        """
        # Проверяем, есть ли хоть один отмеченный объект
        has_checked = False
        for i in range(self.ui.listWidget_objects.count()):
            item = self.ui.listWidget_objects.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                has_checked = True
                break

        # Создаём меню
        menu = QtWidgets.QMenu(self)

        if has_checked:
            delete_action = menu.addAction("Удалить отмеченные")
        else:
            delete_action = menu.addAction("Удалить отмеченные")
            delete_action.setEnabled(False)  # Делаем неактивным, если нет отмеченных

        # Показываем меню в глобальных координатах
        global_pos = self.ui.listWidget_objects.mapToGlobal(pos)
        action = menu.exec_(global_pos)

        # Если выбрано удаление
        if action == delete_action and has_checked:
            self.delete_selected_objects()

    def clear_file(self):
        """
            Функция очистки строки, отображающей путь до файла, удаление отрисованной карты и выделенных полигонов, через кнопку "Очистить"
        """
        self.ui.lineEdit_filePath.clear()
        self.grid_data = None
        self.map_renderer.clear()  # Очищаем карту
        self.point_manager.clear_points()  # Очищаем точки
        self.object_list_manager.clear_all()  # Очищаем список "ТЕКУЩИЕ ОБЪЕКТЫ"
        self.status_label.setText("Файл удален, карта и добавленные объекты очищены")
