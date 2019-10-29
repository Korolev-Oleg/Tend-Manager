import sys  
import os

from PyQt5          import QtCore
from PyQt5          import QtWidgets
from PyQt5.QtCore   import pyqtSignal
from PyQt5          import QtWidgets as Qtw
from win32api       import MessageBox as msg
from win32con       import MB_OKCANCEL

from interface.ui           import mainUi
from interface.variablesTab import Variables

class MainUi(Qtw.QMainWindow, mainUi.Ui_Ui):
    """ Главное окно.
        
        Возвращает заполненую форму с выбранными ссылками на документы
        return:
            form -> {} law, name, regnumber, category, method, object,calculation, appSecurity, contractSecurity, currentPrice, place, peiod, positionCount, links -> []
    """
    def __init__(self, restoredData):
        super().__init__()
        self.setupUi(self)
        self.restoredData = restoredData
        self.__upgateTendMethod()
        self.__updateCategories()
        self.save = False

        self._radio44.clicked.connect(self.__eventHandling)
        self._radio223.clicked.connect(self.__eventHandling)
        self._btnGenerate.clicked.connect(self.__generateDict)
        self._btnView.clicked.connect(self.__opet_liest_editor)
        self.openSettings.triggered.connect(self.__openSettings)
        self._checkBoxPayment.clicked.connect(self.__tougglePayment)
        self._comboMethod.currentIndexChanged.connect(self.__updateList)

    def checkInitPaths(self):
        general = self.restoredData['general']
        path = os.path.exists(general['mainPath'])
        if not path:
            text = 'Выберете директорию в которой будут хранится и создаваться новые заявки'
            self.__setGeneralPath(general, text)
        if self._checkBoxPayment.isChecked():
            path = os.path.exists(general['paymentPath'])
            if not path:
                text = 'Выберете файл расчета в формате xlsx'
                self.__setGeneralPath(general, text, 1)

    def __setGeneralPath(self, obj, text, flag=0):
        """ Обновляет ссылку на дирректорию или файл расчета.
        
            Keyword arguments:
                obj -> {obj} link to file or path
                text -> str message
                flag -> str xlsx filter
        
        """
        msg(0, text, 'Внимание!')
        if flag:
            path = Qtw.QFileDialog.getOpenFileName(self, text, '', r"Документы (*.xlsx)")
            obj['paymentPath'] = path[0]
        else:
            path = Qtw.QFileDialog.getExistingDirectory(self, text)
            obj['mainPath'] = path

    def __tougglePayment(self):
        """ Переключает активность полей расчета. """
        if self._checkBoxPayment.isChecked():
            enabled = True
        else:
            enabled = False

        self._linePlace.setEnabled( enabled )
        self._linePeriod.setEnabled( enabled )
        self.label_place.setEnabled( enabled )
        self.label_period.setEnabled( enabled )
        self._lineAppSecurity.setEnabled( enabled )
        self._lineCurrentPrice.setEnabled( enabled )
        self.label_appSecurity.setEnabled( enabled )
        self._linePositionCount.setEnabled( enabled )
        self.label_currentPrice.setEnabled( enabled )
        self.label_positionCount.setEnabled( enabled )
        self._lineContractSecurity.setEnabled( enabled )
        self.label_contractSecurity.setEnabled( enabled )
    
    def __updateCategories(self):
        catrgories = self.restoredData['categories']
        catrgories.sort()

        # авто комплит
        completer = QtWidgets.QCompleter( self )
        completer.setModel( self._comboCat.model() )
        completer.setCaseSensitivity( 0 )
        self._comboCat.setCompleter(completer)
        
        self._comboCat.clear()
        self._comboCat.addItems(catrgories)

    def __opet_liest_editor(self):
        """ Открывает страницу настроек для текущей заявки. """
        self.__openSettings( [self.law, self._comboMethod.currentText()] )

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
            self._btnGenerate.setEnabled(True)
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
            if self.__checkPath(doc["dir"]):
                try:
                    if doc['law'] == self.law and doc['method'] == self.methodName:
                        if not doc['checked']:
                            check = Qcore.Checked if doc['often'] >= 2 else                                    Qcore.Unchecked
                            _item = Qtw.QListWidgetItem()
                            _item.setCheckState(check)
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

    def __checkPath(self, path):
        """ Проверяет наличие прикрепляемых файлов. """
        if os.path.exists(path):
            return(True)
        else:
            return(False)

    def __checkNewComboItem(self, combo, data):
        line = combo.currentText().strip()
        if line:
            search = self._comboCat.findText(line)
            if search == -1:
                data.append(line)

    def __generateDict(self):
        """ Создает объект с данными формы. """
        self.__checkNewComboItem(\
                    self._comboCat, self.restoredData['categories'])
        self.__checkNewComboItem(\
                    self._comboMethod, self.restoredData['tenderMethodNames'])

        links = []
        _list = self._listDocuments
        for i in range(_list.count()):
            filename = _list.item(i)
            if filename.checkState():
                for doc in self.restoredData['documentList']:
                    if doc['name'] == filename.text():
                        links.append(doc['dir']) # ссылка на файл
                        # для часто используемых
                        if doc['often'] <= 3: 
                            doc['often'] += 1

        
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
            self.checkInitPaths()
            if self.__check_form_data(form):
                msg(0, 'Пожалуйста заполните все данные формы!')
            else:
                self.form = form
                self.save = True
                self.hide()
                self.close()
        except AttributeError:
            msg(0, 'Пожалуйста выберите федеральный закон!')

    def __check_form_data(self, form):
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
            self.__updateCategories()
            self.__upgateTendMethod()

    def getLinks(self):
        """ Возвращает список ссылок выбранных документов. """
        if self.save:
            return self.form
        return False