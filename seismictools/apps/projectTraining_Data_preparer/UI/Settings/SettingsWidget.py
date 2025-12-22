from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QSlider, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from .SettingsWidget_ui import Ui_SettingsWidget

class SettingsWidget(QWidget, Ui_SettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Настройка таблицы
        self.tracesTable.setColumnCount(3)
        self.tracesTable.setHorizontalHeaderLabels(["Трасса", "Координаты", "Класс"])
        self.tracesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tracesTable.setSelectionMode(QAbstractItemView.SingleSelection)


    def update_time_slider(self, max_time_index):
        self.timeSlider.setMaximum(max_time_index)
        self.timeSlider.setValue(0)

    def update_time_label(self, time_ms):
        self.timeLabel.setText(f"Временной срез T, мс: {int(time_ms)}")

    def add_trace_to_table(self, trace_id, coords, class_label):
        row = self.tracesTable.rowCount()
        self.tracesTable.insertRow(row)
        self.tracesTable.setItem(row, 0, QTableWidgetItem(str(trace_id)))
        self.tracesTable.setItem(row, 1, QTableWidgetItem(f"{coords[0]:.1f}, {coords[1]:.1f}"))
        self.tracesTable.setItem(row, 2, QTableWidgetItem(str(class_label)))

    def get_selected_trace_id(self):
        selected = self.tracesTable.selectedItems()
        if selected:
            return int(selected[0].text())
        return None

    def clear_traces_table(self):
        self.tracesTable.setRowCount(0)

    def get_current_class(self):
        selected = self.tracesTable.selectedItems()
        if selected and len(selected) >= 3:
            return int(selected[2].text()) if selected[2].text().isdigit() else None
        return None