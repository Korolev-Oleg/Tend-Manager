# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_left.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Ui(object):
    def setupUi(self, Ui):
        Ui.setObjectName("Ui")
        Ui.resize(755, 536)
        Ui.setMinimumSize(QtCore.QSize(755, 536))
        Ui.setMaximumSize(QtCore.QSize(1000, 536))
        font = QtGui.QFont()
        font.setKerning(True)
        Ui.setFont(font)
        Ui.setWindowOpacity(1.0)
        Ui.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(Ui)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setContentsMargins(-1, 2, 0, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 27))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self._listDocuments = QtWidgets.QListWidget(self.frame_2)
        self._listDocuments.setMinimumSize(QtCore.QSize(233, 383))
        self._listDocuments.setMaximumSize(QtCore.QSize(16777215, 433))
        self._listDocuments.setObjectName("_listDocuments")
        self.verticalLayout_7.addWidget(self._listDocuments)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 4, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setEnabled(False)
        self.pushButton.setMaximumSize(QtCore.QSize(24, 16777215))
        self.pushButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("interface/icons/add.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self._btnView = QtWidgets.QPushButton(self.frame_2)
        self._btnView.setEnabled(False)
        self._btnView.setMinimumSize(QtCore.QSize(0, 0))
        self._btnView.setObjectName("_btnView")
        self.horizontalLayout_6.addWidget(self._btnView)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(12, -1, 10, -1)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, -1, 0, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 3)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.btn_open_documents = QtWidgets.QPushButton(self.frame)
        self.btn_open_documents.setEnabled(True)
        self.btn_open_documents.setMinimumSize(QtCore.QSize(46, 34))
        self.btn_open_documents.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btn_open_documents.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/arrow-right.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("../icons/display-none.ico"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.btn_open_documents.setIcon(icon1)
        self.btn_open_documents.setIconSize(QtCore.QSize(35, 35))
        self.btn_open_documents.setObjectName("btn_open_documents")
        self.gridLayout.addWidget(self.btn_open_documents, 0, 0, 2, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self._radio44 = QtWidgets.QRadioButton(self.frame)
        self._radio44.setObjectName("_radio44")
        self.horizontalLayout_3.addWidget(self._radio44)
        self._radio223 = QtWidgets.QRadioButton(self.frame)
        self._radio223.setObjectName("_radio223")
        self.horizontalLayout_3.addWidget(self._radio223)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self._lineName = QtWidgets.QLineEdit(self.frame)
        self._lineName.setMinimumSize(QtCore.QSize(335, 0))
        self._lineName.setObjectName("_lineName")
        self.verticalLayout_3.addWidget(self._lineName)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self._lineRegNumber = QtWidgets.QLineEdit(self.frame)
        self._lineRegNumber.setObjectName("_lineRegNumber")
        self.verticalLayout_3.addWidget(self._lineRegNumber)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_2.addWidget(self.label_15)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self._comboCat = QtWidgets.QComboBox(self.frame)
        self._comboCat.setEditable(True)
        self._comboCat.setObjectName("_comboCat")
        self.horizontalLayout.addWidget(self._comboCat)
        self._comboMethod = QtWidgets.QComboBox(self.frame)
        self._comboMethod.setEditable(True)
        self._comboMethod.setObjectName("_comboMethod")
        self.horizontalLayout.addWidget(self._comboMethod)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self._lineObject = QtWidgets.QLineEdit(self.frame)
        self._lineObject.setObjectName("_lineObject")
        self.verticalLayout_3.addWidget(self._lineObject)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 17, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self._checkBoxPayment = QtWidgets.QCheckBox(self.frame)
        self._checkBoxPayment.setMinimumSize(QtCore.QSize(0, 20))
        self._checkBoxPayment.setObjectName("_checkBoxPayment")
        self.verticalLayout_6.addWidget(self._checkBoxPayment)
        self.label_appSecurity = QtWidgets.QLabel(self.frame)
        self.label_appSecurity.setEnabled(False)
        self.label_appSecurity.setObjectName("label_appSecurity")
        self.verticalLayout_6.addWidget(self.label_appSecurity)
        self._lineAppSecurity = QtWidgets.QLineEdit(self.frame)
        self._lineAppSecurity.setEnabled(False)
        self._lineAppSecurity.setObjectName("_lineAppSecurity")
        self.verticalLayout_6.addWidget(self._lineAppSecurity)
        self.label_contractSecurity = QtWidgets.QLabel(self.frame)
        self.label_contractSecurity.setEnabled(False)
        self.label_contractSecurity.setObjectName("label_contractSecurity")
        self.verticalLayout_6.addWidget(self.label_contractSecurity)
        self._lineContractSecurity = QtWidgets.QLineEdit(self.frame)
        self._lineContractSecurity.setEnabled(False)
        self._lineContractSecurity.setObjectName("_lineContractSecurity")
        self.verticalLayout_6.addWidget(self._lineContractSecurity)
        self.label_currentPrice = QtWidgets.QLabel(self.frame)
        self.label_currentPrice.setEnabled(False)
        self.label_currentPrice.setObjectName("label_currentPrice")
        self.verticalLayout_6.addWidget(self.label_currentPrice)
        self._lineCurrentPrice = QtWidgets.QLineEdit(self.frame)
        self._lineCurrentPrice.setEnabled(False)
        self._lineCurrentPrice.setObjectName("_lineCurrentPrice")
        self.verticalLayout_6.addWidget(self._lineCurrentPrice)
        self.horizontalLayout_8.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setMinimumSize(QtCore.QSize(0, 20))
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.verticalLayout_5.addWidget(self.label_14)
        self.label_place = QtWidgets.QLabel(self.frame)
        self.label_place.setEnabled(False)
        self.label_place.setObjectName("label_place")
        self.verticalLayout_5.addWidget(self.label_place)
        self._linePlace = QtWidgets.QLineEdit(self.frame)
        self._linePlace.setEnabled(False)
        self._linePlace.setObjectName("_linePlace")
        self.verticalLayout_5.addWidget(self._linePlace)
        self.label_period = QtWidgets.QLabel(self.frame)
        self.label_period.setEnabled(False)
        self.label_period.setObjectName("label_period")
        self.verticalLayout_5.addWidget(self.label_period)
        self._linePeriod = QtWidgets.QLineEdit(self.frame)
        self._linePeriod.setEnabled(False)
        self._linePeriod.setObjectName("_linePeriod")
        self.verticalLayout_5.addWidget(self._linePeriod)
        self.label_positionCount = QtWidgets.QLabel(self.frame)
        self.label_positionCount.setEnabled(False)
        self.label_positionCount.setObjectName("label_positionCount")
        self.verticalLayout_5.addWidget(self.label_positionCount)
        self._linePositionCount = QtWidgets.QLineEdit(self.frame)
        self._linePositionCount.setEnabled(False)
        self._linePositionCount.setObjectName("_linePositionCount")
        self.verticalLayout_5.addWidget(self._linePositionCount)
        self.horizontalLayout_8.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 21, -1, 8)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self._btnGenerate = QtWidgets.QPushButton(self.frame)
        self._btnGenerate.setEnabled(False)
        self._btnGenerate.setMinimumSize(QtCore.QSize(105, 0))
        self._btnGenerate.setObjectName("_btnGenerate")
        self.horizontalLayout_4.addWidget(self._btnGenerate)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addWidget(self.frame)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setMinimumSize(QtCore.QSize(10, 500))
        self.line.setStyleSheet("background-color: rgb(44, 171, 255);\n"
"color: rgb(41, 134, 255);")
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        Ui.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Ui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 755, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setMinimumSize(QtCore.QSize(0, 0))
        self.menubar.setSizeIncrement(QtCore.QSize(0, 0))
        self.menubar.setBaseSize(QtCore.QSize(0, 0))
        self.menubar.setStyleSheet("background: ")
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.menu.setFont(font)
        self.menu.setObjectName("menu")
        self.chose_lasts = QtWidgets.QMenu(self.menu)
        self.chose_lasts.setObjectName("chose_lasts")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setGeometry(QtCore.QRect(269, 125, 135, 94))
        self.menu_2.setObjectName("menu_2")
        Ui.setMenuBar(self.menubar)
        self.openSettings = QtWidgets.QAction(Ui)
        font = QtGui.QFont()
        self.openSettings.setFont(font)
        self.openSettings.setObjectName("openSettings")
        self.actionAbout = QtWidgets.QAction(Ui)
        self.actionAbout.setObjectName("actionAbout")
        self.action0 = QtWidgets.QAction(Ui)
        self.action0.setObjectName("action0")
        self.actionClose = QtWidgets.QAction(Ui)
        self.actionClose.setObjectName("actionClose")
        self.actionLicense = QtWidgets.QAction(Ui)
        self.actionLicense.setObjectName("actionLicense")
        self.actionValidator = QtWidgets.QAction(Ui)
        self.actionValidator.setObjectName("actionValidator")
        self.actionAbout_2 = QtWidgets.QAction(Ui)
        self.actionAbout_2.setObjectName("actionAbout_2")
        self.actionLicense_2 = QtWidgets.QAction(Ui)
        self.actionLicense_2.setObjectName("actionLicense_2")
        self.menu.addAction(self.openSettings)
        self.menu.addAction(self.chose_lasts.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.actionValidator)
        self.menu.addSeparator()
        self.menu.addAction(self.actionClose)
        self.menu_2.addAction(self.actionLicense_2)
        self.menu_2.addAction(self.actionAbout_2)
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(Ui)
        QtCore.QMetaObject.connectSlotsByName(Ui)

    def retranslateUi(self, Ui):
        _translate = QtCore.QCoreApplication.translate
        Ui.setWindowTitle(_translate("Ui", "Tend Менеджер"))
        self.label_6.setText(_translate("Ui", "Документация"))
        self._btnView.setText(_translate("Ui", "Обзор..."))
        self.label.setText(_translate("Ui", "Наименование заказчика"))
        self.label_5.setText(_translate("Ui", "Федеральный закон"))
        self._radio44.setText(_translate("Ui", "№ 44"))
        self._radio223.setText(_translate("Ui", "№ 223"))
        self.label_2.setText(_translate("Ui", "Реестровый номер закупки"))
        self.label_15.setText(_translate("Ui", "Категория"))
        self.label_3.setText(_translate("Ui", "Способ закупки"))
        self.label_4.setText(_translate("Ui", "Предмет закупки"))
        self._checkBoxPayment.setText(_translate("Ui", "Создать расчет"))
        self.label_appSecurity.setText(_translate("Ui", "Обеспечение заявки"))
        self.label_contractSecurity.setText(_translate("Ui", "Обеспечение контракта"))
        self.label_currentPrice.setText(_translate("Ui", "Начальная цена"))
        self.label_place.setText(_translate("Ui", "Место поставки"))
        self.label_period.setText(_translate("Ui", "Срок поставки"))
        self.label_positionCount.setText(_translate("Ui", "Количество позиций"))
        self._btnGenerate.setText(_translate("Ui", "Создать"))
        self.menu.setTitle(_translate("Ui", "Опции       "))
        self.chose_lasts.setTitle(_translate("Ui", "Последние"))
        self.menu_2.setTitle(_translate("Ui", "Справка"))
        self.openSettings.setText(_translate("Ui", "Настройки"))
        self.actionAbout.setText(_translate("Ui", "О программе"))
        self.action0.setText(_translate("Ui", "0"))
        self.actionClose.setText(_translate("Ui", "Выход"))
        self.actionLicense.setText(_translate("Ui", "Лицензия"))
        self.actionValidator.setText(_translate("Ui", "Валидатор"))
        self.actionAbout_2.setText(_translate("Ui", "О программе"))
        self.actionLicense_2.setText(_translate("Ui", "Лицензия"))
