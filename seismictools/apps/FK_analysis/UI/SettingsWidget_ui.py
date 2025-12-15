# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_FK_Filtration(object):
    def setupUi(self, FK_Filtration):
        if not FK_Filtration.objectName():
            FK_Filtration.setObjectName(u"FK_Filtration")
        FK_Filtration.resize(1151, 605)
        FK_Filtration.setStyleSheet(u"")
        self.centralwidget = QWidget(FK_Filtration)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ToolGB = QGroupBox(self.centralwidget)
        self.ToolGB.setObjectName(u"ToolGB")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolGB.sizePolicy().hasHeightForWidth())
        self.ToolGB.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.ToolGB)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SeismicDataGB = QGroupBox(self.ToolGB)
        self.SeismicDataGB.setObjectName(u"SeismicDataGB")
        self.verticalLayout_2 = QVBoxLayout(self.SeismicDataGB)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.SeismicDataLW = QListWidget(self.SeismicDataGB)
        self.SeismicDataLW.setObjectName(u"SeismicDataLW")

        self.verticalLayout_2.addWidget(self.SeismicDataLW)

        self.label = QLabel(self.SeismicDataGB)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.SeismicDataBtn = QPushButton(self.SeismicDataGB)
        self.SeismicDataBtn.setObjectName(u"SeismicDataBtn")

        self.verticalLayout_2.addWidget(self.SeismicDataBtn)

        self.DeleteBtn = QPushButton(self.SeismicDataGB)
        self.DeleteBtn.setObjectName(u"DeleteBtn")

        self.verticalLayout_2.addWidget(self.DeleteBtn)


        self.verticalLayout.addWidget(self.SeismicDataGB)

        self.SeismicStartGB = QGroupBox(self.ToolGB)
        self.SeismicStartGB.setObjectName(u"SeismicStartGB")
        self.verticalLayout_3 = QVBoxLayout(self.SeismicStartGB)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.PlotSeismogramBtn = QPushButton(self.SeismicStartGB)
        self.PlotSeismogramBtn.setObjectName(u"PlotSeismogramBtn")

        self.verticalLayout_3.addWidget(self.PlotSeismogramBtn)

        self.FkBtn = QPushButton(self.SeismicStartGB)
        self.FkBtn.setObjectName(u"FkBtn")

        self.verticalLayout_3.addWidget(self.FkBtn)

        self.SignalStartBtn = QPushButton(self.SeismicStartGB)
        self.SignalStartBtn.setObjectName(u"SignalStartBtn")

        self.verticalLayout_3.addWidget(self.SignalStartBtn)

        self.SignalEndBtn = QPushButton(self.SeismicStartGB)
        self.SignalEndBtn.setObjectName(u"SignalEndBtn")

        self.verticalLayout_3.addWidget(self.SignalEndBtn)

        self.ResultBtn = QPushButton(self.SeismicStartGB)
        self.ResultBtn.setObjectName(u"ResultBtn")

        self.verticalLayout_3.addWidget(self.ResultBtn)


        self.verticalLayout.addWidget(self.SeismicStartGB)

        self.ErrorGB = QGroupBox(self.ToolGB)
        self.ErrorGB.setObjectName(u"ErrorGB")
        self.verticalLayout_4 = QVBoxLayout(self.ErrorGB)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ErrorLW = QListWidget(self.ErrorGB)
        self.ErrorLW.setObjectName(u"ErrorLW")

        self.verticalLayout_4.addWidget(self.ErrorLW)


        self.verticalLayout.addWidget(self.ErrorGB)


        self.horizontalLayout.addWidget(self.ToolGB)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.SeismogramPW = PlotWidget(self.groupBox)
        self.SeismogramPW.setObjectName(u"SeismogramPW")

        self.horizontalLayout_4.addWidget(self.SeismogramPW)

        self.FkPW = PlotWidget(self.groupBox)
        self.FkPW.setObjectName(u"FkPW")

        self.horizontalLayout_4.addWidget(self.FkPW)

        self.ResultPW = PlotWidget(self.groupBox)
        self.ResultPW.setObjectName(u"ResultPW")

        self.horizontalLayout_4.addWidget(self.ResultPW)


        self.horizontalLayout.addWidget(self.groupBox)

        FK_Filtration.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(FK_Filtration)
        self.statusbar.setObjectName(u"statusbar")
        FK_Filtration.setStatusBar(self.statusbar)

        self.retranslateUi(FK_Filtration)

        QMetaObject.connectSlotsByName(FK_Filtration)
    # setupUi

    def retranslateUi(self, FK_Filtration):
        FK_Filtration.setWindowTitle(QCoreApplication.translate("FK_Filtration", u"MainWindow", None))
        self.ToolGB.setTitle(QCoreApplication.translate("FK_Filtration", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u0432", None))
        self.SeismicDataGB.setTitle(QCoreApplication.translate("FK_Filtration", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label.setText(QCoreApplication.translate("FK_Filtration", u"\u0424\u043e\u0440\u043c\u0430\u0442: .sgy / .segy", None))
        self.SeismicDataBtn.setText(QCoreApplication.translate("FK_Filtration", u"\u041e\u0431\u0437\u043e\u0440", None))
        self.DeleteBtn.setText(QCoreApplication.translate("FK_Filtration", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.SeismicStartGB.setTitle(QCoreApplication.translate("FK_Filtration", u"FK - \u0424\u0418\u041b\u042c\u0422\u0420\u0410\u0426\u0418\u042f", None))
        self.PlotSeismogramBtn.setText(QCoreApplication.translate("FK_Filtration", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c \u0441\u0435\u0439\u0441\u043c\u043e\u0433\u0440\u0430\u043c\u043c\u0443", None))
        self.FkBtn.setText(QCoreApplication.translate("FK_Filtration", u"\u041f\u043e\u0441\u0442\u0440\u043e\u0438\u0442\u044c FK-\u0441\u043f\u0435\u043a\u0442\u0440", None))
        self.SignalStartBtn.setText(QCoreApplication.translate("FK_Filtration", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0441\u0438\u0433\u043d\u0430\u043b\u0430", None))
        self.SignalEndBtn.setText(QCoreApplication.translate("FK_Filtration", u"\u0417\u0430\u043a\u043e\u043d\u0447\u0438\u0442\u044c \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0441\u0438\u0433\u043d\u0430\u043b\u0430", None))
        self.ResultBtn.setText(QCoreApplication.translate("FK_Filtration", u"\u041e\u0431\u0440\u0430\u0442\u043d\u043e\u0435 FK-\u043f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.ErrorGB.setTitle(QCoreApplication.translate("FK_Filtration", u"\u041e\u043a\u043d\u043e \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f", None))
        self.groupBox.setTitle(QCoreApplication.translate("FK_Filtration", u"Seismic Filtering (FK)", None))
    # retranslateUi

