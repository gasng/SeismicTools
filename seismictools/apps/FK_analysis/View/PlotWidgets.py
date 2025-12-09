import pyqtgraph as pg
import numpy as np


class PlotSeism:
    def __init__(self, seismogram_pw, fk_pw, result_pw, error_lw):
        """
        :param seismogram_pw: PlotWidget из UI (self.ui.SeismogramPW)
        :param fk_pw:         PlotWidget из UI (self.ui.FkPW)
        :param result_pw:     PlotWidget из UI (self.ui.ResultPW)
        :param error_lw:      QListWidget для логов (self.ui.ErrorLW)
        """
        self.seismogram_pw = seismogram_pw
        self.fk_pw = fk_pw
        self.result_pw = result_pw
        self.error_lw = error_lw
        self._setup_plots()

        self.current_data = None
        self.fk_spectrum = None
        self.filtered_spectrum = None
        self.result_data = None

    def _setup_plots(self):
        """Настройка общего стиля графиков"""
        for pw in [self.seismogram_pw, self.fk_pw, self.result_pw]:
            pw.setBackground('#1e1e1e')
            pw.showGrid(x=True, y=True, alpha=0.3)

    def log_message(self, msg: str):
        self.error_lw.addItem(msg)

    def plot_seismogram(self, data: np.ndarray):
        self.current_data = data
        self.seismogram_pw.clear()
        img = pg.ImageItem()
        img.setImage(data)
        self.seismogram_pw.addItem(img)
        self.seismogram_pw.invertY(True)
        self.seismogram_pw.setLabel('left', 'Время, с')
        self.seismogram_pw.setLabel('bottom', 'Трасса, м')
        self.seismogram_pw.setTitle('Сейсмограмма')
        self.log_message("Сейсмограмма отображена")

    def plot_fk(self, data: np.ndarray):
        self.fk_spectrum = data
        self.fk_pw.clear()
        img = pg.ImageItem()
        cmap = pg.colormap.get('CET-L3')  # или 'CET-R3', 'viridis', 'plasma'
        img.setColorMap(cmap)
        img.setImage(data)
        self.fk_pw.addItem(img)
        self.fk_pw.invertY(True)
        self.fk_pw.setLabel('left', 'Частота, 1/с')
        self.fk_pw.setLabel('bottom', 'Пространственная частота, 1/м')
        self.fk_pw.setTitle('FK - спектр')
        self.log_message("FK - спектр отображен")

    def plot_result(self, data: np.ndarray):
        self.filtered_spectrum = data
        self.result_pw.clear()
        img = pg.ImageItem()
        img.setImage(data)
        self.result_pw.addItem(img)
        self.result_pw.invertY(True)
        self.result_pw.setLabel('left', 'Время, с')
        self.result_pw.setLabel('bottom', 'Трасса, м')
        self.result_pw.setTitle('Сейсмограмма после фильтрации')
        self.log_message("Отфильтрованная сейсмограмма отображена")