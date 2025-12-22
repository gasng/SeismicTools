import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem
from PySide6.QtCore import QThreadPool

from seismictools.apps.Seismic_Filtering_BP.UI.UI_Designer.Designer_Apps_Seismic_ui import Ui_MainWindow
from seismictools.apps.Seismic_Filtering_BP.Controller.WorkerReader import WorkerReader
from seismictools.apps.Seismic_Filtering_BP.Controller.WorkerFilter import WorkerFilter

from seismictools.apps.Seismic_Filtering_BP.UI.ViewWidgets.PlotWidgets import SeismicPlotWidget

class BandPassApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Инициализирует приложение и его компоненты.
        """
        super(BandPassApp, self).__init__()
        self.threadpool = QThreadPool()
        self.setupUi(self)

        icon_path = os.path.join(os.path.dirname(__file__), "icon_app.png")
        self.setWindowIcon(QIcon(icon_path))

        self.file_data = {}
        self.actual_file_path = None
        self.listWidget_File.currentItemChanged.connect(self.select_file)
        self.comboBox_for_typeFilter.currentTextChanged.connect(self.filter_type)
        self.plot_widget = None

        self.pushButton_load.clicked.connect(self.load_files)
        self.pushButton_clear.clicked.connect(self.clear_all)
        self.pushButton_apply.clicked.connect(self.apply_filter)
        self.pushButton_reset.clicked.connect(self.reset_plot)

    #Всё для загрузки и выбора файлов
    def select_file(self, actual):
        """
        Обрабатывает смену выбранного файла в списке.
        Устанавливает текущий путь к файлу и вставляет новое изображение в поле отрисовки сигнала.
        """
        if actual is None:
            return
        file_path = actual.toolTip()
        self.actual_file_path = file_path
        self.update_plot()

    def load_files(self):
        """
        Открывает проводник для выбора SEGY-файлов.
        Добавляет новые файлы в список и запускает их фоновую загрузку через WorkerReader.
        Игнорируется повторная загрузка уже добавленного файла.
        """
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Выберите SEGY файлы", "", "SEGY Files (*.sgy *.segy)"
        )
        if not file_paths:
            return

        for path in file_paths:
            if path in self.file_data:
                self.event_log(f"Файл уже загружен: {os.path.basename(path)}")
                continue

            item = QListWidgetItem(os.path.basename(path))
            item.setToolTip(path)
            self.listWidget_File.addItem(item)
            self.file_data[path] = {"original": None, "filtered": None}

            self.event_log(f"Загрузка: {os.path.basename(path)}")
            worker = WorkerReader(path)
            worker.signals.result.connect(self.load_success)
            worker.signals.error.connect(self.load_error)
            worker.signals.message.connect(self.event_log)
            self.threadpool.start(worker)

    # Всё для отображения сообщений (в частности - ошибок)
    def load_success(self, data, file_path: str):
        """
        Обрабатывает "успешную" загрузку данных.
        Сохраняет исходный сигнал и временной шаг "dt", а так же вычисляет и выводит частоту дискретизации "fs".
        Если файл первый — делает его активным и обновляет график.
        """
        if data is None:
            self.event_log(f"Ошибка: данные не загружены для {os.path.basename(file_path)}")
            return

        self.file_data[file_path]["original"] = data.data
        self.file_data[file_path]["dt"] = data.dt
        self.event_log(f"Загружен файл '{os.path.basename(file_path)}' (fs = {1000000.0/data.dt:.1f} Гц)") #сохраняем как 2D-данные

        if self.actual_file_path is None:
            self.actual_file_path = file_path
            self.listWidget_File.setCurrentRow(0)
            self.update_plot()

    def load_error(self, error_msg: str):
        """
        Обрабатывает ошибку при загрузке файла: выводит сообщение в "Журнал событий" и показывает модальное окно с ошибкой.
        """
        self.event_log(f"Ошибка: {error_msg}")
        QMessageBox.critical(self, "Ошибка", error_msg)

    #Всё для применения фильтра
    def apply_filter(self):
        """
        Запускает фоновое применение цифрового фильтра (bandpass/lowpass/highpass) к данным выбранного файла.
        Проверяет корректность частот, вычисляет частоту дискретизации "fs" из временного шага "dt" и передаёт задачу в WorkerFilter.
        """
        if self.actual_file_path is None:
            self.event_log("Сначала загрузите файл!")
            return

        orig_data = self.file_data[self.actual_file_path]["original"]

        if orig_data is None:
            self.event_log("Данные не загружены!")
            return

        filter_type = self.comboBox_for_typeFilter.currentText()
        order = self.spinBox.value()

        try:
            freq_min = int(self.lineEdit_forMin.text()) if self.lineEdit_forMin.text() else 10
            freq_max = int(self.lineEdit_forMax.text()) if self.lineEdit_forMax.text() else 50
        except ValueError:
            self.event_log("Ошибка: частоты должны быть числами")
            return

        if filter_type == "bandpass" and freq_min >= freq_max:
            self.event_log("Ошибка: min частота должна быть < max")
            return

        self.event_log(f"Применение фильтра к {os.path.basename(self.actual_file_path)}...")

        dt = self.file_data[self.actual_file_path]["dt"]
        fs = 1000000.0/dt
        worker = WorkerFilter(
            type_filter=filter_type,
            data=orig_data,
            low_freq=freq_min,
            high_freq=freq_max,
            fs=fs,
            order=order
        )
        worker.signals.result.connect(self.filter_success)
        worker.signals.error.connect(self.load_error)
        worker.signals.message.connect(self.event_log)
        self.threadpool.start(worker)

    def filter_type(self, filter_type: str):
        """
        Обновляет поля ввода в зависимости от типа фильтра.
        """
        dt = self.file_data[self.actual_file_path]["dt"]
        fs = 1000000.0 / dt if dt > 0 else 1000
        nyquist_freq = int(fs / 2)
        if filter_type == "bandpass":
            self.lineEdit_forMin.setReadOnly(False)
            self.lineEdit_forMax.setReadOnly(False)
        elif filter_type == "lowpass":
            self.lineEdit_forMin.setText("0")
            self.lineEdit_forMin.setReadOnly(True)
            self.lineEdit_forMax.setReadOnly(False)
        elif filter_type == "highpass":
            self.lineEdit_forMax.setText(str(nyquist_freq))
            self.lineEdit_forMax.setReadOnly(True)
            self.lineEdit_forMin.setReadOnly(False)

    def filter_success(self, filtered_data):
        """
        Уведомляет об успешном завершение фильтрации.
        Сохраняет отфильтрованные данные и обновляет график.
        """
        if filtered_data is None or self.actual_file_path is None:
            self.event_log("Ошибка фильтрации")
            return

        self.file_data[self.actual_file_path]["filtered"] = filtered_data
        self.event_log("Фильтр успешно применён")
        self.update_plot()

    #Всё для отрисовки и очистки программы
    def update_plot(self):
        """
        Обновляет график: удаляет старый виджет (если есть) и создаёт новый, с оригинальными и отфильтрованными данными (когда применим фильтр).
        """
        if self.plot_widget:
            self.plot_widget.deleteLater()
            self.plot_widget = None

        if self.actual_file_path is None:
            return

        orig = self.file_data[self.actual_file_path]["original"]
        filt = self.file_data[self.actual_file_path]["filtered"]

        if orig is None:
            return
        self.plot_widget = SeismicPlotWidget(orig, filt)
        self.verticalLayout_for_plotgraf.addWidget(self.plot_widget)

    def clear_all(self):
        """
        Полностью сбрасывает состояние программы: очищает данные, удаляет список файлов и график(-и), сообщает об "очистке".
        """
        self.file_data.clear()
        self.actual_file_path = None
        self.listWidget_File.clear()

        self.update_plot()
        self.event_log("Все данные очищены")

    def reset_plot(self):
        """
        Сбрасывает отфильтрованные данные И параметры фильтра к начальному состоянию.
        """
        if self.actual_file_path is None:
            return
        self.file_data[self.actual_file_path]["filtered"] = None

        self.comboBox_for_typeFilter.setCurrentText("bandpass")
        self.spinBox.setValue(1)
        self.lineEdit_forMin.clear()
        self.lineEdit_forMax.clear()

        self.update_plot()
        self.event_log("Фильтр сброшен")

    def event_log(self, message: str): # Журнал событий
        """
        Записывает событие в (Журнал событий)
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = "lightgreen"
        if "Ошибка" in message or "ошибка" in message:
            color = "red"
        elif "Загрузка" in message or "фильтр" in message:
            color = "yellow"
        self.textBrowser.append(f"<font color='{color}'>[{timestamp}] {message}</font>")
        self.textBrowser.verticalScrollBar().setValue(
            self.textBrowser.verticalScrollBar().maximum()
        )

def main():
    app = QApplication(sys.argv)
    window = BandPassApp()
    window.show()
    return app.exec()

if __name__ == "__main__":
    main()