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
        self.data_set()
        self.__upgateTendMethod()

        self.openSettings.triggered.connect(self.__openSettings)
        self._comboMethod.currentIndexChanged.connect(self.__updateList)
        self._radio223.clicked.connect(self.__eventHandling)
        self._radio44.clicked.connect(self.__eventHandling)
        self._btnGenerate.clicked.connect(self.__generateDict)
        self._btnView.clicked.connect(self.__opet_liest_editor)
        self._checkBoxPayment.clicked.connect(self.__tougglePayment)

    def data_set(self):
        # print(self.restoredData['documentList'])
        pass

    def __tougglePayment(self):
        """ Переключает активность полей расчета. """
        if self._checkBoxPayment.isChecked():
            enabled = True
        else:
            enabled = False

        self.label_appSecurity.setEnabled(enabled)
        self._lineAppSecurity.setEnabled(enabled)
        self.label_contractSecurity.setEnabled(enabled)
        self._lineContractSecurity.setEnabled(enabled)
        self.label_currentPrice.setEnabled(enabled)
        self._lineCurrentPrice.setEnabled(enabled)
        self.label_period.setEnabled(enabled)
        self._linePeriod.setEnabled(enabled)
        self.label_place.setEnabled(enabled)
        self._linePlace.setEnabled(enabled)
        self.label_positionCount.setEnabled(enabled)
        self._linePositionCount.setEnabled(enabled)

    def __opet_liest_editor(self):
        """ Открывает окно оедактирования списка ссылок. """
        self.__openSettings([self.law, self._comboMethod.currentText()])
        # self.list_editor = listView.ListWiew()
        # self.list_editor.params.connect(self.__list_handler)
        # self.list_editor.show()

    def __list_handler(self, signal):
        """ сигналы из ListWiew. """
        pass

    def __upgateTendMethod(self):
        """ Подгружает способы закупок. """
        self._comboMethod.clear()
        items = self.restoredData['tenderMethodNames']
        self._comboMethod.addItems(items)

    def __eventHandling(self):
        law44 = self._radio44.isChecked()
        law223 = self._radio223.isChecked()
        self.law = "44" if law44 else "223"

        if law44 or law223:
            self._btnView.setEnabled(True)
            self.__updateList()


    def __updateList(self):
        """ Обновляет список имен. """
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
        """ Проверяет наличие прикрепляемых файлов. """
        if os.path.exists(path):
            return(True)
        else:
            return(False)

    def __generateDict(self):
        links = []
        _list = self._listDocuments
        for i in range(_list.count()):
            filename = _list.item(i)
            if filename.checkState():
                # filenames.append(filename.text())
                for doc in self.restoredData['documentList']:
                    if doc['name'] == filename.text():
                        links.append(doc['dir'])
        for doc in self.restoredData['documentList']:
            if doc['law'] == self.law:
                if doc['method'] == self._comboMethod.currentText().strip():
                    links.append(doc['dir'])

        try:
            form = {
                'law': self.law,
                'name': self._lineName.text().strip(),
                'regnumber': self._lineRegNumber.text().strip(),
                'category': self._comboCat.currentText().strip(),
                'method': self._comboMethod.currentText().strip(),
                'object': self._lineObject.text().strip(),
                'calculation': self._checkBoxPayment.isChecked(),
                'appSecurity': self._lineAppSecurity.text().strip(),
                'contractSecurity': self._lineContractSecurity.text().strip(),
                'currentPrice': self._lineCurrentPrice.text().strip(),
                'place': self._linePlace.text().strip(),
                'peiod': self._linePeriod.text().strip(),
                'positionCount': self._linePositionCount.text().strip(),
                'links': links
            }
            if self.check_form_data(form):
                msg(0, 'Пожалуйста заполните все данные формы!')
            else:
                print(form)
                pass
        except AttributeError:
            msg(0, 'Пожалуйста выберите федеральный закон!')
        # self.save = True
        # self.hide()
        # self.close()

    def check_form_data(self, form):
        for key in form:
            if form[key] == '':
                return True
            if key == 'calculation':
                if form[key] == False:
                    break

    def __openSettings(self, data=False):
        """ Открывает окно редактирования настройки """
        self.settingsform = Variables(self.restoredData)
        self.settingsform.params.connect(self.__signalHandler)
        self.settingsform.show()
        if data:
            self.settingsform.displayDesired(data)

    def __signalHandler(self, signal):
        """ Получает сигнал из настроек. """
        if signal:
            self.__updateList()

    def getLinks(self):
        """ Возвращает список ссылок выбранных документов. """
        return ["url", "url2"]