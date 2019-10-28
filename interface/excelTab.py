import sys
import re

from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore

from interface.wordTab import WordTab

class ExcelTab(WordTab):
    """ Логика вкладки Excel.
        
        Keyword arguments:
            @param restoredData: list
    """
    def __init__(self, restoredData, setView=False):
        WordTab.__init__(self, restoredData, setView)
        self.updateComboBox(self.excel_combo_default)
        self.variables = restoredData["variables"]
        self.__updateTree()

        self._line = self.excel_editline
        self._field = self.excel_value
        self._checkbox = self.excel_chbx_default
        self._combo = self.excel_combo_default
        self.radCell = self.excel_radio_cell
        self.radVar = self.excel_radio_var

        eventTuple = (self.btn_add_5, self._line, self._field, self._checkbox)
        editlineConnect = self.excel_editline.textChanged.connect
        editlineConnect(lambda: self.textChangedEvent(eventTuple))

        valueConnect = self.excel_value.textChanged.connect
        valueConnect(lambda: self.textChangedEvent(eventTuple))

        triggerTuple = (self._field, self._checkbox, self.btn_add_5,                           self._combo, self._line)

        self.btn_del_5.clicked.connect(self.__removeItm)
        self.btn_add_5.clicked.connect(self.checkfields)
        self._checkbox.clicked.connect(lambda: self.triggeredCheckbox                                        (triggerTuple))

        self.excel_tree.clicked.connect(lambda: self.treeHasFocus                                             (self.excel_tree, self.btn_del_5))


    def checkfields(self):
        if not (self.radCell.isChecked() or self.radVar.isChecked()):
            self.msg(0, "Вы не указали тип переменной (Ячейка или Переменная)", "Предупреждение")
        else:
            if self.radCell.isChecked():
                value = self._line.text()
                if not re.match(r'[A-Z{1,3}]{1,3}\d{1,3}', value):
                    self.msg(0, "Проверьте правильность указанного имени ячейки, рекомендуется скопировать его из программы Excel", "Ошибка в заполнении поля ячейка Excel")
                else:
                    find = False
                    for let in self.variables['excel']:
                        if let['cell'] == value:
                            find = True
                        else:
                            continue
                    if find:
                        self.msg(0, "Ячейка уже используется")
                    else:
                        self.__addItem()
            else:
                self.__addItem()


    def __addItem(self):
        # [{'var': None, 'cell': 'A1', 'sheet': 'active', 'default': None, 'value': ''}, {'var': 'wsfesf', 'default': None, 'value': 'esf'}]
        lets = self.variables['excel']

        if self.radCell.isChecked():
            cell = self._line.text()
            var = None
        else:
            cell = None
            var = self._line.text()
        
        if self._checkbox.isChecked():
            default = self._combo.currentText().strip()
            value = None
        else:
            default = None
            value = self._field.toPlainText().strip()
        
        item = {
            'var': var,
            "cell": cell,
            'sheet': self.excel_combo_sheet.currentText(),
            'default': default,
            'value': value
        }

        if self.radCell.isChecked():
            condition = "var"
            required = cell
        else:
            condition = "cell"
            required = var

        if len(lets) > 0:
            find = False
            for let in lets:
                if let[condition] == required:
                    find = True
                else:
                    continue
            if not find:
                lets.append(item)
        else:
            lets.append(item)

        self.__updateTree()

    def __removeItm(self):
        """ Удаляет итем из variables["excel"]. """
        lets = self.variables["excel"]
        try:
            name = self.excel_tree.selectedIndexes()[0].data()
            cell = self.excel_tree.selectedIndexes()[1].data()
        except IndexError:
            pass
        
        for item in lets:
            try:
                if name == "-" and item["cell"] == cell:
                    lets.remove(item)

                if item["var"] == name:
                    lets.remove(item)
            except UnboundLocalError:
                pass
        self.__updateTree()

    def __updateTree(self):
        Qcore = QtCore.Qt
        _translate = QtCore.QCoreApplication.translate
        tree = self.excel_tree.topLevelItem
        
        self.excel_tree.clear()


        for index, item in enumerate(self.variables["excel"]):
            item_0 = Qtw.QTreeWidgetItem(self.excel_tree)
            item_0.setFlags(Qcore.ItemIsSelectable|                                            Qcore.ItemIsDragEnabled|                                           Qcore.ItemIsEnabled)

            if item['default'] == None:
                value = item['value']
            else:
                value = item['default']

            if item["cell"] == None:
                cell = "-"
                var = item["var"]
            else:
                cell = item["cell"]
                var = "-"

            tree(index).setText(0, _translate("settings", var) )
            tree(index).setText(1, _translate("settings", cell) )
            tree(index).setText(2, _translate("settings", item["sheet"]) )
            tree(index).setText(3, _translate("settings", value) )
            self.excel_tree.resizeColumnToContents(0)