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

        colors = [(0, 0, 100),  (0, 100, 200),  (200, 200, 100),  (100, 200, 100),  (150, 50, 50)]
        pos = np.linspace(0.0, 1.0, len(colors))
        cmap = pg.ColorMap(pos, colors)
        lut = cmap.getLookupTable(nPts=256)

        self.image_item.setLookupTable(lut)
        self.image_item.setImage(data)
        self.plot_widget.autoRange()
    def clear(self):
        """
            Функция для очистки карты
        """
        self.image_item.clear()
