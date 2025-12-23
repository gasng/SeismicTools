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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_NMOWidget(object):
    def setupUi(self, NMOWidget):
        if not NMOWidget.objectName():
            NMOWidget.setObjectName(u"NMOWidget")
        NMOWidget.resize(1035, 963)
        NMOWidget.setStyleSheet(u"/* \u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0441\u0442\u0438\u043b\u044c \u2014 \u0442\u0451\u043c\u043d\u0430\u044f \u0442\u0435\u043c\u0430 */\n"
"QWidget {\n"
"    background-color: #2d2d2d;\n"
"    color: #e6e6e6;\n"
"    font-family: \"Segoe UI\", \"Noto Sans\", sans-serif;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0438 \u2014 \u043e\u043a\u0440\u0443\u0433\u043b\u044b\u0435, \u0441 \u0433\u0440\u0430\u043d\u0438\u0446\u0435\u0439, \u0445\u043e\u0440\u043e\u0448\u043e \u0440\u0430\u0437\u043b\u0438\u0447\u0438\u043c\u044b */\n"
"QPushButton {\n"
"    background-color: #3e3e3e;\n"
"    border: 1px solid #555555;\n"
"    border-radius: 10px;\n"
"    padding: 8px 16px;\n"
"    color: #ffffff;\n"
"    min-width: 80px;\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4c4c4c;\n"
"    border: 1px solid #666666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2a2a2a;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
""
                        "QPushButton:disabled {\n"
"    background-color: #353535;\n"
"    color: #888888;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
"/* RadioButton \u2014 \u0442\u0435\u043f\u0435\u0440\u044c \u0447\u0451\u0442\u043a\u043e \u0432\u0438\u0434\u0435\u043d, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0435 \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 */\n"
"QRadioButton {\n"
"    color: #e6e6e6;\n"
"    background-color: transparent;\n"
"    spacing: 8px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border: 2px solid #777777;\n"
"    border-radius: 8px;\n"
"    background-color: #252525;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border: 2px solid #aaaaaa;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border: 2px solid #00a8ff;\n"
"    background-color: #00a8ff;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover {\n"
"    border: 2px solid #33ccff;\n"
"    background-color: #00a8ff;\n"
""
                        "}\n"
"\n"
"/* \u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0438 \u0442\u0430\u0431\u043b\u0438\u0446 \u2014 \u0442\u0451\u043c\u043d\u044b\u0435 \u0441 \u0431\u0435\u043b\u044b\u043c \u0442\u0435\u043a\u0441\u0442\u043e\u043c */\n"
"QHeaderView::section {\n"
"    background-color: #333333;\n"
"    color: #ffffff;\n"
"    padding: 6px;\n"
"    border: 1px solid #444444;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QHeaderView::section:hover {\n"
"    background-color: #3a3a3a;\n"
"}\n"
"\n"
"/* \u0422\u0430\u0431\u043b\u0438\u0446\u044b */\n"
"QTableWidget, QTableView {\n"
"    background-color: #252525;\n"
"    alternate-background-color: #2a2a2a;\n"
"    gridline-color: #3c3c3c;\n"
"    selection-background-color: #005682;\n"
"    selection-color: #ffffff;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
"/* \u041f\u043e\u043b\u044f \u0432\u0432\u043e\u0434\u0430 */\n"
"QLineEdit, QSpinBox, QDoubleSpinBox {\n"
"    background-color: #333333;\n"
"    border: 1px solid #555555;\n"
"    border-radius: 6px;\n"
""
                        "    padding: 5px;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #0078d7;\n"
"}\n"
"\n"
"/* \u0421\u043a\u0440\u043e\u043b\u043b\u0431\u0430\u0440 */\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
"    background: #2b2b2b;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical, QScrollBar::handle:horizontal {\n"
"    background: #444444;\n"
"    border-radius: 4px;\n"
"    min-height: 20px;\n"
"    min-width: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:hover {\n"
"    background: #555555;\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(NMOWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.mainBox = QWidget(NMOWidget)
        self.mainBox.setObjectName(u"mainBox")
        self.horizontalLayout_4 = QHBoxLayout(self.mainBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.leftBox = QWidget(self.mainBox)
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

        self.Datalist = QListWidget(self.DataLoadBox)
        self.Datalist.setObjectName(u"Datalist")

        self.verticalLayout_2.addWidget(self.Datalist)

        self.widget_3 = QWidget(self.DataLoadBox)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_choice = QPushButton(self.widget_3)
        self.pushButton_choice.setObjectName(u"pushButton_choice")

        self.horizontalLayout_7.addWidget(self.pushButton_choice)

        self.pushButton_load = QPushButton(self.widget_3)
        self.pushButton_load.setObjectName(u"pushButton_load")

        self.horizontalLayout_7.addWidget(self.pushButton_load)

        self.pushButton_clear = QPushButton(self.widget_3)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.horizontalLayout_7.addWidget(self.pushButton_clear)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.label_2 = QLabel(self.DataLoadBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.DataLoadBox)

        self.VanalisisBox = QGroupBox(self.leftBox)
        self.VanalisisBox.setObjectName(u"VanalisisBox")
        self.verticalLayout_3 = QVBoxLayout(self.VanalisisBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget = QWidget(self.VanalisisBox)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_8 = QHBoxLayout(self.widget)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_velocitySpectrum = QPushButton(self.widget)
        self.pushButton_velocitySpectrum.setObjectName(u"pushButton_velocitySpectrum")

        self.horizontalLayout_8.addWidget(self.pushButton_velocitySpectrum)

        self.pushButton_applyCorrections = QPushButton(self.widget)
        self.pushButton_applyCorrections.setObjectName(u"pushButton_applyCorrections")

        self.horizontalLayout_8.addWidget(self.pushButton_applyCorrections)


        self.verticalLayout_3.addWidget(self.widget)

        self.pickBox = QGroupBox(self.VanalisisBox)
        self.pickBox.setObjectName(u"pickBox")
        self.horizontalLayout = QHBoxLayout(self.pickBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton_pick = QRadioButton(self.pickBox)
        self.radioButton_pick.setObjectName(u"radioButton_pick")

        self.horizontalLayout.addWidget(self.radioButton_pick)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.radioButton_view = QRadioButton(self.pickBox)
        self.radioButton_view.setObjectName(u"radioButton_view")

        self.horizontalLayout.addWidget(self.radioButton_view)


        self.verticalLayout_3.addWidget(self.pickBox)

        self.tableWidget_picks = QTableWidget(self.VanalisisBox)
        if (self.tableWidget_picks.columnCount() < 3):
            self.tableWidget_picks.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_picks.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_picks.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_picks.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_picks.setObjectName(u"tableWidget_picks")
        self.tableWidget_picks.setColumnCount(3)
        self.tableWidget_picks.horizontalHeader().setVisible(True)
        self.tableWidget_picks.horizontalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_3.addWidget(self.tableWidget_picks)

        self.widget_2 = QWidget(self.VanalisisBox)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_undoPick = QPushButton(self.widget_2)
        self.pushButton_undoPick.setObjectName(u"pushButton_undoPick")

        self.horizontalLayout_6.addWidget(self.pushButton_undoPick)

        self.pushButton_clearAll = QPushButton(self.widget_2)
        self.pushButton_clearAll.setObjectName(u"pushButton_clearAll")

        self.horizontalLayout_6.addWidget(self.pushButton_clearAll)


        self.verticalLayout_3.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.VanalisisBox)

        self.groupBox = QGroupBox(self.leftBox)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.MessageLine = QLineEdit(self.groupBox)
        self.MessageLine.setObjectName(u"MessageLine")

        self.horizontalLayout_3.addWidget(self.MessageLine)


        self.verticalLayout.addWidget(self.groupBox)


        self.horizontalLayout_4.addWidget(self.leftBox)

        self.rightBox = QGroupBox(self.mainBox)
        self.rightBox.setObjectName(u"rightBox")
        self.horizontalLayout_5 = QHBoxLayout(self.rightBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.plotLayout = QVBoxLayout()
        self.plotLayout.setObjectName(u"plotLayout")
        self.frame = QFrame(self.rightBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.plotLayout.addWidget(self.frame)


        self.horizontalLayout_5.addLayout(self.plotLayout)

        self.plotLayout2 = QVBoxLayout()
        self.plotLayout2.setObjectName(u"plotLayout2")
        self.frame_2 = QFrame(self.rightBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.plotLayout2.addWidget(self.frame_2)


        self.horizontalLayout_5.addLayout(self.plotLayout2)

        self.plotLayout3 = QVBoxLayout()
        self.plotLayout3.setObjectName(u"plotLayout3")
        self.frame_3 = QFrame(self.rightBox)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.plotLayout3.addWidget(self.frame_3)


        self.horizontalLayout_5.addLayout(self.plotLayout3)


        self.horizontalLayout_4.addWidget(self.rightBox)


        self.horizontalLayout_2.addWidget(self.mainBox)


        self.retranslateUi(NMOWidget)

        QMetaObject.connectSlotsByName(NMOWidget)
    # setupUi

    def retranslateUi(self, NMOWidget):
        NMOWidget.setWindowTitle(QCoreApplication.translate("NMOWidget", u"Form", None))
        self.DataLoadBox.setTitle(QCoreApplication.translate("NMOWidget", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label.setText(QCoreApplication.translate("NMOWidget", u"SGY -  \u0444\u0430\u0439\u043b", None))
        self.pushButton_choice.setText(QCoreApplication.translate("NMOWidget", u"\u041e\u0431\u0437\u043e\u0440", None))
        self.pushButton_load.setText(QCoreApplication.translate("NMOWidget", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.pushButton_clear.setText(QCoreApplication.translate("NMOWidget", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.label_2.setText(QCoreApplication.translate("NMOWidget", u"\u0444\u043e\u0440\u043c\u0430\u0442: .sgy / .segy", None))
        self.VanalisisBox.setTitle(QCoreApplication.translate("NMOWidget", u"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u043d\u043e\u0439 \u0430\u043d\u0430\u043b\u0438\u0437", None))
        self.pushButton_velocitySpectrum.setText(QCoreApplication.translate("NMOWidget", u"\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u043d\u043e\u0439 \u0441\u043f\u0435\u043a\u0442\u0440", None))
        self.pushButton_applyCorrections.setText(QCoreApplication.translate("NMOWidget", u"\u041f\u043e\u043f\u0440\u0430\u0432\u043a\u0438", None))
        self.pickBox.setTitle("")
        self.radioButton_pick.setText(QCoreApplication.translate("NMOWidget", u"\u0440\u0435\u0436\u0438\u043c \u043f\u0438\u043a\u0438\u0440\u043e\u0432\u043a\u0438", None))
        self.radioButton_view.setText(QCoreApplication.translate("NMOWidget", u"\u0440\u0435\u0436\u0438\u043c \u043e\u0431\u0437\u043e\u0440\u0430", None))
        ___qtablewidgetitem = self.tableWidget_picks.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("NMOWidget", u"\u2116", None));
        ___qtablewidgetitem1 = self.tableWidget_picks.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("NMOWidget", u"t (\u0441)", None));
        ___qtablewidgetitem2 = self.tableWidget_picks.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("NMOWidget", u"v (\u043c/\u0441)", None));
#if QT_CONFIG(tooltip)
        self.tableWidget_picks.setToolTip(QCoreApplication.translate("NMOWidget", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_undoPick.setText(QCoreApplication.translate("NMOWidget", u"\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u0438\u043a", None))
        self.pushButton_clearAll.setText(QCoreApplication.translate("NMOWidget", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0451", None))
        self.groupBox.setTitle(QCoreApplication.translate("NMOWidget", u"\u041e\u043a\u043d\u043e \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f", None))
        self.rightBox.setTitle("")
    # retranslateUi

