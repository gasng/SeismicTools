from PyQt5 import QtWidgets, QtCore, QtGui
from ..Settings.SettingsWidget import Ui_GridWorkerWindow
from seismictools.apps.GridWorker.Calculate.Reader.GrdReader import read_grd_file
from seismictools.apps.GridWorker.Calculate.Data.PoligonData import PointManager
from seismictools.apps.GridWorker.Calculate.Data.GridData import MapRenderer
from seismictools.apps.GridWorker.Calculate.Data.ObjectList import ObjectListManager
from seismictools.apps.GridWorker.Controller.WorkerSaver import WorkerSaver
from seismictools.apps.GridWorker.Controller.SessionManager import SessionManager
import pyqtgraph as pg
import os

pg.setConfigOption('imageAxisOrder', 'row-major')
class ViewWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GridWorkerWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        # Заменяем QGraphicsView на PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')

        # Заменяем виджет в layout
        self.ui.horizontalLayout.replaceWidget(self.ui.label_map, self.plot_widget)
        self.ui.label_map.deleteLater()
        self.ui.label_map = self.plot_widget

        # Подключение кнопок "Загрузить", "Очистить","Добавить объект" и "Сохранить"
        self.ui.pushButton_load.clicked.connect(self.load_file)
        self.ui.pushButton_clear.clicked.connect(self.clear_file)
        self.ui.pushButton_addObject.clicked.connect(self.add_object)
        self.ui.pushButton_save.clicked.connect(self.save_selected_objects)

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
        self.session_manager = SessionManager(
            session_file="session.json",
            message_callback=self.update_status
        )

        # Инициализируем менеджер сессии
        self.session_manager = SessionManager()

        # Загружаем сохранённую сессию при старте
        self._load_session()

        # Подключаем обработчик закрытия окна
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.grid_data = None

    def _load_session(self):
        """
            Функция восстанавливает сессию при запуске приложения
        """
        session = self.session_manager.load_session()
        if not session:
            return

        file_path = session.get('file_path')
        objects = session.get('objects', [])

        # Загружаем карту
        if file_path and os.path.exists(file_path):
            try:
                self.ui.lineEdit_filePath.setText(file_path)

                # Загружаем данные
                self.grid_data = read_grd_file(file_path)
                self.original_data = self.grid_data.copy()

                # Устанавливаем метаданные
                self.metadata = {
                    'xllcorner': 0.0,
                    'yllcorner': 0.0,
                    'cellsize': 1.0
                }

                self.map_renderer.display_heatmap(self.grid_data)

                # Восстанавливаем объекты
                for obj in objects:
                    name = obj.get('name', 'Без имени')
                    obj_type = obj.get('type', 'other')
                    polygon = obj.get('polygon', [])

                    if len(polygon) >= 3:
                        self.object_list_manager.add_object(name, obj_type, polygon)

                        color_map = {"channel": (0, 0, 255), "bar": (255, 0, 0), "other": (0, 255, 0)}
                        color = color_map.get(obj_type, (0, 255, 0))
                        self.point_manager.add_saved_polygon(polygon, color=color)

                self.status_label.setText(f"Восстановлено объектов: {len(objects)}")
            except Exception as e:
                self.status_label.setText(f"Ошибка восстановления: {str(e)}")
        else:
            self.status_label.setText("Файл карты не найден. Объекты не могут быть отображены.")

    def closeEvent(self, event):
        """
            Функция сохраняет сессию при закрытии приложения
            Данные сохраняются в файл 'session.json' в корневой директории проекта
            event: QCloseEvent — событие закрытия окна
        """
        objects = []
        for i in range(self.ui.listWidget_objects.count()):
            item = self.ui.listWidget_objects.item(i)
            data = item.data(QtCore.Qt.UserRole)
            # Проверяем, что данные валидны
            if data and 'polygon' in data and len(data['polygon']) >= 3:
                objects.append(data)

        # Сохраняем путь к файлу
        file_path = self.ui.lineEdit_filePath.text()
        if file_path and os.path.exists(file_path):
            self.session_manager.save_session(file_path=file_path, objects=objects)
        else:
            self.session_manager.save_session(objects=objects)

        event.accept()

    def update_status(self, message: str):
        """
            Функция, принимающая информацию о сообщениях, передаваемых в StatusBar
            message: Текст сообщения для отображения
        """
        self.status_label.setText(message)

    def load_file(self):
        """
            Функция загрузки пути до файла через кнопку "Загрузить"
            - Открывает проводник для выбора файла
            - Читает данные с помощью GrdReader
            - Отображает карту через MapRenderer
            - Обновляет строку состояния
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
                self.metadata = {
                    'xllcorner': 0.0,
                    'yllcorner': 0.0,
                    'cellsize': 1.0
                }
                self.map_renderer.display_heatmap(self.grid_data)
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
            - Очищает текущий полигон
            - Обновляет строку состояния с инструкцией
        """
        # Сбрасываем текущий полигон
        self.point_manager.clear_current_polygon()

        # Обновляем статус
        self.status_label.setText("Режим выделения: кликайте по карте, двойной клик — завершить")

    def on_polygon_completed(self):
        """
            Функция, вызываемая после замыкания полигона
            - Получает координаты замкнутого полигона
            - Открывает диалог ввода имени объекта
        """
        polygon = self.point_manager.get_polygon()
        if polygon:
            self.show_polygon_dialog(polygon)

    def show_polygon_dialog(self, polygon):
        """
            Функция ввода имени объекта в диалоговое окно
            polygon: Список координат замкнутого полигона
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
            self.point_manager.clear_current_polygon()
            self.status_label.setText("Выделение отменено")

    def add_object_to_list(self, name, obj_type, polygon):
        """
            Функция добавляет объект в список и отображает его на карте
            name: Имя объекта
            obj_type: Тип объекта
            polygon: Список координат полигона
        """
        self.object_list_manager.add_object(name, obj_type, polygon)

        # Определяем цвет
        color_map = {"channel": (0, 0, 255), "bar": (255, 0, 0), "other": (0, 255, 0)}
        color = color_map.get(obj_type, (0, 255, 0))

        # Рисуем на карте
        self.point_manager.add_saved_polygon(polygon, color=color)

    def delete_selected_objects(self):
        """
            Фунция удаляет отмеченные объекты ИЗ списка и с карты
        """
        # Собираем индексы для удаления (в прямом порядке для сохранения соответствия)
        indices_to_remove = []
        for i in range(self.ui.listWidget_objects.count()):
            item = self.ui.listWidget_objects.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                indices_to_remove.append(i)

        if not indices_to_remove:
            self.status_label.setText("Нет отмеченных объектов для удаления")
            return

        # Удаляем с конца, чтобы индексы не сбивались
        for index in reversed(indices_to_remove):
            # Удаляем из списка
            self.ui.listWidget_objects.takeItem(index)

            # Удаляем с карты
            if index < len(self.point_manager.saved_polygon_items):
                # Удаляем графический элемент
                item_to_remove = self.point_manager.saved_polygon_items.pop(index)
                self.point_manager.plot_widget.removeItem(item_to_remove)
                # Удаляем данные
                self.point_manager.saved_polygons.pop(index)

        self.status_label.setText(f"Удалено объектов: {len(indices_to_remove)}")

    def show_context_menu(self, pos):
        """
            Фунция показывает контекстное меню при правом клике на списке объектов
            pos: Позиция клика относительно списка
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
            Функция полной очистки приложения через кнопку "Очистить"
        """
        self.ui.lineEdit_filePath.clear()
        self.grid_data = None
        self.map_renderer.clear()  # Очищаем карту
        self.point_manager.clear_all()  # Очищаем все полигоны
        self.object_list_manager.clear_all()  # Очищаем список "ТЕКУЩИЕ ОБЪЕКТЫ"
        self.status_label.setText("Файл удален, карта и добавленные объекты очищены")

    def save_selected_objects(self):
        """
            Функция сохраняет выделенные объекты
        """
        # Получаем выделенные объекты
        selected_objects = self.object_list_manager.get_selected_objects()

        # Создаём контроллер сохранения
        saver = WorkerSaver(self.grid_data, self.metadata)  # metadata нужно хранить при загрузке

        # Получаем путь
        file_path = saver.get_save_path(self)
        if not file_path:
            return

        # Сохраняем
        if saver.save_selected_objects(self, selected_objects, file_path):
            self.status_label.setText(f"Сохранено: {len(selected_objects)} объектов")

            # Спрашиваем о загрузке
            reply = QtWidgets.QMessageBox.question(
                self, "Загрузить файл?", "Файл сохранён. Загрузить его?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.load_saved_file(file_path)
        else:
            self.status_label.setText("Ошибка сохранения")

    def load_saved_file(self, file_path):
        """
            Фунция загружает сохранённый файл
        """
        try:
            self.grid_data = read_grd_file(file_path)
            self.ui.lineEdit_filePath.setText(file_path)
            self.map_renderer.display_heatmap(self.grid_data)
            self.point_manager.clear_all()
            self.object_list_manager.clear_all()
            self.status_label.setText("Сохранённый файл загружен")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))