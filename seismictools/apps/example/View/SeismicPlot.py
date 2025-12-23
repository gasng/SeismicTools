import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class GatherPlotWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.plot_widget = None
        self.scatter_plot_item = None
        self.scatter_data_x = []
        self.scatter_data_y = []
        self.__plot_data()
        self.__create_callbacks()

    def __create_callbacks(self):
        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClicked)

    def mouseClicked(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.scatter_plot_item = pg.ScatterPlotItem(size=10, symbol='o', brush='r')
            self.plot_widget.addItem(self.scatter_plot_item)

            pos = self.plot_widget.plotItem.vb.mapSceneToView(event.pos())
            x_data = pos.x()
            y_data = pos.y()

            self.scatter_data_x.append(x_data)
            self.scatter_data_y.append(y_data)
            self.scatter_plot_item.setData(x=self.scatter_data_x, y=self.scatter_data_y)
            super().mousePressEvent(event)

    def __plot_data(self):
        if self.plot_widget:
            self.plot_widget.clear()
        self.plot_widget = pg.PlotWidget()
        idx = np.random.randint(low=0, high=len(self.data))
        self.plot_widget.plot(self.data[idx])
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
