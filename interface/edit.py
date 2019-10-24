import sys  
import os


from PyQt5          import QtWidgets as Qtw
from PyQt5.QtCore   import pyqtSignal
from PyQt5          import QtCore

from interface.ui import editForm


class EditForm(Qtw.QMainWindow, editForm.Ui_editForm):
    """ Открывает диалоговое окно для заполнения tenderMethodsNames. """
    
    params = pyqtSignal(object)
    def __init__(self, methodNames):
        super().__init__()
        self.methodNames = methodNames
        self.setupUi(self)

        self.btn_pushTotree.clicked.connect(self.addItem)
        self.lineEdit.textChanged.connect(self.lineEvent)
        self.listTenderMethods.clicked.connect(self.listEvent)
        self.btn_removeFromtree.clicked.connect(self.delItem)

        self.updateItems()

    def updateItems(self):
        """ Обновляет список. """

        lists = self.listTenderMethods
        lists.clear()
        lists.addItems(self.methodNames)
            
    def addItem(self):
        """ Добавляет новый item в список. """

        lists = self.listTenderMethods
        line = self.lineEdit

        search = lists.findItems( line.text(), QtCore.Qt.MatchFixedString )

        if not search:
            lists.addItem(line.text())
            self.methodNames.append(line.text())

        line.clear()
        print(self.methodNames)

    def lineEvent(self):
        """ Переключает видимость кнопок. """
     
        text = self.lineEdit.text()

        if not text.strip() == "":
            self.btn_pushTotree.setEnabled(True)
        else:
            self.btn_pushTotree.setEnabled(False)

    def listEvent(self):
        """ Включает кнопку удаления. """
        
        self.btn_removeFromtree.setEnabled(True)

    def delItem(self):
        """ Удаляет item из списка. """

        lists = self.listTenderMethods
        currentName = lists.currentItem().text()

        lists.takeItem( lists.currentRow() )

        if self.methodNames.count(currentName):
            self.methodNames.remove(currentName)