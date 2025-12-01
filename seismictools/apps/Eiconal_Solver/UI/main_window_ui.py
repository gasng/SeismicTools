# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QSlider, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(875, 515)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QWidget {\n"
"    font-family: \"Segoe UI\", Arial, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.BigGroupBox = QGroupBox(self.centralwidget)
        self.BigGroupBox.setObjectName(u"BigGroupBox")
        self.horizontalLayout = QHBoxLayout(self.BigGroupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.LeftBlocks = QGroupBox(self.BigGroupBox)
        self.LeftBlocks.setObjectName(u"LeftBlocks")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LeftBlocks.sizePolicy().hasHeightForWidth())
        self.LeftBlocks.setSizePolicy(sizePolicy)
        self.LeftBlocks.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(self.LeftBlocks)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ModelBox = QGroupBox(self.LeftBlocks)
        self.ModelBox.setObjectName(u"ModelBox")
        self.verticalLayout_3 = QVBoxLayout(self.ModelBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.UploadedFileWidget = QListWidget(self.ModelBox)
        self.UploadedFileWidget.setObjectName(u"UploadedFileWidget")

        self.verticalLayout_3.addWidget(self.UploadedFileWidget)

        self.groupBox_5 = QGroupBox(self.ModelBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.UploadButton = QPushButton(self.groupBox_5)
        self.UploadButton.setObjectName(u"UploadButton")

        self.horizontalLayout_2.addWidget(self.UploadButton)

        self.ClearButton = QPushButton(self.groupBox_5)
        self.ClearButton.setObjectName(u"ClearButton")

        self.horizontalLayout_2.addWidget(self.ClearButton)


        self.verticalLayout_3.addWidget(self.groupBox_5)


        self.verticalLayout.addWidget(self.ModelBox)

        self.SourceBox = QGroupBox(self.LeftBlocks)
        self.SourceBox.setObjectName(u"SourceBox")
        self.verticalLayout_4 = QVBoxLayout(self.SourceBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_6 = QGroupBox(self.SourceBox)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.AngleSlider = QSlider(self.groupBox_6)
        self.AngleSlider.setObjectName(u"AngleSlider")
        self.AngleSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.AngleSlider)

        self.AngleLabel = QLabel(self.groupBox_6)
        self.AngleLabel.setObjectName(u"AngleLabel")

        self.horizontalLayout_4.addWidget(self.AngleLabel)


        self.verticalLayout_4.addWidget(self.groupBox_6)


        self.verticalLayout.addWidget(self.SourceBox)

        self.AnimationBox = QGroupBox(self.LeftBlocks)
        self.AnimationBox.setObjectName(u"AnimationBox")
        self.horizontalLayout_3 = QHBoxLayout(self.AnimationBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.StartButton = QPushButton(self.AnimationBox)
        self.StartButton.setObjectName(u"StartButton")

        self.horizontalLayout_3.addWidget(self.StartButton)

        self.PauseButton = QPushButton(self.AnimationBox)
        self.PauseButton.setObjectName(u"PauseButton")

        self.horizontalLayout_3.addWidget(self.PauseButton)

        self.ResetButton = QPushButton(self.AnimationBox)
        self.ResetButton.setObjectName(u"ResetButton")

        self.horizontalLayout_3.addWidget(self.ResetButton)


        self.verticalLayout.addWidget(self.AnimationBox)


        self.horizontalLayout.addWidget(self.LeftBlocks)

        self.RightBlocks = QGroupBox(self.BigGroupBox)
        self.RightBlocks.setObjectName(u"RightBlocks")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.RightBlocks.sizePolicy().hasHeightForWidth())
        self.RightBlocks.setSizePolicy(sizePolicy1)
        self.RightBlocks.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.RightBlocks)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.PlotWidget = PlotWidget(self.RightBlocks)
        self.PlotWidget.setObjectName(u"PlotWidget")

        self.verticalLayout_2.addWidget(self.PlotWidget)

        self.StatusWidget = QListWidget(self.RightBlocks)
        self.StatusWidget.setObjectName(u"StatusWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.StatusWidget.sizePolicy().hasHeightForWidth())
        self.StatusWidget.setSizePolicy(sizePolicy2)
        self.StatusWidget.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_2.addWidget(self.StatusWidget)


        self.horizontalLayout.addWidget(self.RightBlocks)


        self.gridLayout.addWidget(self.BigGroupBox, 1, 0, 1, 1)

        self.Label = QLabel(self.centralwidget)
        self.Label.setObjectName(u"Label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Label.sizePolicy().hasHeightForWidth())
        self.Label.setSizePolicy(sizePolicy3)
        self.Label.setStyleSheet(u"QLabel{        \n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"    padding: 8px 16px;\n"
"    border-radius: 12px;\n"
"    qproperty-alignment: AlignCenter;\n"
"    border: 1px solid #ffe0b2;\n"
"}")

        self.gridLayout.addWidget(self.Label, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.BigGroupBox.setTitle("")
        self.LeftBlocks.setTitle("")
        self.ModelBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u043d\u043e\u0439 \u043c\u043e\u0434\u0435\u043b\u0438", None))
        self.groupBox_5.setTitle("")
        self.UploadButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043c\u043e\u0434\u0435\u043b\u044c", None))
        self.ClearButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.SourceBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0432\u043e\u043b\u043d\u044b", None))
        self.groupBox_6.setTitle("")
        self.AngleLabel.setText("")
        self.AnimationBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0410\u043d\u0438\u043c\u0430\u0446\u0438\u044f \u0432\u043e\u043b\u043d\u044b", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.PauseButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0443\u0437\u0430", None))
        self.ResetButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441", None))
        self.RightBlocks.setTitle("")
        self.Label.setText(QCoreApplication.translate("MainWindow", u"Eiconal Solver", None))
    # retranslateUi

