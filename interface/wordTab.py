import sys

from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore


from interface.documentsTab import DocumentsTab


class WordTab(DocumentsTab):
    """ Логика вкладки Word.
        
        Keyword arguments:
            @param restoredData: list
    """
    def __init__(self, restoredData):
        super().__init__(restoredData)
        self.variables = restoredData["variables"]
        self.updateComboBox(self.word_combo_default)
        self.__updateTreeWidget()

        self.line = self.word_editline
        self.field = self.word_value
        self.checkbox = self.word_chbx_default

        self.word_btn_del.clicked.connect(self.__removeItem)



        self.eventTuple = (self.word_btn_add, self.line, self.field,                              self.checkbox)

        self.triggerTuple = (self.word_value, self.checkbox, self.word_btn_add,                     self.word_combo_default, self.line)

        self.checkbox.clicked.connect(lambda: 
                                     self.triggeredCheckbox(self.triggerTuple))

        self.word_tree.clicked.connect(lambda:                                                                self.treeHasFocus(self.word_tree,                                      self.word_btn_del))

        editlineConnect = self.word_editline.textChanged.connect
        editlineConnect(lambda: self.textChangedEvent(self.eventTuple))

        valueConnect = self.word_value.textChanged.connect
        valueConnect(lambda: self.textChangedEvent(self.eventTuple))
        
        btnAddConnect = self.word_btn_add.clicked.connect
        btnAddConnect(lambda: self.addItem(self.variables["word"]))
        # self.

    def treeHasFocus(self, tree, btn):
        if tree.hasFocus():
            btn.setEnabled(True)
        else:
            btn.setEnabled(False)

    def updateComboBox(self, combo):

        for item in self.variables["default"]:
            combo.addItem(item["name"])

    def textChangedEvent(self, *args):
        """ Отслеживает изменения полей.
            
            Keyword arguments:
                @param *args -> (
                    valueEdit
                    checkbox,
                    button,
                    combo,
                    line,
                    ________
                    radio_cell,
                    radio_var
                )
        """
        """ Отслеживает изменения полей. """
        btn = args[0][0]
        line = args[0][1].text()
        field = args[0][2].toPlainText()
        checkbox = args[0][3]

        if not line.strip() == "" and not field.strip() == ""                                            or checkbox.isChecked():
            btn.setEnabled(True)
            return(True)
        else:
            btn.setEnabled(False)
            return(False)

    def triggeredCheckbox(self, *args):
        """ Переключает видимость полей.
            
            Keyword arguments:
                *args -> (
                    valueEdit
                    checkbox,
                    button,
                    combo,
                    line,
                    ________
                    radio_cell,
                    radio_var
                )
            
        """
        valueEdit = args[0][0]
        checkbox = args[0][1]
        button = args[0][2]
        combo = args[0][3]
        line = args[0][4].text()


        if checkbox.isChecked():
            combo.setEnabled(True)
            valueEdit.setEnabled(False)
            if not line.strip() == "":
                button.setEnabled(True)
        else:
            self.textChangedEvent(self.eventTuple)
            valueEdit.setEnabled(True)
            combo.setEnabled(False)


    def addItem(self, lets):
        """ Добавляет новый итем в variables["word"]. """
        checkbox = self.checkbox
        combo = self.word_combo_default
        

        if checkbox.isChecked():
            default = combo.currentText()
            value = None
        else:
            default = None
            value = self.word_value.toPlainText().strip()

        var = self.word_editline.text().strip()

        item = {
            "var": var,
            "default": default,
            "value": value
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
            lets.append(item)
        
        self.__updateTreeWidget()

    def __removeItem(self):
        """ Удаляет итем из variables["word"]. """
        wordVars = self.variables["word"]
        try:
            name = self.word_tree.selectedIndexes()[0].data()
        except IndexError:
            pass
        
        for item in wordVars:
            try:
                if item["var"] == name:
                    wordVars.remove(item)
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
            item_0 = Qtw.QTreeWidgetItem(self.word_tree)
            item_0.setFlags(Qcore.ItemIsSelectable|                                            Qcore.ItemIsDragEnabled|                                           Qcore.ItemIsEnabled)

            tree(index).setText(0, _translate("settings", item["var"]) )
            tree(index).setText(1, _translate("settings", item["value"]) )
            tree(index).setText(2, _translate("settings", item["default"]) )
            self.word_tree.resizeColumnToContents(0)