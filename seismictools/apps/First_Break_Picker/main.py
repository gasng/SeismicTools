import sys
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog, QLayout, QLayoutItem, QWidget

from seismictools.apps.First_Break_Picker.Calculate.Data.SeismicPicks import Picks_data
from seismictools.apps.First_Break_Picker.UI.Settings.SettingsWidget import Ui_MainWindow
from seismictools.apps.First_Break_Picker.Controller.WorkerReader import WorkerReader
from seismictools.apps.First_Break_Picker.UI.View.ViewWidget import ViewWidget


class FirstBreakPicker(QtWidgets.QMainWindow):
    def __init__(self):
        super(FirstBreakPicker, self).__init__()
        self.threadpool = QtCore.QThreadPool()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #######################################Перечисление виджетов####################################################
        self.worker_reader = None
        self.view_widget = None

        #######################################Перечисление виджетов####################################################

        #################################################Кнопки#########################################################
        self.ui.Upload_buttom.clicked.connect(self.load_sgy)
        self.ui.pushButton.clicked.connect(self.toggle_display_mode)
        self.ui.Clear_buttom.clicked.connect(self.clear_sgy)

        #################################################Кнопки#########################################################

        self.display_mode = "heatmap"
        self.init_plot()
        Pick_type = self.ui.Picks_choose
        Pick_type.addItem('First_Break')
        Pick_type.addItem('Refraction')
        Pick_type.addItem('Reflection')
        Pick_type.currentTextChanged.connect(self.set_pick_type)
    ##################################Подключение виждета смены режимов отображения#####################################
    def toggle_display_mode(self):
        return None

    ##################################Подключение виждета отображения фаилов############################################
    def init_plot(self):

        self.view_widget = ViewWidget()
        self.ui.verticalLayout_2.addWidget(self.view_widget)
        self.view_widget.signals.result.connect(self.on_pick_added)
        self.view_widget.signals.error.connect(self.on_error)

    ##################################Подключение виждета загрузки фаилов###############################################
    def load_sgy(self):
        filepath = self.ui.SGY_files_line.text().strip()
        if not filepath:
            filepath, _ = QFileDialog.getOpenFileName(
                self, "Выбрать SGY-файл", "", "SGY Files (*.sgy *.segy)"
            )
            if not filepath:
                return
            self.ui.SGY_files_line.setText(filepath)
        self.worker_reader = WorkerReader(filepath)
        self.worker_reader.signals.result.connect(self.on_data_loaded)
        self.worker_reader.signals.error.connect(self.on_error)
        self.threadpool.start(self.worker_reader)

    #######################################Функция пересылки результата загрузки########################################
    def on_data_loaded(self, data):  #
        self.current_data = data
        self.view_widget.getData(data)
        self.ui.Tab_widget.setCurrentWidget(self.ui.Plotting_Page)
        self.ui.statusbar.showMessage("Файл загружен", 3000)

    #Функция очистки всего...
    def clear_sgy(self):
        self.view_widget.clear()
        self.ui.SGY_files_line.clear()


    def print_message(self, string):
        return None

    def on_pick_added(self, pick_data : Picks_data):
        self.add_to_log(f"Пик добавлен: трасса {pick_data.trace_index}, время {pick_data.time}")

    def set_pick_type(self, pick_type):
        self.view_widget.set_pick_type(pick_type)
    ##################################Блок обработки ошибок#############################################################
    def on_error(self, error_msg: str):
        # 1. Добавляем в лог
        self.add_to_log(f"[ОШИБКА] {error_msg}")

    def add_to_log(self, message: str):
        """Добавляет сообщение в лог-виджет"""
        # Если используете QListWidget:
        self.ui.Log_line.addItem(message)
        self.ui.Log_line.scrollToBottom()


        #Конец класса



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FirstBreakPicker()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()



