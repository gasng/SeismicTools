from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton,
    QDoubleSpinBox, QGroupBox, QPushButton, QFileDialog, QInputDialog, QMessageBox
)
import pyqtgraph as pg
import numpy as np


class ViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Карта
        self.image_view = pg.ImageView()
        self.image_view.ui.menuBtn.hide()  # Убираем встроенную кнопку Menu
        self.layout.addWidget(self.image_view)

        # График трассы
        self.plot_widget = pg.PlotWidget(title="Выбранная трасса")
        self.plot_widget.showGrid(True, True)
        self.layout.addWidget(self.plot_widget)

        # Панель Normalization
        self.create_normalization_panel()

        # Кнопка Export
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_data_or_image)
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        export_layout.addWidget(self.export_button)
        self.layout.addLayout(export_layout)

        # Маркер выбранной точки
        self.selected_point = None
        self.add_selected_point_marker()

        # Параметры нормализации
        self.operation = "Off"
        self.blur_x = 0.0
        self.blur_y = 0.0
        self.blur_t = 0.0

        self.image_view.getView().setAspectLocked(False)
        self.image_view.view.invertY(True)

    def create_normalization_panel(self):
        norm_group = QGroupBox("Normalization")
        norm_layout = QVBoxLayout(norm_group)

        op_layout = QHBoxLayout()
        op_label = QLabel("Operation:")
        self.operation_off = QRadioButton("Off")
        self.operation_divide = QRadioButton("Divide")
        self.operation_subtract = QRadioButton("Subtract")
        self.operation_off.setChecked(True)

        op_layout.addWidget(op_label)
        op_layout.addWidget(self.operation_off)
        op_layout.addWidget(self.operation_divide)
        op_layout.addWidget(self.operation_subtract)
        norm_layout.addLayout(op_layout)

        blur_layout = QHBoxLayout()
        blur_label = QLabel("Blur:")
        blur_layout.addWidget(blur_label)

        blur_layout.addWidget(QLabel("X"))
        self.blur_x_spin = QDoubleSpinBox()
        self.blur_x_spin.setRange(0.0, 10.0)
        self.blur_x_spin.setSingleStep(0.5)
        self.blur_x_spin.setValue(0.0)
        blur_layout.addWidget(self.blur_x_spin)

        blur_layout.addWidget(QLabel("Y"))
        self.blur_y_spin = QDoubleSpinBox()
        self.blur_y_spin.setRange(0.0, 10.0)
        self.blur_y_spin.setSingleStep(0.5)
        self.blur_y_spin.setValue(0.0)
        blur_layout.addWidget(self.blur_y_spin)

        blur_layout.addWidget(QLabel("T"))
        self.blur_t_spin = QDoubleSpinBox()
        self.blur_t_spin.setRange(0.0, 10.0)
        self.blur_t_spin.setSingleStep(0.5)
        self.blur_t_spin.setValue(0.0)
        blur_layout.addWidget(self.blur_t_spin)

        norm_layout.addLayout(blur_layout)
        self.layout.addWidget(norm_group)

    def set_normalization_params(self, operation, blur_x, blur_y, blur_t):
        """Устанавливает параметры нормализации (обязателен для main.py)"""
        self.operation = operation
        self.blur_x = blur_x
        self.blur_y = blur_y
        self.blur_t = blur_t

    def apply_normalization(self, data):
        result = data.astype(np.float32).copy()

        if self.blur_x > 0 or self.blur_y > 0:
            from scipy.ndimage import gaussian_filter
            sigma = (self.blur_y, self.blur_x)
            result = gaussian_filter(result, sigma=sigma)

        if self.operation == "Off":
            return result

        mean_val = np.mean(result)
        if self.operation == "Subtract":
            result -= mean_val
        elif self.operation == "Divide":
            mean_val = max(mean_val, 1e-6)
            result /= mean_val

        return result

    def update_heatmap(self, slice_data, title="", normalized=False):
        if not normalized:
            processed_data = self.apply_normalization(slice_data)
        else:
            processed_data = slice_data
        self.image_view.setImage(processed_data.T, autoLevels=True)
        self.last_slice_data_original = slice_data

    def update_trace_plot(self, trace_data, trace_id, coords):
        self.plot_widget.clear()
        self.plot_widget.plot(trace_data, pen='b')
        self.plot_widget.setTitle(f"Выбранная трасса #{trace_id}\nInline {coords[0]}, Xline {coords[1]}")

    def get_normalization_params(self):
        operation = "Off"
        if self.operation_divide.isChecked():
            operation = "Divide"
        elif self.operation_subtract.isChecked():
            operation = "Subtract"

        blur_x = self.blur_x_spin.value()
        blur_y = self.blur_y_spin.value()
        blur_t = self.blur_t_spin.value()

        return operation, blur_x, blur_y, blur_t

    def add_selected_point_marker(self):
        #Создаёт маркер для отображения выбранной точки
        self.selected_point = pg.ScatterPlotItem(
            size=12,
            pen=pg.mkPen('yellow', width=2),
            brush=pg.mkBrush(None),
            symbol='x'
        )
        self.image_view.addItem(self.selected_point)

    def show_selected_point(self, inline_idx, xline_idx):
        #Показывает маркер в координатах (inline_idx, xline_idx)
        if self.selected_point:
            x = float(xline_idx)
            y = float(inline_idx)
            self.selected_point.setData([x], [y])

    def export_data_or_image(self):
        if not hasattr(self, 'last_slice_data_original'):
            QMessageBox.warning(self, "Ошибка", "Нет данных для экспорта")
            return

        item, ok = QInputDialog.getItem(
            self, "Экспорт", "Выберите формат:",
            ["Изображение (PNG)", "Данные (NPY)"], 0, False
        )
        if not ok or not item:
            return

        if item == "Изображение (PNG)":
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Сохранить изображение", "", "PNG (*.png)"
            )
            if filepath:
                if not filepath.endswith(".png"):
                    filepath += ".png"
                pixmap = self.image_view.getImageItem().getPixmap()
                if pixmap and not pixmap.isNull():
                    pixmap.save(filepath)
                    print(f"Изображение сохранено: {filepath}")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось сохранить изображение")

        elif item == "Данные (NPY)":
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Сохранить данные", "", "NumPy (*.npy)"
            )
            if filepath:
                if not filepath.endswith(".npy"):
                    filepath += ".npy"
                try:
                    np.save(filepath, self.last_slice_data_original)
                    print(f"Данные сохранены: {filepath}")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные:\n{e}")