# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExampleWidget.ui'
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
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_ExampleWidget(object):
    def setupUi(self, ExampleWidget):
        if not ExampleWidget.objectName():
            ExampleWidget.setObjectName(u"ExampleWidget")
        ExampleWidget.resize(621, 630)
        self.horizontalLayout = QHBoxLayout(ExampleWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ToolGB = QGroupBox(ExampleWidget)
        self.ToolGB.setObjectName(u"ToolGB")
        self.ToolGB.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(self.ToolGB)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SeismicDataGB = QGroupBox(self.ToolGB)
        self.SeismicDataGB.setObjectName(u"SeismicDataGB")
        self.verticalLayout_2 = QVBoxLayout(self.SeismicDataGB)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.SeismicDataLW = QListWidget(self.SeismicDataGB)
        self.SeismicDataLW.setObjectName(u"SeismicDataLW")

        self.verticalLayout_2.addWidget(self.SeismicDataLW)

        self.SeismicDataBtn = QPushButton(self.SeismicDataGB)
        self.SeismicDataBtn.setObjectName(u"SeismicDataBtn")

        self.verticalLayout_2.addWidget(self.SeismicDataBtn)


        self.verticalLayout.addWidget(self.SeismicDataGB)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.RunBtn = QPushButton(self.ToolGB)
        self.RunBtn.setObjectName(u"RunBtn")

        self.verticalLayout.addWidget(self.RunBtn)


        self.horizontalLayout.addWidget(self.ToolGB)

        self.frame = QFrame(ExampleWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.plotLayout = QVBoxLayout()
        self.plotLayout.setObjectName(u"plotLayout")

        self.verticalLayout_4.addLayout(self.plotLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.MessageGB = QGroupBox(self.frame)
        self.MessageGB.setObjectName(u"MessageGB")
        self.MessageGB.setMaximumSize(QSize(16777215, 75))
        self.horizontalLayout_2 = QHBoxLayout(self.MessageGB)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.MessageLine = QLineEdit(self.MessageGB)
        self.MessageLine.setObjectName(u"MessageLine")

        self.horizontalLayout_2.addWidget(self.MessageLine)

        self.MessageBtn = QPushButton(self.MessageGB)
        self.MessageBtn.setObjectName(u"MessageBtn")

        self.horizontalLayout_2.addWidget(self.MessageBtn)


        self.verticalLayout_4.addWidget(self.MessageGB)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(ExampleWidget)

        QMetaObject.connectSlotsByName(ExampleWidget)
    # setupUi

    def retranslateUi(self, ExampleWidget):
        ExampleWidget.setWindowTitle(QCoreApplication.translate("ExampleWidget", u"Form", None))
        self.ToolGB.setTitle(QCoreApplication.translate("ExampleWidget", u"\u041f\u0430\u043d\u0435\u043b\u044c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u0432", None))
        self.SeismicDataGB.setTitle(QCoreApplication.translate("ExampleWidget", u"\u041f\u043e\u0434\u0440\u0433\u0443\u0437\u043a\u0430 \u0441\u0435\u0439\u0441\u043c\u043e\u0433\u0440\u0430\u043c\u043c\u044b", None))
        self.SeismicDataBtn.setText(QCoreApplication.translate("ExampleWidget", u"\u041e\u0431\u0437\u043e\u0440", None))
        self.RunBtn.setText(QCoreApplication.translate("ExampleWidget", u"\u0417\u0430\u043f\u0443\u0441\u043a", None))
        self.MessageGB.setTitle(QCoreApplication.translate("ExampleWidget", u"\u041e\u043a\u043d\u043e \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f", None))
        self.MessageBtn.setText(QCoreApplication.translate("ExampleWidget", u"PushButton", None))
    # retranslateUi

