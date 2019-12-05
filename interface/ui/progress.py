# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\progress.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Progress_Form(object):
    def setupUi(self, Progress_Form):
        Progress_Form.setObjectName("Progress_Form")
        Progress_Form.resize(392, 61)
        Progress_Form.setMinimumSize(QtCore.QSize(392, 61))
        Progress_Form.setMaximumSize(QtCore.QSize(392, 61))
        self.centralwidget = QtWidgets.QWidget(Progress_Form)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        Progress_Form.setCentralWidget(self.centralwidget)

        self.retranslateUi(Progress_Form)
        QtCore.QMetaObject.connectSlotsByName(Progress_Form)

    def retranslateUi(self, Progress_Form):
        _translate = QtCore.QCoreApplication.translate
        Progress_Form.setWindowTitle(_translate("Progress_Form", "Загрузка"))
        self.label.setText(_translate("Progress_Form", "TextLabel"))
