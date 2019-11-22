import sys

from PyQt5.QtWidgets        import QTreeWidgetItem
from PyQt5.QtWidgets        import QMessageBox
from PyQt5                  import QtCore

from interface.documentsTab import DocumentsTab


class WordTab(DocumentsTab):
    """ Логика вкладки Word.
        
        Keyword arguments:
            @param restoredData: list
    """
    def __init__(self, restoredData, setView=False):
        super().__init__(restoredData, setView)
        self.variables = restoredData["variables"]
        self.__updateTreeWidget()

        self.line = self.word_editline
        self.field = self.word_value
        self.word_btn_del.clicked.connect(self.__removeItem)
        self.word_editline.textChanged.connect(self.toggle_btn_enabled)
        self.word_value.textChanged.connect(self.__toggle_btn_enabled)
        self.word_tree.doubleClicked.connect(self._change_variable)

        self.word_tree.clicked.connect(lambda:                                                                self.tree_has_focus(self.word_tree,                                      self.word_btn_del))
        
        lets = self.variables["word"]
        tree = self.__updateTreeWidget
        value = self.word_value
        var = self.word_editline
        remove = self.__removeItem
        args = lets, tree, value, var, remove
        self.word_btn_add.clicked.connect(lambda: self.addItem(args))

    def _change_variable(self):
        variableName = self.word_tree.currentItem().text(0)
        variableValue = self.word_tree.currentItem().text(1) 
        self.word_editline.setText(str(variableName))
        self.word_value.setText(str(variableValue))

    def __toggle_btn_enabled(self):
        if self.word_editline.text() and self.word_value.toPlainText():
            self.word_btn_add.setEnabled(True)
        else:
            self.word_btn_add.setEnabled(False)


    def tree_has_focus(self, tree, btn):
        if tree.hasFocus():
            btn.setEnabled(True)
        else:
            btn.setEnabled(False)

    def addItem(self, args):
  
        """ Добавляет новый элемент в дерево.

            *args:
                lets, update_tree, value, var
        """
        lets, update_tree, value_f, var_f, remove_item = args

        var = var_f.text().strip()
        value = value_f.toPlainText().strip()

        item = {
            "var": var,
            'value': value
        }

        if len(lets) > 0:
            find = False
            for let in lets:
                if let["var"] == var:
                    find = True
                else:
                    continue
            if not find:
                lets.append(item)
            else:
                yes = 6
                text_0 = 'Переменная с именем'
                text_1 = 'уже существует.\nВнести изменения?'
                text = '%s %s %s' % (text_0, item['var'], text_1)

                self.beep()
                self.setDisabled(True)
                buttons = QMessageBox.Yes|QMessageBox.No
                chose = QMessageBox.warning(self, "Внимание", text, buttons)
                self.setDisabled(False)
                if chose == QMessageBox.Yes:
                    remove_item(item['var'])
                    lets.append(item)
        else:
            lets.append(item)
        
        value_f.setText('')
        var_f.setText('')
        update_tree()

    def __removeItem(self, name=False, lets=False):
        """ Удаляет указаный элемент из tree. """

        if not lets:
            lets = self.variables["word"]

        if not name:
            name = self.word_tree.selectedIndexes()[0].data()
        
        for item in lets:
            try:
                if item["var"] == name:
                    lets.remove(item)
            except UnboundLocalError:
                pass
        
        self.__updateTreeWidget()

    def __updateTreeWidget(self):
        """ Обновляет treeWidget. """
        Qcore = QtCore.Qt
        _translate = QtCore.QCoreApplication.translate
        tree = self.word_tree.topLevelItem
        
        self.word_tree.clear()

        for index, item in enumerate(self.variables["word"]):
            item_0 = QTreeWidgetItem(self.word_tree)
            item_0.setFlags(Qcore.ItemIsSelectable|                                            Qcore.ItemIsDragEnabled|                                           Qcore.ItemIsEnabled)

            tree(index).setText(0, _translate("settings", item["var"]) )
            tree(index).setText(1, _translate("settings", item['value']) )
            # tree(index).setText(2, _translate("settings", item["default"]) )
            self.word_tree.resizeColumnToContents(0)