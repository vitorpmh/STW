# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mw.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_mw(object):
    def setupUi(self, mw):
        if not mw.objectName():
            mw.setObjectName(u"mw")
        mw.resize(944, 676)
        self.centralwidget = QWidget(mw)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 457, 509))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_4.addWidget(self.scrollArea)

        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 457, 509))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout_4.addWidget(self.scrollArea_2)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_class_1 = QPushButton(self.centralwidget)
        self.pb_class_1.setObjectName(u"pb_class_1")

        self.horizontalLayout.addWidget(self.pb_class_1)

        self.pb_class_2 = QPushButton(self.centralwidget)
        self.pb_class_2.setObjectName(u"pb_class_2")

        self.horizontalLayout.addWidget(self.pb_class_2)

        self.pb_class_3 = QPushButton(self.centralwidget)
        self.pb_class_3.setObjectName(u"pb_class_3")

        self.horizontalLayout.addWidget(self.pb_class_3)

        self.pb_class_4 = QPushButton(self.centralwidget)
        self.pb_class_4.setObjectName(u"pb_class_4")

        self.horizontalLayout.addWidget(self.pb_class_4)

        self.pb_class_5 = QPushButton(self.centralwidget)
        self.pb_class_5.setObjectName(u"pb_class_5")

        self.horizontalLayout.addWidget(self.pb_class_5)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pb_class_6 = QPushButton(self.centralwidget)
        self.pb_class_6.setObjectName(u"pb_class_6")

        self.horizontalLayout_2.addWidget(self.pb_class_6)

        self.pb_class_7 = QPushButton(self.centralwidget)
        self.pb_class_7.setObjectName(u"pb_class_7")

        self.horizontalLayout_2.addWidget(self.pb_class_7)

        self.pb_class_8 = QPushButton(self.centralwidget)
        self.pb_class_8.setObjectName(u"pb_class_8")

        self.horizontalLayout_2.addWidget(self.pb_class_8)

        self.pb_class_9 = QPushButton(self.centralwidget)
        self.pb_class_9.setObjectName(u"pb_class_9")

        self.horizontalLayout_2.addWidget(self.pb_class_9)

        self.pb_class_10 = QPushButton(self.centralwidget)
        self.pb_class_10.setObjectName(u"pb_class_10")

        self.horizontalLayout_2.addWidget(self.pb_class_10)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pb_erro = QPushButton(self.centralwidget)
        self.pb_erro.setObjectName(u"pb_erro")

        self.horizontalLayout_3.addWidget(self.pb_erro)

        self.pb_incerto = QPushButton(self.centralwidget)
        self.pb_incerto.setObjectName(u"pb_incerto")

        self.horizontalLayout_3.addWidget(self.pb_incerto)

        self.pb_next = QPushButton(self.centralwidget)
        self.pb_next.setObjectName(u"pb_next")

        self.horizontalLayout_3.addWidget(self.pb_next)


        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        mw.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mw)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 944, 22))
        mw.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mw)
        self.statusbar.setObjectName(u"statusbar")
        mw.setStatusBar(self.statusbar)

        self.retranslateUi(mw)

        QMetaObject.connectSlotsByName(mw)
    # setupUi

    def retranslateUi(self, mw):
        mw.setWindowTitle(QCoreApplication.translate("mw", u"Annotation Process", None))
        self.pb_class_1.setText(QCoreApplication.translate("mw", u"1", None))
        self.pb_class_2.setText(QCoreApplication.translate("mw", u"2", None))
        self.pb_class_3.setText(QCoreApplication.translate("mw", u"3", None))
        self.pb_class_4.setText(QCoreApplication.translate("mw", u"4", None))
        self.pb_class_5.setText(QCoreApplication.translate("mw", u"5", None))
        self.pb_class_6.setText(QCoreApplication.translate("mw", u"6", None))
        self.pb_class_7.setText(QCoreApplication.translate("mw", u"7", None))
        self.pb_class_8.setText(QCoreApplication.translate("mw", u"8", None))
        self.pb_class_9.setText(QCoreApplication.translate("mw", u"9", None))
        self.pb_class_10.setText(QCoreApplication.translate("mw", u"10", None))
        self.pb_erro.setText(QCoreApplication.translate("mw", u"ERRO", None))
        self.pb_incerto.setText(QCoreApplication.translate("mw", u"Incerto", None))
        self.pb_next.setText(QCoreApplication.translate("mw", u"Pr\u00f3xima Foto", None))
    # retranslateUi

