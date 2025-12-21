from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QAbstractItemView, QCheckBox, QDoubleSpinBox,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QRadioButton, QSlider, QTableWidget,
                               QVBoxLayout, QWidget)


class Ui_SettingsWidget(object):
    def setupUi(self, SettingsWidget):
        if not SettingsWidget.objectName():
            SettingsWidget.setObjectName(u"SettingsWidget")
        SettingsWidget.resize(320, 800)
        self.verticalLayout = QVBoxLayout(SettingsWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        # ЗАГРУЗКА КУБА
        self.label = QLabel(SettingsWidget)
        self.label.setObjectName(u"label")
        self.verticalLayout.addWidget(self.label)

        self.filePathEdit = QLineEdit(SettingsWidget)
        self.filePathEdit.setObjectName(u"filePathEdit")
        self.verticalLayout.addWidget(self.filePathEdit)

        self.loadButton = QPushButton(SettingsWidget)
        self.loadButton.setObjectName(u"loadButton")
        self.verticalLayout.addWidget(self.loadButton)

        self.clearButton = QPushButton(SettingsWidget)
        self.clearButton.setObjectName(u"clearButton")
        self.verticalLayout.addWidget(self.clearButton)

        #ПРОСМОТР КУБА
        self.label_2 = QLabel(SettingsWidget)
        self.label_2.setObjectName(u"label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.timeSlider = QSlider(SettingsWidget)
        self.timeSlider.setOrientation(Qt.Horizontal)
        self.timeSlider.setObjectName(u"timeSlider")
        self.verticalLayout.addWidget(self.timeSlider)

        self.timeLabel = QLabel(SettingsWidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.verticalLayout.addWidget(self.timeLabel)


        #РАЗМЕТКА ТРАСС
        self.label_3 = QLabel(SettingsWidget)
        self.label_3.setObjectName(u"label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.tracesTable = QTableWidget(SettingsWidget)
        self.tracesTable.setObjectName(u"tracesTable")
        self.tracesTable.setColumnCount(3)
        self.tracesTable.setRowCount(0)
        self.tracesTable.setHorizontalHeaderLabels(["Трасса", "Координаты", "Класс"])
        self.tracesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tracesTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.verticalLayout.addWidget(self.tracesTable)

        self.deleteButton = QPushButton(SettingsWidget)
        self.deleteButton.setObjectName(u"deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)

        self.changeClassButton = QPushButton(SettingsWidget)
        self.changeClassButton.setObjectName(u"changeClassButton")
        self.verticalLayout.addWidget(self.changeClassButton)

        self.saveDatasetButton = QPushButton(SettingsWidget)
        self.saveDatasetButton.setObjectName(u"saveDatasetButton")
        self.verticalLayout.addWidget(self.saveDatasetButton)

        self.normalizationPlaceholder = QLabel(SettingsWidget)
        self.normalizationPlaceholder.setObjectName(u"normalizationPlaceholder")
        self.normalizationPlaceholder.setText("Normalization (создаётся в коде)")
        self.normalizationPlaceholder.setVisible(False)
        self.verticalLayout.addWidget(self.normalizationPlaceholder)

        self.retranslateUi(SettingsWidget)
        QMetaObject.connectSlotsByName(SettingsWidget)

    def retranslateUi(self, SettingsWidget):
        SettingsWidget.setWindowTitle(QCoreApplication.translate("SettingsWidget", u"Settings", None))
        self.label.setText(QCoreApplication.translate("SettingsWidget", u"ЗАГРУЗКА КУБА", None))
        self.loadButton.setText(QCoreApplication.translate("SettingsWidget", u"Загрузить", None))
        self.clearButton.setText(QCoreApplication.translate("SettingsWidget", u"Очистить", None))
        self.label_2.setText(QCoreApplication.translate("SettingsWidget", u"ПРОСМОТР КУБА", None))
        self.timeLabel.setText(QCoreApplication.translate("SettingsWidget", u"Временной срез T, мс: 0", None))
        self.label_3.setText(QCoreApplication.translate("SettingsWidget", u"РАЗМЕТКА ТРАСС", None))
        self.deleteButton.setText(QCoreApplication.translate("SettingsWidget", u"Удалить трассу", None))
        self.changeClassButton.setText(QCoreApplication.translate("SettingsWidget", u"Изменить класс", None))
        self.saveDatasetButton.setText(QCoreApplication.translate("SettingsWidget", u"Сохранить выборку (X, Y)", None))