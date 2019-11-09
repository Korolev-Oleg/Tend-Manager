import re, sys, datetime

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore   import pyqtSignal, Qt

from interface.variablesTab import VariablesTab
from interface.edit import EditForm

class GeneralTab(VariablesTab):
    params = pyqtSignal(object)
    def __init__(self, restoredData, setView=False):
        VariablesTab.__init__(self, restoredData, setView)
        self.setWindowModality(Qt.ApplicationModal)
        self.lets = restoredData["variables"]['default']
        self.btn_save.clicked.connect(self._save)
        self.generalInit() # __________вкладка основные__________

        self.checkBox_openfolder.clicked.connect(self.set_openfolder)
        self.checkBox_openpayment.clicked.connect(self.set_openpayment)

    def set_openpayment(self):
        checkbox = self.checkBox_openpayment.checkState()
        if checkbox:
            self.restoredData['general']['openpayment'] = True
        else:
            self.restoredData['general']['openpayment'] = False

    def set_openfolder(self):
        checkbox = self.checkBox_openfolder.checkState()
        if checkbox:
            self.restoredData['general']['openfolder'] = True
        else:
            self.restoredData['general']['openfolder'] = False

    def displayDesired(self, data):
        if data[0] == '44':
            print(44)
            self.radio_Law44.setChecked(True)
            self.law = 44
        else:
            print(223)
            self.law = 223
            self.radio_Law223.setChecked(True)
        self.innerUpdate(data[1])

    def _save(self):
        sheetName = self.sheetName.text().strip()
        self.restoredData['general']['sheetName'] = sheetName
        if self.validateCells():
            self.msg(0, "Введите числовой номер ячейки!")
            self.tabWidget.setCurrentIndex(2)
        else:
            cellTopLeft = self.cellTopLeft.text().strip()
            self.restoredData['general']['cellTopLeft'] = cellTopLeft
            cellBotDn = self.cellBotDn.text().strip()
            self.restoredData['general']['cellBotDn'] = cellBotDn
            self.params.emit(1)
            self.hide()

    def validateCells(self):
        cell = self.cellTopLeft.text()
        ru_symbols = re.search(r'[А-я]', cell)
        en_symbols = re.search(r'[A-z]', cell)
        other = re.search(r'\W', cell)
        if ru_symbols or en_symbols:
            return True

        cell = self.cellBotDn.text()
        if ru_symbols or en_symbols:
            return True

    def closeEvent(self, event):
        self.params.emit(1)
        self.hide()
        event.accept()

    def generalInit(self):
        """ Вкладка основные."""
        def update():
            general = self.restoredData['general']
            self.projectspath.setText(general['mainPath'])
            self.paymentpath.setText(general['paymentPath'])
            self.sheetName.setText(general['sheetName'])
            self.cellTopLeft.setText(general['cellTopLeft'])
            self.cellBotDn.setText(general['cellBotDn'])
            comboDataSet()
            checkbox_data_set()

        def checkbox_data_set():
            general = self.restoredData['general']
            if general['openfolder']:
                self.checkBox_openfolder.setChecked(True)
            else:
                self.checkBox_openfolder.setChecked(False)

            if general['openpayment']:
                self.checkBox_openpayment.setChecked(True)
            else:
                self.checkBox_openpayment.setChecked(False)


        def __signalHandler(signal):
            """ Получает сигнал из EditForm о сохранении. """
            if signal:
                self.setDisabled(False)
                comboDataSet()

        def __openEditForm():
            """ Открывает окно редактирования объекта {tenderMethodNames}. """
            self.setDisabled(True)
            self.form = EditForm(self.restoredData, 1, title='Новая категория')
            self.form.params.connect(__signalHandler)
            self.form.show()

        def comboDataSet():
            self._catCombo.clear()
            self._catCombo.addItems(self.restoredData['categories'])

        def choseProjectpath():
            text = r"Выберите основную папку проектов"
            path = QFileDialog.getExistingDirectory(self, text)
            if path:
                self.restoredData['general']['mainPath'] = path
            update()

        def chosePaymentpath():
            text = r"Выберите файл расчета"
            path = QFileDialog.getOpenFileName(self, text, '', r"Документы (*.xlsx)")
            print(path[0])
            if path[0]:
                self.restoredData['general']['paymentPath'] = path[0]
            update()

        self.btnProjectpath.clicked.connect(choseProjectpath)
        self.btnPaymentpath.clicked.connect(chosePaymentpath)
        self._catComboBtn.clicked.connect(__openEditForm)
        update()