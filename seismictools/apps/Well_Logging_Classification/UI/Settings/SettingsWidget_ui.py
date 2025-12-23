import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTabWidget, QTableWidget, QComboBox, 
    QAbstractItemView, QGroupBox, QFormLayout,
    QDialog, QSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QBrush, QColor, QLinearGradient, QPen


class GradientButton(QPushButton):
    def __init__(self, text="", parent=None, color1="#4A90E2", color2="#357ABD"):
        super().__init__(text, parent)
        self._color1 = QColor(color1)
        self._color2 = QColor(color2)
        self._hovered = False
        self._pressed = False
        self.setMinimumHeight(28)
        
        button_font = QFont()
        button_font.setPointSize(9)
        button_font.setWeight(QFont.Medium)
        self.setFont(button_font)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover)

    def setColors(self, color1, color2):
        """Установка цветов градиента"""
        self._color1 = QColor(color1)
        self._color2 = QColor(color2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        c1, c2 = self._color1, self._color2
        if self._pressed:
            c1 = c1.darker(120)
            c2 = c2.darker(120)
        elif self._hovered:
            c1 = c1.lighter(110)
            c2 = c2.lighter(110)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, c1)
        gradient.setColorAt(1, c2)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        radius = self.height() / 2
        painter.drawRoundedRect(self.rect(), radius, radius)
        
        text_color = Qt.white if not self._pressed else QColor(220, 220, 220)
        painter.setPen(QPen(text_color))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._pressed = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = False
            self._hovered = self.underMouse()
            self.update()
        super().mouseReleaseEvent(event)


class StyledGroupBox(QGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Medium)
        self.setFont(font)
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #333333;
            }
        """)


class SettingsWidgetUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setAcceptDrops(True)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
            }
            QLineEdit {
                border: 1px solid #D1D9E6;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
            QComboBox {
                border: 1px solid #D1D9E6;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #4A90E2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QTabWidget::pane {
                border: 1px solid #D1D9E6;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F0F2F5;
                border: 1px solid #D1D9E6;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                font-size: 12px;
                font-weight: medium;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4A90E2;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #E8ECF1;
            }
            QTableWidget {
                border: 1px solid #D1D9E6;
                border-radius: 8px;
                background-color: white;
                alternate-background-color: #F8F9FA;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #F0F2F5;
                border-bottom: 1px solid #F0F2F5;
            }
            QTableWidget::item:selected {
                background-color: #4A90E2;
                color: white;
            }
            QHeaderView::section {
                background-color: #F0F2F5;
                padding: 8px;
                border: none;
                border-right: 1px solid #D1D9E6;
                border-bottom: 1px solid #D1D9E6;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton {
                border: none;
                border-radius: 14px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: medium;
                background-color: #F0F2F5;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #E8ECF1;
            }
            QPushButton:pressed {
                background-color: #D1D9E6;
            }
        """)

        group_load = StyledGroupBox("ЗАГРУЗКА ДАННЫХ")
        layout.addWidget(group_load)
        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(15, 20, 15, 15)

        self.lineEdit_file = QLineEdit()
        self.lineEdit_file.setPlaceholderText("Введите путь к файлу или перетащите его сюда")
        self.lineEdit_file.setMinimumHeight(35)
        
        self.comboBox_history = QComboBox()
        self.comboBox_history.setPlaceholderText("Последние файлы")
        self.comboBox_history.setMinimumHeight(35)
        
        self.pushButton_load = GradientButton("Загрузить")
        self.pushButton_load.setColors("#4A90E2", "#357ABD")
        self.pushButton_clear = GradientButton("Очистить")
        self.pushButton_clear.setColors("#E74C3C", "#C0392B")

        form_layout.addRow("Файл:", self.lineEdit_file)
        form_layout.addRow("История:", self.comboBox_history)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.pushButton_load)
        button_layout.addWidget(self.pushButton_clear)
        button_layout.setSpacing(10)
        form_layout.addRow("", button_layout)
        group_load.setLayout(form_layout)

        group_carotage = StyledGroupBox("ПРОСМОТР КАРОТАЖА")
        layout.addWidget(group_carotage)
        tab_widget = QTabWidget()
        tab_widget.setMaximumHeight(300)

        self.tableWidget_curves = QTableWidget()
        self.tableWidget_curves.setColumnCount(4)
        self.tableWidget_curves.setHorizontalHeaderLabels(['Назв. крив.', 'Мин.', 'Макс.', 'Δ'])
        self.tableWidget_curves.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_curves.setAlternatingRowColors(True)
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.setContentsMargins(5, 5, 5, 5)
        tab1_layout.addWidget(self.tableWidget_curves)
        tab_widget.addTab(tab1, "КАРОТАЖ")

        self.comboBox_xcurve = QComboBox()
        self.comboBox_ycurve = QComboBox()
        self.pushButton_plot = GradientButton("Построить кросс-плот")
        self.pushButton_plot.setColors("#2ECC71", "#27AE60")
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.setContentsMargins(15, 15, 15, 15)
        tab2_layout.setSpacing(8)
        tab2_layout.addWidget(QLabel("<span style='color: #666;'>X-кривая</span>"))
        tab2_layout.addWidget(self.comboBox_xcurve)
        tab2_layout.addWidget(QLabel("<span style='color: #666;'>Y-кривая</span>"))
        tab2_layout.addWidget(self.comboBox_ycurve)
        tab2_layout.addWidget(self.pushButton_plot)
        tab_widget.addTab(tab2, "КРОСС-ПЛОТ")

        group_carotage.setLayout(QVBoxLayout())
        group_carotage.layout().addWidget(tab_widget)

        group_classification = StyledGroupBox("КЛАССИФИКАЦИЯ")
        layout.addWidget(group_classification)
        tab_class = QTabWidget()

        tab3 = QWidget()
        vlayout3 = QVBoxLayout(tab3)
        vlayout3.setContentsMargins(15, 15, 15, 15)
        vlayout3.setSpacing(10)
        
        self.pushButton_draw_polygon = GradientButton("Нарисовать полигон")
        self.pushButton_draw_polygon.setColors("#9B59B6", "#8E44AD")
        self.pushButton_assign_class = GradientButton("Присвоить класс")
        self.pushButton_assign_class.setColors("#3498DB", "#2980B9")
        self.pushButton_cancel_polygon = GradientButton("Отменить полигон")
        self.pushButton_cancel_polygon.setColors("#E67E22", "#D35400")
        self.pushButton_clear_markup = GradientButton("Очистить разметку")
        self.pushButton_clear_markup.setColors("#E74C3C", "#C0392B")
        
        vlayout3.addWidget(self.pushButton_draw_polygon)
        vlayout3.addWidget(self.pushButton_assign_class)
        vlayout3.addWidget(self.pushButton_cancel_polygon)
        vlayout3.addWidget(self.pushButton_clear_markup)
        tab_class.addTab(tab3, "РАЗМЕТКА")

        tab5 = QWidget()
        vlayout5 = QVBoxLayout(tab5)
        vlayout5.setContentsMargins(10, 10, 10, 10)
        vlayout5.setSpacing(5)
        
        self.tableWidget_polygons = QTableWidget()
        self.tableWidget_polygons.setColumnCount(3)
        self.tableWidget_polygons.setMinimumHeight(180)
        self.tableWidget_polygons.setHorizontalHeaderLabels(["ID", "Класс", "Точек"])
        self.tableWidget_polygons.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_polygons.setAlternatingRowColors(True)
        
        self.btn_delete_polygon = GradientButton("Удалить выбранный")
        self.btn_delete_polygon.setColors("#E74C3C", "#C0392B")
        self.btn_clear_all_polygons = GradientButton("Очистить все полигоны")
        self.btn_clear_all_polygons.setColors("#95A5A6", "#7F8C8D")
        
        vlayout5.addWidget(self.tableWidget_polygons)
        vlayout5.addWidget(self.btn_delete_polygon)
        vlayout5.addWidget(self.btn_clear_all_polygons)
        tab_class.addTab(tab5, "ПОЛИГОНЫ")

        self.tableWidget_classes = QTableWidget()
        self.tableWidget_classes.setColumnCount(4)
        self.tableWidget_classes.setMinimumHeight(180)
        self.tableWidget_classes.setHorizontalHeaderLabels(["ID", "Название", "Точек", "Цвет"])
        self.tableWidget_classes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_classes.setAlternatingRowColors(True)
        
        self.btn_add_class = GradientButton("Добавить класс")
        self.btn_add_class.setColors("#2ECC71", "#27AE60")
        self.btn_del_class = GradientButton("Удалить выбранный")
        self.btn_del_class.setColors("#E74C3C", "#C0392B")
        
        tab4 = QWidget()
        vlayout4 = QVBoxLayout(tab4)
        vlayout4.setContentsMargins(10, 10, 10, 10)
        vlayout4.setSpacing(5)
        vlayout4.addWidget(self.tableWidget_classes)
        vlayout4.addWidget(self.btn_add_class)
        vlayout4.addWidget(self.btn_del_class)
        tab_class.addTab(tab4, "КЛАССЫ")

        group_classification.setLayout(QVBoxLayout())
        group_classification.layout().addWidget(tab_class)

        self.pushButton_save = GradientButton("Сохранить LAS с классами")
        self.pushButton_save.setColors("#A600FF", "#FF0088")
        self.pushButton_save.setMinimumHeight(45)
        save_button_font = self.pushButton_save.font()
        save_button_font.setPointSize(12)
        save_button_font.setWeight(QFont.Bold)
        self.pushButton_save.setFont(save_button_font)
        layout.addWidget(self.pushButton_save)
        layout.addStretch()


class AddClassDialogUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить класс")
        self.setMinimumWidth(350)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
                font-size: 13px;
            }
            QSpinBox, QLineEdit {
                border: 1px solid #D1D9E6;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QSpinBox:focus, QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
        """)

        form = QFormLayout()
        form.setSpacing(10)
        
        self.spin_id = QSpinBox()
        self.spin_id.setRange(1, 999)
        self.spin_id.setMinimumHeight(35)
        
        self.line_name = QLineEdit()
        self.line_name.setMinimumHeight(35)
        self.line_name.setPlaceholderText("Например: песчаник")
        
        self.color_button = QPushButton("Выбрать цвет")
        self.color_button.setMinimumHeight(35)
        self.color_button.setProperty("color", "#FF69B4")

        self.color_button.setStyleSheet("""
            QPushButton {
                color: white;
                border-radius: 6px;
                font-weight: medium;
                padding: 8px;
                border: 1px solid #ccc;
                background-color: #FF69B4;
            }
            QPushButton:hover {
                border: 1px solid #999;
                background-color: #FF5CA0;
            }
        """)

        form.addRow("ID класса:", self.spin_id)
        form.addRow("Название:", self.line_name)
        form.addRow("Цвет:", self.color_button)

        btn_box = QHBoxLayout()
        btn_box.setSpacing(10)
        
        self.btn_ok = GradientButton("OK")
        self.btn_ok.setColors("#2ECC71", "#27AE60")
        self.btn_cancel = GradientButton("Отмена")
        self.btn_cancel.setColors("#95A5A6", "#7F8C8D")
        
        btn_box.addWidget(self.btn_ok)
        btn_box.addWidget(self.btn_cancel)

        layout.addLayout(form)
        layout.addLayout(btn_box)