import sys
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog
from seismictools.apps.Eiconal_Solver.Controller.Reader_worker import ReaderWorker
from seismictools.apps.Eiconal_Solver.Controller.Solver_worker import SolverWorker
from seismictools.apps.Eiconal_Solver.UI.main_window_ui import Ui_MainWindow
from seismictools.apps.Eiconal_Solver.View.Plot import GatherPlotWidget


class EiconalSolver(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QtCore.QThreadPool()

        self.current_model_path = None
        self.model_trajectories_names = dict()
        self.current_plot_widget = None


        self.solver_worker = None
        self.reader_worker = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.UploadButton.clicked.connect(self.upload_npy_file)
        self.ui.ClearButton.clicked.connect(self.clear_npy_file)
        self.ui.StartButton.clicked.connect(self.calculation)
        self.ui.UploadedFileWidget.itemDoubleClicked.connect(self.load_model)
        self.ui.X_line.editingFinished.connect(self.set_default_x)
        self.ui.Z_line.editingFinished.connect(self.set_default_z)
        self.ui.theta_line.editingFinished.connect(self.set_default_theta)
        self.ui.delta_line.editingFinished.connect(self.set_default_delta)
        self.ui.delta_line.editingFinished.connect(self.replot_model)
        self.ui.pushButton.clicked.connect(self.export_trajectory)
        self.ui.ShowButton.clicked.connect(self.show_trajectory)
        self.ui.HideButton.clicked.connect(self.hide_trajectory)
        self.ui.DeleteButton.clicked.connect(self.delete_trajectory)

    def upload_npy_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,"Выберите файл модели","","NumPy файлы (*.npy)")

        if file_path:
            if any(self.ui.UploadedFileWidget.item(i).text() == file_path for i in
                   range(self.ui.UploadedFileWidget.count())):
                self.ui.StatusWidget.addItem(f"Уже загружен: {file_path}")
                return

            self.ui.UploadedFileWidget.addItem(file_path)
            self.model_trajectories_names[file_path] = dict()
            self.ui.StatusWidget.addItem(f"Загружен: {file_path}")


    def clear_npy_file(self):
        selected_items = self.ui.UploadedFileWidget.selectedItems()

        if not selected_items:
            self.ui.StatusWidget.addItem("Ничего не выбрано для удаления")
            return

        for item in selected_items:
            self.ui.UploadedFileWidget.takeItem(
                self.ui.UploadedFileWidget.row(item)
            )
            path = item.text()
            self.model_trajectories_names.pop(path)

        self.ui.StatusWidget.addItem(f"Удалено {len(selected_items)} файлов")


    def load_model(self):
        items = self.ui.UploadedFileWidget.selectedItems()

        if len(items) == 1:
            path = items[0].text()
            self.reader_worker = ReaderWorker(path)
            self.reader_worker.signals.message.connect(self.print_message)
            self.reader_worker.signals.error.connect(self.print_error)
            self.reader_worker.signals.result.connect(self.plot_model)
            self.reader_worker.signals.result.connect(self.set_model)
            self.threadpool.start(self.reader_worker)
            self.current_model_path = path
            self.ui.trajectoriesWidget.clear()
            for i in self.model_trajectories_names[path]:
                self.ui.trajectoriesWidget.addItem(i)


        else:
            self.ui.StatusWidget.addItem("Для отрисовки необходимо выбрать один файл модели.")
            return


    def plot_model(self, result):
        delta = float(self.ui.delta_line.text())

        if self.ui.PlotWidget.count():
            self.ui.PlotWidget.takeAt(0).widget().deleteLater()

        self.current_plot_widget = GatherPlotWidget(result, on_ray_selected=self.update_initial_conditions, delta=delta, path=self.current_model_path)
        self.ui.PlotWidget.addWidget(self.current_plot_widget)


    def replot_model(self):
        delta = float(self.ui.delta_line.text())

        if self.ui.PlotWidget.count():
            self.ui.PlotWidget.takeAt(0).widget().deleteLater()

        self.current_plot_widget = GatherPlotWidget(self.model, on_ray_selected=self.update_initial_conditions, delta=delta, path=self.current_model_path)
        self.ui.PlotWidget.addWidget(self.current_plot_widget)

        self.ui.trajectoriesWidget.clear()


    def calculation(self):
        x_0 = float(self.ui.X_line.text())
        z_0 = float(self.ui.Z_line.text())
        theta = float(self.ui.theta_line.text()) * np.pi / 180
        delta = float(self.ui.delta_line.text())

        if self.model is None:
            self.print_error('Сперва загрузите скоростную модель.')
            return

        self.solver_worker = SolverWorker(self.model, x_0, z_0, theta, delta)
        self.solver_worker.signals.message.connect(self.print_message)
        self.solver_worker.signals.error.connect(self.print_error)
        self.solver_worker.signals.result.connect(self.add_trajectory)
        self.threadpool.start(self.solver_worker)


    def add_trajectory(self, result):
        x_0 = float(self.ui.X_line.text())
        z_0 = float(self.ui.Z_line.text())
        theta = float(self.ui.theta_line.text())

        name = 'x=' + str(x_0) + ', z=' + str(z_0) + ', theta=' + str(theta)
        self.current_plot_widget.animate_trajectory(result, name)
        self.model_trajectories_names[self.current_model_path][name] = result
        self.ui.trajectoriesWidget.addItem(name)
        self.model_trajectories_names[self.current_model_path][name] = result


    def show_trajectory(self):
        items = self.ui.trajectoriesWidget.selectedItems()
        for i in items:
            name = i.text()
            self.current_plot_widget.animate_trajectory(self.model_trajectories_names[self.current_model_path][name], name)


    def hide_trajectory(self):
        items = self.ui.trajectoriesWidget.selectedItems()
        for i in items:
            name = i.text()
            self.current_plot_widget.hide_trajectory(name)


    def delete_trajectory(self):
        items = self.ui.trajectoriesWidget.selectedItems()

        if not items:
            self.ui.StatusWidget.addItem("Ничего не выбрано для удаления")
            return

        for item in items:
            self.ui.trajectoriesWidget.takeItem(self.ui.trajectoriesWidget.row(item))
            name = item.text()
            self.model_trajectories_names[self.current_model_path].pop(name)
            self.current_plot_widget.delete_trajectory(name)

        self.ui.StatusWidget.addItem(f"Удалено {len(items)} траекторий.")


    def set_initial_conditions_interactively(self):
        if self.current_plot_widget is None:
            self.print_error("Сначала загрузите и отобразите скоростную модель.")
            return
        x0, y0 = self.current_plot_widget.start_point
        theta = self.current_plot_widget.theta
        self.update_initial_conditions(x0, y0, theta)


    def update_initial_conditions(self, x0, y0, theta_rad):
        print(f"update_initial_conditions called with: x0={x0:.6f}, y0={y0:.6f}, theta={np.degrees(theta_rad):.2f}°")
        self.ui.X_line.setText(f"{x0:.2f}")
        self.ui.Z_line.setText(f"{y0:.2f}")
        self.ui.theta_line.setText(f"{np.degrees(theta_rad):.0f}")


    def set_default_x(self):
        if self.ui.X_line.text() == "":
            self.ui.X_line.setText("0.0")
        try:
            float(self.ui.X_line.text())
        except ValueError:
            self.ui.X_line.setText("0.0")
            self.print_error('Вы должны ввести число. Если дробное, используйте точку.')


    def set_default_z(self):
        if self.ui.Z_line.text() == "":
            self.ui.Z_line.setText("0.0")
        try:
            float(self.ui.Z_line.text())
        except ValueError:
            self.ui.Z_line.setText("0.0")
            self.print_error('Вы должны ввести число. Если дробное, используйте точку.')


    def set_default_theta(self):
        if self.ui.theta_line.text() == "":
            self.ui.theta_line.setText("45")
        try:
            float(self.ui.theta_line.text())
        except ValueError:
            self.ui.theta_line.setText("0.0")
            self.print_error('Вы должны ввести число. Если дробное, используйте точку.')


    def set_default_delta(self):
        if self.ui.delta_line.text() == "":
            self.ui.delta_line.setText("1.0")
        try:
            float(self.ui.delta_line.text())
        except ValueError:
            self.ui.delta_line.setText("1.0")
            self.print_error('Вы должны ввести число. Если дробное, используйте точку.')


    def set_model(self, result):
        self.model = result


    def export_trajectory(self):
        items = self.ui.trajectoriesWidget.selectedItems()

        if not items:
            self.ui.StatusWidget.addItem('Ничего не выбрано для экспорта')
            return

        if len(items) == 1:
            name = items[0].text()
            trajectory = self.trajectories[name]
            file_path, selected_filter = QFileDialog.getSaveFileName(
                self,
                'Сохранить массив как .npy',
                '',
                'NumPy binary files (*.npy);;All files (*)',
                'NumPy binary files (*.npy)'
            )

            if not file_path:
                return

            try:
                np.save(file_path, trajectory)
                self.print_message(f'Массив сохранён: {file_path}')
            except Exception as e:
                self.print_error(f'Ошибка при сохранении:\n{e}')

        else:
            self.print_message('Выберите только 1 файл для сохранения.')



    def print_message(self, text):
        self.ui.StatusWidget.addItem(text)


    def print_error(self, text):
        self.ui.StatusWidget.addItem(text)


    def scroll_status_bar(self):
        self.ui.StatusWidget.scrollToBottom()





def main():
    app = QtWidgets.QApplication(sys.argv)
    window = EiconalSolver()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()