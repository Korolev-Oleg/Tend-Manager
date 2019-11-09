import os, sys, re, pickle

from PyQt5.QtCore           import pyqtSignal
from PyQt5.QtCore           import QCoreApplication
from PyQt5.QtCore           import Qt    
from PyQt5                  import QtWidgets    

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
        self.__update_tend_method()
        self.__update_categories()
        self.__clean_completed_apps()
        self.__set_lastform_triggers()
        self.save = False
        self.law = False

        self._radio44.clicked.connect(self.__event_handling)
        self._radio223.clicked.connect(self.__event_handling)
        self._btnGenerate.clicked.connect(self.__generate_dict)
        self._btnView.clicked.connect(self.__opet_list_editor)
        self.openSettings.triggered.connect(self.__open_settings)
        self._checkBoxPayment.clicked.connect(self.__touggle_payment)
        self._comboMethod.currentIndexChanged.connect(self.__update_list)
    
    def __clean_completed_apps(self):
        items = self.restoredData['completedApps']
        for item in items:
            if not os.path.exists(item['path']):
                items.remove(item)

    def __check_init_paths(self):
        """ Проверяет наличие путей к файлу расчета и к папке с заявками. """
        general = self.restoredData['general']
        path = os.path.exists(general['mainPath'])
        if not path:
            text = 'Выберите директорию в которой будут хранится и создаваться новые заявки'
            self.__set_general_path(general, text)
        if self._checkBoxPayment.isChecked():
            path = os.path.exists(general['paymentPath'])
            if not path:
                text = 'Выберите файл расчета в формате Excel'
                self.__set_general_path(general, text, 1)

    def __set_general_path(self, obj, text, flag=0):
        """ Обновляет ссылку на дирректорию или файл расчета в restoredData.
                obj -> {obj} link to file or path
                text -> str message
                flag -> str xlsx filter
        """
        path = ''
        self.setDisabled(True)
        msg(0, text, 'Внимание!')
        self.setDisabled(False)
        if flag:
            while not path:
                path = QFileDialog.getOpenFileName(self, text, '', r"Документы (*.xlsx; *.xls)")
            obj['paymentPath'] = path[0]
        else:
            while not path:
                path = QFileDialog.getExistingDirectory(self, text)
            obj['mainPath'] = path

    def __touggle_payment(self):
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
    
    def __update_categories(self):
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
        self.__open_settings( [self.law, self._comboMethod.currentText()] )

    def __list_handler(self, signal):
        """ сигналы из ListWiew. """
        pass

    def __update_tend_method(self):
        """ Подгружает способы закупок. """
        self._comboMethod.clear()
        items = self.restoredData['tenderMethodNames']
        self._comboMethod.addItems(items)
        self._comboMethod.setCurrentIndex(-1)

    def __event_handling(self):
        """ Обработчик радиобоксов. """
        law44 = self._radio44.isChecked()
        law223 = self._radio223.isChecked()
        self.law = "44" if law44 else "223"

        if law44 or law223:
            print(self._comboMethod.currentText())
            if self._comboMethod.currentText():
                self._btnView.setEnabled(True)
            self._btnGenerate.setEnabled(True)
            self.__update_list()

    def __check_path(self, path):
        """ Проверяет наличие прикрепляемых файлов. """
        if os.path.exists(path):
            return(True)
        else:
            return(False)

    def __update_list(self):
        """ Обновляет список имен. """
        _translate = QCoreApplication.translate
        self.methodName = self._comboMethod.currentText()
        self._listDocuments.clear()
        self.checkboxes = []

        for doc in self.restoredData['documentList']:
            if self.__check_path(doc["dir"]): # проверка наличия файла
                try:
                    if doc['law'] == self.law and doc['method'] ==                                           self.methodName:

                        if not doc['checked']:
                            check = Qt.Checked if doc['often'] >= 2 else                                    Qt.Unchecked
                            _item = QListWidgetItem()
                            _item.setCheckState(check)
                            _item.setText(doc['name'])
                            self._listDocuments.addItem(_item)

                            self.checkboxes.append(_item)

                except AttributeError:
                    print("'MainUi' object has no attribute 'law'")
            else:
                self.__update_old_path(doc)

        if self._comboMethod.currentText():
            self._btnView.setEnabled(True)
        else:
            self._btnView.setEnabled(False)
    def __update_old_path(self, doc):
        """ Обновляет путь к файлу. """

        text = "Файл: {}\nперемещен или удален. Указать новый файл?"\
                                                .format(doc['name'])
        self.setDisabled(True)
        chose = msg(0, text, "Файл ненайден", 4)
        self.setDisabled(False)
        if chose == 6:
            # edit Path
            old_path = doc['dir']
            text = r"Выберите новый файл вместо {}".format(doc['name'])

            openFile = QFileDialog.getOpenFileName
            path = openFile(self, text, "", r"Документы (*.*)")

            # проверка всего макета данных
            name = os.path.basename(path[0])
            for ex_doc in self.restoredData['documentList']:
                if ex_doc['dir'] == old_path:
                    ex_doc['dir'] = path[0]
                    ex_doc['name'] = name

            self.__update_list()
        else:
            # remove link
            self.restoredData['documentList'].remove(doc)

    def __check_new_combo_item(self, combo, data):
        """ Проверяент наличие элемента combobox в списке. """
        line = combo.currentText().strip()
        if line:
            search = combo.findText(line)
            if search == -1:
                data.append(line)

    def __chech_excel_fields(self):
        """ Проверяет заполненость полей для расчета. """
        def check_row(row):
            ru = re.search(r'[А-я]', row)
            en = re.search(r'[A-z]', row)
            ex = re.search(r'\W', row)
            if ru or en or ex:
                self.setDisabled(True)
                msg(0, 'Укажите числовой номер!')
                self.setDisabled(False)
                return True

        general = self.restoredData['general']
        if self._checkBoxPayment.isChecked():    
            if not general['cellTopLeft']:
                text = "Укажите номер строки с первой позицией в расчете\n"
                rowTop = ''
                while not rowTop:
                    title = ''
                    rowTop, ok = QInputDialog.getText(self, title, text)
                    ok
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

    def __generate_dict(self):
        """ Создает объект с данными формы. """
        
        checkNewItem = self.__check_new_combo_item
        checkNewItem(self._comboCat, self.restoredData['categories'])
        checkNewItem(self._comboMethod, self.restoredData['tenderMethodNames'])

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
                'appSecurity': get_cash( self._lineAppSecurity ),
                'contractSecurity': get_cash( self._lineContractSecurity ),
                'currentPrice': get_cash( self._lineCurrentPrice ),
                'positionCount': self._linePositionCount.text().strip(),
                'place': self._linePlace.text().strip(),
                'peiod': self._linePeriod.text().strip(),
                'links': links
            }
            self.__check_init_paths() # проверка основных путей 
            self.__chech_excel_fields() # проверка полей для расчета
            if self.__check_form_data(form):
                self.setDisabled(True)
                msg(0, 'Пожалуйста заполните все данные формы!')
                self.setDisabled(True)
            else:
                self.form = form
                self.save = True
                self.hide()
                self.close()
        except AttributeError:
            self.setDisabled(True)
            msg(0, 'Пожалуйста выберите федеральный закон!')
            self.setDisabled(False)

    def __check_form_data(self, form):
        for key in form:
            if form[key] == '':
                return True
            if key == 'calculation':
                if form[key] == False:
                    break

    def __open_settings(self, data=False):
        """ Открывает окно редактирования настроек """
        self.setDisabled(True)
        self.settingsform = GeneralTab(self.restoredData)
        self.settingsform.params.connect(self.__settings_callback)
        self.settingsform.show()
        if data:
            self.settingsform.displayDesired(data)

    def __set_lastform_triggers(self):
        """ Последние заполненные заявки. """
        apps = self.restoredData['completedApps']
        if len(apps) > 0:
            i = -1
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action0 = QAction(self)
            self.action0.setText( name )
            self.chose_lasts.addAction(self.action0)
            self.action0.triggered.connect(lambda: __get_old_form(apps[-1]['path']))
        if len(apps) > 1:
            i = -2
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action1 = QAction(self)
            self.action1.setText( name )
            self.chose_lasts.addAction(self.action1)
            self.action1.triggered.connect(lambda: __get_old_form(apps[-2]['path']))
        if len(apps) > 2:
            i = -3
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: __get_old_form(apps[-3]['path']))
        if len(apps) > 3:
            i = -4
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: __get_old_form(apps[-4]['path']))
        if len(apps) > 4:
            i = -5
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: __get_old_form(apps[-5]['path']))

        def setform(form):
            if form['law'] == '44':
                self._radio44.setChecked(True)
            else:
                self._radio223.setChecked(True)
            self.__event_handling()

            self._lineName.setText(form['name'])
            self._lineRegNumber.setText(form['regnumber'])
            self._comboCat.setCurrentText(form['category'])
            self._comboMethod.setCurrentText(form['method'])
            self._lineObject.setText(form['object'])

            if form['calculation']:
                print(form)
                self._checkBoxPayment.setChecked(True)
                self.__touggle_payment()
                self._lineAppSecurity.setText(form['appSecurity'])
                self._lineContractSecurity.setText(form['contractSecurity'])
                self._lineCurrentPrice.setText(form['currentPrice'])
                self._linePlace.setText(form['place'])
                self._linePeriod.setText(form['peiod'])
                self._linePositionCount.setText(form['positionCount'])
                self.__update_list()

        def __get_old_form(path):
            path = r'%s\data' % path
            with open(path, "rb") as file:
                form = pickle.load(file)
            setform(form)

    def __settings_callback(self, signal):
        """ Получает сигнал из настроек. """
        if signal:
            self.__update_list()
            self.__update_categories()
            self.__update_tend_method()
            self.setDisabled(False)

    def get_links(self):
        """ Возвращает список ссылок выбранных документов. """
        if self.save:
            return self.form
        return False


def start(restored):
    app = QtWidgets.QApplication(sys.argv) 
    window = MainUi(restored)
    window.show()
    app.exec_()
    form = window.get_links()
    return form