import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QWidget, QHBoxLayout
)
from PySide6.QtCore import QThread
from seismictools.apps.projectTraining_Data_preparer.UI.Settings.SettingsWidget import SettingsWidget
from seismictools.apps.projectTraining_Data_preparer.UI.View.ViewWidget import ViewWidget
from seismictools.apps.projectTraining_Data_preparer.UI.Dialogs.SavingDialog import SavingDialog
from seismictools.apps.projectTraining_Data_preparer.Calculate.Data.TraceData import TraceData
from seismictools.apps.projectTraining_Data_preparer.Controller.WorkerReader import WorkerReader
from seismictools.apps.projectTraining_Data_preparer.Controller.WorkerVisualization import WorkerVisualization
from seismictools.apps.projectTraining_Data_preparer.Controller.WorkerSaver import WorkerSaver


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Training Data Preparer")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.settings_widget = SettingsWidget()
        self.main_layout.addWidget(self.settings_widget)

        self.view_widget = ViewWidget()
        self.main_layout.addWidget(self.view_widget)

        self.cube_data = None
        self.traces = []
        self.current_trace_id = 0
        self.saving_dialog = None
        self.worker_thread = None

        # Подключаем сигналы с Normalization
        self.view_widget.operation_off.toggled.connect(self.update_normalization)
        self.view_widget.operation_divide.toggled.connect(self.update_normalization)
        self.view_widget.operation_subtract.toggled.connect(self.update_normalization)
        self.view_widget.blur_x_spin.valueChanged.connect(self.update_normalization)
        self.view_widget.blur_y_spin.valueChanged.connect(self.update_normalization)
        self.view_widget.blur_t_spin.valueChanged.connect(self.update_normalization)

        # Основные сигналы
        self.settings_widget.loadButton.clicked.connect(self.load_cube)
        self.settings_widget.clearButton.clicked.connect(self.clear_cube)
        self.settings_widget.timeSlider.valueChanged.connect(self.update_slice)
        self.settings_widget.deleteButton.clicked.connect(self.delete_trace)
        self.settings_widget.changeClassButton.clicked.connect(self.change_class)
        self.settings_widget.saveDatasetButton.clicked.connect(self.save_dataset)

        self.view_widget.image_view.scene.sigMouseClicked.connect(self.on_image_click)

    def update_normalization(self):
        operation, blur_x, blur_y, blur_t = self.view_widget.get_normalization_params()
        self.view_widget.set_normalization_params(operation, blur_x, blur_y, blur_t)
        self.update_slice(self.settings_widget.timeSlider.value())

    def load_cube(self):
        filepath = self.settings_widget.filePathEdit.text().strip()
        if not filepath:
            QMessageBox.warning(self, "Ошибка", "Укажите путь к файлу SEGY")
            return

        self.worker_thread = QThread()
        self.worker_reader = WorkerReader(filepath)
        self.worker_reader.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker_reader.run)
        self.worker_reader.finished.connect(self.on_cube_loaded)
        self.worker_reader.error.connect(self.on_error)
        self.worker_thread.start()

    def on_cube_loaded(self, cube_data):
        self.cube_data = cube_data
        self.settings_widget.update_time_slider(self.cube_data.shape()[2] - 1)
        self.update_slice(0)
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None

    def update_slice(self, time_index):
        if self.cube_data is None:
            return

        worker_viz = WorkerVisualization(self.cube_data)
        slice_data, title = worker_viz.get_slice_data(time_index)
        if slice_data is not None:
            self.view_widget.update_heatmap(slice_data, title, normalized=False)

        time_ms = self.cube_data.get_time_value(time_index)
        self.settings_widget.update_time_label(time_ms)

    def on_image_click(self, event):
        if self.cube_data is None:
            return

        pos = event.pos()
        vb = self.view_widget.image_view.getImageItem().getViewBox()
        scene_pos = vb.mapSceneToView(pos)
        x, y = scene_pos.x(), scene_pos.y()

        shape = self.cube_data.shape()
        inline_idx = int(max(0, min(shape[0] - 1, y)))
        xline_idx = int(max(0, min(shape[1] - 1, x)))

        worker_viz = WorkerVisualization(self.cube_data)
        trace_data, trace_id, coords = worker_viz.get_trace_data(inline_idx, xline_idx)
        if trace_data is not None:
            self.on_trace_updated(trace_data, trace_id, coords)
            # Показываем маркер выбранной точки
            self.view_widget.show_selected_point(inline_idx, xline_idx)

    def on_trace_updated(self, trace_data, trace_id, coords):
        self.view_widget.update_trace_plot(trace_data, trace_id, coords)
        self.current_trace_id += 1
        new_trace = TraceData(
            trace_id=self.current_trace_id,
            coordinates=coords,
            data=trace_data,
            class_label=1
        )
        self.traces.append(new_trace)
        self.settings_widget.add_trace_to_table(self.current_trace_id, coords, 1)

    def delete_trace(self):
        trace_id = self.settings_widget.get_selected_trace_id()
        if trace_id is None:
            return

        self.traces = [t for t in self.traces if t.trace_id != trace_id]
        self.settings_widget.clear_traces_table()
        for t in self.traces:
            self.settings_widget.add_trace_to_table(t.trace_id, t.coordinates, t.class_label)

    def change_class(self):
        trace_id = self.settings_widget.get_selected_trace_id()
        if trace_id is None:
            return

        current_class = self.settings_widget.get_current_class()
        if current_class is None:
            current_class = 1  # Если по какой-то причине класс None — стартуем с 1

        # Циклическое переключение между 4 классами
        new_class = current_class % 4 + 1

        for t in self.traces:
            if t.trace_id == trace_id:
                t.set_class(new_class)
                break

        self.settings_widget.clear_traces_table()
        for t in self.traces:
            self.settings_widget.add_trace_to_table(t.trace_id, t.coordinates, t.class_label)

    def save_dataset(self):
        if not self.traces:
            QMessageBox.warning(self, "Ошибка", "Нет трасс для сохранения")
            return

        app_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(app_dir, "dataset.npz")

        self.saving_dialog = SavingDialog(self)
        self.saving_dialog.show()

        self.worker_thread = QThread()
        self.worker_saver = WorkerSaver(self.traces, filepath)
        self.worker_saver.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker_saver.run)
        self.worker_saver.saved.connect(self.on_save_success)
        self.worker_saver.error.connect(self.on_save_error)
        self.worker_thread.start()

    def on_save_success(self, filepath):
        if self.saving_dialog:
            self.saving_dialog.close()
            self.saving_dialog = None
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None
        QMessageBox.information(self, "Успех", f"Сохранено: {filepath}")

    def on_save_error(self, error_msg):
        if self.saving_dialog:
            self.saving_dialog.close()
            self.saving_dialog = None
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None
        QMessageBox.critical(self, "Ошибка", error_msg)

    def on_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def clear_cube(self):
        self.cube_data = None
        self.traces = []
        self.current_trace_id = 0
        self.settings_widget.clear_traces_table()
        self.view_widget.image_view.clear()
        self.view_widget.plot_widget.clear()
        # УБИРАЕМ МАРКЕР ПРИ ОЧИСТКЕ
        if self.view_widget.selected_point:
            self.view_widget.selected_point.clear()
        self.settings_widget.filePathEdit.clear()

    def closeEvent(self, event):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
        event.accept()


def main():
    """Точка входа для запуска через poetry run"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())