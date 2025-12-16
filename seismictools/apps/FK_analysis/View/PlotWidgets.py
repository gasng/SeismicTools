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

    def plot_seismogram(self, data: np.ndarray, dt: float, dx: float):
        """
        :param  массив [трассы, время] — как из SegYReader (shape = (nx, nt))
        :param dt: шаг по времени (сек)
        :param dx: шаг по пространству (м)
        """
        self.current_data = data
        self.seismogram_pw.clear()
        vmin, vmax = np.percentile(data, [1, 99])
        img = pg.ImageItem()
        img.setImage(data, levels=(vmin, vmax))
        img.setRect((0, 0, dx * data.shape[1], dt * data.shape[0]))
        self.seismogram_pw.addItem(img)
        self.seismogram_pw.invertY(True)
        self.seismogram_pw.setLabel('left', 'Время', units='с')
        self.seismogram_pw.setLabel('bottom', 'Координата приёмника', units='м')
        self.seismogram_pw.setTitle('Сейсмограмма')
        self.log_message("Сейсмограмма отображена")

    def plot_fk(self, data: np.ndarray, dt: float, dx: float):
        self.fk_spectrum = data
        self.fk_pw.clear()
        amplitude = np.abs(data)
        img = pg.ImageItem()
        cmap = pg.colormap.get('CET-C3')
        img.setColorMap(cmap)
        img.setImage(amplitude)
        self.fk_pw.addItem(img)
        self.image_item = img

        h, w = data.shape
        f_nyquist = 1 / (2 * dt)
        k_nyquist = 1 / (2 * dx)
        img.setRect((-k_nyquist, -f_nyquist, 2 * k_nyquist, 2 * f_nyquist))

        # Ось Y: Частота
        y_ticks = [
            (-h // 2, f"{-f_nyquist:.1f}"),
            (0, "0"),
            (h // 2, f"{f_nyquist:.1f}")
        ]
        self.fk_pw.getAxis('left').setTicks([y_ticks])
        self.fk_pw.setLabel('left', 'Частота (Гц)')

        # Ось X: Пространственная частота
        x_ticks = [
            (-w // 2, f"{-k_nyquist:.2f}"),
            (0, "0"),
            (w // 2, f"{k_nyquist:.2f}")
        ]
        self.fk_pw.getAxis('bottom').setTicks([x_ticks])
        self.fk_pw.setLabel('bottom', 'Пространственная частота (1/м)')

        self.fk_pw.setTitle('FK - спектр')
        self.log_message("FK - спектр отображен")

    def plot_result(self, data: np.ndarray, dt: float, dx: float):
        self.filtered_spectrum = data
        self.result_pw.clear()
        vmin, vmax = np.percentile(data, [1, 99])
        img = pg.ImageItem()
        img.setImage(data, levels=(vmin, vmax))
        img.setRect((0, 0, dx * data.shape[1], dt * data.shape[0]))
        self.result_pw.addItem(img)
        self.result_pw.invertY(True)
        self.result_pw.setLabel('left', 'Время, mc')
        self.result_pw.setLabel('bottom', 'Координата приемника, м')
        self.result_pw.setTitle('Сейсмограмма после фильтрации')
        self.log_message("Отфильтрованная сейсмограмма отображена")