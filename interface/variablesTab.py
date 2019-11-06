import re, sys, datetime

from PyQt5.QtWidgets import  QTreeWidgetItem
from PyQt5.QtGui    import QFont 
from PyQt5.QtCore   import pyqtSignal
from PyQt5.QtCore   import QCoreApplication
from PyQt5.QtCore   import Qt
from PyQt5          import QtCore


from interface.excelTab import ExcelTab
from interface.edit import EditForm


class VariablesTab(ExcelTab):
    """ Логика вкладки Стандартные значения.
        
        Keyword arguments:
            restoredData -> list
    """
    def __init__(self, restoredData, setView=False):
        ExcelTab.__init__(self, restoredData, setView)
        self.lets = restoredData["variables"]['default']
        self.__updateTreeWidget()

    def __updateTreeWidget(self):
        """ Обновляет treeWidget. """
        Qcore = Qt
        _translate = QCoreApplication.translate
        treetop = self.default_tree.topLevelItem
        tree = self.default_tree
        
        tree.clear()

        for index, item in enumerate(self.lets):
            item_0 = QTreeWidgetItem(tree)
            item_0.setFlags(Qcore.ItemIsSelectable|                                            Qcore.ItemIsDragEnabled|                                           Qt.ItemIsUserCheckable|                                            Qcore.ItemIsEnabled)
                            
            font = QFont()
            font.setItalic(True)
            item_0.setFont(0, font)
            item_0.setFont(1, font)
            item_0.setFont(2, font)

            treetop(index).setText(0, _translate("settings", item["name"]) )
            treetop(index).setText(1, _translate("settings", item["var"]) )
            treetop(index).setText(2, _translate("settings", item["val"]) )
            tree.resizeColumnToContents(0)
            tree.resizeColumnToContents(1)