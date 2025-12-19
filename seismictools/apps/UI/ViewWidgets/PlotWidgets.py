import pyqtgraph as pg
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout

class SeismicPlotWidget(QWidget):
    def __init__(self, original_data, filtered_data=None, split_pos=0.5):
        super().__init__()

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('black')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)

        # Создадим вертикальную палку-разделитель, или по другому drag-n-drop
        self.split_line = pg.InfiniteLine(
            angle=90,
            movable=True,
            pen=pg.mkPen(color='magenta', width=2),
            hoverPen=pg.mkPen(color='white', width=3)
        )
        self.split_line.setPos(0)
        self.plot_widget.addItem(self.split_line)

        self.marker = pg.ScatterPlotItem(
            size=12,
            symbol='o',
            brush=pg.mkBrush('w'),
            pen=pg.mkPen('magenta', width=2)
        )
        self.plot_widget.addItem(self.marker)

        self.original_data = original_data
        self.filtered_data = filtered_data
        self.split_pos = split_pos

        self.plot_data()

        self.split_line.sigPositionChanged.connect(self.split_moved)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def split_moved(self):
        """
        Данная функция нужна, чтобы обновлять маркер/кружочек на нашей вертикальной палке
        при ее передвижении.
        """
        x = self.split_line.getXPos()
        y_min, y_max = self.plot_widget.getViewBox().viewRange()[1]
        y_mid = (y_min + y_max) / 2
        self.marker.setData([x], [y_mid])

    def plot_data(self):
        """
        Отрисовка данных
        Оригинальный сигнал - слева от разделителя, отфильтрованный - справа.
        """
        if self.original_data is None:
            return
        x = np.arange(len(self.original_data))

        split_idx = int(len(x) * self.split_pos)
        self.plot_widget.clear()
        self.plot_widget.plot(x[:split_idx], self.original_data[:split_idx], pen=pg.mkPen('w', width=0.5), name="Оригинальный сигнал")
        if self.filtered_data is not None:
            self.plot_widget.plot(x[split_idx:], self.filtered_data[split_idx:], pen=pg.mkPen('b', width=0.5), name="Отфильтрованный сигнал")

        if len(x) > 0:
            x_split = x[split_idx] if split_idx < len(x) else x[-1]
            self.split_line.setPos(x_split)
            y_min, y_max = self.plot_widget.getViewBox().viewRange()[1]
            y_mid = (y_min + y_max) / 2
            self.marker.setData([x_split], [y_mid])

        self.plot_widget.enableAutoRange()

    def set_split_pos(self, pos):
        """
        Устанавливаем положение палки-разделителя
        """
        self.split_pos = max(0.0, min(1.0, pos))
        self.plot_data()