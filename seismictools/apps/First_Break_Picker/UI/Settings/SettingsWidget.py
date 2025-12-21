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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(758, 709)
        icon = QIcon()
        icon.addFile(u"software_17122633.gif", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        self.CentralWidget = QWidget(MainWindow)
        self.CentralWidget.setObjectName(u"CentralWidget")
        self.gridLayout = QGridLayout(self.CentralWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 5, 9, 9)
        self.Tab_widget = QTabWidget(self.CentralWidget)
        self.Tab_widget.setObjectName(u"Tab_widget")
        self.Tab_widget.setStyleSheet(u"")
        self.Settings_page = QWidget()
        self.Settings_page.setObjectName(u"Settings_page")
        self.formLayout = QFormLayout(self.Settings_page)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        self.formLayout.setHorizontalSpacing(120)
        self.formLayout.setContentsMargins(-1, 8, -1, -1)
        self.Layout_with_Picks_box = QHBoxLayout()
        self.Layout_with_Picks_box.setObjectName(u"Layout_with_Picks_box")

        self.formLayout.setLayout(9, QFormLayout.ItemRole.LabelRole, self.Layout_with_Picks_box)

        self.Upload_Box = QGroupBox(self.Settings_page)
        self.Upload_Box.setObjectName(u"Upload_Box")
        self.Upload_Box.setEnabled(True)
        self.Upload_Box.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.Upload_Box)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(-1, 9, 9, -1)
        self.Upload_layout_1 = QVBoxLayout()
        self.Upload_layout_1.setObjectName(u"Upload_layout_1")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.Upload_layout_1.addItem(self.verticalSpacer)

        self.SGY_file_label = QLabel(self.Upload_Box)
        self.SGY_file_label.setObjectName(u"SGY_file_label")
        self.SGY_file_label.setStyleSheet(u" Qlabel {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}")

        self.Upload_layout_1.addWidget(self.SGY_file_label)

        self.SGY_files_line = QLineEdit(self.Upload_Box)
        self.SGY_files_line.setObjectName(u"SGY_files_line")

        self.Upload_layout_1.addWidget(self.SGY_files_line)

        self.Upload_buttoms_layout = QHBoxLayout()
        self.Upload_buttoms_layout.setObjectName(u"Upload_buttoms_layout")
        self.Upload_buttom = QPushButton(self.Upload_Box)
        self.Upload_buttom.setObjectName(u"Upload_buttom")
        self.Upload_buttom.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(242, 110, 2);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 113, 184);\n"
"}")

        self.Upload_buttoms_layout.addWidget(self.Upload_buttom)

        self.Clear_buttom = QPushButton(self.Upload_Box)
        self.Clear_buttom.setObjectName(u"Clear_buttom")
        self.Clear_buttom.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(242, 110, 2);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 113, 184);\n"
"}")

        self.Upload_buttoms_layout.addWidget(self.Clear_buttom)


        self.Upload_layout_1.addLayout(self.Upload_buttoms_layout)

        self.Load_Picks_buttom = QPushButton(self.Upload_Box)
        self.Load_Picks_buttom.setObjectName(u"Load_Picks_buttom")
        self.Load_Picks_buttom.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(242, 110, 2);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 113, 184);\n"
"}")

        self.Upload_layout_1.addWidget(self.Load_Picks_buttom)

        self.Formats_label = QLabel(self.Upload_Box)
        self.Formats_label.setObjectName(u"Formats_label")

        self.Upload_layout_1.addWidget(self.Formats_label)


        self.verticalLayout_4.addLayout(self.Upload_layout_1)


        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.Upload_Box)

        self.Toggele_mode = QComboBox(self.Settings_page)
        self.Toggele_mode.setObjectName(u"Toggele_mode")
        self.Toggele_mode.setStyleSheet(u"QComboBox {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border: 1px solid #555;\n"
"    padding: 5px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background-color: rgb(254, 146, 35);\n"
"    width: 20px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/down-arrow.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    selection-background-color: rgb(254, 146, 35);\n"
"    border: 1px solid #555;\n"
"}")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.Toggele_mode)

        self.Picks_layout = QVBoxLayout()
        self.Picks_layout.setSpacing(0)
        self.Picks_layout.setObjectName(u"Picks_layout")
        self.Picks_layout.setContentsMargins(0, 14, 30, 0)
        self.Picks_table_widget = QTableWidget(self.Settings_page)
        if (self.Picks_table_widget.columnCount() < 3):
            self.Picks_table_widget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.Picks_table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.Picks_table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.Picks_table_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.Picks_table_widget.setObjectName(u"Picks_table_widget")

        self.Picks_layout.addWidget(self.Picks_table_widget)

        self.Picks_buttoms_layout = QHBoxLayout()
        self.Picks_buttoms_layout.setSpacing(0)
        self.Picks_buttoms_layout.setObjectName(u"Picks_buttoms_layout")
        self.Picks_buttoms_layout.setContentsMargins(-1, -1, 0, -1)
        self.Delite_one_buttom = QPushButton(self.Settings_page)
        self.Delite_one_buttom.setObjectName(u"Delite_one_buttom")
        self.Delite_one_buttom.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(242, 110, 2);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 113, 184);\n"
