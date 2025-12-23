import logging
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QMessageBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
import pyqtgraph as pg

logger = logging.getLogger(__name__)

class ViewWidget(QWidget):
    polygon_finished = Signal(object)
    MAX_POLYGON_POINTS = 500

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.carotage_widget = QWidget()
        self.carotage_layout = QHBoxLayout(self.carotage_widget)
        self.carotage_layout.setContentsMargins(0, 0, 0, 0)
        self.carotage_layout.setSpacing(1)

        self.scroll_area.setWidget(self.carotage_widget)
        layout.addWidget(self.scroll_area, 2)

        self.crossplot_widget = pg.PlotWidget(title="Кросс-плот")
        self.crossplot_widget.setBackground('w')
        self.crossplot_widget.setLabel('left', 'Y')
        self.crossplot_widget.setLabel('bottom', 'X')
        self.crossplot_widget.showGrid(True, True)
        layout.addWidget(self.crossplot_widget, 1)

        self.scatter_items = {}
        self.crossplot_scatter = None
        self.polygon_points = []
        self.polygon_mode = False
        self.all_depth = None
        self.all_curves = {}
        self.depth_name = None
        self.plot_widgets = []
        self.fill_items = {}
        self.current_labels = None
        self.current_colors = {}
        self.class_scatter = None
        self._syncing = False
        self._sync_handlers = []
        self.x_ranges = {}
        self.original_scatter_data = None
        self.original_labels = None

        self.crossplot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)

    def on_mouse_click(self, event):
        if not self.polygon_mode:
            return

        if len(self.polygon_points) >= self.MAX_POLYGON_POINTS:
            logger.warning("Достигнут лимит точек полигона (%d). Новые клики игнорируются.", self.MAX_POLYGON_POINTS)
            return

        view_box = self.crossplot_widget.getViewBox()
        pos = event.scenePos()
        scene_pos_in_view = view_box.mapSceneToView(pos)

        if event.button() == Qt.LeftButton:
            self.polygon_points.append((scene_pos_in_view.x(), scene_pos_in_view.y()))
            self.update_polygon()
        elif event.button() == Qt.RightButton:
            self.finish_polygon()

    def start_polygon_mode(self):
        if self.crossplot_scatter is None:
            QMessageBox.warning(self, "Ошибка", "Сначала постройте кросс-плот.")
            return
            
        self.polygon_mode = True
        self.polygon_points = []
        self.update_polygon()
        logger.info("Режим полигона включён: ЛКМ — добавить точку, ПКМ — завершить.")

    def update_polygon(self):
        for item in list(self.crossplot_widget.items()):
            if hasattr(item, '_temp_polygon'):
                try:
                    self.crossplot_widget.removeItem(item)
                except:
                    pass

        if len(self.polygon_points) == 1:
            pt = pg.ScatterPlotItem(
                x=[self.polygon_points[0][0]],
                y=[self.polygon_points[0][1]],
                size=8,
                pen=pg.mkPen('orange', width=2),
                brush=pg.mkBrush('orange')
            )
            pt._temp_polygon = True
            self.crossplot_widget.addItem(pt)
        elif len(self.polygon_points) > 1:
            pen = pg.mkPen('orange', width=2)
            x_vals = [p[0] for p in self.polygon_points]
            y_vals = [p[1] for p in self.polygon_points]
            line = pg.PlotDataItem(x_vals, y_vals, pen=pen)
            line._temp_polygon = True
            self.crossplot_widget.addItem(line)
            
            scatter = pg.ScatterPlotItem(
                x=x_vals,
                y=y_vals,
                size=8,
                pen=pg.mkPen('orange', width=2),
                brush=pg.mkBrush('orange')
            )
            scatter._temp_polygon = True
            self.crossplot_widget.addItem(scatter)

    def finish_polygon(self):
        self.polygon_mode = False

        for item in list(self.crossplot_widget.items()):
            if hasattr(item, '_temp_polygon'):
                try:
                    self.crossplot_widget.removeItem(item)
                except:
                    pass

        if len(self.polygon_points) < 3:
            self.polygon_points = []
            QMessageBox.warning(self, "Ошибка", "Для создания полигона нужно минимум 3 точки.")
            return

        try:
            if len(self.polygon_points) > 200:
                step = max(1, len(self.polygon_points) // 200)
                simplified = self.polygon_points[::step]
                if len(simplified) < 3:
                    simplified = self.polygon_points[:200]
                closed_points = simplified + [simplified[0]]
            else:
                closed_points = self.polygon_points + [self.polygon_points[0]]

            if self.crossplot_scatter is not None:
                x_data, y_data = self.crossplot_scatter.getData()
                
                if len(x_data) > 0 and len(y_data) > 0:
                    points = np.column_stack((x_data, y_data))
                    poly = np.array(closed_points)
                    inside = self.points_in_polygon(points, poly)
                    indices = np.where(inside)[0]
                    self.polygon_finished.emit(indices)
                    logger.info(f"Полигон завершен: {len(indices)} точек внутри")

        except Exception as e:
            logger.error(f"Ошибка полигона: {e}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обработки полигона: {e}")

        self.polygon_points = []

    def points_in_polygon(self, points, poly):
        if len(poly) < 3 or len(points) == 0:
            return np.zeros(len(points), dtype=bool)

        poly = np.asarray(poly)
        points = np.asarray(points)

        n = len(poly)
        inside = np.zeros(len(points), dtype=bool)

        for i, (x, y) in enumerate(points):
            if not np.isfinite(x) or not np.isfinite(y):
                continue

            j = n - 1
            odd = False
            for k in range(n):
                if ((poly[k][1] > y) != (poly[j][1] > y)):
                    if abs(poly[j][1] - poly[k][1]) < 1e-12:
                        j = k
                        continue
                    intersect_x = (poly[j][0] - poly[k][0]) * (y - poly[k][1]) / (poly[j][1] - poly[k][1]) + poly[k][0]
                    if x < intersect_x:
                        odd = not odd
                j = k
            inside[i] = odd

        return inside

    def clear_carotage(self):
        for handler in self._sync_handlers:
            try:
                viewbox = handler['viewbox']
                if viewbox and hasattr(viewbox, 'sigYRangeChanged'):
                    viewbox.sigYRangeChanged.disconnect(handler['handler'])
            except:
                pass
        self._sync_handlers.clear()
        
        while self.carotage_layout.count():
            child = self.carotage_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.scatter_items.clear()
        self.plot_widgets = []
        self.fill_items = {}
        self.x_ranges.clear()
        self.all_depth = None
        self.all_curves = {}
        self.depth_name = None
        logger.debug("Каротаж очищен.")

    def clear_crossplot(self):
        if self.crossplot_scatter:
            self.crossplot_widget.removeItem(self.crossplot_scatter)
            self.crossplot_scatter = None
        if self.class_scatter:
            self.crossplot_widget.removeItem(self.class_scatter)
            self.class_scatter = None
            
        for item in list(self.crossplot_widget.items()):
            if isinstance(item, (pg.ScatterPlotItem, pg.PlotDataItem)):
                self.crossplot_widget.removeItem(item)
                
        logger.debug("Кросс-плот очищен.")

    def plot_carotage(self, curves, depth_name, scale_types=None):
        self.clear_carotage()
        
        if curves is None or depth_name not in curves:
            logger.error(f"Кривые или глубина '{depth_name}' не найдены!")
            return
            
        depth = curves.get(depth_name)
        if depth is None or len(depth) == 0:
            logger.error(f"Кривая глубины '{depth_name}' пуста!")
            return

        curve_names = [name for name in curves.keys() if name != depth_name]
        if not curve_names:
            logger.warning("Нет кривых для отображения (только глубина).")
            return

        logger.info("Отображение %d кривых: %s", len(curve_names), curve_names)

        global_min_depth = np.min(depth)
        global_max_depth = np.max(depth)

        self.all_depth = depth
        self.all_curves = curves
        self.depth_name = depth_name

        for name in curve_names:
            data = curves[name]
            if data is None or len(data) == 0:
                continue

            plot = pg.PlotWidget()
            plot.setBackground('w')
            plot.setLabel('bottom', name)
            plot.setLabel('left', 'Глубина, м')
            plot.showGrid(x=True, y=True, alpha=0.7)
            plot.setFixedWidth(250)
            
            if scale_types and name in scale_types:
                if scale_types[name] == 'log':
                    plot.getAxis('bottom').setLogMode(True)

            plot.plot(data, depth, pen=pg.mkPen("#006EFF", width=2))

            scatter = pg.ScatterPlotItem(
                size=7,
                pen=pg.mkPen('#FF0000', width=1),
                brush=pg.mkBrush(None)
            )
            plot.addItem(scatter)
            self.scatter_items[name] = scatter
            self.plot_widgets.append(plot)
            self.carotage_layout.addWidget(plot)

            plot.invertY(True)
            
            if len(data) > 0:
                valid_data = data[~np.isnan(data)]
                if len(valid_data) > 0:
                    min_val = np.min(valid_data)
                    max_val = np.max(valid_data)
                    padding = abs(max_val - min_val) * 0.1
                    if padding == 0:
                        padding = abs(min_val) * 0.1 if min_val != 0 else 1.0
                else:
                    min_val, max_val = 0, 1
                    padding = 0.1
            else:
                min_val, max_val = 0, 1
                padding = 0.1
            
            x_min = min_val - padding
            x_max = max_val + padding
            self.x_ranges[plot] = (x_min, x_max)
            
            plot.getViewBox().setXRange(x_min, x_max, padding=0)

        if self.plot_widgets:
            self._sync_plot_ranges(self.plot_widgets, global_min_depth, global_max_depth)

        self.carotage_widget.adjustSize()
        logger.info("Каротаж отображён: %d графиков.", len(self.plot_widgets))

    def _sync_plot_ranges(self, plots, global_min_depth, global_max_depth):
        if len(plots) <= 1:
            return

        for i in range(len(plots) - 1):
            viewbox1 = plots[i].getViewBox()
            viewbox2 = plots[i + 1].getViewBox()
            viewbox1.setYLink(viewbox2)
        
        first_viewbox = plots[0].getViewBox()
        first_viewbox.setYRange(global_max_depth, global_min_depth, padding=0)
        
        for plot in plots:
            viewbox = plot.getViewBox()
            viewbox.setMouseEnabled(x=False, y=True)

    def plot_crossplot(self, x, y, title=""):
        self.clear_crossplot()
        
        if hasattr(x, 'values'):
            x_array = x.values
        else:
            x_array = np.array(x)
            
        if hasattr(y, 'values'):
            y_array = y.values
        else:
            y_array = np.array(y)
        
        if len(x_array) == 0 or len(y_array) == 0:
            logger.warning("Пустые данные для кросс+pлота")
            return
            
        self.original_scatter_data = (x_array.copy(), y_array.copy())
        
        self.crossplot_scatter = pg.ScatterPlotItem(
            x=x_array, y=y_array, size=7,
            pen=pg.mkPen(None),
            brush=pg.mkBrush(100, 100, 255, 120),
            pxMode=True
        )
        
        self.crossplot_widget.addItem(self.crossplot_scatter)
        
        if title:
            self.crossplot_widget.setTitle(title)
            
        if hasattr(x, 'name'):
            self.crossplot_widget.setLabel('bottom', x.name)
        if hasattr(y, 'name'):
            self.crossplot_widget.setLabel('left', y.name)
            
        self.crossplot_widget.autoRange()
        logger.info("Кросс-плот построен: '%s' (%d точек)", title, len(x_array))

    def update_crossplot_with_classes(self, labels, colors, x_data, y_data):
        if x_data is None or y_data is None or len(x_data) == 0 or len(y_data) == 0:
            logger.debug("Кросс-плот: данные пусты")
            return
            
        if labels is None:
            logger.warning("Кросс-плот: labels is None")
            return
            
        if len(labels) != len(x_data):
            logger.error("Несовпадение длины labels и данных: %d != %d", len(labels), len(x_data))
            return

        self.current_labels = labels.copy()
        self.current_colors = colors.copy()

        brushes = []
        for i in range(len(x_data)):
            cls = labels[i]
            if cls == 0:
                brushes.append(pg.mkBrush(100, 100, 255, 120))
            else:
                color = colors.get(cls, "#808080")
                try:
                    if isinstance(color, str):
                        qcolor = pg.mkColor(color)
                    elif isinstance(color, (tuple, list)) and len(color) >= 3:
                        if len(color) == 3:
                            qcolor = pg.mkColor(color[0], color[1], color[2])
                        else:
                            qcolor = pg.mkColor(color[0], color[1], color[2], color[3] if len(color) > 3 else 255)
                    else:
                        qcolor = pg.mkColor(128, 128, 128)
                except:
                    qcolor = pg.mkColor(128, 128, 128)
                brushes.append(pg.mkBrush(qcolor))

        if self.crossplot_scatter:
            self.crossplot_scatter.setData(x=x_data, y=y_data, brush=brushes)
        else:
            self.crossplot_scatter = pg.ScatterPlotItem(
                x=x_data, y=y_data, size=7,
                pen=pg.mkPen(None),
                brush=brushes,
                pxMode=True
            )
            self.crossplot_widget.addItem(self.crossplot_scatter)
            
        logger.info("Кросс-плот обновлён с классами: %d точек", len(x_data))

    def _add_interval_fill(self, plot_widget, min_depth, max_depth, color, class_id):
        if plot_widget not in self.x_ranges:
            logger.warning(f"Не найден диапазон X для графика {plot_widget}")
            return
            
        x_min, x_max = self.x_ranges[plot_widget]
        
        if x_min > x_max:
            x_min, x_max = x_max, x_min
        
        if min_depth > max_depth:
            min_depth, max_depth = max_depth, min_depth
        
        try:
            qcolor = QColor(color)
            if not qcolor.isValid():
                qcolor = QColor("#FF0000")
            qcolor.setAlpha(100)
            
            xs = [x_min, x_max, x_max, x_min, x_min]
            ys = [min_depth, min_depth, max_depth, max_depth, min_depth]
            
            fill_item = pg.PlotCurveItem(
                x=xs,
                y=ys,
                pen=None,
                brush=pg.mkBrush(qcolor),
                fillLevel=0,
                fillBrush=pg.mkBrush(qcolor)
            )
            
            fill_item.setZValue(10)
            plot_widget.addItem(fill_item)
            
            if plot_widget not in self.fill_items:
                self.fill_items[plot_widget] = []
            self.fill_items[plot_widget].append(fill_item)
            
            plot_widget.update()
            
        except Exception as e:
            logger.error(f"Ошибка при создании заливки: {e}")

    def clear_carotage_fills(self):
        for plot_widget, fill_items in list(self.fill_items.items()):
            if plot_widget is None:
                continue
                
            for fill_item in fill_items:
                try:
                    plot_widget.removeItem(fill_item)
                except Exception as e:
                    logger.error(f"Ошибка при удалении заливки: {e}")
        
        self.fill_items.clear()

    def update_selected_points_colors(self, indices, class_id, color):
        if not self.crossplot_scatter:
            logger.warning("Нет scatter plot для обновления цветов")
            return
            
        if indices is None or len(indices) == 0:
            return
            
        current_x, current_y = self.crossplot_scatter.getData()
        if current_x is None or current_y is None or len(current_x) == 0:
            return
            
        self.current_colors[class_id] = color
        
        if self.current_labels is not None:
            for idx in indices:
                if idx < len(self.current_labels):
                    self.current_labels[idx] = class_id
        else:
            self.current_labels = np.zeros(len(current_x), dtype=int)
            for idx in indices:
                if idx < len(self.current_labels):
                    self.current_labels[idx] = class_id
            
        brushes = []
        for i in range(len(current_x)):
            if self.current_labels is not None and i < len(self.current_labels):
                cls = self.current_labels[i]
                if cls == 0:
                    brushes.append(pg.mkBrush(100, 100, 255, 120))
                elif cls in self.current_colors:
                    color_for_class = self.current_colors[cls]
                    brushes.append(pg.mkBrush(color_for_class))
                else:
                    brushes.append(pg.mkBrush(100, 100, 255, 120))
            else:
                brushes.append(pg.mkBrush(100, 100, 255, 120))
        
        self.crossplot_scatter.setData(x=current_x, y=current_y, brush=brushes)
        logger.info(f"Обновлены цвета {len(indices)} точек класса {class_id}")

    def clear_points_colors(self, indices):
        if not self.crossplot_scatter:
            logger.warning("Нет scatter plot для очистки цветов")
            return
            
        if indices is None or len(indices) == 0:
            return
            
        current_x, current_y = self.crossplot_scatter.getData()
        if current_x is None or len(current_x) == 0:
            return
            
        if self.current_labels is not None:
            for idx in indices:
                if idx < len(self.current_labels):
                    self.current_labels[idx] = 0
        
        brushes = []
        for i in range(len(current_x)):
            if self.current_labels is not None and i < len(self.current_labels):
                cls = self.current_labels[i]
                if cls == 0:
                    brushes.append(pg.mkBrush(100, 100, 255, 120))
                elif cls in self.current_colors:
                    color_for_class = self.current_colors[cls]
                    brushes.append(pg.mkBrush(color_for_class))
                else:
                    brushes.append(pg.mkBrush(100, 100, 255, 120))
            else:
                brushes.append(pg.mkBrush(100, 100, 255, 120))
        
        self.crossplot_scatter.setData(x=current_x, y=current_y, brush=brushes)
        logger.info(f"Очищены цвета {len(indices)} точек")

    def highlight_depth_ranges_on_carotage(self, indices_by_class=None, labels=None):
        if self.all_depth is None:
            logger.warning("Нет данных глубины для заливки")
            return
            
        if not self.x_ranges:
            logger.warning("Диапазоны X не установлены. Сначала отобразите кривые.")
            return
        
        self.clear_carotage_fills()
        
        if indices_by_class is None and labels is None:
            return
            
        class_indices = {}
        if indices_by_class is not None:
            class_indices = indices_by_class
        elif labels is not None:
            unique_classes = np.unique(labels)
            for class_id in unique_classes:
                if class_id != 0:
                    indices = np.where(labels == class_id)[0]
                    if len(indices) > 0:
                        class_indices[class_id] = indices
    
        if not class_indices:
            return
            
        depth_data = self.all_depth
        
        for class_id, indices in class_indices.items():
            if len(indices) == 0:
                continue
                
            indices_array = np.array(indices)
            valid_indices = indices_array[indices_array < len(depth_data)]
            
            if len(valid_indices) == 0:
                continue
                
            class_depths = depth_data[valid_indices]
            
            min_depth_val = np.min(class_depths)
            max_depth_val = np.max(class_depths)
            
            sort_order = np.argsort(class_depths)
            sorted_indices = valid_indices[sort_order]
            sorted_depths = depth_data[sorted_indices]
            
            intervals = []
            current_start = sorted_indices[0]
            current_start_depth = sorted_depths[0]
            
            for i in range(1, len(sorted_indices)):
                prev_idx = sorted_indices[i-1]
                curr_idx = sorted_indices[i]
                prev_depth = depth_data[prev_idx]
                curr_depth = depth_data[curr_idx]
                
                if curr_idx == prev_idx + 1 or abs(curr_depth - prev_depth) <= 2.0:
                    continue
                else:
                    current_end = sorted_indices[i-1]
                    current_end_depth = sorted_depths[i-1]
                    
                    intervals.append((
                        min(current_start_depth, current_end_depth),
                        max(current_start_depth, current_end_depth)
                    ))
                    
                    current_start = curr_idx
                    current_start_depth = curr_depth
            
            if len(sorted_indices) > 0:
                current_end = sorted_indices[-1]
                current_end_depth = sorted_depths[-1]
                intervals.append((
                    min(current_start_depth, current_end_depth),
                    max(current_start_depth, current_end_depth)
                ))
            
            if not intervals:
                intervals = [(min_depth_val, max_depth_val)]
            
            color = self.current_colors.get(class_id, "#808080")
            
            for min_depth, max_depth in intervals:
                if min_depth >= max_depth:
                    continue
                    
                for plot_widget in self.plot_widgets:
                    if plot_widget in self.x_ranges:
                        self._add_interval_fill(plot_widget, min_depth, max_depth, color, class_id)