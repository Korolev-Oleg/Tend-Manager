import os, sys, re, pickle

from PyQt5.QtCore           import pyqtSignal
from PyQt5.QtCore           import QCoreApplication
from PyQt5.QtCore           import Qt    
from PyQt5.QtWidgets        import QMainWindow 
from PyQt5.QtWidgets        import QFileDialog 
from PyQt5.QtWidgets        import QListWidgetItem 
from PyQt5.QtWidgets        import QInputDialog
from PyQt5.QtWidgets        import QCompleter
from PyQt5.QtWidgets        import QAction
from PyQt5.QtWidgets        import QLineEdit
from win32api               import MessageBox as msg
from win32con               import MB_OKCANCEL

from interface.ui           import mainUi
from interface.generalTab   import GeneralTab

class MainUi(QMainWindow, mainUi.Ui_Ui):
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
        self.clean_completed_apps()
        self.__set_popup_actions()
        self.save = False

        self._radio44.clicked.connect(self.__eventHandling)
        self._radio223.clicked.connect(self.__eventHandling)
        self._btnGenerate.clicked.connect(self.__generateDict)
        self._btnView.clicked.connect(self.__opet_list_editor)
        self.openSettings.triggered.connect(self.__openSettings)
        self._checkBoxPayment.clicked.connect(self.__tougglePayment)
        self._comboMethod.currentIndexChanged.connect(self.__updateList)
    
    def clean_completed_apps(self):
        items = self.restoredData['completedApps']
        for item in items:
            if not os.path.exists(item['path']):
                items.remove(item)
        print(items)

    def checkInitPaths(self):
        """ Проверяет наличие путей к файлу расчета и к папке с заявками. """
        general = self.restoredData['general']
        path = os.path.exists(general['mainPath'])
        if not path:
            text = 'выберите директорию в которой будут хранится и создаваться новые заявки'
            self.__setGeneralPath(general, text)
        if self._checkBoxPayment.isChecked():
            path = os.path.exists(general['paymentPath'])
            if not path:
                text = 'Выберите файл расчета в формате Excel'
                self.__setGeneralPath(general, text, 1)

    def __setGeneralPath(self, obj, text, flag=0):
        """ Обновляет ссылку на дирректорию или файл расчета в restoredData.
                obj -> {obj} link to file or path
                text -> str message
                flag -> str xlsx filter
        """
        path = ''
        msg(0, text, 'Внимание!')
        if flag:
            while not path:
                path = QFileDialog.getOpenFileName(self, text, '', r"Документы (*.xlsx; *.xls)")
            obj['paymentPath'] = path[0]
        else:
            while not path:
                path = QFileDialog.getExistingDirectory(self, text)
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
        completer = QCompleter( self )
        completer.setModel( self._comboCat.model() )
        completer.setCaseSensitivity( 0 )
        self._comboCat.setCompleter(completer)
        
        self._comboCat.clear()
        self._comboCat.addItems(catrgories)
        self._comboCat.setCurrentIndex(-1)

    def __opet_list_editor(self):
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
        self._comboMethod.setCurrentIndex(-1)

    def __eventHandling(self):
        """ Обработчик радиобоксов. """
        law44 = self._radio44.isChecked()
        law223 = self._radio223.isChecked()
        self.law = "44" if law44 else "223"

        if law44 or law223:
            self._btnView.setEnabled(True)
            self._btnGenerate.setEnabled(True)
            self.__updateList()

    def __updateList(self):
        """ Обновляет список имен. """
        _translate = QCoreApplication.translate
        self.methodName = self._comboMethod.currentText()
        self._listDocuments.clear()
        Qcore = Qt
        self.checkboxes = []
        index = 0
        for doc in self.restoredData['documentList']:
            if self.__checkPath(doc["dir"]):
                try:
                    if doc['law'] == self.law and doc['method'] == self.methodName:
                        if not doc['checked']:
                            check = Qcore.Checked if doc['often'] >= 2 else                                    Qcore.Unchecked
                            _item = QListWidgetItem()
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
                    path = QFileDialog.getOpenFileName\
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
        """ Проверяент наличие элемента combobox в списке. """
        line = combo.currentText().strip()
        if line:
            search = combo.findText(line)
            if search == -1:
                data.append(line)

    def chech_excel_fields(self):
        """ Проверяет заполненость полей для расчета. """
        def check_row(row):
            ru = re.search(r'[А-я]', row)
            en = re.search(r'[A-z]', row)
            ex = re.search(r'\W', row)
            if ru or en or ex:
                msg(0, 'Укажите числовой номер!')
                return True

        general = self.restoredData['general']
        if self._checkBoxPayment.isChecked():    
            if not general['cellTopLeft']:
                text = "Укажите номер строки с первой позицией в расчете\n"
                rowTop = ''
                while not rowTop:
                    title = ''
                    rowTop, ok = QInputDialog.getText(self, title, text)
                    if check_row(rowTop):
                        rowTop = ''
                general['cellTopLeft'] = rowTop

            if not general['cellBotDn']:
                text = "Укажите номер строки с последней позицией в расчете\n"
                rowBot = ''
                while not rowBot:
                    title = ''
                    rowBot, ok = QInputDialog.getText(self, title, text)
                    if check_row(rowBot):
                        rowBot = ''
                    
                general['cellBotDn'] = rowBot

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

        def get_cash(line):
            line = line.text().strip()
            if '.' in line:
                return line.replace('.', ',')
            else:
                return line
        try:
            form = {
                'law': self.law,
                'name': self._lineName.text().strip(),
                'regnumber': self._lineRegNumber.text().strip(),
                'category': self._comboCat.currentText().strip(),
                'method': self._comboMethod.currentText().strip(),
                'object': self._lineObject.text().strip(),
                'calculation': self._checkBoxPayment.isChecked(),
                'appSecurity': get_cash(self._lineAppSecurity),
                'contractSecurity': get_cash(self._lineContractSecurity),
                'currentPrice': get_cash(self._lineCurrentPrice),
                'place': self._linePlace.text().strip(),
                'peiod': self._linePeriod.text().strip(),
                'positionCount': self._linePositionCount.text().strip(),
                'links': links
            }
            self.checkInitPaths() # проверка основных путей 
            self.chech_excel_fields() # проверка полей для расчета
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
        """ Открывает окно редактирования настроек """
        self.settingsform = GeneralTab(self.restoredData)
        self.settingsform.params.connect(self.__signalHandler)
        self.settingsform.show()
        if data:
            self.settingsform.displayDesired(data)

    def __set_popup_actions(self):
        apps = self.restoredData['completedApps']
        if len(apps) > 0:
            i = -1
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action0 = QAction(self)
            self.action0.setText( name )
            self.chose_lasts.addAction(self.action0)
            self.action0.triggered.connect(lambda: getData(apps[-1]['path']))
            print(apps[i]['path'])
        if len(apps) > 1:
            i = -2
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action1 = QAction(self)
            self.action1.setText( name )
            self.chose_lasts.addAction(self.action1)
            self.action1.triggered.connect(lambda: getData(apps[-2]['path']))
            print(apps[i]['path'])
        if len(apps) > 2:
            i = -3
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: getData(apps[-3]['path']))
            print(apps[i]['path'])
        if len(apps) > 3:
            i = -4
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: getData(apps[-4]['path']))
            print(apps[i]['path'])
        if len(apps) > 4:
            i = -5
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: getData(apps[-5]['path']))
            print(apps[i]['path'])

        def setform(form):
            if form['law'] == '44':
                self._radio44.setChecked(True)
            else:
                self._radio223.setChecked(True)
            self.__eventHandling()

            self._lineName.setText(form['name'])
            self._lineRegNumber.setText(form['regnumber'])
            self._comboCat.setCurrentText(form['category'])
            self._comboMethod.setCurrentText(form['method'])
            self._lineObject.setText(form['object'])

            if form['calculation']:
                print(form)
                self._checkBoxPayment.setChecked(True)
                self.__tougglePayment()
                self._lineAppSecurity.setText(form['appSecurity'])
                self._lineContractSecurity.setText(form['contractSecurity'])
                self._lineCurrentPrice.setText(form['currentPrice'])
                self._linePlace.setText(form['place'])
                self._linePeriod.setText(form['peiod'])
                self._linePositionCount.setText(form['positionCount'])
                self.__updateList()

        def getData(path):
            path = '%s\data' % path
            with open(path, "rb") as file:
                form = pickle.load(file)
            setform(form)

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