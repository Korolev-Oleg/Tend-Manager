import sys  
import os

from PyQt5          import QtCore
from PyQt5.QtCore   import pyqtSignal
from PyQt5          import QtWidgets as Qtw
from win32api       import MessageBox as msg
from win32con       import MB_OKCANCEL

from interface.ui           import mainUi
from interface.variablesTab import Variables

class MainUi(Qtw.QMainWindow, mainUi.Ui_Ui):
    def __init__(self, restoredData):
        super().__init__()
        self.setupUi(self)
        self.restoredData = restoredData
        self.__upgateTendMethod()

        self.openSettings.triggered.connect(self.__openSettings)
        self._comboMethod.currentIndexChanged.connect(self.__updateList)
        self._radio223.clicked.connect(self.__eventHandling)
        self._radio44.clicked.connect(self.__eventHandling)
        self._btnGenerate.clicked.connect(self.__generateDict)

    def __upgateTendMethod(self):
        self._comboMethod.clear()
        items = self.restoredData['tenderMethodNames']
        self._comboMethod.addItems(items)

    def __eventHandling(self):
        law44 = self._radio44.isChecked()
        law223 = self._radio223.isChecked()
        self.law = "44" if law44 else "223"

        if law44 or law223:
            self._btnAdd.setEnabled(True)
            self.__updateList()
        if self._listDocuments.hasFocus():
            self._btnDel.setEnabled(True)
        else:
            self._btnDel.setEnabled(False)

    def __updateList(self):
        _translate = QtCore.QCoreApplication.translate
        self.methodName = self._comboMethod.currentText()
        self._listDocuments.clear()
        Qcore = QtCore.Qt

        self.checkboxes = []
        index = 0
        for doc in self.restoredData['documentList']:
            if self.checkPath(doc["dir"]):
                try:
                    if doc['law'] == self.law and doc['method'] == self.methodName:
                        if not doc['checked']:
                            _item = Qtw.QListWidgetItem()
                            _item.setCheckState(Qcore.Unchecked)
                            _item.setText(doc['name'])
                            self._listDocuments.addItem(_item)

                            index += 1
                            self.checkboxes.append(_item)
                except AttributeError:
                    print("'MainUi' object has no attribute 'law'")

            else:
                text = "Файл: {}\nперемещен или удален. Указать новый файл?".format(doc['name'])

                chose = msg(0, text, "Файл ненайден", 4)

                if chose == 6:
                    # edit Path
                    text = r"Выберите файлы, необходимые для дайнной категории"
                    path = Qtw.QFileDialog.getOpenFileName\
                           (self, text, "", r"Документы (*.*)")

                    name = os.path.basename(path[0])
                    doc['dir'] = path[0]
                    doc['name'] = name
                    self.__updateList()
                else:
                    # remove link
                    self.restoredData['documentList'].remove(doc)

    def checkPath(self, path):
        """ Проверяет наличие файла. """
        if os.path.exists(path):
            return(True)
        else:
            return(False)

    def __generateDict(self):
        item = self._listDocuments.item
        print(item)
        # self.save = True
        # self.hide()
        # self.close()

    def __openSettings(self):
        """ Открывает окно редактирования настройки """
        self.form = Variables(self.restoredData)
        self.form.params.connect(self.__signalHandler)
        self.form.show()

    def __signalHandler(self, signal):
        """ Получает сигнал из настроек. """
        if signal:
            self.__updateList()

    def getLinks(self):
        """ Возвращает список ссылок выбранных документов. """
        return ["url", "url2"]