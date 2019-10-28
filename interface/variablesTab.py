import re, sys, datetime

from PyQt5          import QtWidgets as Qtw
from PyQt5          import QtCore, QtGui
from PyQt5.QtCore   import pyqtSignal

from interface.excelTab import ExcelTab


class Variables(ExcelTab):
    """ Логика вкладки Стандартные значения.
        
        Keyword arguments:
            restoredData -> list
    """
    params = pyqtSignal(object)
    def __init__(self, restoredData, setView=False):
        ExcelTab.__init__(self, restoredData, setView)
        self.lets = restoredData["variables"]['default']
        self.__updateTreeWidget()
        self.btn_save.clicked.connect(self._save)
        self.generalInit()

    def displayDesired(self, data):
        if data[0] == '44':
            print(44)
            self.radio_Law44.setChecked(True)
            self.law = 44
        else:
            print(223)
            self.law = 223
            self.radio_Law223.setChecked(True)
        self.innerUpdate(data[1])

    def _save(self):
        self.params.emit(1)
        self.hide()

    def closeEvent(self, event):
        self.params.emit(1)
        self.hide()
        event.accept()

    def __updateTreeWidget(self):
        """ Обновляет treeWidget. """
        Qcore = QtCore.Qt
        _translate = QtCore.QCoreApplication.translate
        treetop = self.default_tree.topLevelItem
        tree = self.default_tree
        
        tree.clear()

        for index, item in enumerate(self.lets):
            item_0 = Qtw.QTreeWidgetItem(tree)
            item_0.setFlags(Qcore.ItemIsSelectable|                                            Qcore.ItemIsDragEnabled|                                           QtCore.Qt.ItemIsUserCheckable|                                     Qcore.ItemIsEnabled)
                            
            font = QtGui.QFont()
            font.setItalic(True)
            item_0.setFont(0, font)
            item_0.setFont(1, font)
            item_0.setFont(2, font)

            treetop(index).setText(0, _translate("settings", item["name"]) )
            treetop(index).setText(1, _translate("settings", item["var"]) )
            treetop(index).setText(2, _translate("settings", item["val"]) )
            tree.resizeColumnToContents(0)
            tree.resizeColumnToContents(1)

    def generalInit(self):
        def update():
            general = self.restoredData['general']
            self.projectspath.setText(general['mainPath'])
            self.paymentpath.setText(general['paymentPath'])
            self.sheetName.setText(general['sheetName'])
            self.cellTopLeft.setText(general['cellTopLeft'])
            self.cellBotDn.setText(general['cellBotDn'])

        def choseProjectpath():
            text = r"Выберите основную папку проектов"
            path = Qtw.QFileDialog.getExistingDirectory(self, text)
            self.restoredData['general']['mainPath'] = path
            update()

        def chosePaymentpath():
            text = r"Выберите файл расчета"
            path = Qtw.QFileDialog.getOpenFileName(self, text, '', r"Документы (*.xlsx)")
            print(path)
            self.restoredData['general']['paymentPath'] = path[0]
            update()

        def datasave(obj):
            sheetName = self.sheetName.text().strip()
            self.restoredData['general']['sheetName'] = sheetName
            if validateCells():
                self.msg(0, "Неверный формат ячейки")
            else:
                cellTopLeft = self.cellTopLeft.text().strip()
                self.restoredData['general']['cellTopLeft'] = cellTopLeft
                cellBotDn = self.cellBotDn.text().strip()
                self.restoredData['general']['cellBotDn'] = cellBotDn
                self.msg(0, "Готово!", "")

        def validateCells():
            cell = self.cellTopLeft.text()
            if not re.match(r'[A-Z{1,3}]{1,3}\d{1,3}', cell):
                return True
            cell = self.cellBotDn.text()
            if not re.match(r'[A-Z{1,3}]{1,3}\d{1,3}', cell):
                return True


        self.btnProjectpath.clicked.connect(choseProjectpath)
        self.btnPaymentpath.clicked.connect(chosePaymentpath)
        self.saveDataGeneral.clicked.connect(datasave)
        update()