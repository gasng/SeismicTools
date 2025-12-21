import pyqtgraph as pg
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout

class SeismicPlotWidget(QWidget):
    def __init__(self, original_data, filtered_data=None):
        """
        Инициализацция всех настроек для отрисовки.
        """
        super().__init__()

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('black')
        self.plot_widget.setAspectLocked(False)

        self.im_item = pg.ImageItem()
        self.plot_widget.addItem(self.im_item)

        self.mask_item = pg.ImageItem()
        self.plot_widget.addItem(self.mask_item)

        self.curtain = pg.InfiniteLine(
            angle=90,
            movable=True,
            pen=pg.mkPen(color='red', width=2),
            hoverPen=pg.mkPen(color='white', width=3)
        ) #вертикальная палка-разделитель (шторка)
        self.plot_widget.addItem(self.curtain)
        self.curtain.sigPositionChanged.connect(self.curtain_moved)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        self.split_pos = 0.5
        self.original_data = None
        self.filtered_data = None
        if original_data is not None:
            self.set_data(original_data, filtered_data)

    def set_data(self, original_data, filtered_data=None):
        """
        Устанавливает исходные и отфильтрованные согналы для отображения.
        После вызова автоматически обновляет изображение. Если отфильтрованные данные не переданы, используется копия исходных данных.
        __________
        Параметры:
            original_data - (np.ndarray): Исходная сейсмограмма в формате (номер трассы, время).
            Filtered_data - (np.ndarray): Результат фильтрации тех же размеров и в том же формате.
        """
        self.original_data = original_data
        self.filtered_data = filtered_data if filtered_data is not None else original_data
        self.update_image()

    def update_image(self):
        """
         Отрисовка данных. Наш сигнал в 2D (номер трассы, время).
         Оригинальный сигнал - слева от разделителя, отфильтрованный - справа.
         """
        if self.original_data is None:
            return

        n_traces = self.original_data.shape[0] #первая координата - номер трасы
        n_samples = self.original_data.shape[1] #вторая координата - номер времени
        split_x_for_Ntraces = int(self.split_pos * n_traces)

        combined = np.copy(self.original_data)
        if self.filtered_data is not None:
            if self.filtered_data.shape != self.original_data.shape:
                return
            combined[split_x_for_Ntraces:,:] = self.filtered_data[split_x_for_Ntraces:, :]

        self.im_item.setRect(0, 0, n_traces, n_samples)

        self.curtain.setPos(split_x_for_Ntraces)

        self.plot_widget.enableAutoRange()
        self.plot_widget.getViewBox().setAspectLocked(False)
        self.plot_widget.invertY(True)

    def curtain_moved(self):
        """
        Функция для двимжения шторки.
        Возвращает/считывает текущее положение шторки.
        Так же, она ограничивает движение шторки: она движетися от 0 до самой последней трассы (n_traces).
        Возвращает положение шторки в 50/50.
        """
        if self.original_data is None:
            return
        n_traces = self.original_data.shape[0]
        split_x = self.curtain.getXPos()

        split_x = np.clip(split_x, 0, n_traces) #ограничиваем положение шторки от 0 - до номера трассы
        self.split_pos = split_x / n_traces

        self.update_image()