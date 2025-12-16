import numpy as np
import pyqtgraph as pg

class MapRenderer:
    def __init__(self, plot_widget):
        """
        Функия управелния отрисовкой тепловой карты.
        plot_widget: pyqtgraph.PlotWidget — виджет для отображения
        """
        self.plot_widget = plot_widget

        # Создаём ImageItem
        self.image_item = pg.ImageItem()
        self.plot_widget.addItem(self.image_item)

        # Настройки отображения
        self.plot_widget.setAspectLocked(False)
        self.plot_widget.invertY(True)

    def display_heatmap(self, data: np.ndarray):
        """
        Фунция отображения тепловой карты из numpy-массива.
        data: 2D numpy массив
        """
        if data is None or data.size == 0:
            self.clear()
            return

        lut = pg.colormap.get('CET-D1').getLookupTable()
        self.image_item.setLookupTable(lut)

        # Настройка уровней яркости
        vmax = np.nanpercentile(data, 98)  # 98-й процентиль
        vmin = np.nanpercentile(data, 2)  # 2-й процентиль

        # Отображаем с настроенными уровнями
        self.image_item.setImage(data, levels=(vmin, vmax))
        self.plot_widget.autoRange()

    def clear(self):
        """
        Функция для очистки карты
        """
        self.image_item.clear()
