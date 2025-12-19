# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Designer_Apps_Seismic.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 600)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: #1e1e1e;\n"
"	font-size: 12pt;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    font-weight: bold;\n"
"    border: 1px solid #333;\n"
"    border-radius: 8px;\n"
"    margin-top: 10px;\n"
"    padding-top: 5px;\n"
"    background-color: #2d2d2d;\n"
"    color: #ffffff;\n"
"	font-size: 12pt;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 5px;\n"
"    color: #ffffff;\n"
"	font-size: 12pt;\n"
"}\n"
"\n"
"/*\u041a\u043d\u043e\u043f\u043a\u0430 \u0441 \u0432\u044b\u0431\u043e\u0440\u043e\u043c \u043f\u043e\u0440\u044f\u0434\u043a\u0430 \u0444\u0438\u043b\u044c\u0442\u0440\u0430*/\n"
"QSpinBox {\n"
"    background-color: #333;\n"
"    border: 1px solid #555;\n"
"    border-radius: 12px;\n"
"    padding: 5px;\n"
"    color: #ffffff;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-le"
                        "ft: 1px solid #555;\n"
"    border-radius: 9px;\n"
"    background-color: #444;\n"
"    margin-right: 3px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-left: 1px solid #555;\n"
"    border-radius: 9px;\n"
"    background-color: #444;\n"
"    margin-right: 3px; \n"
"}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 10px;\n"
"    height: 10px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"QSpinBox::down-arrow {\n"
"    width: 10px;\n"
"    height: 10px;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"/*\u0422\u0435\u043a\u0441\u0442\u043e\u0432\u044b\u0435 \u043f\u043e\u043b\u044f*/\n"
"QLabel {\n"
"    color: #ffffff;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #555;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #ffffff;\n"
"	font-size: 12pt;\n"
"}\n"
"\n"
"/*\u041a\u043d\u043e\u043f\u043a\u0430 \u0441 \u0432\u044b\u0431\u043e"
                        "\u0440\u043e\u043c \u0444\u0438\u043b\u044c\u0442\u0440\u0430*/\n"
"QComboBox {\n"
"    border: 1px solid #555;\n"
"    border-radius: 12px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #ffffff;\n"
"	font-size: 12pt;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 0px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: none;\n"
"}\n"
"\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0430 \"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c\" */\n"
"#pushButton_load {\n"
"    background-color: #ff3b30;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"#pushButton_load:hover {\n"
"    background-color: #ff574d;\n"
"}\n"
"\n"
"#pushButton_load:pressed {\n"
"    background-color: #ff2a1f;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0430 \"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c\"*/\n"
"#pushButton_clear {\n"
""
                        "    background-color: #555;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"#pushButton_clear:hover {\n"
"    background-color: #666;\n"
"}\n"
"\n"
"#pushButton_clear:pressed {\n"
"    background-color: #444;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0430 \"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c\"*/\n"
"#pushButton_apply {\n"
"    background-color: #ff3b30;\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"#pushButton_apply:hover {\n"
"    background-color: #ff574d;\n"
"}\n"
"\n"
"#pushButton_apply:pressed {\n"
"    background-color: #ff2a1f;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0430 \"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c\"*/\n"
"#pushButton_reset {\n"
"    background-color: #555;\n"
"    border: none;\n"
"    border-radius: 12p"
                        "x;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"    font-size: 12pt;\n"
"}\n"
"\n"
"#pushButton_reset:hover {\n"
"    background-color: #666;\n"
"}\n"
"\n"
"#pushButton_reset:pressed {\n"
"    background-color: #444;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.centralwidget.setAutoFillBackground(False)
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_panel = QVBoxLayout()
        self.left_panel.setSpacing(0)
        self.left_panel.setObjectName(u"left_panel")
        self.left_panel.setContentsMargins(0, 0, 0, 0)
        self.groupBox_LoadSEGY = QGroupBox(self.centralwidget)
        self.groupBox_LoadSEGY.setObjectName(u"groupBox_LoadSEGY")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_LoadSEGY.sizePolicy().hasHeightForWidth())
        self.groupBox_LoadSEGY.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_LoadSEGY)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_between_border_and_File = QSpacerItem(20, 7, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_between_border_and_File)

        self.verticalLayout_for_LoadSEGY = QVBoxLayout()
        self.verticalLayout_for_LoadSEGY.setObjectName(u"verticalLayout_for_LoadSEGY")
        self.verticalLayout_for_LoadSEGY.setContentsMargins(6, 5, 10, 5)
        self.horizontalLayout_for_file = QHBoxLayout()
        self.horizontalLayout_for_file.setObjectName(u"horizontalLayout_for_file")
        self.horizontalLayout_for_file.setContentsMargins(6, 5, 10, 5)
        self.label_File = QLabel(self.groupBox_LoadSEGY)
        self.label_File.setObjectName(u"label_File")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_File.setFont(font1)

        self.horizontalLayout_for_file.addWidget(self.label_File)

        self.horizontalSpacer_between_File_lineEdit = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_for_file.addItem(self.horizontalSpacer_between_File_lineEdit)

        self.lineEdit_NameFile = QLineEdit(self.groupBox_LoadSEGY)
        self.lineEdit_NameFile.setObjectName(u"lineEdit_NameFile")

        self.horizontalLayout_for_file.addWidget(self.lineEdit_NameFile)

        self.horizontalLayout_for_file.setStretch(0, 1)
        self.horizontalLayout_for_file.setStretch(1, 2)
        self.horizontalLayout_for_file.setStretch(2, 5)

        self.verticalLayout_for_LoadSEGY.addLayout(self.horizontalLayout_for_file)

        self.verticalSpacer_between_File_and_pButton_double = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_for_LoadSEGY.addItem(self.verticalSpacer_between_File_and_pButton_double)

        self.horizontalLayout_for_pbutton = QHBoxLayout()
        self.horizontalLayout_for_pbutton.setSpacing(5)
        self.horizontalLayout_for_pbutton.setObjectName(u"horizontalLayout_for_pbutton")
        self.horizontalLayout_for_pbutton.setContentsMargins(6, 5, 10, 5)
        self.pushButton_load = QPushButton(self.groupBox_LoadSEGY)
        self.pushButton_load.setObjectName(u"pushButton_load")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load.sizePolicy().hasHeightForWidth())
        self.pushButton_load.setSizePolicy(sizePolicy1)

        self.horizontalLayout_for_pbutton.addWidget(self.pushButton_load)

        self.horizontalSpacer_between_pBLoad_and_pBClear = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_for_pbutton.addItem(self.horizontalSpacer_between_pBLoad_and_pBClear)

        self.pushButton_clear = QPushButton(self.groupBox_LoadSEGY)
        self.pushButton_clear.setObjectName(u"pushButton_clear")
        sizePolicy1.setHeightForWidth(self.pushButton_clear.sizePolicy().hasHeightForWidth())
        self.pushButton_clear.setSizePolicy(sizePolicy1)

        self.horizontalLayout_for_pbutton.addWidget(self.pushButton_clear)

        self.horizontalLayout_for_pbutton.setStretch(0, 4)
        self.horizontalLayout_for_pbutton.setStretch(1, 1)
        self.horizontalLayout_for_pbutton.setStretch(2, 4)

        self.verticalLayout_for_LoadSEGY.addLayout(self.horizontalLayout_for_pbutton)


        self.verticalLayout_2.addLayout(self.verticalLayout_for_LoadSEGY)

        self.verticalSpacer_between_pButton_and_border = QSpacerItem(20, 7, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_between_pButton_and_border)


        self.left_panel.addWidget(self.groupBox_LoadSEGY)

        self.groupBox_SettingFilter = QGroupBox(self.centralwidget)
        self.groupBox_SettingFilter.setObjectName(u"groupBox_SettingFilter")
        sizePolicy.setHeightForWidth(self.groupBox_SettingFilter.sizePolicy().hasHeightForWidth())
        self.groupBox_SettingFilter.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_SettingFilter)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_SettingFilter = QVBoxLayout()
        self.verticalLayout_SettingFilter.setObjectName(u"verticalLayout_SettingFilter")
        self.verticalLayout_SettingFilter.setContentsMargins(6, 5, 10, 5)
        self.verticalSpacer_between_border_and_Filter = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_SettingFilter.addItem(self.verticalSpacer_between_border_and_Filter)

        self.horizontalLayout_for_Filter = QHBoxLayout()
        self.horizontalLayout_for_Filter.setObjectName(u"horizontalLayout_for_Filter")
        self.horizontalLayout_for_Filter.setContentsMargins(6, 5, 10, 5)
        self.label_Filter = QLabel(self.groupBox_SettingFilter)
        self.label_Filter.setObjectName(u"label_Filter")
        self.label_Filter.setFont(font1)

        self.horizontalLayout_for_Filter.addWidget(self.label_Filter)

        self.horizontalSpacer_between_Filter_and_comboBox = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_for_Filter.addItem(self.horizontalSpacer_between_Filter_and_comboBox)

        self.comboBox_for_typeFilter = QComboBox(self.groupBox_SettingFilter)
        self.comboBox_for_typeFilter.addItem("")
        self.comboBox_for_typeFilter.addItem("")
        self.comboBox_for_typeFilter.addItem("")
        self.comboBox_for_typeFilter.setObjectName(u"comboBox_for_typeFilter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBox_for_typeFilter.sizePolicy().hasHeightForWidth())
        self.comboBox_for_typeFilter.setSizePolicy(sizePolicy2)
        self.comboBox_for_typeFilter.setEditable(False)

        self.horizontalLayout_for_Filter.addWidget(self.comboBox_for_typeFilter)

        self.horizontalLayout_for_Filter.setStretch(0, 4)
        self.horizontalLayout_for_Filter.setStretch(1, 3)
        self.horizontalLayout_for_Filter.setStretch(2, 3)

        self.verticalLayout_SettingFilter.addLayout(self.horizontalLayout_for_Filter)

        self.verticalSpacer_between_Filter_and_NFilter = QSpacerItem(20, 7, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_SettingFilter.addItem(self.verticalSpacer_between_Filter_and_NFilter)

        self.horizontalLayout_for_NFilter = QHBoxLayout()
        self.horizontalLayout_for_NFilter.setObjectName(u"horizontalLayout_for_NFilter")
        self.horizontalLayout_for_NFilter.setContentsMargins(6, 5, 10, 5)
        self.label_NFilter = QLabel(self.groupBox_SettingFilter)
        self.label_NFilter.setObjectName(u"label_NFilter")
        self.label_NFilter.setFont(font1)

        self.horizontalLayout_for_NFilter.addWidget(self.label_NFilter)

        self.horizontalSpacer_between_NFilter_and_spinBox = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_for_NFilter.addItem(self.horizontalSpacer_between_NFilter_and_spinBox)

        self.spinBox = QSpinBox(self.groupBox_SettingFilter)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy2)
        self.spinBox.setMaximum(10)

        self.horizontalLayout_for_NFilter.addWidget(self.spinBox)

        self.horizontalLayout_for_NFilter.setStretch(0, 2)
        self.horizontalLayout_for_NFilter.setStretch(1, 3)
        self.horizontalLayout_for_NFilter.setStretch(2, 1)

        self.verticalLayout_SettingFilter.addLayout(self.horizontalLayout_for_NFilter)

        self.verticalSpacer_between_NFilter_and_ArrangeFreq = QSpacerItem(20, 7, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_SettingFilter.addItem(self.verticalSpacer_between_NFilter_and_ArrangeFreq)

        self.horizontalLayout_for_RangeFreq = QHBoxLayout()
        self.horizontalLayout_for_RangeFreq.setObjectName(u"horizontalLayout_for_RangeFreq")
        self.horizontalLayout_for_RangeFreq.setContentsMargins(6, 5, 10, 5)
        self.label_RangeFreq = QLabel(self.groupBox_SettingFilter)
        self.label_RangeFreq.setObjectName(u"label_RangeFreq")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_RangeFreq.sizePolicy().hasHeightForWidth())
        self.label_RangeFreq.setSizePolicy(sizePolicy3)
        self.label_RangeFreq.setFont(font1)

        self.horizontalLayout_for_RangeFreq.addWidget(self.label_RangeFreq)


        self.verticalLayout_SettingFilter.addLayout(self.horizontalLayout_for_RangeFreq)

        self.horizontalLayout_Min_Max = QHBoxLayout()
        self.horizontalLayout_Min_Max.setObjectName(u"horizontalLayout_Min_Max")
        self.horizontalLayout_Min_Max.setContentsMargins(6, 5, 10, -1)
        self.label_Min = QLabel(self.groupBox_SettingFilter)
        self.label_Min.setObjectName(u"label_Min")
        self.label_Min.setFont(font1)

        self.horizontalLayout_Min_Max.addWidget(self.label_Min)

        self.horizontalSpacer_between_Min_lineEdit = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_Min_Max.addItem(self.horizontalSpacer_between_Min_lineEdit)

        self.lineEdit_forMin = QLineEdit(self.groupBox_SettingFilter)
        self.lineEdit_forMin.setObjectName(u"lineEdit_forMin")

        self.horizontalLayout_Min_Max.addWidget(self.lineEdit_forMin)

        self.horizontalSpacer_between_lineEdit_Max = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_Min_Max.addItem(self.horizontalSpacer_between_lineEdit_Max)

        self.label_Max = QLabel(self.groupBox_SettingFilter)
        self.label_Max.setObjectName(u"label_Max")
        self.label_Max.setFont(font1)

        self.horizontalLayout_Min_Max.addWidget(self.label_Max)

        self.horizontalSpacer_between_Max_lineEdit = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_Min_Max.addItem(self.horizontalSpacer_between_Max_lineEdit)

        self.lineEdit_forMax = QLineEdit(self.groupBox_SettingFilter)
        self.lineEdit_forMax.setObjectName(u"lineEdit_forMax")

        self.horizontalLayout_Min_Max.addWidget(self.lineEdit_forMax)

        self.horizontalLayout_Min_Max.setStretch(0, 1)
        self.horizontalLayout_Min_Max.setStretch(1, 1)
        self.horizontalLayout_Min_Max.setStretch(2, 2)
        self.horizontalLayout_Min_Max.setStretch(3, 1)
        self.horizontalLayout_Min_Max.setStretch(4, 1)
        self.horizontalLayout_Min_Max.setStretch(5, 1)
        self.horizontalLayout_Min_Max.setStretch(6, 2)

        self.verticalLayout_SettingFilter.addLayout(self.horizontalLayout_Min_Max)

        self.verticalSpacer_between_ArrangeFreq_and_border = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_SettingFilter.addItem(self.verticalSpacer_between_ArrangeFreq_and_border)

        self.verticalLayout_SettingFilter.setStretch(0, 1)
        self.verticalLayout_SettingFilter.setStretch(1, 4)
        self.verticalLayout_SettingFilter.setStretch(2, 1)
        self.verticalLayout_SettingFilter.setStretch(3, 4)
        self.verticalLayout_SettingFilter.setStretch(4, 1)
        self.verticalLayout_SettingFilter.setStretch(5, 2)
        self.verticalLayout_SettingFilter.setStretch(6, 2)
        self.verticalLayout_SettingFilter.setStretch(7, 1)

        self.verticalLayout_4.addLayout(self.verticalLayout_SettingFilter)


        self.left_panel.addWidget(self.groupBox_SettingFilter)

        self.groupBox_ApplyFilter = QGroupBox(self.centralwidget)
        self.groupBox_ApplyFilter.setObjectName(u"groupBox_ApplyFilter")
        sizePolicy.setHeightForWidth(self.groupBox_ApplyFilter.sizePolicy().hasHeightForWidth())
        self.groupBox_ApplyFilter.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox_ApplyFilter)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_for_applyFilter = QVBoxLayout()
        self.verticalLayout_for_applyFilter.setObjectName(u"verticalLayout_for_applyFilter")
        self.horizontalLayout_ApplyFilter = QHBoxLayout()
        self.horizontalLayout_ApplyFilter.setSpacing(5)
        self.horizontalLayout_ApplyFilter.setObjectName(u"horizontalLayout_ApplyFilter")
        self.horizontalLayout_ApplyFilter.setContentsMargins(6, 5, 10, 5)
        self.pushButton_apply = QPushButton(self.groupBox_ApplyFilter)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        sizePolicy1.setHeightForWidth(self.pushButton_apply.sizePolicy().hasHeightForWidth())
        self.pushButton_apply.setSizePolicy(sizePolicy1)

        self.horizontalLayout_ApplyFilter.addWidget(self.pushButton_apply)

        self.horizontalSpacer_between_pBApply_and_pBReset = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_ApplyFilter.addItem(self.horizontalSpacer_between_pBApply_and_pBReset)

        self.pushButton_reset = QPushButton(self.groupBox_ApplyFilter)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        sizePolicy1.setHeightForWidth(self.pushButton_reset.sizePolicy().hasHeightForWidth())
        self.pushButton_reset.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButton_reset.setFont(font2)

        self.horizontalLayout_ApplyFilter.addWidget(self.pushButton_reset)

        self.horizontalLayout_ApplyFilter.setStretch(0, 4)
        self.horizontalLayout_ApplyFilter.setStretch(1, 1)
        self.horizontalLayout_ApplyFilter.setStretch(2, 4)

        self.verticalLayout_for_applyFilter.addLayout(self.horizontalLayout_ApplyFilter)


        self.verticalLayout.addLayout(self.verticalLayout_for_applyFilter)


        self.left_panel.addWidget(self.groupBox_ApplyFilter)

        self.left_panel.setStretch(0, 3)
        self.left_panel.setStretch(1, 6)
        self.left_panel.setStretch(2, 2)

        self.horizontalLayout.addLayout(self.left_panel)

        self.widget_plot = QWidget(self.centralwidget)
        self.widget_plot.setObjectName(u"widget_plot")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_plot.sizePolicy().hasHeightForWidth())
        self.widget_plot.setSizePolicy(sizePolicy4)
        self.gridLayout = QGridLayout(self.widget_plot)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_for_plotgraf = QVBoxLayout()
        self.verticalLayout_for_plotgraf.setObjectName(u"verticalLayout_for_plotgraf")

        self.gridLayout.addLayout(self.verticalLayout_for_plotgraf, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.widget_plot)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 5)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_LoadSEGY.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 SEGY", None))
        self.label_File.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b:", None))
        self.pushButton_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.pushButton_clear.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.groupBox_SettingFilter.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432 \u0444\u0438\u043b\u044c\u0442\u0440\u0430", None))
        self.label_Filter.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0438\u043b\u044c\u0442\u0440:", None))
        self.comboBox_for_typeFilter.setItemText(0, QCoreApplication.translate("MainWindow", u"bandpass", None))
        self.comboBox_for_typeFilter.setItemText(1, QCoreApplication.translate("MainWindow", u"lowpass", None))
        self.comboBox_for_typeFilter.setItemText(2, QCoreApplication.translate("MainWindow", u"highpass", None))

        self.label_NFilter.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0444\u0438\u043b\u044c\u0442\u0440\u0430:", None))
        self.label_RangeFreq.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0438\u0430\u043f\u0430\u0437\u043e\u043d \u0447\u0430\u0441\u0442\u043e\u0442, \u0413\u0446:", None))
        self.label_Min.setText(QCoreApplication.translate("MainWindow", u"Min:", None))
        self.label_Max.setText(QCoreApplication.translate("MainWindow", u"Max:", None))
        self.groupBox_ApplyFilter.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0444\u0438\u043b\u044c\u0442\u0440\u0430", None))
        self.pushButton_apply.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.pushButton_reset.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c", None))
    # retranslateUi

