import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QFileDialog

from seismictools.apps.FK_analysis.Calculate.Reader import SegYReader
from seismictools.apps.FK_analysis.Controller.FkForwardWorker import FkForwardWorker
from seismictools.apps.FK_analysis.Controller.FkInverseWorker import FkInverseWorker
from seismictools.apps.FK_analysis.Controller.PolygonMaskWorker import PolygonMaskWorker
from seismictools.apps.FK_analysis.Controller.WorkerReader import WorkerReader
from seismictools.apps.FK_analysis.UI.SettingsWidget_ui import  Ui_FK_Filtration
from seismictools.apps.FK_analysis.View.PlotWidgets import PlotSeism
from seismictools.apps.FK_analysis.View.PolygonSelector import PolygonSelector


class FK_filter(QtWidgets.QMainWindow):
    def __init__(self):
        super(FK_filter, self).__init__()
        self.ui = Ui_FK_Filtration()
        self.ui.setupUi(self)
        self.apply_style()
        self.current_segy_data = None # Это наши сохраненные прочитанные данные
        self.current_fk_spectrum = None # Это сохраненные данные FK-преобразования
        self.current_result_data = None  # "Это сохраненный результат обратного FK
        self.fk_mask = None # Это маска фильтра
        self.dt = None # Частота дискретизации t
        self.dx = None # Частота дискретизации x

        self.ui.SeismicDataBtn.clicked.connect(self.get_filepath)
        self.ui.DeleteBtn.clicked.connect(self.delete_selected_file)
        self.threadpool = QThreadPool()
        self.ui.PlotSeismogramBtn.clicked.connect(self.start_reading)

        self.plot_seism = PlotSeism(
            seismogram_pw=self.ui.SeismogramPW,
            fk_pw=self.ui.FkPW,
            result_pw=self.ui.ResultPW,
            error_lw=self.ui.ErrorLW
        )

        self.ui.FkBtn.clicked.connect(self.start_plot_fk)
        self.ui.ResultBtn.clicked.connect(self.start_plot_ifk)

        self.ui.SignalStartBtn.clicked.connect(self.start_selection)
        self.ui.SignalEndBtn.clicked.connect(self.finish_selection)

        # Подключаем клики по FK-графику
        self.ui.FkPW.scene().sigMouseClicked.connect(self.on_fk_click)


    def get_filepath(self):

        lw_items = [self.ui.SeismicDataLW.item(i).text() for i in range(self.ui.SeismicDataLW.count())]
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Дай файл",
                                                   "",
                                                   "*.segy *.sgy")
        lw_items.append(file_path)
        lw_items = list(set(lw_items))
        self.ui.SeismicDataLW.clear()
        for item in lw_items:
            self.ui.SeismicDataLW.addItem(item)

    def delete_selected_file(self):
        current_row = self.ui.SeismicDataLW.currentRow()
        self.ui.ErrorLW.addItem("Файл успешно удален.")
        self.ui.ErrorLW.scrollToBottom()
        if current_row >= 0:
            self.ui.SeismicDataLW.takeItem(current_row)
        else:
            self.ui.ErrorLW.addItem("Сначала выберите файл для удаления.")
            self.ui.ErrorLW.scrollToBottom()

    def start_reading(self):
        current_item = self.ui.SeismicDataLW.currentItem()
        if not current_item:
            self.ui.ErrorLW.addItem("Выберите файл для загрузки.")
            self.ui.ErrorLW.scrollToBottom()
            return

        filepath = current_item.text()
        worker = WorkerReader(filepath)
        worker.signals.message.connect(self.on_worker_message)
        worker.signals.result.connect(self.on_reader_result)
        worker.signals.error.connect(self.on_worker_error)
        self.threadpool.start(worker)

    def on_worker_message(self, msg: str):
        self.ui.ErrorLW.addItem(f"{msg}")
        self.ui.ErrorLW.scrollToBottom()

    def on_worker_error(self, error: str):
        self.ui.ErrorLW.addItem(f"{error}")
        self.ui.ErrorLW.scrollToBottom()

    def on_reader_result(self, result):
        if result is not None:
            self.current_segy_data = result
            self.dt = result.dt
            self.dx = result.dx
            self.plot_seism.plot_seismogram(result.data, dt=self.dt, dx=self.dx)
        else:
            self.ui.ErrorLW.addItem("Не удалось загрузить данные")
            self.ui.ErrorLW.scrollToBottom()

    def start_plot_fk(self):
        print(">>> start_plot_fk вызвана")
        if self.current_segy_data is None:
            self.ui.ErrorLW.addItem("Сначала загрузите данные")
            return
        worker = FkForwardWorker(self.current_segy_data.data)
        worker.signals.error.connect(self.on_worker_error)
        worker.signals.message.connect(self.on_worker_message)
        worker.signals.result.connect(self.on_fk_ready)
        self.threadpool.start(worker)
        print(">>> Воркер FK запущен")

    def on_fk_ready(self, fk_spectrum):
        if fk_spectrum is not None:
            self.current_fk_spectrum = fk_spectrum
            self.plot_seism.plot_fk(self.current_fk_spectrum, dt=self.dt, dx=self.dx)
            self.polygon_selector = PolygonSelector(
                plot_widget=self.ui.FkPW,
                data_shape=self.current_fk_spectrum.shape,
                f_nyquist=1 / (2 * self.dt),
                k_nyquist=1 / (2 * self.dx)
            )
        else:
            self.ui.ErrorLW.addItem("Не удалось вычислить и отрисовать")
            self.ui.ErrorLW.scrollToBottom()

    def start_plot_ifk(self):
        if self.current_fk_spectrum is None:
            self.ui.ErrorLW.addItem("Сначала расчитайте FK-спектр")
            return
        # Применяем маску ТОЛЬКО если она есть
        if hasattr(self, 'fk_mask') and self.fk_mask is not None:
            filtered = self.current_fk_spectrum * self.fk_mask
            print(f"Маска применена: ненулевых пикселей = {self.fk_mask.sum()}")
        else:
            filtered = self.current_fk_spectrum
            print("Маска не задана — используем полный спектр")

        worker = FkInverseWorker(filtered)
        worker.signals.error.connect(self.on_worker_error)
        worker.signals.message.connect(self.on_worker_message)
        worker.signals.result.connect(self.on_ifk_ready)
        self.threadpool.start(worker)

    def on_ifk_ready(self, ifk_spectrum):
        if ifk_spectrum is not None:
            self.current_result_data = ifk_spectrum
            self.plot_seism.plot_result(ifk_spectrum, dt=self.dt, dx=self.dx)
        else:
            self.ui.ErrorLW.addItem("Не удалось вычислить и отрисовать")
            self.ui.ErrorLW.scrollToBottom()

    def start_selection(self):
        self.polygon_selector.start_selection()
        self.ui.ErrorLW.addItem("Кликайте по FK-спектру")

    def on_fk_click(self, event):
        # Передаём клик напрямую селектору
        if self.polygon_selector.is_selecting and event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.polygon_selector.add_point(event.scenePos())

    def finish_selection(self):
        if self.polygon_selector.finish_selection():
            points = self.polygon_selector.get_points()  # ← точки есть!
            if self.current_fk_spectrum is not None:
                worker = PolygonMaskWorker(points, self.current_fk_spectrum.shape)
                worker.signals.result.connect(self.on_mask_ready)
                worker.signals.error.connect(self.on_worker_error)
                self.threadpool.start(worker)
            else:
                self.ui.ErrorLW.addItem("Нет FK-спектра")
        else:
            self.ui.ErrorLW.addItem("Минимум 3 точки")

    def on_mask_ready(self, mask):
        if mask is not None:
            self.fk_mask = mask
            self.ui.ErrorLW.addItem("Маска полигона создана")
        else:
            self.ui.ErrorLW.addItem("Маска не создана")

    def apply_style(self):
        style = """
            QMainWindow {
                background-color: #0f172a;
            }
            QGroupBox {
                color: #e2e8f0;
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                font-size: 10pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: #60a5fa;
            }
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid #475569;
                padding: 7px 14px;
                border-radius: 6px;
                font-size: 9pt;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #334155;
                border: 1px solid #60a5fa;
            }
            QPushButton:pressed {
                background-color: #0ea5e9;
                color: #0f172a;
                border: 1px solid #0ea5e9;
            }
            QLabel {
                color: #94a3b8;
            }
            QListWidget {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #1d4ed8;
                color: white;
                border-left: 3px solid #60a5fa;
            }
            QStatusBar {
                color: #94a3b8;
                background-color: #1e293b;
                border-top: 1px solid #334155;
            }
        """
        self.setStyleSheet(style)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FK_filter()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()