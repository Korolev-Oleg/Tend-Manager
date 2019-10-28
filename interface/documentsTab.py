import sys  
import os

from PyQt5          import QtCore
from PyQt5.QtCore   import pyqtSignal
from PyQt5          import QtWidgets as Qtw
from win32api       import MessageBox as msg

from interface.ui   import settingsForm
from interface.ui   import editForm

class DocumentsTab(Qtw.QMainWindow, settingsForm.Ui_settings):
    """ Открывает окно настроек.
        
        Keyword arguments:
            @param restoredData: list восстановленный объект настроек:
                - listDocuments -> Последовательность словарей содержащих информацию о документах
                - tenderMethodsNames -> Последовательность строк с названиями способов закупок

    """
    def __init__(self, restoredData, setView=False):
        super().__init__()
        self.setupUi(self)  # инициализация формы
        self.restoredData = restoredData
        self.__updateComboTend()   # востановление параметров формы
        self.msg = msg

        self.treeDocuments.clicked.connect(self.__toggleCheck)
        self.radio_Law44.clicked.connect(self.__eventHandling)
        self.radio_Law223.clicked.connect(self.__eventHandling)
        self.btn_pushTotree.clicked.connect(self.__pushNewItems)
        self.combo_tendMethod.currentIndexChanged.connect(self.__eventHandling)
        self.btn_removeFromtree.clicked.connect(self.__removeSelectedItem)
        self.btn_tendMethod.clicked.connect(self.__openEditForm)
        self.btn_clear.clicked.connect(self.__clearAll)

    def innerUpdate(self, combodata):
        # self.__toggleCheck()
        self.__updateComboTend()
        self.__updateTreeWidget()
        self.combo_tendMethod.addItem(combodata)
        item = self.combo_tendMethod.findText(combodata)
        self.combo_tendMethod.setCurrentIndex(item)
    def save(self):
        print("save")

    def __openEditForm(self):
        """ Открывает окно редактирования объекта {tenderMethodNames}. """
        self.form = EditForm(self.restoredData)
        self.form.params.connect(self.__signalHandler)
        self.form.show()

    def __signalHandler(self, signal):
        """ Получает сигнал из EditForm о сохранении. """
        if signal:
            self.__updateComboTend()

    def __toggleCheck(self):
        """ Переключает чекбокс. """

        self.btn_removeFromtree.setEnabled(True)

        
        
        obj = self.treeDocuments.currentItem()
        try:
            count = self.treeDocuments.topLevelItemCount()
            for i in range(count):
                obj = self.treeDocuments.topLevelItem(i)
                for item in self.listDocuments:
                    if item['name'] == obj.text(0) and item['law'] == self.law:
                        if item["method"] == self.methodName:
                            if obj.checkState(2):
                                item['checked'] = True
                                print('set True')
                            else:
                                item['checked'] = False
                                print('set False')
                
        except AttributeError:
            print("atrr error")
            pass


    def __updateComboTend(self):
        """ Обновляет Combobox способов закупок. """

        self.combo_tendMethod.clear()
        listDocuments = self.restoredData['documentList']

        tenderMethodsNames = self.restoredData['tenderMethodNames']

        tenderMethodsNames.sort()

        self.listDocuments = listDocuments
        self.combo_tendMethod.addItems(tenderMethodsNames)


    def __eventHandling(self, delete=False):
        """ обрабатывает события radioBox и ComboBox. """
        law44 = self.radio_Law44.isChecked()
        law223 = self.radio_Law223.isChecked()
        self.methodName = self.combo_tendMethod.currentText()

        self.law = "44" if law44 else "223"

        if law44 or law223:
            self.btn_pushTotree.setEnabled(True)
            self.__updateTreeWidget()

        if self.treeDocuments.hasFocus():
            self.btn_removeFromtree.setEnabled(True)
        else:
            self.btn_removeFromtree.setEnabled(False)


    def __pushNewItems(self):
        """ Добавляет новый объект в {listDocuments}.. """
        text = r"Выберите файлы, необходимые для дайнной категории"
        dirs = Qtw.QFileDialog.getOpenFileNames\
               (self, text, "", r"Документы (*.*)")

        for url in dirs[0]:
            name = os.path.basename(url)

            item = {
                "checked": False,
                "name": name,
                "dir": url,
                "method": self.methodName,
                "law": self.law
            }
            
            if not self.listDocuments.count(item):
                self.listDocuments.append(item)

        self.__updateTreeWidget()

    def __removeSelectedItem(self):
        """ Удаляет выбраный в дереве элемент из {listDocuments}. """
        try:
            name = self.treeDocuments.selectedIndexes()[0].data()
        except IndexError:
            pass
        
        for item in self.listDocuments:
            try:
                if item["name"] == name and item["law"] == self.law:
                    if item["method"] == self.methodName:
                        self.listDocuments.remove(item)
            except UnboundLocalError:
                pass
        
        self.__updateTreeWidget()

    def __clearAll(self):
        """ Удаляет все элементы дерева. """
        print("clear")


    def __updateTreeWidget(self):
        """ Заполняет threeWidget из {listDocuments}. """
        _translate = QtCore.QCoreApplication.translate
        self.treeDocuments.clear()
        Qcore = QtCore.Qt

        index = 0
        for item in self.restoredData["documentList"]:
            if item['law'] == self.law and item["method"] == self.methodName:
                if item["method"] == self.methodName:
                    check = Qcore.Checked if item["checked"] else                                           Qcore.Unchecked
                    
                    item_0 = Qtw.QTreeWidgetItem(self.treeDocuments)
                    item_0.setCheckState(2, check)
                    # item_0.setFlags(Qcore.ItemIsSelectable|                                    Qcore.ItemIsDragEnabled|                                   Qcore.ItemIsEnabled)

                    self.treeDocuments.resizeColumnToContents(0)
                    self.treeDocuments.topLevelItem(index).setText(0,                   _translate ( "settings", item["name"] ))

                    index += 1

        item = self.treeDocuments.topLevelItem(0)
        self.treeDocuments.setCurrentItem(item)
        # активирует btn_clear() в зависимости от наличия элементов в дереве
        if index:
            self.btn_clear.setEnabled(True)
        else:
            self.btn_clear.setEnabled(False)

        self.__resize()

    def __resize(self):
        """ Переопределяет размер ячеек. """
        tree = self.treeDocuments
        tree.columnWidth(0)
        if tree.columnWidth(0) > 274:
            tree.setColumnWidth(0, 274)


