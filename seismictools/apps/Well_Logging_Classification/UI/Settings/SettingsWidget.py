from PySide6.QtWidgets import (
    QFileDialog, QMessageBox, QColorDialog, QLabel, 
    QHBoxLayout, QWidget, QDialog, QTableWidgetItem, QPushButton
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor
from .SettingsWidget_ui import SettingsWidgetUI, AddClassDialogUI

import logging

logger = logging.getLogger(__name__)

class SettingsWidget(SettingsWidgetUI):

    loadRequested = Signal(str)
    clearRequested = Signal()
    plotCrossplotRequested = Signal(str, str)
    drawPolygonRequested = Signal()
    assignClassRequested = Signal(int)
    cancelPolygonRequested = Signal()
    clearMarkupRequested = Signal()
    saveRequested = Signal(str)
    addClassRequested = Signal(int, str, str)
    deleteClassRequested = Signal(int)
    historyRequested = Signal(str)
    deletePolygonRequested = Signal(int)
    clearAllPolygonsRequested = Signal()
    classColorChanged = Signal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._history = []
        self._connect_signals()

    def _connect_signals(self):
        """Подключаем все обработчики"""
        self.pushButton_load.clicked.connect(self.on_load_clicked)
        self.pushButton_clear.clicked.connect(self.on_clear_clicked)
        self.pushButton_plot.clicked.connect(self.on_plot_clicked)
        self.pushButton_draw_polygon.clicked.connect(self.on_draw_polygon_clicked)
        self.pushButton_assign_class.clicked.connect(self.on_assign_class_clicked)
        self.pushButton_cancel_polygon.clicked.connect(self.on_cancel_polygon_clicked)
        self.pushButton_clear_markup.clicked.connect(self.on_clear_markup_clicked)
        self.pushButton_save.clicked.connect(self.on_save_clicked)
        self.btn_add_class.clicked.connect(self.on_add_class_clicked)
        self.btn_del_class.clicked.connect(self.on_delete_class_clicked)
        self.btn_delete_polygon.clicked.connect(self.on_delete_polygon_clicked)
        self.btn_clear_all_polygons.clicked.connect(self.on_clear_all_polygons_clicked)
        self.comboBox_history.currentTextChanged.connect(self.on_history_selected)

    def on_load_clicked(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Выберите LAS файл", "", "LAS Files (*.las)")
        if filepath:
            self.lineEdit_file.setText(filepath)
            self.add_to_history(filepath)
            self.loadRequested.emit(filepath)

    def on_history_selected(self, filepath):
        if filepath and filepath.strip() and filepath in self._history:
            self.lineEdit_file.setText(filepath)
            self.historyRequested.emit(filepath)

    def add_to_history(self, filepath):
        if not filepath or not isinstance(filepath, str):
            return
        if filepath not in self._history:
            self._history.insert(0, filepath)
            if len(self._history) > 10:
                self._history = self._history[:10]
            self._update_history_combo()

    def _update_history_combo(self):
        current = self.comboBox_history.currentText()
        self.comboBox_history.clear()
        self.comboBox_history.addItems(self._history)
        if current in self._history:
            self.comboBox_history.setCurrentText(current)

    def on_clear_clicked(self):
        self.clearRequested.emit()

    def on_plot_clicked(self):
        x = self.comboBox_xcurve.currentText()
        y = self.comboBox_ycurve.currentText()
        if x and y:
            self.plotCrossplotRequested.emit(x, y)
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите X и Y кривые.")

    def on_draw_polygon_clicked(self):
        self.drawPolygonRequested.emit()

    def on_assign_class_clicked(self):
        row = self.tableWidget_classes.currentRow()
        if row >= 0:
            item = self.tableWidget_classes.item(row, 0)
            if item:
                try:
                    class_id = int(item.text())
                    self.assignClassRequested.emit(class_id)
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Неверный ID класса.")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите класс в таблице.")

    def on_cancel_polygon_clicked(self):
        self.cancelPolygonRequested.emit()

    def on_clear_markup_clicked(self):
        self.clearMarkupRequested.emit()

    def on_save_clicked(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Сохранить LAS файл", "", "LAS Files (*.las)")
        if filepath:
            if not filepath.endswith('.las'):
                filepath += '.las'
            self.saveRequested.emit(filepath)

    def on_add_class_clicked(self):
        dialog = AddClassDialog(self)
        if dialog.exec() == QDialog.Accepted:
            class_id = dialog.spin_id.value()
            name = dialog.line_name.text().strip()
            color = dialog.color_button.property("color") or "#808080"
            if name:
                self.addClassRequested.emit(class_id, name, color)

    def on_delete_class_clicked(self):
        row = self.tableWidget_classes.currentRow()
        if row >= 0:
            item = self.tableWidget_classes.item(row, 0)
            if item:
                class_id_str = item.text()
                reply = QMessageBox.question(
                    self,
                    "Подтверждение удаления",
                    f"Вы уверены, что хотите удалить класс {class_id_str}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    try:
                        class_id = int(class_id_str)
                        self.deleteClassRequested.emit(class_id)
                    except ValueError:
                        pass

    def on_delete_polygon_clicked(self):
        row = self.tableWidget_polygons.currentRow()
        if row >= 0:
            item = self.tableWidget_polygons.item(row, 0)
            if item:
                try:
                    polygon_id = int(item.text())
                    self.deletePolygonRequested.emit(polygon_id)
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Неверный ID полигона.")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите полигон для удаления.")

    def on_clear_all_polygons_clicked(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Очистить всю разметку (все полигоны)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.clearAllPolygonsRequested.emit()

    def populate_curve_table(self, curves_info):
        self.tableWidget_curves.setRowCount(len(curves_info))
        for i, (name, min_val, max_val, delta) in enumerate(curves_info):
            self.tableWidget_curves.setItem(i, 0, QTableWidgetItem(str(name)))
            self.tableWidget_curves.setItem(i, 1, QTableWidgetItem(f"{min_val:.3f}"))
            self.tableWidget_curves.setItem(i, 2, QTableWidgetItem(f"{max_val:.3f}"))
            delta_item = QTableWidgetItem(f"{delta:.3f}")
            delta_item.setTextAlignment(Qt.AlignCenter)
            if delta > 100:
                delta_item.setBackground(QColor(255, 255, 200))
            self.tableWidget_curves.setItem(i, 3, delta_item)
        self.tableWidget_curves.resizeColumnsToContents()

    def populate_curve_combos(self, names):
        self.comboBox_xcurve.clear()
        self.comboBox_ycurve.clear()
        self.comboBox_xcurve.addItems(names)
        self.comboBox_ycurve.addItems(names)

    def populate_class_table(self, class_info, class_colors=None):
        """Заполняет таблицу классов с информацией о цветах"""
        self.tableWidget_classes.setRowCount(len(class_info))
        
        # Если переданы цвета классов, сохраняем их
        if class_colors is not None:
            self._class_colors = class_colors.copy()
        
        for row, (class_id, class_name, point_count) in enumerate(class_info):
            id_item = QTableWidgetItem(str(class_id))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_classes.setItem(row, 0, id_item)
            self.tableWidget_classes.setItem(row, 1, QTableWidgetItem(class_name))
            count_item = QTableWidgetItem(str(point_count))
            count_item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_classes.setItem(row, 2, count_item)

            # Получаем цвет для класса
            color = self._class_colors.get(class_id, "#808080")
            
            # Создаем виджет с цветом и кнопкой для его изменения
            color_widget = QWidget()
            color_layout = QHBoxLayout(color_widget)
            color_layout.setContentsMargins(0, 0, 0, 0)
            color_layout.setSpacing(5)
            
            # Квадратик с цветом
            color_square = QLabel()
            color_square.setFixedSize(30, 20)
            color_square.setStyleSheet(f"""
                background-color: {color}; 
                border: 1px solid #ccc; 
                border-radius: 3px;
            """)
            color_square.setProperty("class_id", class_id)
            color_square.setProperty("color", color)
            
            color_btn = QPushButton("...")
            color_btn.setFixedSize(25, 20)
            color_btn.setProperty("class_id", class_id)
            color_btn.setProperty("color_square", color_square)
            color_btn.clicked.connect(lambda checked, cid=class_id, cs=color_square: 
                                     self._select_class_color(cid, cs))
            
            color_layout.addWidget(color_square)
            color_layout.addWidget(color_btn)
            color_layout.setAlignment(Qt.AlignCenter)
            self.tableWidget_classes.setCellWidget(row, 3, color_widget)
        
        self.tableWidget_classes.resizeColumnsToContents()

    def _select_class_color(self, class_id, color_square):
        """Обработчик выбора цвета для класса"""
        current_color = color_square.property("color") or "#808080"
        logger.debug(f"Выбор цвета для класса {class_id}. Текущий цвет: {current_color}")
        
        color = QColorDialog.getColor(QColor(current_color), self, f"Выберите цвет для класса {class_id}")
        
        if color.isValid():
            new_color = color.name()
            logger.debug(f"Выбран новый цвет для класса {class_id}: {new_color}")
            
            color_square.setStyleSheet(f"""
                background-color: {new_color}; 
                border: 1px solid #ccc; 
                border-radius: 3px;
            """)
            color_square.setProperty("color", new_color)
            
            self._class_colors[class_id] = new_color
            
            # Отправляем сигнал об изменении цвета
            logger.debug(f"Отправка сигнала classColorChanged для класса {class_id}")
            self.classColorChanged.emit(class_id, new_color)
        else:
            logger.debug(f"Выбор цвета отменен для класса {class_id}")

    def populate_polygon_table(self, polygon_info):
        self.tableWidget_polygons.setRowCount(len(polygon_info))
        for i, (pid, class_name, count) in enumerate(polygon_info):
            self.tableWidget_polygons.setItem(i, 0, QTableWidgetItem(str(pid)))
            self.tableWidget_polygons.setItem(i, 1, QTableWidgetItem(str(class_name)))
            self.tableWidget_polygons.setItem(i, 2, QTableWidgetItem(str(count)))
        self.tableWidget_polygons.resizeColumnsToContents()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith('.las'):
                event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            filepath = urls[0].toLocalFile()
            if filepath.endswith('.las'):
                self.lineEdit_file.setText(filepath)
                self.add_to_history(filepath)
                self.loadRequested.emit(filepath)
                event.acceptProposedAction()


class AddClassDialog(AddClassDialogUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.color_button.clicked.connect(self.select_color)
        # Устанавливаем начальный цвет
        self.color_button.setProperty("color", "#FF69B4")
        self._update_button_color("#FF69B4")

    def select_color(self):
        current_color = self.color_button.property("color") or "#FF69B4"
        color = QColorDialog.getColor(QColor(current_color), self, "Выберите цвет класса")
        
        if color.isValid():
            hex_color = color.name()
            self.color_button.setProperty("color", hex_color)
            self._update_button_color(hex_color)

    def _update_button_color(self, hex_color):
        """Обновляет внешний вид кнопки с выбранным цветом"""
        self.color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {hex_color};
                color: white;
                border-radius: 6px;
                font-weight: medium;
                padding: 8px;
                border: 1px solid #ccc;
            }}
            QPushButton:hover {{
                background-color: {self._adjust_color(hex_color, -20)};
                border: 1px solid #999;
            }}
        """)

    def _adjust_color(self, hex_color, amount):
        color = QColor(hex_color)
        if amount > 0:
            return color.lighter(100 + amount).name()
        else:
            return color.darker(100 - amount).name()