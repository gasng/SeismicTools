import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6 import QtCore
import numpy as np

class GatherPlotWidget(QWidget):
    def __init__(self, model, on_ray_selected=None, delta=1.0):
        super().__init__()
        self.model = model
        self.on_ray_selected = on_ray_selected
        self.delta = delta
        self.plot_widget = None
        self.trajectory_lines = dict()
        self.start_point = None
        self.is_drawing_vector = False
        self.theta = None
        self.vector = None
        self.plot_model()
        self.create_callbacks()

    def plot_model(self):
        self.plot_widget = pg.PlotWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)
        nz, nx = self.model.shape
        width_phys = nx * self.delta
        height_phys = nz * self.delta
        self.plot_widget.setBackground('w')
        view_box = self.plot_widget.plotItem.getViewBox()
        view_box.invertY(True)

        view_box.setMouseEnabled(x=True, y=True)

        view_box.setAspectLocked(lock=True, ratio=1.0)
        view_box.setLimits(
            minXRange=width_phys / 50,
            minYRange=height_phys / 50,
            maxXRange=width_phys,
            maxYRange=height_phys,
            xMin=0, xMax=width_phys,
            yMin=0, yMax=height_phys,
        )

        img = pg.ImageItem(self.model.T)
        img.setLevels([np.min(self.model), np.max(self.model)])

        pos = [0.0, 0.5, 1.0]
        color = [(255, 255, 255), (0, 0, 150), (150, 0, 0)]
        cmap = pg.ColorMap(pos, color)

        pos = [0.0, 0.25, 0.5, 0.75, 1.0]
        color = [(30, 144, 255), (100, 200, 150), (255, 255, 100), (255, 165, 0), (255, 69, 0)]
        cmap = pg.ColorMap(pos, color)
        img.setLookupTable(cmap.getLookupTable())

        self.plot_widget.plotItem.showAxis('top', show=True)
        self.plot_widget.plotItem.showAxis('bottom', show=False)
        top_axis = self.plot_widget.plotItem.getAxis('top')
        top_axis.setLabel('X, м')
        top_axis.setStyle(tickLength=-5)

        img.setLevels([np.min(self.model), np.max(self.model)])
        img.setLookupTable(cmap.getLookupTable())
        img.setRect((0, 0, width_phys, height_phys))
        self.plot_widget.addItem(img)
        self.plot_widget.setLabel('left', 'Z, м')


    def animate_trajectory(self, trajectory: np.ndarray, name):
        self.plot_widget.removeItem(self.vector)
        self.vector = None
        self.is_drawing_vector = False

        self.trajectory_lines[name] = pg.PlotDataItem(x=[trajectory[0, 0]], y=[trajectory[0, 1]], pen=pg.mkPen('white', width=3), symbol='o', symbolSize=4, symbolBrush='white')

        self.plot_widget.addItem(self.trajectory_lines[name])

        timer = QtCore.QTimer(self)
        index = [1]
        k = 100

        def update():
            if index[0] < len(trajectory) - len(trajectory)//k:
                x_data = trajectory[:index[0]+len(trajectory)//k, 0]
                z_data = trajectory[:index[0]+len(trajectory)//k, 1]
                self.trajectory_lines[name].setData(x=x_data, y=z_data)
                index[0] += len(trajectory)//k
            else:
                timer.stop()
                timer.deleteLater()
                self.trajectory_lines[name].setData(x=trajectory[:, 0], y=trajectory[:, 1])

        timer.timeout.connect(update)
        timer.start()


    def hide_trajectory(self, name):
        self.plot_widget.removeItem(self.trajectory_lines[name])


    def delete_trajectory(self, name):
        self.plot_widget.removeItem(self.trajectory_lines[name])
        self.trajectory_lines.pop(name)


    def create_callbacks(self):
        self.plot_widget.scene().sigMouseClicked.connect(self.mouse_clicked)
        self.plot_widget.scene().sigMouseMoved.connect(self.mouse_moved)


    def mouse_clicked(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            pos = self.plot_widget.plotItem.vb.mapSceneToView(event.scenePos())
            x, y = pos.x(), pos.y()

            if not self.is_drawing_vector:
                self.start_point = (x, y)
                self.is_drawing_vector = True
                if self.vector is not None:
                    self.plot_widget.removeItem(self.vector)
                self.vector = pg.PlotDataItem(x=[x, x],my=[y, y],npen=pg.mkPen('white', width=4))
                self.plot_widget.addItem(self.vector)

            else:
                x0, y0 = self.start_point
                dx = x - x0
                dy = y - y0
                self.theta = np.arctan2(dy, dx)
                if self.on_ray_selected is not None:
                    x0, y0 = self.start_point
                    self.on_ray_selected(x0, y0, self.theta)
                self.is_drawing_vector = False


    def mouse_moved(self, pos_scene):
        if self.is_drawing_vector and self.start_point is not None:
            pos_view = self.plot_widget.plotItem.vb.mapSceneToView(pos_scene)
            x0, y0 = self.start_point
            x1, y1 = pos_view.x(), pos_view.y()
            dx = x1 - x0
            dy = y1 - y0
            length = np.hypot(dx, dy)

            if length > 1e-6:
                scale = 30.0 / length
                dx *= scale
                dy *= scale
            self.vector.setData(x=[x0, x0 + dx], y=[y0, y0 + dy])