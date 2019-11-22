import sys, os


from PyQt5.QtCore       import pyqtSignal
from PyQt5.QtCore       import QCoreApplication
from PyQt5.QtCore       import Qt
from PyQt5              import QtGui

from PyQt5.QtWidgets    import QMainWindow
from PyQt5.QtWidgets    import QFileDialog
from PyQt5.QtWidgets    import QTreeWidgetItem
from PyQt5.QtWidgets    import QApplication
from win32api           import MessageBeep

from interface.ui           import settingsForm
from interface.edit         import EditForm
from interface.ui.RESOURSE  import resource_path

class DocumentsTab(QMainWindow, settingsForm.Ui_settings):
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
        self._up_combo_tnd_method()   # востановление параметров формы
        self._set_icons()
        self.beep = MessageBeep

        self.pushAllButton.clicked.connect(self.__push_general_items)
        self.treeDocuments.clicked.connect(self.__toggle_check)
        self.radio_Law44.clicked.connect(self.__event_handling)
        self.radio_Law223.clicked.connect(self.__event_handling)
        self.btn_pushTotree.clicked.connect(self.__push_new_items)
        self.choseAllCheckBox.clicked.connect(self.__chose_all)
        self.btn_removeFromtree.clicked.connect(self.__remove_selected_item)
        self.btn_tendMethod.clicked.connect(self.__open_edit_form)
        self.btn_clear.clicked.connect(self.__clear_all)
        self.combo_tendMethod.currentIndexChanged.connect                                                 (self.__event_handling)


    

    def _set_icons(self):
        def setup(icon, item, window=False):
            path = resource_path(icon)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(path),                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
            if window:
                item.setWindowIcon(icon)
            else:
                item.setIcon(icon)

        setup('add.ico', self.btn_pushTotree)
        setup('clear.ico', self.btn_clear)
        setup('docs.ico', self.pushAllButton)
        setup('remove.ico', self.btn_removeFromtree)
        setup('settings.ico', self, 1)
    

    def innerUpdate(self, combodata):
        # self.__toggle_check()
        self._up_combo_tnd_method()
        self.__update_tree_widget()
        self.combo_tendMethod.addItem(combodata)
        item = self.combo_tendMethod.findText(combodata)
        self.combo_tendMethod.setCurrentIndex(item)
    def save(self):
        print("save")

    def __open_edit_form(self):
        """ Открывает окно редактирования объекта {tenderMethodNames}. """
        self.setDisabled(True)
        self.form = EditForm(self.restoredData, title='Новый способ закупки')
        self.form.params.connect(self.__signal_handler)
        self.form.show()

    def __signal_handler(self, signal):
        """ Получает сигнал из EditForm о сохранении. """
        self.setDisabled(False)
        if signal:
            self._up_combo_tnd_method()

    def __chose_all(self):
        """ Добавляет общий список документов. """
        checkBox = self.choseAllCheckBox
        print(checkBox.checkState())
        check = Qt.Checked if checkBox.checkState() else Qt.Unchecked

        len_items = self.treeDocuments.topLevelItemCount()
        for i in range(len_items):
           current_item = self.treeDocuments.topLevelItem(i)
           current_item.setCheckState(2, check)
        self.__toggle_check()

    def __toggle_check(self):
        """ Переключает чекбокс. """
        self.btn_removeFromtree.setEnabled(True)

        obj = self.treeDocuments.currentItem()
        try:
            count = self.treeDocuments.topLevelItemCount()
            for i in range(count):
                obj = self.treeDocuments.topLevelItem(i)
                for item in self.listDocuments:
                    if item['common']:
                        if item['name'] == obj.text(0) and item['law'] ==                                               self.law:
                            if obj.checkState(2):
                                item['checked'] = True
                            else:
                                item['checked'] = False
                    else:
                        if item['name'] == obj.text(0) and item['law'] ==                                               self.law:

                            if item["method"] == self.methodName:
                                if obj.checkState(2):
                                    item['checked'] = True
                                else:
                                    item['checked'] = False
                
        except AttributeError:
            print("atrr error")
            pass


    def _up_combo_tnd_method(self):
        """ Обновляет Combobox способов закупок. """

        self.combo_tendMethod.clear()
        listDocuments = self.restoredData['documentList']

        tenderMethodsNames = self.restoredData['tenderMethodNames']

        tenderMethodsNames.sort()

        self.listDocuments = listDocuments
        self.combo_tendMethod.addItems(tenderMethodsNames)


    def __event_handling(self, delete=False):
        """ обрабатывает события radioBox и ComboBox. """
        self.choseAllCheckBox.setCheckState(Qt.Unchecked)
        law44 = self.radio_Law44.isChecked()
        law223 = self.radio_Law223.isChecked()
        self.methodName = self.combo_tendMethod.currentText()

        self.law = "44" if law44 else "223"

        if law44 or law223:
            if self.combo_tendMethod.currentText():
                self.btn_pushTotree.setEnabled(True)
                self.pushAllButton.setEnabled(True)
                self.__update_tree_widget()

        if self.treeDocuments.hasFocus():
            self.btn_removeFromtree.setEnabled(True)
        else:
            self.btn_removeFromtree.setEnabled(False)

    def __push_general_items(self):
        text = r"Выберите общие файлы для всех способов закупок"
        dirs = QFileDialog.getOpenFileNames\
               (self, text, "", r"Документы (*.*)")

        for method in self.restoredData['tenderMethodNames']:
            for url in dirs[0]:

                name = os.path.basename(url)

                item = {
                    "checked": False,
                    "name": name,
                    "dir": url,
                    "method": method,
                    "law": self.law,
                    'common': True,
                    'often': 0
                }

                if not self.listDocuments.count(item):
                    self.listDocuments.append(item)

        self.__update_tree_widget()
            
        

    def __push_new_items(self):
        """ Добавляет новый объект в {listDocuments}.. """
        text = r"Выберите файлы, необходимые для дайнной категории"
        dirs = QFileDialog.getOpenFileNames\
               (self, text, "", r"Документы (*.*)")

        for url in dirs[0]:
            name = os.path.basename(url)

            item = {
                "checked": False,
                "name": name,
                "dir": url,
                "method": self.methodName,
                "law": self.law,
                'common': False,
                'often': 0
            }
            
            if not self.listDocuments.count(item):
                self.listDocuments.append(item)

        self.__update_tree_widget()
  
    def __remove_selected_item(self):
        """ Удаляет выбраный в дереве элемент из {listDocuments}. """
        try:
            name = self.treeDocuments.selectedIndexes()[0].data()
        except IndexError:
            pass
        
        for item in self.listDocuments:
            try:
                if item['common']:
                    if item["name"] == name and item["law"] == self.law:
                        self.listDocuments.remove(item)
                else:       
                    if item["name"] == name and item["law"] == self.law:
                        if item["method"] == self.methodName:
                            self.listDocuments.remove(item)
            except UnboundLocalError:
                pass
        
        self.__update_tree_widget()

    def __clear_all(self):
        """ Удаляет все элементы дерева. """
        self.choseAllCheckBox.setCheckState(Qt.Unchecked)
        len_items = self.treeDocuments.topLevelItemCount()
        for i in range(len_items):
            self.__remove_selected_item()

    def __update_tree_widget(self):
        """ Заполняет threeWidget из {listDocuments}. """
        _translate = QCoreApplication.translate
        self.treeDocuments.clear()
        Qcore = Qt

        index = 0
        for item in self.restoredData["documentList"]:
            if item['law'] == self.law and item["method"] == self.methodName:
                if item["method"] == self.methodName:
                    check = Qcore.Checked if item["checked"] else                                           Qcore.Unchecked
                    
                    item_0 = QTreeWidgetItem(self.treeDocuments)
                    item_0.setCheckState(2, check)


                    Qbrush = QtGui.QBrush
                    if item['common']:
                        item_0.setForeground(0, Qbrush(QtGui.QColor ('#08f')))
                        item_0.setForeground(1, Qbrush(QtGui.QColor ('#08f')))

                    self.treeDocuments.resizeColumnToContents(0)
                    self.treeDocuments.topLevelItem(index).setText(0,                   _translate ( "settings", item["name"] ))

                    index += 1

        item = self.treeDocuments.topLevelItem(0)
        self.treeDocuments.setCurrentItem(item)
        # активирует btn_clear() в зависимости от наличия элементов в дереве
        if index:
            self.btn_clear.setEnabled(True)
            self.choseAllCheckBox.setEnabled(True)
        else:
            self.btn_clear.setEnabled(False)
            self.choseAllCheckBox.setEnabled(False)

        self.__resize()

    def __resize(self):
        """ Переопределяет размер ячеек. """
        tree = self.treeDocuments
        tree.columnWidth(0)
        if tree.columnWidth(0) > 274:
            tree.setColumnWidth(0, 274)



def main(restoredData):
    import sys
    app = QApplication(sys.argv)
    window = DocumentsTab(restoredData)
    window.show()
    app.exec_()

if __name__ == '__main__':
    restoredData = [[{'checked': True, 'name': 'uTorrent.exe', 'dir': 'C:/                       Users/Huston/Downloads/uTorrent.exe', 'method':                            'Аукцион', 'law': '44'},{'checked': False, 'name':                         'ALiBaba', 'dir': 'C:/Users/Huston/Downloads/                               uTorrent.exe', 'method':'Аукцион', 'law': '44'}],                       ["Аукцион","Конкурс"]]

    main(restoredData)
else:
    pass
    # from interface.ui import settingsForm