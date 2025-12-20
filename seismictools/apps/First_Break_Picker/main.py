import sys
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog, QLayout, QLayoutItem, QWidget, QMessageBox, QTableWidgetItem
import json
from PySide6.QtWidgets import QFileDialog, QMessageBox
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

        self.init_plot()
        #######################################Перечисление виджетов####################################################

        # Подключаем сигналы ОТ ViewWidget
        self.view_widget.pickSignal.pick_added.connect(self._add_or_update_pick_in_table)
        self.view_widget.pickSignal.pick_removed.connect(self.on_pick_removed)

        # Подключаем кнопки удаления
        self.ui.Delite_one_buttom.clicked.connect(self.delete_selected_pick)
        self.ui.Delite_all_buttom.clicked.connect(self.delete_all_picks)

        #################################################Кнопки#########################################################
        self.ui.Upload_buttom.clicked.connect(self.load_sgy)
        self.ui.Clear_buttom.clicked.connect(self.clear_sgy)
        self.ui.Save_Picks_buttom.clicked.connect(self.save_picks_to_json)
        self.ui.Load_Picks_buttom.clicked.connect(self.load_picks_from_json)
        #################################################Списки#########################################################
        Map_modes = self.ui.Toggele_mode
        Map_modes.addItems(['seismic', 'viridis', 'CET-L1', 'bwr', 'inferno',
                            'magma'])
        Map_modes.currentTextChanged.connect(self.toggle_display_mode)

        Pick_type = self.ui.Picks_choose
        Pick_type.addItem('First_Break')
        Pick_type.addItem('Refraction')
        Pick_type.addItem('Reflection')
        Pick_type.currentTextChanged.connect(self.set_pick_type)
    ##################################Подключение виждета смены режимов отображения#####################################
    def toggle_display_mode(self, display_mode):
        self.view_widget.change_display_mode(display_mode)



    ##################################Подключение виждета отображения фаилов############################################
    def init_plot(self):

        self.view_widget = ViewWidget()
        self.ui.verticalLayout_2.addWidget(self.view_widget)
        self.view_widget.pickSignal.pick_added.connect(self._add_or_update_pick_in_table)
        self.view_widget.signals.error.connect(self.on_error)
        self.view_widget.signals.message.connect(self.print_message)

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
        self.worker_reader.signals.message.connect(self.print_message)
        self.view_widget.pickSignal.picks_interpolated.connect(self.on_picks_interpolated)
        self.worker_reader.signals.error.connect(self.on_error)
        self.threadpool.start(self.worker_reader)

    #######################################Функция пересылки результата загрузки########################################
    def on_data_loaded(self, data):  #
        self.current_data = data
        self.view_widget.getData(data)
        self.ui.Tab_widget.setCurrentWidget(self.ui.Plotting_Page)

    def print_message(self, string):
        self.add_to_log(string)

    #Функция очистки всего...
    def clear_sgy(self):
        self.view_widget.clear()
        self.ui.SGY_files_line.clear()
        self.print_message('Files cleared')

    def delete_selected_pick(self):
        current_row = self.ui.Picks_table_widget.currentRow()
        if current_row < 0:
            return

        trace_str = self.ui.Picks_table_widget.item(current_row, 0).text()
        type_str = self.ui.Picks_table_widget.item(current_row, 2).text()

        trace_idx = int(trace_str) - 1  # конвертация 1→0

        # ===== ИСПОЛЬЗУЕМ СТАНДАРТНЫЙ МЕТОД =====
        self.view_widget.remove_pick(trace_idx, type_str)

        # Удаляем из таблицы
        self.ui.Picks_table_widget.removeRow(current_row)

    def delete_all_picks(self):
        """Удаляет все пики"""
        reply = QMessageBox.question(
            self, "Подтверждение", "Удалить все пики?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.view_widget.clear_all_picks()
            self.ui.Picks_table_widget.setRowCount(0)
            self.add_to_log("Все пики удалены")

    def on_picks_interpolated(self, pick_type: str, picks_list: list):
        """Добавляет несколько пиков за один раз"""
        for trace_idx, time_idx in picks_list:
            self._add_or_update_pick_in_table(trace_idx, time_idx, pick_type)

    def _add_or_update_pick_in_table(self, trace_idx: int, time_idx: float, pick_type: str):
        """Вспомогательный метод для добавления/обновления пика"""
        trace_ui = str(trace_idx + 1)
        for row in range(self.ui.Picks_table_widget.rowCount()):
            trace_item = self.ui.Picks_table_widget.item(row, 0)
            type_item = self.ui.Picks_table_widget.item(row, 2)
            if (trace_item and type_item and
                    trace_item.text() == trace_ui and
                    type_item.text() == pick_type):
                self.ui.Picks_table_widget.item(row, 1).setText(str(time_idx))
                return
        # Добавляем новую строку
        row = self.ui.Picks_table_widget.rowCount()
        self.ui.Picks_table_widget.insertRow(row)
        self.ui.Picks_table_widget.setItem(row, 0, QTableWidgetItem(trace_ui))
        self.ui.Picks_table_widget.setItem(row, 1, QTableWidgetItem(str(time_idx)))
        self.ui.Picks_table_widget.setItem(row, 2, QTableWidgetItem(pick_type))

    def on_pick_removed(self, trace_idx: int, pick_type: str):
        """Удаляет пик из таблицы по данным из ViewWidget"""
        for row in range(self.ui.Picks_table_widget.rowCount()):
            trace_item = self.ui.Picks_table_widget.item(row, 0)
            type_item = self.ui.Picks_table_widget.item(row, 2)

            if (trace_item and type_item and
                    int(trace_item.text()) - 1 == trace_idx and  # конвертация 1→0
                    type_item.text() == pick_type):
                self.ui.Picks_table_widget.removeRow(row)
                self.add_to_log(f"Пик удалён: трасса {trace_idx + 1}, тип {pick_type}")
                break

    def set_pick_type(self, pick_type):
        self.view_widget.set_pick_type(pick_type)

    def save_picks_to_json(self):
        """Сохраняет все пики из ViewWidget в JSON-файл"""
        # Проверка: есть ли пики
        if not self.view_widget.picks:
            QMessageBox.warning(self, "Сохранение", "Нет пиков для сохранения!")
            return

        # Формируем структуру данных
        picks_data = {}
        for pick_type, traces_dict in self.view_widget.picks.items():
            picks_data[pick_type] = [
                {
                    "trace": trace_idx + 1,  # нумерация с 1 для пользователя
                    "time": float(time_idx)
                }
                for trace_idx, time_idx in traces_dict.items()
            ]

        # Диалог сохранения
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить пики",
            "",
            "JSON Files (*.json)"
        )

        if not filepath:
            return  # Отмена пользователем

        # Добавляем расширение .json, если его нет
        if not filepath.endswith('.json'):
            filepath += '.json'

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(picks_data, f, indent=2, ensure_ascii=False)
            self.add_to_log(f"Пики сохранены: {filepath}")
            QMessageBox.information(self, "Успех", f"Пики сохранены в:\n{filepath}")
        except Exception as e:
            error_msg = f"Ошибка сохранения: {str(e)}"
            self.add_to_log(error_msg)
            QMessageBox.critical(self, "Ошибка", error_msg)

    def load_picks_from_json(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Загрузить пики", "", "JSON Files (*.json)"
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                picks_data = json.load(f)

            # Очищаем текущие пики
            self.view_widget.clear_all_picks()
            self.ui.Picks_table_widget.setRowCount(0)

            # Добавляем новые пики
            for pick_type, picks_list in picks_data.items():
                for pick in picks_list:
                    trace_idx = pick["trace"] - 1  # конвертация 1→0
                    time_idx = pick["time"]
                    self.view_widget.add_pick(trace_idx, time_idx, pick_type)

            self.add_to_log(f"Пики загружены: {filepath}")
            QMessageBox.information(self, "Успех", "Пики загружены!")

        except Exception as e:
            error_msg = f"Ошибка загрузки: {str(e)}"
            self.add_to_log(error_msg)
            QMessageBox.critical(self, "Ошибка", error_msg)

    ##################################Блок обработки ошибок#############################################################

    def on_error(self, error_msg: str):
        # 1. Добавляем в лог
        self.add_to_log(f"[ОШИБКА] {error_msg}")

    def add_to_log(self, message: str):
        """Добавляет сообщение в лог-виджет"""
        # Если используете QListWidget:
        self.ui.Log_line.addItem(message)
        self.ui.Log_line.scrollToBottom()

    ######################################Конец класса##################################################################



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FirstBreakPicker()
    window.show()

    return app.exec_()

if __name__ == '__main__':
    main()



