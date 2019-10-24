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
    def __init__(self, restoredData):
        ExcelTab.__init__(self, restoredData)
        self.lets = restoredData["variables"]['default']
        self.__updateTreeWidget()
        self.btn_save.clicked.connect(self._save)

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