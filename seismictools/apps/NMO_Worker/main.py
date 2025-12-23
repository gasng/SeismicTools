import sys
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog, QLayout, QLayoutItem, QWidget

from seismictools.apps.NMO_Worker.Controller.ReaderWorker import WorkerReader
from seismictools.apps.NMO_Worker.Controller.SpectrumWorker import SpectrumWorker
from seismictools.apps.NMO_Worker.UI.Settings.NMOWidget_ui import  Ui_NMOWidget
from seismictools.apps.NMO_Worker.View.SeismicPlot import GatherPlotWidget
from seismictools.apps.NMO_Worker.View.SeismicPlot import SpectrumPlotWidget
from seismictools.apps.NMO_Worker.Controller.CorrectionWorker import CorrectionWorker


class Nmo_worker(QtWidgets.QWidget):
    def __init__(self):
        super(Nmo_worker, self).__init__()
        self.threadpool = QtCore.QThreadPool()
        self.worker_reader = None
        self.worker_spectrum = None
        self.worker_correction = None
        self.loaded_data = None
        self.plotWidget = None
        self.ui = Ui_NMOWidget()
        self.ui.setupUi(self)
        self.ui.pushButton_choice.clicked.connect(self.get_filepath)
        self.ui.pushButton_load.clicked.connect(self.load_data)
        self.ui.pushButton_velocitySpectrum.clicked.connect(self.velocity_spectrum)
        self.ui.radioButton_pick.toggled.connect(self.on_pick_mode_toggled)
        self.ui.radioButton_view.toggled.connect(self.on_view_mode_toggled)
        self.ui.pushButton_clearAll.clicked.connect(self.on_clear_all)
        self.ui.pushButton_undoPick.clicked.connect(self.on_undo_pick)
        self.ui.pushButton_applyCorrections.clicked.connect(self.apply_corrections)
        self.ui.pushButton_clear.clicked.connect(self.on_clear_selected_file)

    def get_filepath(self):

        lw_items = [self.ui.Datalist.item(i).text() for i in range(self.ui.Datalist.count())]
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Дай файл",
                                                   "",
                                                   "*.sgy *.segy")
        lw_items.append(file_path)
        lw_items = list(set(lw_items))
        self.ui.Datalist.clear()
        for item in lw_items:
            self.ui.Datalist.addItem(item)

    def load_data(self):
        filepath = self.ui.Datalist.currentItem().text()
        self.worker_reader = WorkerReader(filepath=filepath)
        self.worker_reader.signals.result.connect(self.show_data)
        self.worker_reader.signals.message.connect(self.print_message)
        self.worker_reader.signals.error.connect(self.print_error)
        self.threadpool.start(self.worker_reader)

    def print_message(self, string):
        self.ui.MessageLine.setText(string)

    def print_error(self, string):
        self.ui.MessageLine.setText(string)

    def clear_layout(self, layout: QLayout):

        if layout is None:
            return

        while layout.count():
            item: QLayoutItem = layout.takeAt(0)
            if item.widget() is not None:
                widget: QWidget = item.widget()
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())
            del item

    def show_data(self, result):
        self.loaded_data = result
        self.clear_layout(self.ui.plotLayout)
        my_plot_widget = GatherPlotWidget(result.data, dt=result.dt)
        self.ui.plotLayout.addWidget(my_plot_widget)

    def velocity_spectrum(self):
        if not hasattr(self, 'loaded_data'):
            self.ui.MessageLine.setText("Сначала загрузите данные!")
            return

        self.worker_spectrum = SpectrumWorker(
            data=self.loaded_data.data,
            offsets=self.loaded_data.offsets,
            dt=self.loaded_data.dt
        )
        self.worker_spectrum.signals.result.connect(self.show_spectrum)
        self.worker_spectrum.signals.message.connect(self.print_message)
        self.worker_spectrum.signals.error.connect(self.print_error)
        self.threadpool.start(self.worker_spectrum)

    def show_spectrum(self, spectrum_result):
        self.clear_layout(self.ui.plotLayout2)
        self.plot_widget = SpectrumPlotWidget(data=spectrum_result)
        self.ui.plotLayout2.addWidget(self.plot_widget)

        if self.ui.radioButton_pick.isChecked():
            try:
                self.plot_widget.plot_widget.scene().sigMouseClicked.connect(self.on_spectrum_click)
            except (TypeError, RuntimeError):
                pass

    def on_clear_selected_file(self):
        current_item = self.ui.Datalist.currentItem()
        if current_item:
            row = self.ui.Datalist.row(current_item)
            self.ui.Datalist.takeItem(row)
            self.ui.MessageLine.setText(f"Файл '{current_item.text()}' удалён")
        else:
            self.ui.MessageLine.setText("Нет выделенного файла для удаления")

    def on_pick_mode_toggled(self, checked):
        if checked:
            if hasattr(self, 'plot_widget') and self.plot_widget is not None:
                try:
                    self.plot_widget.plot_widget.scene().sigMouseClicked.connect(self.on_spectrum_click)
                except (TypeError, RuntimeError):
                    pass
            self.ui.MessageLine.setText("Режим пикировки активен")

    def on_view_mode_toggled(self, checked):

        if checked:
            try:
                self.plot_widget.plot_widget.scene().sigMouseClicked.disconnect(self.on_spectrum_click)
            except TypeError:
                pass
            self.ui.MessageLine.setText("Режим просмотра активен")

    def on_spectrum_click(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        vb = self.plot_widget.plot_widget.plotItem.vb
        pos = vb.mapSceneToView(event.scenePos())
        velocity = pos.x()
        time = pos.y()

        nt, nv = self.plot_widget.data.shape
        t_max = nt * self.plot_widget.dt
        v_min, v_max = self.plot_widget.velocities[0], self.plot_widget.velocities[-1]

        if not (v_min <= velocity <= v_max and 0 <= time <= t_max):
            return

        row = self.ui.tableWidget_picks.rowCount()
        self.ui.tableWidget_picks.insertRow(row)

        self.ui.tableWidget_picks.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
        self.ui.tableWidget_picks.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{time:.3f}"))
        self.ui.tableWidget_picks.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{velocity:.1f}"))

        self.plot_widget.add_pick(velocity, time)

        #self.ui.MessageLine.setText(f"Пик {row + 1}: t={time:.3f} с, v={velocity:.1f} м/с")

    def on_clear_all(self):

        self.ui.tableWidget_picks.clearContents()
        self.ui.tableWidget_picks.setRowCount(0)

        self.plot_widget.scatter_data_x.clear()
        self.plot_widget.scatter_data_y.clear()

        if self.plot_widget.scatter_plot_item is not None:
            self.plot_widget.plot_widget.removeItem(self.plot_widget.scatter_plot_item)
            self.plot_widget.scatter_plot_item = None

        self.ui.MessageLine.setText("Все пики удалены")

    def on_undo_pick(self):
        row_count = self.ui.tableWidget_picks.rowCount()
        if row_count == 0:
            self.ui.MessageLine.setText("Нет пиков для отмены")
            return

        self.ui.tableWidget_picks.removeRow(row_count - 1)

        if len(self.plot_widget.scatter_data_x) > 0:
            self.plot_widget.scatter_data_x.pop()
            self.plot_widget.scatter_data_y.pop()

            # Обновляем данные на графике
            if self.plot_widget.scatter_plot_item is not None:
                self.plot_widget.scatter_plot_item.setData(
                    x=self.plot_widget.scatter_data_x,
                    y=self.plot_widget.scatter_data_y
                )

        self.ui.MessageLine.setText("Последний пик отменён")

    def apply_corrections(self):
        if not hasattr(self, 'loaded_data'):
            self.ui.MessageLine.setText("Сначала загрузите данные!")
            return

        rows = self.ui.tableWidget_picks.rowCount()
        if rows == 0:
            self.ui.MessageLine.setText("Нет пиков для построения закона")
            return

        times = []
        velocities = []

        for row in range(rows):
            t_item = self.ui.tableWidget_picks.item(row, 1)
            v_item = self.ui.tableWidget_picks.item(row, 2)
            if t_item and v_item:
                try:
                    t_val = float(t_item.text())
                    v_val = float(v_item.text())
                    times.append(t_val)
                    velocities.append(v_val)
                except ValueError:
                    continue

        if len(times) == 0:
            self.ui.MessageLine.setText("Не удалось прочитать данные из таблицы")
            return

        sorted_indices = np.argsort(times)
        times = np.array(times)[sorted_indices]
        velocities = np.array(velocities)[sorted_indices]

        nt = self.loaded_data.data.shape[0]
        dt = self.loaded_data.dt
        t_full = np.arange(nt) * dt

        from scipy.interpolate import interp1d
        interp_func = interp1d(
            times,
            velocities,
            kind='linear',
            fill_value="extrapolate"
        )
        law = interp_func(t_full)

        law = np.nan_to_num(law, nan=law[0], posinf=law[-1], neginf=law[0])

        self.worker_correction = CorrectionWorker(
            data=self.loaded_data.data,
            law=law,
            offsets=self.loaded_data.offsets,
            dt=self.loaded_data.dt
        )
        self.worker_correction.signals.result.connect(self.show_corrected)
        self.worker_correction.signals.message.connect(self.print_message)
        self.worker_correction.signals.error.connect(self.print_error)
        self.threadpool.start(self.worker_correction)

    def show_corrected(self, corrected_data):
        self.clear_layout(self.ui.plotLayout3)  # предположим, это третий график
        plot_widget = GatherPlotWidget(corrected_data)
        self.ui.plotLayout3.addWidget(plot_widget)
        self.ui.MessageLine.setText("NMO-коррекция применена")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Nmo_worker()
    window.show()

    return app.exec()

if __name__ == "__main__":
    main()