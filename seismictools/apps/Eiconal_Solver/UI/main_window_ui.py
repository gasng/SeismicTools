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
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(875, 667)
        MainWindow.setStyleSheet(u"/* \u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043e\u043a\u043d\u043e \u2014 \u0447\u0438\u0441\u0442\u044b\u0439 \u0431\u0435\u043b\u044b\u0439 \u0444\u043e\u043d */\n"
"QMainWindow {\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"/* \u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u2014 \u043c\u044f\u0433\u043a\u0438\u0439 \u043e\u0432\u0430\u043b\u044c\u043d\u044b\u0439 \u0431\u043b\u043e\u043a \u0441 \u0442\u0435\u043d\u044c\u044e */\n"
"QLabel#Label {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"    color: #FF8C42;\n"
"    padding: 10px 20px;\n"
"    margin: 10px 0 15px 0;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        stop: 0 #FFF2E8,\n"
"        stop: 1 #FFE6D5\n"
"    );\n"
"    border-radius: 20px;\n"
"    border: 1px solid #FFD0B0;\n"
"    min-width: 180px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* \u0413\u0440\u0443\u043f\u043f\u044b \u2014 \u0441 \u043c\u044f\u0433"
                        "\u043a\u0438\u043c\u0438 \u0442\u0435\u043d\u044f\u043c\u0438 \u0438 \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u043c\u0438 \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0430\u043c\u0438 */\n"
"QGroupBox {\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 12px;\n"
"    margin-top: 16px;\n"
"    background: #ffffff;\n"
"    padding: 10px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0 10px;\n"
"    color: #FF8C42;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"    border-left: 3px solid #FF8C42;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0438 \u2014 \u0441 \u0433\u0440\u0430\u0434\u0438\u0435\u043d\u0442\u043e\u043c \u043e\u0442 \u0440\u043e\u0437\u043e\u0432\u043e\u0433\u043e \u043a \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u043e\u043c\u0443 */\n"
"QPushButton {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        stop: 0 #FF9A76,\n"
"        stop"
                        ": 1 #FF8C42\n"
"    );\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    min-width: 80px;\n"
"    box-shadow: 0 2px 4px rgba(255, 140, 66, 0.2);\n"
"}\n"
"QPushButton:hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        stop: 0 #FF7F50,\n"
"        stop: 1 #FF6B2F\n"
"    );\n"
"}\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        stop: 0 #E06320,\n"
"        stop: 1 #D0531A\n"
"    );\n"
"    padding: 9px 17px 7px 15px;\n"
"    box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);\n"
"}\n"
"\n"
"/* \u041e\u0441\u043e\u0431\u0430\u044f \u043a\u043d\u043e\u043f\u043a\u0430 \"\u0421\u0442\u0430\u0440\u0442\" \u2014 \u044f\u0440\u0447\u0435, \u043a\u0430\u043a \u043d\u0430 \u043c\u0430\u043a\u0435\u0442\u0435 */\n"
"QPushButton#StartButton {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"  "
                        "      x2: 1, y2: 0,\n"
"        stop: 0 #FF6B9D,\n"
"        stop: 1 #FF5A8C\n"
"    );\n"
"    box-shadow: 0 2px 6px rgba(255, 106, 157, 0.3);\n"
"}\n"
"QPushButton#StartButton:hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        stop: 0 #FF5080,\n"
"        stop: 1 #FF3F6F\n"
"    );\n"
"}\n"
"QPushButton#StartButton:pressed {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        stop: 0 #E04070,\n"
"        stop: 1 #D03060\n"
"    );\n"
"}\n"
"\n"
"/* \u041f\u043e\u043b\u0435 \u0432\u0432\u043e\u0434\u0430 \u2014 \u0441\u0432\u0435\u0442\u043b\u043e\u0435, \u0441 \u0442\u043e\u043d\u043a\u043e\u0439 \u0433\u0440\u0430\u043d\u0438\u0446\u0435\u0439 */\n"
"QLineEdit {\n"
"    background: #fafafa;\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 6px;\n"
"    padding: 6px 10px;\n"
"    color: #333;\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 1px solid #FF8C42;\n"
"    background: #fff;\n"
"}\n"
"\n"
""
                        "/* \u041c\u0435\u0442\u043a\u0438 \u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442 \u2014 \u043d\u0435\u0431\u043e\u043b\u044c\u0448\u0438\u0435, \u0441 \u043c\u044f\u0433\u043a\u0438\u043c \u0444\u043e\u043d\u043e\u043c */\n"
"QLabel#XSource, QLabel#ZSource, QLabel#AngleLabel {\n"
"    background: #f5f5f5;\n"
"    border-radius: 6px;\n"
"    padding: 4px 8px;\n"
"    color: #555;\n"
"    font-size: 13px;\n"
"    min-width: 60px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* \u0421\u043b\u0430\u0439\u0434\u0435\u0440 \u2014 \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u0439 \u0442\u0440\u0435\u043a */\n"
"QSlider::groove:horizontal {\n"
"    height: 6px;\n"
"    background: #FFD0B0;\n"
"    border-radius: 3px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: #FF8C42;\n"
"    border: 1px solid #FF8C42;\n"
"    height: 14px;\n"
"    width: 14px;\n"
"    margin: -4px 0;\n"
"    border-radius: 7px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background: #FF6B2F;\n"
"}\n"
"\n"
"/* \u0421"
                        "\u043f\u0438\u0441\u043e\u043a \u0444\u0430\u0439\u043b\u043e\u0432 / \u0441\u0442\u0430\u0442\u0443\u0441 \u2014 \u0441 \u043b\u0451\u0433\u043a\u0438\u043c \u0444\u043e\u043d\u043e\u043c */\n"
"QListWidget {\n"
"    background: #fafafa;\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"    color: #444;\n"
"}\n"
"QListWidget#StatusWidget {\n"
"    background: #f8f8f8;\n"
"    border-top: 1px solid #e0e0e0;\n"
"    color: #666;\n"
"    font-size: 11px;\n"
"    selection-background-color: #FF8C42;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"/* \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u0432\u0438\u0434\u0436\u0435\u0442 \u2014 \u0431\u0435\u0437 \u0444\u043e\u043d\u0430, \u0447\u0442\u043e\u0431\u044b \u0433\u0440\u0430\u0444\u0438\u043a \u0431\u044b\u043b \u043d\u0430 \u0431\u0435\u043b\u043e\u043c */\n"
"QWidget#widget {\n"
"    background: transparent;\n"
"    border: none;\n"
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
        self.UploadButton.setMaximumSize(QSize(16777215, 16777215))

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
        self.XSource = QLabel(self.groupBox_6)
        self.XSource.setObjectName(u"XSource")

        self.horizontalLayout_4.addWidget(self.XSource)

        self.ZSource = QLabel(self.groupBox_6)
        self.ZSource.setObjectName(u"ZSource")

        self.horizontalLayout_4.addWidget(self.ZSource)

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
        self.widget = QWidget(self.RightBlocks)
        self.widget.setObjectName(u"widget")

        self.verticalLayout_2.addWidget(self.widget)

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
        self.Label.setStyleSheet(u"")

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
        self.UploadButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.ClearButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.SourceBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0432\u043e\u043b\u043d\u044b", None))
        self.groupBox_6.setTitle("")
        self.XSource.setText("")
        self.ZSource.setText("")
        self.AngleLabel.setText("")
        self.AnimationBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0410\u043d\u0438\u043c\u0430\u0446\u0438\u044f \u0432\u043e\u043b\u043d\u044b", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.PauseButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0443\u0437\u0430", None))
        self.ResetButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441", None))
        self.RightBlocks.setTitle("")
        self.Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Eiconal Solver</span></p></body></html>", None))
    # retranslateUi

