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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(899, 647)
        MainWindow.setStyleSheet(u"/* \u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043e\u043a\u043d\u043e \u2014 \u0447\u0438\u0441\u0442\u044b\u0439 \u0431\u0435\u043b\u044b\u0439 \u0444\u043e\u043d */\n"
"QMainWindow {\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"/* \u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u2014 \u043c\u044f\u0433\u043a\u0438\u0439 \u043e\u0432\u0430\u043b\u044c\u043d\u044b\u0439 \u0431\u043b\u043e\u043a \u0441 \u0442\u0435\u043d\u044c\u044e */\n"
"QLabel#Label {\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"    color: black;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* \u0413\u0440\u0443\u043f\u043f\u044b \u2014 \u0441 \u043c\u044f\u0433\u043a\u0438\u043c\u0438 \u0442\u0435\u043d\u044f\u043c\u0438 \u0438 \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u043c\u0438 \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0430\u043c\u0438 */\n"
"QGroupBox {\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 12px;\n"
"    margin-top: 16p"
                        "x;\n"
"    background: #ffffff;\n"
"    padding: 10px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 0px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0438 \u2014 \u0441 \u0433\u0440\u0430\u0434\u0438\u0435\u043d\u0442\u043e\u043c \u043e\u0442 \u0440\u043e\u0437\u043e\u0432\u043e\u0433\u043e \u043a \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u043e\u043c\u0443 */\n"
"QPushButton {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        stop: 0 #FF9A76,\n"
"        stop: 1 #FF8C42\n"
"    );\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    box-shadow: 0 2px 4px rgba(255, 140, 66, 0.2);\n"
"}\n"
"QPushButton:hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 1, y2: 0,\n"
"        s"
                        "top: 0 #FF7F50,\n"
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
"        x2: 1, y2: 0,\n"
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
"QPushBut"
                        "ton#StartButton:pressed {\n"
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
"	text-align: center;\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 1px solid #FF8C42;\n"
"    background: #fff;\n"
"}\n"
"\n"
"/* \u041c\u0435\u0442\u043a\u0438 \u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442 \u2014 \u043d\u0435\u0431\u043e\u043b\u044c\u0448\u0438\u0435, \u0441 \u043c\u044f\u0433\u043a\u0438\u043c \u0444\u043e\u043d\u043e\u043c */\n"
"QLabel#XSource, QLabel#ZSource, QLabel#AngleLabel {\n"
"    background: #f5f5f5;\n"
"    border-radius"
                        ": 6px;\n"
"    padding: 4px 8px;\n"
"    color: #555;\n"
"    font-size: 13px;\n"
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
"/* \u0421\u043f\u0438\u0441\u043e\u043a \u0444\u0430\u0439\u043b\u043e\u0432 / \u0441\u0442\u0430\u0442\u0443\u0441 \u2014 \u0441 \u043b\u0451\u0433\u043a\u0438\u043c \u0444\u043e\u043d\u043e\u043c */\n"
"QListWidget {\n"
"    background: #fafafa;\n"
"    border: 1px solid #e0e0e0;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"    color: #444;\n"
"}\n"
"QList"
                        "Widget#StatusWidget {\n"
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
        self.Label = QLabel(self.centralwidget)
        self.Label.setObjectName(u"Label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label.sizePolicy().hasHeightForWidth())
        self.Label.setSizePolicy(sizePolicy)
        self.Label.setStyleSheet(u"QLabel#titleLabel {\n"
"    color: black;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background: transparent;\n"
"    border: none;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"}")

        self.gridLayout.addWidget(self.Label, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.BigWidget = QWidget(self.centralwidget)
        self.BigWidget.setObjectName(u"BigWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.BigWidget.sizePolicy().hasHeightForWidth())
        self.BigWidget.setSizePolicy(sizePolicy1)
        self.BigWidget.setMinimumSize(QSize(0, 500))
        self.horizontalLayout = QHBoxLayout(self.BigWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.LeftBlocks = QWidget(self.BigWidget)
        self.LeftBlocks.setObjectName(u"LeftBlocks")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.LeftBlocks.sizePolicy().hasHeightForWidth())
        self.LeftBlocks.setSizePolicy(sizePolicy2)
        self.LeftBlocks.setMinimumSize(QSize(343, 0))
        self.LeftBlocks.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(self.LeftBlocks)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ModelBox = QGroupBox(self.LeftBlocks)
        self.ModelBox.setObjectName(u"ModelBox")
        self.ModelBox.setMaximumSize(QSize(16777215, 200))
        self.ModelBox.setStyleSheet(u"QGroupBox:title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 0px;\n"
"    background: transparent;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.ModelBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.UploadedFileWidget = QListWidget(self.ModelBox)
        self.UploadedFileWidget.setObjectName(u"UploadedFileWidget")
        self.UploadedFileWidget.setMaximumSize(QSize(16777215, 100))
        self.UploadedFileWidget.setMouseTracking(False)
        self.UploadedFileWidget.setAutoFillBackground(False)
        self.UploadedFileWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.UploadedFileWidget.setSortingEnabled(True)

        self.verticalLayout_3.addWidget(self.UploadedFileWidget)

        self.widget = QWidget(self.ModelBox)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.UploadButton = QPushButton(self.widget)
        self.UploadButton.setObjectName(u"UploadButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.UploadButton.sizePolicy().hasHeightForWidth())
        self.UploadButton.setSizePolicy(sizePolicy3)
        self.UploadButton.setMinimumSize(QSize(93, 33))
        self.UploadButton.setMaximumSize(QSize(93, 33))
        self.UploadButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #FF8C42; /* \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u0439 */\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #FF702A; /* \u0447\u0443\u0442\u044c \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #E66B25; /* \u0435\u0449\u0451 \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}")

        self.horizontalLayout_2.addWidget(self.UploadButton)

        self.ClearButton = QPushButton(self.widget)
        self.ClearButton.setObjectName(u"ClearButton")
        sizePolicy3.setHeightForWidth(self.ClearButton.sizePolicy().hasHeightForWidth())
        self.ClearButton.setSizePolicy(sizePolicy3)
        self.ClearButton.setMinimumSize(QSize(93, 33))
        self.ClearButton.setMaximumSize(QSize(93, 33))
        self.ClearButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #8BC34A; /* \u0441\u0432\u0435\u0442\u043b\u043e-\u0437\u0435\u043b\u0451\u043d\u044b\u0439 */\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #7CB342; /* \u0447\u0443\u0442\u044c \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: #689F38; /* \u0435\u0449\u0451 \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}")

        self.horizontalLayout_2.addWidget(self.ClearButton)

        self.delta_line = QLineEdit(self.widget)
        self.delta_line.setObjectName(u"delta_line")
        self.delta_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.delta_line)


        self.verticalLayout_3.addWidget(self.widget)


        self.verticalLayout.addWidget(self.ModelBox)

        self.SourceBox = QGroupBox(self.LeftBlocks)
        self.SourceBox.setObjectName(u"SourceBox")
        self.SourceBox.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_4 = QVBoxLayout(self.SourceBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_6 = QWidget(self.SourceBox)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.X_line = QLineEdit(self.widget_6)
        self.X_line.setObjectName(u"X_line")
        self.X_line.setToolTipDuration(-1)
        self.X_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.X_line.setClearButtonEnabled(False)

        self.horizontalLayout_4.addWidget(self.X_line)

        self.Z_line = QLineEdit(self.widget_6)
        self.Z_line.setObjectName(u"Z_line")
        self.Z_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.Z_line)

        self.theta_line = QLineEdit(self.widget_6)
        self.theta_line.setObjectName(u"theta_line")
        self.theta_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.theta_line)


        self.verticalLayout_4.addWidget(self.widget_6)


        self.verticalLayout.addWidget(self.SourceBox)

        self.AnimationBox = QGroupBox(self.LeftBlocks)
        self.AnimationBox.setObjectName(u"AnimationBox")
        self.AnimationBox.setMinimumSize(QSize(0, 223))
        self.AnimationBox.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_5 = QVBoxLayout(self.AnimationBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.trajectoriesWidget = QListWidget(self.AnimationBox)
        self.trajectoriesWidget.setObjectName(u"trajectoriesWidget")
        self.trajectoriesWidget.setMaximumSize(QSize(16777215, 63))
        self.trajectoriesWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.trajectoriesWidget.setDragEnabled(False)
        self.trajectoriesWidget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        self.verticalLayout_5.addWidget(self.trajectoriesWidget)

        self.widget_2 = QWidget(self.AnimationBox)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.StartButton = QPushButton(self.widget_2)
        self.StartButton.setObjectName(u"StartButton")
        sizePolicy3.setHeightForWidth(self.StartButton.sizePolicy().hasHeightForWidth())
        self.StartButton.setSizePolicy(sizePolicy3)
        self.StartButton.setMinimumSize(QSize(84, 33))
        self.StartButton.setMaximumSize(QSize(84, 33))
        self.StartButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #FF8C42; /* \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u0439 */\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #FF702A; /* \u0447\u0443\u0442\u044c \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #E66B25; /* \u0435\u0449\u0451 \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}")

        self.horizontalLayout_6.addWidget(self.StartButton)

        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(84, 33))
        self.pushButton.setMaximumSize(QSize(84, 33))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #FF8C42; /* \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u0439 */\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #FF702A; /* \u0447\u0443\u0442\u044c \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #E66B25; /* \u0435\u0449\u0451 \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}")

        self.horizontalLayout_6.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.DeleteButton = QPushButton(self.widget_2)
        self.DeleteButton.setObjectName(u"DeleteButton")
        sizePolicy3.setHeightForWidth(self.DeleteButton.sizePolicy().hasHeightForWidth())
        self.DeleteButton.setSizePolicy(sizePolicy3)
        self.DeleteButton.setMinimumSize(QSize(84, 33))
        self.DeleteButton.setMaximumSize(QSize(84, 33))
        self.DeleteButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #8BC34A; /* \u0441\u0432\u0435\u0442\u043b\u043e-\u0437\u0435\u043b\u0451\u043d\u044b\u0439 */\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #7CB342; /* \u0447\u0443\u0442\u044c \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: #689F38; /* \u0435\u0449\u0451 \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}")

        self.horizontalLayout_6.addWidget(self.DeleteButton)


        self.verticalLayout_5.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.AnimationBox)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ShowButton = QPushButton(self.widget_3)
        self.ShowButton.setObjectName(u"ShowButton")
        self.ShowButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #FF8C42; /* \u043e\u0440\u0430\u043d\u0436\u0435\u0432\u044b\u0439 */\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #FF702A; /* \u0447\u0443\u0442\u044c \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #E66B25; /* \u0435\u0449\u0451 \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}")

        self.horizontalLayout_3.addWidget(self.ShowButton)

        self.HideButton = QPushButton(self.widget_3)
        self.HideButton.setObjectName(u"HideButton")
        self.HideButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #8BC34A; /* \u0441\u0432\u0435\u0442\u043b\u043e-\u0437\u0435\u043b\u0451\u043d\u044b\u0439 */\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #7CB342; /* \u0447\u0443\u0442\u044c \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u0438 */\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: #689F38; /* \u0435\u0449\u0451 \u0442\u0435\u043c\u043d\u0435\u0435 \u043f\u0440\u0438 \u043d\u0430\u0436\u0430\u0442\u0438\u0438 */\n"
"}")

        self.horizontalLayout_3.addWidget(self.HideButton)


        self.verticalLayout_5.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.AnimationBox)


        self.horizontalLayout.addWidget(self.LeftBlocks)

        self.RightBlocks = QGroupBox(self.BigWidget)
        self.RightBlocks.setObjectName(u"RightBlocks")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.RightBlocks.sizePolicy().hasHeightForWidth())
        self.RightBlocks.setSizePolicy(sizePolicy4)
        self.RightBlocks.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.RightBlocks)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.PlotWidget = QVBoxLayout()
        self.PlotWidget.setObjectName(u"PlotWidget")
        self.PlotWidget.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.verticalLayout_2.addLayout(self.PlotWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.StatusWidget = QListWidget(self.RightBlocks)
        self.StatusWidget.setObjectName(u"StatusWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.StatusWidget.sizePolicy().hasHeightForWidth())
        self.StatusWidget.setSizePolicy(sizePolicy5)
        self.StatusWidget.setMinimumSize(QSize(0, 50))
        self.StatusWidget.setMaximumSize(QSize(16777215, 81))

        self.verticalLayout_2.addWidget(self.StatusWidget)


        self.horizontalLayout.addWidget(self.RightBlocks)


        self.gridLayout.addWidget(self.BigWidget, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Eiconal Solver", None))
        self.Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Eiconal Solver</span></p></body></html>", None))
        self.ModelBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u043d\u043e\u0439 \u043c\u043e\u0434\u0435\u043b\u0438", None))
        self.UploadButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.ClearButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.delta_line.setToolTip(QCoreApplication.translate("MainWindow", u"\u0428\u0430\u0433 \u0441\u0435\u0442\u043a\u0438, \u043c", None))
#endif // QT_CONFIG(tooltip)
        self.delta_line.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.SourceBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u043b\u044c\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435", None))
#if QT_CONFIG(tooltip)
        self.X_line.setToolTip(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430 X \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430, \u043c ", None))
#endif // QT_CONFIG(tooltip)
        self.X_line.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.Z_line.setToolTip(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430 Z \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430, \u043c ", None))
#endif // QT_CONFIG(tooltip)
        self.Z_line.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.theta_line.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0433\u043e\u043b \u0432 \u0433\u0440\u0430\u0434\u0443\u0441\u0430\u0445", None))
#endif // QT_CONFIG(tooltip)
        self.theta_line.setText(QCoreApplication.translate("MainWindow", u"45", None))
        self.AnimationBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0441\u0447\u0451\u0442 \u0442\u0440\u0430\u0435\u043a\u0442\u043e\u0440\u0438\u0439", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442", None))
        self.DeleteButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.ShowButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c", None))
        self.HideButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043a\u0440\u044b\u0442\u044c", None))
        self.RightBlocks.setTitle("")
    # retranslateUi