"}")

        self.Picks_buttoms_layout.addWidget(self.Delite_one_buttom)

        self.Delite_all_buttom = QPushButton(self.Settings_page)
        self.Delite_all_buttom.setObjectName(u"Delite_all_buttom")
        self.Delite_all_buttom.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(242, 110, 2);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 113, 184);\n"
"}")

        self.Picks_buttoms_layout.addWidget(self.Delite_all_buttom)


        self.Picks_layout.addLayout(self.Picks_buttoms_layout)

        self.Save_Picks_buttom = QPushButton(self.Settings_page)
        self.Save_Picks_buttom.setObjectName(u"Save_Picks_buttom")
        self.Save_Picks_buttom.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(242, 110, 2);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 113, 184);\n"
"}")

        self.Picks_layout.addWidget(self.Save_Picks_buttom)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.Picks_layout)

        self.PIcks_box = QGroupBox(self.Settings_page)
        self.PIcks_box.setObjectName(u"PIcks_box")
        self.PIcks_box.setStyleSheet(u" QGroupBox {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.PIcks_box)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.PIcks_box)

        self.Log_line = QListWidget(self.Settings_page)
        self.Log_line.setObjectName(u"Log_line")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.Log_line)

        self.show_log_buttom = QPushButton(self.Settings_page)
        self.show_log_buttom.setObjectName(u"show_log_buttom")
        self.show_log_buttom.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(242, 110, 2);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 113, 184);\n"
"}")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.show_log_buttom)

        self.Settings_list_label = QLabel(self.Settings_page)
        self.Settings_list_label.setObjectName(u"Settings_list_label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.Settings_list_label)

        self.Tab_widget.addTab(self.Settings_page, "")
        self.Plotting_Page = QWidget()
        self.Plotting_Page.setObjectName(u"Plotting_Page")
        self.horizontalLayout = QHBoxLayout(self.Plotting_Page)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout.setContentsMargins(2, 2, 1, 2)
        self.layout_with_plot = QVBoxLayout()
        self.layout_with_plot.setObjectName(u"layout_with_plot")
        self.Groupe_box_of_Plot_screen = QGroupBox(self.Plotting_Page)
        self.Groupe_box_of_Plot_screen.setObjectName(u"Groupe_box_of_Plot_screen")
        self.verticalLayout_5 = QVBoxLayout(self.Groupe_box_of_Plot_screen)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.Plot_screen = QWidget(self.Groupe_box_of_Plot_screen)
        self.Plot_screen.setObjectName(u"Plot_screen")
        self.verticalLayout_2 = QVBoxLayout(self.Plot_screen)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout_5.addWidget(self.Plot_screen)

        self.Picks_choose = QComboBox(self.Groupe_box_of_Plot_screen)
        self.Picks_choose.setObjectName(u"Picks_choose")
        self.Picks_choose.setStyleSheet(u"QComboBox {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    border: 1px solid #555;\n"
"    padding: 5px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    background-color: rgb(254, 146, 35);\n"
"    width: 20px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/down-arrow.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgb(254, 146, 35);\n"
"    color: white;\n"
"    selection-background-color: rgb(254, 146, 35);\n"
"    border: 1px solid #555;\n"
"}")

        self.verticalLayout_5.addWidget(self.Picks_choose)


        self.layout_with_plot.addWidget(self.Groupe_box_of_Plot_screen)


        self.horizontalLayout.addLayout(self.layout_with_plot)

        self.Tab_widget.addTab(self.Plotting_Page, "")

        self.gridLayout.addWidget(self.Tab_widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.CentralWidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.Tab_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"First Break Picker", None))
        self.Upload_Box.setTitle(QCoreApplication.translate("MainWindow", u"Upload Data", None))
        self.SGY_file_label.setText(QCoreApplication.translate("MainWindow", u"SGY-file", None))
        self.Upload_buttom.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.Clear_buttom.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.Load_Picks_buttom.setText(QCoreApplication.translate("MainWindow", u"Load Picks", None))
        self.Formats_label.setText(QCoreApplication.translate("MainWindow", u"files formats - .sgy/.segy for seismogramm json for Picks", None))
        self.Toggele_mode.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Color Palet", None))
        ___qtablewidgetitem = self.Picks_table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Trace", None));
        ___qtablewidgetitem1 = self.Picks_table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Time", None));
        ___qtablewidgetitem2 = self.Picks_table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Pick type", None));
        self.Delite_one_buttom.setText(QCoreApplication.translate("MainWindow", u"Delete Pick", None))
        self.Delite_all_buttom.setText(QCoreApplication.translate("MainWindow", u"Delete All", None))
        self.Save_Picks_buttom.setText(QCoreApplication.translate("MainWindow", u"Save picks as .json", None))
        self.PIcks_box.setTitle(QCoreApplication.translate("MainWindow", u"Picks avilabel", None))
        self.show_log_buttom.setText(QCoreApplication.translate("MainWindow", u"Show log", None))
        self.Settings_list_label.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.Tab_widget.setTabText(self.Tab_widget.indexOf(self.Settings_page), QCoreApplication.translate("MainWindow", u"Settings Page", None))
        self.Groupe_box_of_Plot_screen.setTitle(QCoreApplication.translate("MainWindow", u"Plotting", None))
        self.Tab_widget.setTabText(self.Tab_widget.indexOf(self.Plotting_Page), QCoreApplication.translate("MainWindow", u"Plotting Page", None))
    # retranslateUi

