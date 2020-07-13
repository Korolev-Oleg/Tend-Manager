from PyQt5.QtWidgets    import QTreeWidgetItem
from PyQt5.QtCore       import Qt
from PyQt5.QtCore       import QCoreApplication

from interface.UX.TabWord import WordTab

class ExcelTab(WordTab):
    """ Логика вкладки Excel.
        
        Keyword arguments:
            restoredData: list
    """
    def __init__(self, restoredData, setView=False):
        WordTab.__init__(self, restoredData, setView)
        self.variables = restoredData["variables"]
        self.__updateTree()

        self._line = self.excel_editline
        self._field = self.excel_value

        # self.btn_add_5.clicked.connect(self.__add_item)
        self.btn_del_5.clicked.connect(self.__removeItem)
        self.excel_editline.textChanged.connect(self.toggle_btn_enabled)
        self.excel_value.textChanged.connect(self.toggle_btn_enabled)
        self.excel_tree.doubleClicked.connect(self.change_variable)

        self.excel_tree.clicked.connect(lambda: self.tree_has_focus                                             (self.excel_tree, self.btn_del_5))

        lets = self.variables['excel']
        tree = self.__updateTree
        value = self.excel_value
        var = self.excel_editline
        remove = self.__removeItem
        
        args = lets, tree, value, var, remove
        self.btn_add_5.clicked.connect(lambda: self.addItem(args))

    def change_variable(self):
        variableName = self.excel_tree.currentItem().text(0)
        variableValue = self.excel_tree.currentItem().text(1) 
        self.excel_editline.setText(str(variableName))
        self.excel_value.setText(str(variableValue))

    def toggle_btn_enabled(self):
        if self.excel_editline.text() and self.excel_value.toPlainText():
            self.btn_add_5.setEnabled(True)
        else:
            self.btn_add_5.setEnabled(False)

    def __add_item(self):
        lets = self.variables['excel']
        var = self._line.text()
        value = self._field.toPlainText().strip()
        
        item = {
            'var': var,
            'value': value
        }

        if len(lets) > 0:
            find = False
            for let in lets:
                if let['var'] == var:
                    find = True
                else:
                    continue
            if not find:
                lets.append(item)
        else:
            lets.append(item)

        self.__updateTree()

    def __removeItem(self, name=False, lets=False):
        """ Удаляет указаный элемент из tree. """

        if not lets:
            lets = self.variables["excel"]

        if not name:
            try:
                name = self.excel_tree.selectedIndexes()[0].data()
            except IndexError:
                pass
            
        for item in lets:
            try:
                if item["var"] == name:
                    lets.remove(item)
            except UnboundLocalError:
                pass

        self.__updateTree()

    def __updateTree(self):
        Qcore = Qt
        _translate = QCoreApplication.translate
        tree = self.excel_tree.topLevelItem
        
        self.excel_tree.clear()


        for index, item in enumerate(self.variables["excel"]):
            item_0 = QTreeWidgetItem(self.excel_tree)
            item_0.setFlags(Qcore.ItemIsSelectable|                                            Qcore.ItemIsDragEnabled|                                           Qcore.ItemIsEnabled)

            value = item['value']
            var = item["var"]

            tree(index).setText(0, _translate("settings", var) )
            tree(index).setText(1, _translate("settings", value) )
            self.excel_tree.resizeColumnToContents(0)