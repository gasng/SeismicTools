import logging
import os
import numpy as np
import pyqtgraph as pg

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStatusBar, QMessageBox, QProgressDialog
from PySide6.QtCore import QThreadPool, QSettings, Qt, QTimer

from seismictools.apps.Well_Logging_Classification.UI.Settings.SettingsWidget import SettingsWidget
from seismictools.apps.Well_Logging_Classification.UI.View.ViewWidget import ViewWidget
from seismictools.apps.Well_Logging_Classification.Calculate.Data.WellLogData import WellLogData
from seismictools.apps.Well_Logging_Classification.Controller.WorkerReader import WorkerReader
from seismictools.apps.Well_Logging_Classification.Controller.WorkerSaver import WorkerSaver
from seismictools.apps.Well_Logging_Classification.Controller.WorkerVisualization import WorkerVisualisation

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Открываем главное окно")
        self.setWindowTitle("Well Logging Classification")
        self.resize(1400, 800)

        self.settings = QSettings("WellLoggingApp", "Classifier")
        self.well_data = WellLogData()
        self.filepath = ""
        self.selected_indices = None
        self.current_x_curve = ""
        self.current_y_curve = ""
        self.raw_x_data = None
        self.raw_y_data = None
        self.valid_mask = None
        self.original_indices = None
        self.last_save_path = None
        self.polygons = []
        self.next_polygon_id = 1
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(3)
        self.progress_dialog = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.settings_widget = SettingsWidget()
        self.view_widget = ViewWidget()
        main_layout.addWidget(self.settings_widget, 1)
        main_layout.addWidget(self.view_widget, 3)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self._connect_signals()
        self._init_default_classes()
        self._load_last_session()

    def _connect_signals(self):
        s = self.settings_widget
        s.loadRequested.connect(self.on_load_requested)
        s.clearRequested.connect(self.on_clear_requested)
        s.plotCrossplotRequested.connect(self.on_plot_crossplot_requested)
        s.drawPolygonRequested.connect(self.on_draw_polygon_requested)
        s.assignClassRequested.connect(self.on_assign_class_requested)
        s.cancelPolygonRequested.connect(self.on_cancel_polygon_requested)
        s.clearMarkupRequested.connect(self.on_clear_markup_requested)
        s.saveRequested.connect(self.on_save_requested)
        s.addClassRequested.connect(self.on_add_class_requested)
        s.deleteClassRequested.connect(self.on_delete_class_requested)
        s.historyRequested.connect(self.on_history_requested)
        s.deletePolygonRequested.connect(self.on_delete_polygon_requested)
        s.clearAllPolygonsRequested.connect(self.on_clear_all_polygons_requested)
        self.view_widget.polygon_finished.connect(self.on_polygon_finished)
        if hasattr(self.settings_widget, 'classColorChanged'):
            self.settings_widget.classColorChanged.connect(self.on_class_color_changed)     

    def on_class_color_changed(self, class_id, new_color):
        """Обработчик изменения цвета класса."""
        if class_id in self.well_data.class_colors:

            self.well_data.class_colors[class_id] = new_color
            
            logger.info(f"Изменен цвет класса {class_id} на {new_color}")
            logger.debug(f"Текущие цвета классов: {self.well_data.class_colors}")
            
            if hasattr(self.view_widget, 'debug_colors'):
                self.view_widget.debug_colors()
            
            self._update_crossplot_with_current_classes()
            self._update_carotage_fills()
        else:
            logger.warning(f"Попытка изменить цвет несуществующего класса {class_id}")

    def _init_default_classes(self):
        self.well_data.add_class(0, "неразмечено", "#CCCCCC")
        self._update_class_table()

    def _load_last_session(self):
        last_file = self.settings.value("last_file", "")
        if last_file and os.path.exists(last_file):
            logger.info(f"Загрузка последнего сеанса: {last_file}")
            QTimer.singleShot(500, lambda: self.on_load_requested(last_file))

    def _create_progress_dialog(self, title, message):
        if self.progress_dialog:
            self.progress_dialog.close()
        progress = QProgressDialog(message, "Отмена", 0, 100, self)
        progress.setWindowTitle(title)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.canceled.connect(lambda: self.set_status("Операция отменена"))
        return progress

    def _clear_all_data(self):
        self.view_widget.clear_carotage()
        self.view_widget.clear_crossplot()
        self.selected_indices = None
        self.current_x_curve = ""
        self.current_y_curve = ""
        self.raw_x_data = None
        self.raw_y_data = None
        self.valid_mask = None
        self.original_indices = None
        self.polygons.clear()
        self.next_polygon_id = 1

    def on_load_requested(self, filepath):
        logger.info(f"Запрошена загрузка LAS-файла: {filepath}")
        self.set_status("Загрузка LAS-файла...")
        self.filepath = filepath
        self._clear_all_data()
        self.progress_dialog = self._create_progress_dialog("Загрузка файла", f"Загрузка {os.path.basename(filepath)}...")
        self.progress_dialog.setValue(10)
        self.worker_reader = WorkerReader(filepath)
        self.worker_reader.signals.started.connect(lambda: self.progress_dialog.setValue(20))
        self.worker_reader.signals.progress.connect(self.progress_dialog.setValue)
        self.worker_reader.signals.message.connect(self.set_status)
        self.worker_reader.signals.finished.connect(self._handle_load_finished)
        self.worker_reader.signals.error.connect(self._handle_load_error)
        self.thread_pool.start(self.worker_reader)
        self.settings_widget.add_to_history(filepath)

    def _handle_load_finished(self, data_dict):
        if self.progress_dialog:
            self.progress_dialog.setValue(100)
            QTimer.singleShot(500, self.progress_dialog.close)
        try:
            self.well_data.clear()
            filename = data_dict.get('filename', self.filepath)
            curves = data_dict.get('curves', {})
            metadata = data_dict.get('metadata', {})
            self.well_data.set_filename(filename)
            for name, curve_data in curves.items():
                if curve_data is not None:
                    self.well_data.add_curve(name, curve_data)
            for key, value in metadata.items():
                self.well_data.metadata[key] = value
            actual_num_points = self.well_data.get_num_points()
            if actual_num_points > 0:
                self.well_data.set_class_labels(np.zeros(actual_num_points, dtype=int))
            self._update_curve_table()
            self._update_class_table()
            depth_name = self._find_depth_curve(self.well_data.curve_names)
            if depth_name:
                self.view_widget.plot_carotage(self.well_data.curves, depth_name)
            labels_file = filename + ".labels.npy"
            if os.path.exists(labels_file):
                try:
                    labels = np.load(labels_file)
                    if len(labels) == actual_num_points:
                        self.well_data.set_class_labels(labels)
                        self._update_class_table()
                        self._update_carotage_fills()
                except Exception as e:
                    logger.error(f"Ошибка загрузки меток: {e}")
            logger.info(f"Файл успешно загружен: {filename}")
            self.set_status(f"Файл успешно загружен: {len(curves)} кривых, {actual_num_points} точек")
            self.settings.setValue("last_file", filename)
        except Exception as e:
            logger.error(f"Ошибка обработки данных: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка обработки данных: {e}")
            self.set_status(f"Ошибка: {e}")

    def _handle_load_error(self, error_msg):
        if self.progress_dialog:
            self.progress_dialog.close()
        logger.error(f"Ошибка загрузки LAS-файла: {error_msg}")
        self.set_status(f"Ошибка загрузки: {error_msg}")
        QMessageBox.critical(self, "Ошибка", error_msg)

    def _find_depth_curve(self, curve_names):
        depth_candidates = ['DEPT', 'DEPTH', 'DEPTHT', 'MD', 'TVD', '0', 'DEPTH.M', 'DEPT.M']
        for cand in depth_candidates:
            if cand in curve_names:
                return cand
        return curve_names[0] if curve_names else None

    def on_clear_requested(self):
        reply = QMessageBox.question(self, "Подтверждение", "Очистить все данные? Все несохраненные изменения будут потеряны.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            logger.info("Очистка данных")
            self._clear_all_data()
            self.well_data.clear()
            self._update_curve_table()
            self._update_class_table()
            self._update_polygon_table()
            self.set_status("Данные очищены.")

    def on_plot_crossplot_requested(self, x_curve, y_curve):
        logger.info(f"Запрошено построение кросс-плота: {x_curve} vs {y_curve}")
        self.current_x_curve = x_curve
        self.current_y_curve = y_curve
        self.set_status("Построение кросс-плота...")
        self.progress_dialog = self._create_progress_dialog("Построение кросс-плота", f"Обработка {x_curve} vs {y_curve}...")
        self.progress_dialog.setValue(10)
        self.worker_viz = WorkerVisualisation(self.well_data, x_curve, y_curve)
        self.worker_viz.signals.started.connect(lambda: self.progress_dialog.setValue(20))
        self.worker_viz.signals.progress.connect(self.progress_dialog.setValue)
        self.worker_viz.signals.message.connect(self.set_status)
        self.worker_viz.signals.finished.connect(self._handle_plot_finished)
        self.worker_viz.signals.error.connect(self._handle_plot_error)
        self.thread_pool.start(self.worker_viz)

    def _handle_plot_finished(self, result):
        if self.progress_dialog:
            self.progress_dialog.setValue(100)
            QTimer.singleShot(500, self.progress_dialog.close)
        try:
            self.raw_x_data = self.well_data.get_curve(self.current_x_curve)
            self.raw_y_data = self.well_data.get_curve(self.current_y_curve)
            if self.raw_x_data is None or self.raw_y_data is None:
                raise ValueError("Кривые не найдены")
            self.valid_mask = np.isfinite(self.raw_x_data) & np.isfinite(self.raw_y_data)
            valid_count = np.sum(self.valid_mask)
            if valid_count == 0:
                raise ValueError("Нет валидных данных для построения кросс-плота")
            self.original_indices = np.where(self.valid_mask)[0]
            self.view_widget.plot_crossplot(result['x_data'], result['y_data'], result['title'])
            self._update_crossplot_with_current_classes()
            logger.info(f"Кросс-плот построен: {result['title']} ({valid_count} точек)")
            self.set_status(f"Кросс-плот построен ({valid_count} точек)")
        except Exception as e:
            logger.error(f"Ошибка построения кросс-плота: {e}")
            self.set_status(f"Ошибка: {e}")
            QMessageBox.critical(self, "Ошибка", str(e))

    def _handle_plot_error(self, error_msg):
        if self.progress_dialog:
            self.progress_dialog.close()
        logger.error(f"Ошибка построения кросс-плота: {error_msg}")
        self.set_status(f"Ошибка: {error_msg}")
        QMessageBox.critical(self, "Ошибка", error_msg)

    def on_draw_polygon_requested(self):
        logger.info("Активация режима полигона")
        self.view_widget.start_polygon_mode()
        self.set_status("Режим полигона: ЛКМ — добавить точку, ПКМ — завершить.")

    def on_polygon_finished(self, indices):
        logger.info("Полигон завершён: %d точек", len(indices))
        if len(indices) < 3:
            self.selected_indices = None
            self.set_status("Полигон отменён: требуется минимум 3 точки.")
            return
        self.selected_indices = np.array(indices)
        self.set_status(f"Выделено {len(indices)} точек. Выберите класс и нажмите 'Присвоить'.")
        self._highlight_selected_points(indices)

    def _highlight_selected_points(self, indices):
        if self.view_widget.crossplot_scatter is None:
            return
        current_x, current_y = self.view_widget.crossplot_scatter.getData()
        if current_x is None or len(current_x) == 0:
            return
        for item in list(self.view_widget.crossplot_widget.items()):
            if hasattr(item, '_temp_selection'):
                try:
                    self.view_widget.crossplot_widget.removeItem(item)
                except:
                    pass
        if len(indices) > 0:
            selected_x = current_x[indices]
            selected_y = current_y[indices]
            temp_scatter = pg.ScatterPlotItem(x=selected_x, y=selected_y, size=12, pen=pg.mkPen('red', width=2), brush=pg.mkBrush(255, 255, 255, 0), pxMode=True)
            temp_scatter._temp_selection = True
            self.view_widget.crossplot_widget.addItem(temp_scatter)

    def on_assign_class_requested(self, class_id):
        if self.selected_indices is None or len(self.selected_indices) == 0:
            QMessageBox.warning(self, "Ошибка", "Нет выбранных точек. Сначала нарисуйте полигон.")
            return
        if class_id not in self.well_data.class_names:
            QMessageBox.warning(self, "Ошибка", f"Класс с ID {class_id} не найден.")
            return
        class_name = self.well_data.get_class_name(class_id)
        color = self.well_data.get_class_color(class_id)
        logger.info(f"Назначение класса {class_id} ({class_name}) для {len(self.selected_indices)} точек")
        if self.original_indices is None:
            QMessageBox.warning(self, "Ошибка", "Нет данных кросс-плота.")
            return
        absolute_indices = []
        for idx in self.selected_indices:
            if idx < len(self.original_indices):
                absolute_indices.append(self.original_indices[idx])
        if not absolute_indices:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить индексы точек.")
            return
        absolute_indices = np.array(absolute_indices)
        labels = self.well_data.get_class_labels()
        if labels is None:
            num_points = self.well_data.get_num_points()
            if num_points > 0:
                labels = np.zeros(num_points, dtype=int)
                self.well_data.set_class_labels(labels)
            else:
                QMessageBox.warning(self, "Ошибка", "Нет данных каротажа.")
                return
        old_labels = labels[absolute_indices].copy()
        labels[absolute_indices] = class_id
        self.well_data.set_class_labels(labels)
        polygon_id = self.next_polygon_id
        self.next_polygon_id += 1
        polygon_data = {'id': polygon_id, 'class_id': class_id, 'class_name': class_name, 'indices': absolute_indices.copy(), 'count': len(absolute_indices), 'old_labels': old_labels}
        self.polygons.append(polygon_data)
        self.view_widget.update_selected_points_colors(self.selected_indices, class_id, color)
        for item in list(self.view_widget.crossplot_widget.items()):
            if hasattr(item, '_temp_selection'):
                try:
                    self.view_widget.crossplot_widget.removeItem(item)
                except:
                    pass
        self._update_carotage_fills()
        self._update_class_table()
        self._update_polygon_table()
        self.set_status(f"Класс '{class_name}' присвоен {len(absolute_indices)} точкам")
        self.selected_indices = None

    def on_cancel_polygon_requested(self):
        logger.info("Отмена режима полигона")
        self.view_widget.finish_polygon()
        for item in list(self.view_widget.crossplot_widget.items()):
            if hasattr(item, '_temp_selection'):
                try:
                    self.view_widget.crossplot_widget.removeItem(item)
                except:
                    pass
        self.selected_indices = None
        self.set_status("Рисование полигона отменено.")

    def on_clear_markup_requested(self):
        reply = QMessageBox.question(self, "Подтверждение", "Очистить всю разметку? Все классы будут сброшены.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            logger.info("Очистка всей разметки")
            labels = self.well_data.get_class_labels()
            if labels is not None:
                marked_indices = np.where(labels > 0)[0]
                self.well_data.set_class_labels(np.zeros_like(labels, dtype=int))
                if len(marked_indices) > 0 and self.view_widget.crossplot_scatter:
                    crossplot_indices = []
                    for idx in marked_indices:
                        if self.original_indices is not None:
                            pos = np.where(self.original_indices == idx)[0]
                            if len(pos) > 0:
                                crossplot_indices.append(pos[0])
                    if crossplot_indices:
                        self.view_widget.clear_points_colors(crossplot_indices)
            self.polygons.clear()
            self._update_class_table()
            self._update_polygon_table()
            self.view_widget.clear_carotage_fills()
            self._update_crossplot_with_current_classes()
            self.set_status("Разметка очищена.")

    def on_add_class_requested(self, class_id, class_name, color):
        try:
            class_id = int(class_id)
        except (TypeError, ValueError):
            QMessageBox.critical(self, "Ошибка", "ID класса должен быть целым числом.")
            return
        if class_id in self.well_data.class_names:
            QMessageBox.warning(self, "Ошибка", f"Класс с ID {class_id} уже существует.")
            return
        if not class_name.strip():
            QMessageBox.warning(self, "Ошибка", "Имя класса не может быть пустым.")
            return
        self.well_data.add_class(class_id, class_name, color)
        self._update_class_table()
        logger.info(f"Добавлен новый класс: {class_id} - {class_name}")
        self.set_status(f"Добавлен класс: {class_name}")

    def on_delete_class_requested(self, class_id):
        if class_id not in self.well_data.class_names:
            logger.warning(f"Попытка удалить несуществующий класс: {class_id}")
            QMessageBox.warning(self, "Ошибка", f"Класс с ID {class_id} не найден.")
            return
        reply = QMessageBox.question(self, "Подтверждение", f"Удалить класс {class_id}? Все точки этого класса станут неразмеченными.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            logger.info(f"Удаление класса: {class_id}")
            labels = self.well_data.get_class_labels()
            if labels is not None:
                class_indices = np.where(labels == class_id)[0]
                labels[labels == class_id] = 0
                self.well_data.set_class_labels(labels)
                if len(class_indices) > 0 and self.view_widget.crossplot_scatter:
                    crossplot_indices = []
                    for idx in class_indices:
                        if self.original_indices is not None:
                            pos = np.where(self.original_indices == idx)[0]
                            if len(pos) > 0:
                                crossplot_indices.append(pos[0])
                    if crossplot_indices:
                        self.view_widget.clear_points_colors(crossplot_indices)
            deleted_polygons = [p for p in self.polygons if p['class_id'] == class_id]
            self.polygons = [p for p in self.polygons if p['class_id'] != class_id]
            del self.well_data.class_names[class_id]
            del self.well_data.class_colors[class_id]
            self._update_class_table()
            self._update_polygon_table()
            self._update_carotage_fills()
            self._update_crossplot_with_current_classes()
            self.set_status(f"Класс {class_id} удалён ({len(deleted_polygons)} полигонов).")

    def on_delete_polygon_requested(self, polygon_id):
        polygon_index = -1
        polygon_to_remove = None
        for i, poly in enumerate(self.polygons):
            if poly['id'] == polygon_id:
                polygon_index = i
                polygon_to_remove = poly
                break
        if polygon_to_remove is None:
            logger.warning(f"Попытка удаления несуществующего полигона: ID {polygon_id}")
            self.set_status("Ошибка: полигон не найден.")
            return
        reply = QMessageBox.question(self, "Подтверждение", f"Удалить полигон ID {polygon_id} класса {polygon_to_remove['class_name']}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            labels = self.well_data.get_class_labels()
            if labels is not None and 'old_labels' in polygon_to_remove:
                labels[polygon_to_remove['indices']] = polygon_to_remove['old_labels']
                self.well_data.set_class_labels(labels)
            self.polygons.pop(polygon_index)
            if self.view_widget.crossplot_scatter and self.original_indices is not None:
                crossplot_indices = []
                for idx in polygon_to_remove['indices']:
                    pos = np.where(self.original_indices == idx)[0]
                    if len(pos) > 0:
                        crossplot_indices.append(pos[0])
                if crossplot_indices:
                    self.view_widget.clear_points_colors(crossplot_indices)
            self._update_carotage_fills()
            self._update_crossplot_with_current_classes()
            self._update_polygon_table()
            self.set_status(f"Полигон ID {polygon_id} удалён.")

    def on_clear_all_polygons_requested(self):
        reply = QMessageBox.question(self, "Подтверждение", "Очистить все полигоны? Все классы будут сброшены.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            logger.info("Очистка всех полигонов")
            all_indices = []
            for poly in self.polygons:
                all_indices.extend(poly['indices'])
            labels = self.well_data.get_class_labels()
            if labels is not None:
                labels[all_indices] = 0
                self.well_data.set_class_labels(labels)
                if len(all_indices) > 0 and self.view_widget.crossplot_scatter:
                    crossplot_indices = []
                    for idx in all_indices:
                        if self.original_indices is not None:
                            pos = np.where(self.original_indices == idx)[0]
                            if len(pos) > 0:
                                crossplot_indices.append(pos[0])
                    if crossplot_indices:
                        self.view_widget.clear_points_colors(crossplot_indices)
            self.polygons.clear()
            self.view_widget.clear_carotage_fills()
            self._update_crossplot_with_current_classes()
            self._update_polygon_table()
            self.set_status("Вся разметка очищена.")

    def on_save_requested(self, filepath):
        logger.info(f"Запрошено сохранение LAS-файла: {filepath}")
        self.set_status("Сохранение LAS-файла...")
        self.last_save_path = filepath
        self.progress_dialog = self._create_progress_dialog("Сохранение файла", f"Сохранение {os.path.basename(filepath)}...")
        self.progress_dialog.setValue(10)
        if self.well_data.class_labels is not None:
            labels_file = filepath + ".labels.npy"
            try:
                np.save(labels_file, self.well_data.class_labels)
            except Exception as e:
                logger.error(f"Ошибка сохранения меток: {e}")
        self.settings.setValue("last_file", filepath)
        self.worker_saver = WorkerSaver(filepath, self.well_data)
        self.worker_saver.signals.started.connect(lambda: self.progress_dialog.setValue(20))
        self.worker_saver.signals.progress.connect(self.progress_dialog.setValue)
        self.worker_saver.signals.message.connect(self.set_status)
        self.worker_saver.signals.finished.connect(self._handle_save_finished)
        self.worker_saver.signals.error.connect(self._handle_save_error)
        self.thread_pool.start(self.worker_saver)

    def _handle_save_finished(self, success):
        if self.progress_dialog:
            self.progress_dialog.setValue(100)
            QTimer.singleShot(500, self.progress_dialog.close)
        if success:
            logger.info(f"Файл успешно сохранён: {self.last_save_path}")
            class_curves = [name for name in self.well_data.curve_names if name.startswith('CLASS_')]
            if class_curves:
                message = f"Файл сохранён: {self.last_save_path}\n\nСохранено {len(class_curves)} кривых классов:\n"
                for curve_name in class_curves:
                    message += f"• {curve_name}\n"
                QMessageBox.information(self, "Сохранение успешно", message)
            else:
                self.set_status(f"Файл сохранён: {self.last_save_path}")
        else:
            logger.error("Неизвестная ошибка при сохранении")
            self.set_status("Неизвестная ошибка при сохранении.")

    def _handle_save_error(self, error_msg):
        if self.progress_dialog:
            self.progress_dialog.close()
        logger.error(f"Ошибка сохранения LAS-файла: {error_msg}")
        self.set_status(f"Ошибка сохранения: {error_msg}")
        QMessageBox.critical(self, "Ошибка", error_msg)

    def on_history_requested(self, filepath):
        logger.info(f"Загрузка из истории: {filepath}")
        self.on_load_requested(filepath)

    def _update_curve_table(self):
        if not self.well_data.curve_names:
            self.settings_widget.populate_curve_table([])
            self.settings_widget.populate_curve_combos([])
            return
        
        regular_curves = []
        class_curves = []
        
        for name in self.well_data.curve_names:
            data = self.well_data.get_curve(name)
            if data is not None:
                finite_data = data[np.isfinite(data)]
                if len(finite_data) > 0:
                    min_val = np.min(finite_data)
                    max_val = np.max(finite_data)
                    delta = max_val - min_val
                    
                    if name.startswith('CLASS_'):
                        class_curves.append((name, min_val, max_val, delta))
                    else:
                        regular_curves.append((name, min_val, max_val, delta))
        
        self.settings_widget.populate_curve_table(regular_curves)
        
        regular_curve_names = [name for name in self.well_data.curve_names 
                            if not name.startswith('CLASS_')]
        self.settings_widget.populate_curve_combos(regular_curve_names)
        
        if hasattr(self.settings_widget, 'populate_class_curves_table') and class_curves:
            self.settings_widget.populate_class_curves_table(class_curves)

    def _update_class_table(self):
        labels = self.well_data.get_class_labels()
        class_info = []
        for class_id in sorted(self.well_data.class_names.keys()):
            if class_id == 0:
                continue
            count = np.sum(labels == class_id) if labels is not None else 0
            name = self.well_data.get_class_name(class_id)
            class_info.append((class_id, name, count))
        
        class_colors = self.well_data.class_colors.copy() if hasattr(self.well_data, 'class_colors') else {}
        
        self.settings_widget.populate_class_table(class_info, class_colors)

    def _update_polygon_table(self):
        polygon_info = []
        for poly in self.polygons:
            polygon_info.append((poly['id'], poly['class_name'], poly['count']))
        self.settings_widget.populate_polygon_table(polygon_info)

    def _update_carotage_fills(self):
        labels = self.well_data.get_class_labels()
        if labels is None or self.view_widget.all_depth is None:
            return
        indices_by_class = {}
        for class_id in self.well_data.class_names.keys():
            if class_id != 0:
                class_indices = np.where(labels == class_id)[0]
                if len(class_indices) > 0:
                    indices_by_class[class_id] = class_indices
        if indices_by_class:
            if hasattr(self.view_widget, 'highlight_depth_ranges_on_carotage'):
                self.view_widget.highlight_depth_ranges_on_carotage(indices_by_class=indices_by_class)

            elif hasattr(self.view_widget, 'highlight_depth_ranges_on_carotage'):
                self.view_widget.highlight_depth_ranges_on_carotage(indices_by_class=indices_by_class)

            else:
                logger.warning("Метод highlight_depth_ranges_on_carotage не найден в ViewWidget")

                for method_name in dir(self.view_widget):
                    if 'highlight' in method_name.lower() or 'carotage' in method_name.lower():
                        logger.info(f"Найден похожий метод: {method_name}")

    def _update_crossplot_with_current_classes(self):
        if self.raw_x_data is None or self.raw_y_data is None or self.valid_mask is None:
            return
        labels = self.well_data.get_class_labels()
        if labels is None:
            return
        if len(labels) != len(self.raw_x_data):
            return
        x_clean = self.raw_x_data[self.valid_mask]
        y_clean = self.raw_y_data[self.valid_mask]
        labels_clean = labels[self.valid_mask]
        if len(x_clean) == 0 or len(y_clean) == 0:
            return
        if len(labels_clean) != len(x_clean):
            return
        colors = {cid: self.well_data.get_class_color(cid) for cid in self.well_data.class_names}
        self.view_widget.update_crossplot_with_classes(labels_clean, colors, x_clean, y_clean)

    def set_status(self, message):
        self.status_bar.showMessage(message)

    def closeEvent(self, event):
        if hasattr(self.well_data, 'filename') and self.well_data.filename:
            self.settings.setValue("last_file", self.well_data.filename)
        self.thread_pool.clear()
        self.thread_pool.waitForDone(1000)
        super().closeEvent(event)