import pyqtgraph as pg

class PolygonSelector:
    def __init__(self, plot_widget: pg.PlotWidget):
        self.plot_widget = plot_widget
        self.points = []
        self.scatter = None
        self.polygon_line = None
        self.is_selecting = False

    def start_selection(self):
        self.clear()
        self.points = []
        self.is_selecting = True

    def finish_selection(self):
        self.is_selecting = False
        return len(self.points) >= 3

    def clear(self):
        if self.scatter:
            self.plot_widget.removeItem(self.scatter)
            self.scatter = None
        if self.polygon_line:
            self.plot_widget.removeItem(self.polygon_line)
            self.polygon_line = None
        self.points = []

    def add_point(self, scene_pos):
        view_pos = self.plot_widget.plotItem.vb.mapSceneToView(scene_pos)
        self.points.append((view_pos.x(), view_pos.y()))  # (kx, f)
        self._update_visuals()

    def _update_visuals(self):
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]

        if self.scatter is None:
            self.scatter = pg.ScatterPlotItem(size=8, pen='r', brush=pg.mkBrush('r'))
            self.plot_widget.addItem(self.scatter)
        self.scatter.setData(x=xs, y=ys)

        if len(self.points) > 1:
            if self.polygon_line is None:
                self.polygon_line = pg.PlotCurveItem(pen=pg.mkPen('g', width=2))
                self.plot_widget.addItem(self.polygon_line)
            closed_x = xs + [xs[0]] if len(self.points) >= 3 else xs
            closed_y = ys + [ys[0]] if len(self.points) >= 3 else ys
            self.polygon_line.setData(x=closed_x, y=closed_y)

    def get_points(self):
        return self.points.copy()

    def remove_last_point(self):
        if self.points:
            self.points.pop()
            self._update_visuals()
            if not self.points:
                if self.scatter:
                    self.plot_widget.removeItem(self.scatter)
                    self.scatter = None
                if self.polygon_line:
                    self.plot_widget.removeItem(self.polygon_line)
                    self.polygon_line = None
        return True