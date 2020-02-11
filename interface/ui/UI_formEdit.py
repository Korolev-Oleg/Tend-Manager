# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\FormEdit.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from interface.ui.RESOURSE import resource_path

class Ui_editForm(object):
    def setupUi(self, editForm, title='Новый элемент'):
        #######################################################################
        self._title = title  ## WRITED
        editForm.setObjectName("editForm")
        width = 307
        height = 430
        editForm.resize(width, height)
        #######################################################################
        editForm.setMinimumSize(QtCore.QSize(width, height)) ## WRITED
        editForm.setMaximumSize(QtCore.QSize(width, height)) ## WRITED
        self.centralwidget = QtWidgets.QWidget(editForm)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_pushTotree = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pushTotree.setEnabled(False)
        self.btn_pushTotree.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_pushTotree.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.btn_pushTotree.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btn_pushTotree.setText("")
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap(resource_path('add.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_pushTotree.setIcon(icon)
        self.btn_pushTotree.setObjectName("btn_pushTotree")
        self.horizontalLayout.addWidget(self.btn_pushTotree)
        self.btn_removeFromtree = QtWidgets.QPushButton(self.centralwidget)
        self.btn_removeFromtree.setEnabled(False)
        self.btn_removeFromtree.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_removeFromtree.setStyleSheet("background-color: rgba(255, 255, 255, 5);")
        self.btn_removeFromtree.setText("")
        icon1 = QtGui.QIcon()

        icon1.addPixmap(QtGui.QPixmap(resource_path('remove.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_removeFromtree.setIcon(icon1)
        self.btn_removeFromtree.setObjectName("btn_removeFromtree")
        self.horizontalLayout.addWidget(self.btn_removeFromtree)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.listTenderMethods = QtWidgets.QListWidget(self.centralwidget)
        self.listTenderMethods.setObjectName("listTenderMethods")
        self.verticalLayout.addWidget(self.listTenderMethods)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(105, 0))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        editForm.setCentralWidget(self.centralwidget)

        self.retranslateUi(editForm)
        QtCore.QMetaObject.connectSlotsByName(editForm)

    def retranslateUi(self, editForm):
        _translate = QtCore.QCoreApplication.translate
        #######################################################################
        editForm.setWindowTitle(_translate("editForm", self._title))  ## WRITED
        self.label.setText(_translate("editForm", "Наименование"))
        self.pushButton.setText(_translate("editForm", "Сохранить"))
