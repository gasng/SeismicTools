# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NMOWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_NMOWidget(object):
    def setupUi(self, NMOWidget):
        if not NMOWidget.objectName():
            NMOWidget.setObjectName(u"NMOWidget")
        NMOWidget.resize(1035, 623)
        self.horizontalLayout_2 = QHBoxLayout(NMOWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.leftBox = QGroupBox(NMOWidget)
        self.leftBox.setObjectName(u"leftBox")
        self.verticalLayout = QVBoxLayout(self.leftBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.DataLoadBox = QGroupBox(self.leftBox)
        self.DataLoadBox.setObjectName(u"DataLoadBox")
        self.verticalLayout_2 = QVBoxLayout(self.DataLoadBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.DataLoadBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.lineEdit_filePath = QLineEdit(self.DataLoadBox)
        self.lineEdit_filePath.setObjectName(u"lineEdit_filePath")

        self.verticalLayout_2.addWidget(self.lineEdit_filePath)

        self.pushButton_load = QPushButton(self.DataLoadBox)
        self.pushButton_load.setObjectName(u"pushButton_load")

        self.verticalLayout_2.addWidget(self.pushButton_load)

        self.pushButton_clear = QPushButton(self.DataLoadBox)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.verticalLayout_2.addWidget(self.pushButton_clear)

        self.label_2 = QLabel(self.DataLoadBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.DataLoadBox)

        self.VanalisisBox = QGroupBox(self.leftBox)
        self.VanalisisBox.setObjectName(u"VanalisisBox")
        self.verticalLayout_3 = QVBoxLayout(self.VanalisisBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_velocitySpectrum = QPushButton(self.VanalisisBox)
        self.pushButton_velocitySpectrum.setObjectName(u"pushButton_velocitySpectrum")

        self.verticalLayout_3.addWidget(self.pushButton_velocitySpectrum)

        self.pushButton_velocityLaw = QPushButton(self.VanalisisBox)
        self.pushButton_velocityLaw.setObjectName(u"pushButton_velocityLaw")

        self.verticalLayout_3.addWidget(self.pushButton_velocityLaw)

        self.pickBox = QGroupBox(self.VanalisisBox)
        self.pickBox.setObjectName(u"pickBox")
        self.horizontalLayout = QHBoxLayout(self.pickBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton_pick = QRadioButton(self.pickBox)
        self.radioButton_pick.setObjectName(u"radioButton_pick")

        self.horizontalLayout.addWidget(self.radioButton_pick)

        self.radioButton_view = QRadioButton(self.pickBox)
        self.radioButton_view.setObjectName(u"radioButton_view")

        self.horizontalLayout.addWidget(self.radioButton_view)


        self.verticalLayout_3.addWidget(self.pickBox)

        self.tableWidget_picks = QTableWidget(self.VanalisisBox)
        if (self.tableWidget_picks.columnCount() < 3):
            self.tableWidget_picks.setColumnCount(3)
        self.tableWidget_picks.setObjectName(u"tableWidget_picks")
        self.tableWidget_picks.setColumnCount(3)

        self.verticalLayout_3.addWidget(self.tableWidget_picks)

        self.pushButton_undoPick = QPushButton(self.VanalisisBox)
        self.pushButton_undoPick.setObjectName(u"pushButton_undoPick")

        self.verticalLayout_3.addWidget(self.pushButton_undoPick)

        self.pushButton_clearAll = QPushButton(self.VanalisisBox)
        self.pushButton_clearAll.setObjectName(u"pushButton_clearAll")

        self.verticalLayout_3.addWidget(self.pushButton_clearAll)

        self.pushButton_applyCorrections = QPushButton(self.VanalisisBox)
        self.pushButton_applyCorrections.setObjectName(u"pushButton_applyCorrections")

        self.verticalLayout_3.addWidget(self.pushButton_applyCorrections)


        self.verticalLayout.addWidget(self.VanalisisBox)


        self.horizontalLayout_2.addWidget(self.leftBox)

        self.rightBox = QGroupBox(NMOWidget)
        self.rightBox.setObjectName(u"rightBox")

        self.horizontalLayout_2.addWidget(self.rightBox)


        self.retranslateUi(NMOWidget)

        QMetaObject.connectSlotsByName(NMOWidget)
    # setupUi

    def retranslateUi(self, NMOWidget):
        NMOWidget.setWindowTitle(QCoreApplication.translate("NMOWidget", u"Form", None))
        self.leftBox.setTitle("")
        self.DataLoadBox.setTitle(QCoreApplication.translate("NMOWidget", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label.setText(QCoreApplication.translate("NMOWidget", u"SGY -  \u0444\u0430\u0439\u043b", None))
        self.lineEdit_filePath.setText("")
        self.pushButton_load.setText(QCoreApplication.translate("NMOWidget", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.pushButton_clear.setText(QCoreApplication.translate("NMOWidget", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.label_2.setText(QCoreApplication.translate("NMOWidget", u"\u0444\u043e\u0440\u043c\u0430\u0442: .sgy / .segy", None))
        self.VanalisisBox.setTitle(QCoreApplication.translate("NMOWidget", u"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u043d\u043e\u0439 \u0430\u043d\u0430\u043b\u0438\u0437", None))
        self.pushButton_velocitySpectrum.setText(QCoreApplication.translate("NMOWidget", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u043d\u043e\u0439 \u0441\u043f\u0435\u043a\u0442\u0440", None))
        self.pushButton_velocityLaw.setText(QCoreApplication.translate("NMOWidget", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u043d\u043e\u0439 \u0437\u0430\u043a\u043e\u043d", None))
        self.pickBox.setTitle("")
        self.radioButton_pick.setText(QCoreApplication.translate("NMOWidget", u"\u0440\u0435\u0436\u0438\u043c \u043f\u0438\u043a\u0438\u0440\u043e\u0432\u043a\u0438", None))
        self.radioButton_view.setText(QCoreApplication.translate("NMOWidget", u"\u0440\u0435\u0436\u0438\u043c \u043e\u0431\u0437\u043e\u0440\u0430", None))
        self.pushButton_undoPick.setText(QCoreApplication.translate("NMOWidget", u"\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u0438\u043a", None))
        self.pushButton_clearAll.setText(QCoreApplication.translate("NMOWidget", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0451", None))
        self.pushButton_applyCorrections.setText(QCoreApplication.translate("NMOWidget", u"\u0412\u0432\u0435\u0434\u0435\u043d\u0438\u0435 \u043a\u0438\u043d\u0435\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043f\u043e\u043f\u0440\u0430\u0432\u043e\u043a", None))
        self.rightBox.setTitle(QCoreApplication.translate("NMOWidget", u"GroupBox", None))
    # retranslateUi

