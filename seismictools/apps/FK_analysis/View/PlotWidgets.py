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
        img.setImage(data.T)  # время по вертикали
        self.seismogram_pw.addItem(img)
        self.seismogram_pw.setLabel('left', 'Время')
        self.seismogram_pw.setLabel('bottom', 'Трасса')
        self.seismogram_pw.setTitle('Сейсмограмма')
        self.log_message("✅ Сейсмограмма отображена")