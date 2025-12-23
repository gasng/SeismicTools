from PyQt5 import QtWidgets, QtCore

class ObjectListManager:
    def __init__(self, list_widget: QtWidgets.QListWidget):
        self.list_widget = list_widget

    def add_object(self, name: str, obj_type: str, polygon: list):
        """
            Функция добавляет объект в список с чекбоксом
            name (str): Имя объекта (отображается в списке).
            obj_type (str): Тип объекта (channel/bar/other).
            polygon (list): Список координат полигона в формате
        """
        item_text = f"{name} ({obj_type})"
        item = QtWidgets.QListWidgetItem(item_text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        item.setData(QtCore.Qt.UserRole, {
            'name': name,
            'type': obj_type,
            'polygon': polygon
        })
        self.list_widget.addItem(item)

    def clear_all(self):
        """
            Функция очищает весь список объектов
        """
        self.list_widget.clear()

    def delete_selected(self):
        """
            Фукнция удаляет отмеченные галочкой объекты и возвращает количество удаленных
            Удаление происходит с конца списка к началу, чтобы избежать
            смещения индексов при последовательном удалении
        """
        indices_to_remove = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                indices_to_remove.append(i)

        for index in reversed(indices_to_remove):
            self.list_widget.takeItem(index)

        return len(indices_to_remove)

    def get_selected_objects(self):
        """
            Функция возвращает список данных отмеченных объектов
        """
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                data = item.data(QtCore.Qt.UserRole)
                selected.append(data)
        return selected