class EditForm(Qtw.QMainWindow, editForm.Ui_editForm):
    """ Открывает диалоговое окно для заполнения tenderMethodsNames..
        
        Keyword arguments:
            methodNames -> ссылка на список способов закупок
        
    """
    params = pyqtSignal(object) # передача аргументов обратно в settings
    def __init__(self, methodNames):
        super().__init__()
        self.methodNames = methodNames['tenderMethodNames']
        self.setupUi(self)

        self.btn_pushTotree.clicked.connect(self.addItem)
        self.lineEdit.textChanged.connect(self.lineEvent)
        self.listTenderMethods.clicked.connect(self.listEvent)
        self.btn_removeFromtree.clicked.connect(self.delItem)
        self.pushButton.clicked.connect(self.__save)

        self.updateItems()

    def __save(self):
        """ отправляет сигнаал в DocumentsTab о сохранении. """
        self.params.emit(1)
        self.hide()

    def updateItems(self):
        """ Обновляет список. """
        lists = self.listTenderMethods
        lists.clear()
        self.methodNames.sort()
        lists.addItems(self.methodNames)
            
    def addItem(self):
        """ Добавляет новый item в список. """
        lists = self.listTenderMethods
        line = self.lineEdit
        text = line.text().strip()

        search = lists.findItems( text, QtCore.Qt.MatchFixedString )

        if not search:
            lists.addItem(text)
            self.methodNames.append(text)

        line.clear()
        self.updateItems()

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

    def closeEvent(self, event):
        self.params.emit(1)
        self.hide()
        event.accept()


def main(restoredData):
    import sys
    app = Qtw.QApplication(sys.argv)
    window = DocumentsTab(restoredData)
    window.show()
    app.exec_()

if __name__ == '__main__':
    restoredData = [[{'checked': True, 'name': 'uTorrent.exe', 'dir': 'C:/                       Users/Huston/Downloads/uTorrent.exe', 'method':                            'Аукцион', 'law': '44'},{'checked': False, 'name':                         'ALiBaba', 'dir': 'C:/Users/Huston/Downloads/                               uTorrent.exe', 'method':'Аукцион', 'law': '44'}],                       ["Аукцион","Конкурс"]]

    main(restoredData)
else:
    pass
    # from interface.ui import settingsForm