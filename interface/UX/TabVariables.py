import pyperclip
import time
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTreeWidgetItem

from interface.UX.TabExcel import ExcelTab


class VariablesTab(ExcelTab):
    """ Логика вкладки Стандартные значения.
        
        Keyword arguments:
            restoredData -> list
    """

    def __init__(self, restoredData, setView=False):
        ExcelTab.__init__(self, restoredData, setView)
        self.lets = restoredData["variables"]['default']
        self.__updateTreeWidget()
        self.default_tree.doubleClicked.connect(self.copy)

    def copy(self):
        current_item = self.default_tree.currentItem()
        pyperclip.copy(current_item.text(1))
        pyperclip.paste()

        to = time.time() + 0.2
        while time.time() < to:
            QCoreApplication.processEvents()
            current_item.setForeground(1, QBrush(QColor('#08f')))
            current_item.setForeground(0, QBrush(QColor('#08f')))

        current_item.setForeground(1, QBrush(QColor('#000')))
        current_item.setForeground(0, QBrush(QColor('#000')))

    def __updateTreeWidget(self):
        """ Обновляет treeWidget. """
        Qcore = Qt
        _translate = QCoreApplication.translate
        treetop = self.default_tree.topLevelItem
        tree = self.default_tree

        tree.clear()

        for index, item in enumerate(self.lets):
            item_0 = QTreeWidgetItem(tree)
            item_0.setFlags(
                Qcore.ItemIsSelectable | Qcore.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qcore.ItemIsEnabled)

            font = QFont()
            font.setItalic(True)
            item_0.setFont(0, font)
            item_0.setFont(1, font)
            item_0.setFont(2, font)

            treetop(index).setText(0, _translate("settings", item["name"]))
            treetop(index).setText(1, _translate("settings", item["var"]))
            treetop(index).setText(2, _translate("settings", item['value']))
            tree.resizeColumnToContents(0)
            tree.resizeColumnToContents(1)
