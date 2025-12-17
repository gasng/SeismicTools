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
        self.fk_freq_axis = None
        self.fk_kx_axis = None

    def _setup_plots(self):
        """Настройка общего стиля графиков"""
        for pw in [self.seismogram_pw, self.fk_pw, self.result_pw]:
            pw.setBackground('#1e1e1e')
            pw.showGrid(x=True, y=True, alpha=0.3)

    def log_message(self, msg: str):
        self.error_lw.addItem(msg)

    def plot_seismogram(self, data: np.ndarray, dt: float, dx: float):
        """
        Функция отрисовки сейсмограммы

        :param data:  массив [трассы, время]
        :param dt: шаг дискретизации по времени (сек)
        :param dx: шаг дискретизации по пространству (м)
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
        """
        Функция отрисовки FK-спектра сейсмограммы.

        :param data: Массив [пространственная частота, частота]
        :param dt: шаг дискретизации по времени (сек)
        :param dx: шаг дискретизации по пространству (м)
        """
        self.fk_spectrum = data
        self.fk_pw.clear()

        amplitude = np.log(np.abs(data) + 1e-10)

        nt, nx = data.shape
        freqs = np.fft.fftshift(np.fft.fftfreq(nt, dt))
        kx = np.fft.fftshift(np.fft.fftfreq(nx, dx))

        # Сохраняем для маски
        self.fk_freq_axis = freqs
        self.fk_kx_axis = kx

        img = pg.ImageItem()
        cmap = pg.colormap.get('CET-C3')
        img.setLookupTable(cmap.getLookupTable())

        vmin, vmax = np.percentile(amplitude, [1, 99])
        img.setImage(amplitude, levels=(vmin, vmax))

        x0, x1 = kx[0], kx[-1]
        y0, y1 = freqs[0], freqs[-1]
        img.setRect((x0, y0, x1 - x0, y1 - y0))

        self.fk_pw.addItem(img)
        self.fk_pw.setLabel('left', 'Частота', units='Гц')
        self.fk_pw.setLabel('bottom', 'Волновое число', units='1/м')
        self.fk_pw.setTitle('FK-спектр')
        self.log_message("FK - спектр отображен")

    def plot_result(self, data: np.ndarray, dt: float, dx: float):
        """
        Функция отрисовки отфильтрованной сейсмограммы

        :param data:  массив [трассы, время]
        :param dt: шаг дискретизации по времени (сек)
        :param dx: шаг дискретизации по пространству (м)
         """
        self.filtered_spectrum = data
        self.result_pw.clear()
        vmin, vmax = np.percentile(data, [1, 99])
        img = pg.ImageItem()
        img.setImage(data, levels=(vmin, vmax))
        img.setRect((0, 0, dx * data.shape[1], dt * data.shape[0]))
        self.result_pw.addItem(img)
        self.result_pw.invertY(True)
        self.result_pw.setLabel('left', 'Время', units='с')
        self.result_pw.setLabel('bottom', 'Координата приемника', units='м')
        self.result_pw.setTitle('Сейсмограмма после фильтрации')
        self.log_message("Отфильтрованная сейсмограмма отображена")