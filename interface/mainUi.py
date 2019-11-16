import os, sys, re, pickle, string

from PyQt5                  import QtCore
from PyQt5                  import QtWidgets
from win32api               import MessageBox as msg
from win32con               import MB_OKCANCEL
from win32api               import MessageBeep

from interface.ui           import mainUi
from interface.generalTab   import GeneralTab
from processing             import dbase

class MainUi(QtWidgets.QMainWindow, mainUi.Ui_Ui):
    """ Главное окно.
        
        Возвращает заполненую форму с выбранными ссылками на документы
        return:
            form -> {} law, name, regnumber, category, method, object,calculation, appSecurity, contractSecurity, currentPrice, place, peiod, positionCount, links -> []
    """
    def __init__(self, restoredData, localGeneral):
        super().__init__()
        self.setupUi(self)
        self.restoredData = restoredData
        self.localGeneral = localGeneral
        self.__update_tend_method()
        self.__update_categories()
        self.__clean_deleted_apps()
        self.__set_lastform_triggers()
        self.__set_max_field_lenght()
        self.save = False
        self.law = False
        self.attachs = []
        self.beep = MessageBeep

        self.pushButton.clicked.connect(self.add_to_attach)
        self._radio44.clicked.connect(self.__event_handling)
        self._radio223.clicked.connect(self.__event_handling)
        self._btnGenerate.clicked.connect(self.__generate_form)
        self._btnView.clicked.connect(self.__open_documentstab)
        self.openSettings.triggered.connect(self.__open_settings)
        self._checkBoxPayment.clicked.connect(self.__touggle_payment)
        self._comboMethod.currentIndexChanged.connect(self.__update_list)
        self._comboMethod.currentTextChanged.connect(self.__update_max_lenght)
        self._comboCat.currentTextChanged.connect(self.__update_max_lenght)

    def __update_max_lenght(self):
        cur_cat = self._comboCat.currentText()
        cur_meth = self._comboMethod.currentText()
        self.__set_max_field_lenght(cur_cat=cur_cat, cur_meth=cur_meth)

    def __set_max_field_lenght(self, cur_cat=False, cur_meth=False):
        pathToApps = self.localGeneral['mainPath']

        if not cur_cat:
            categories = self.restoredData['categories']
        else:
            categories = cur_cat

        if not cur_meth:
            methods = self.restoredData['tenderMethodNames']
        else:
            methods = cur_meth

        def get_bigger_len(array):
            big = array[0]
            for item in array:
                if len(item) > len(big):
                    big = item
        
            return big

        if not categories:
            categories = '-' * 20

        if not methods:
            methods = '-' * 20

        if not cur_cat and not cur_meth:
            categories = get_bigger_len(categories)
            methods = get_bigger_len(methods)

        maxLenght = 218 - ( len(pathToApps) + len(categories) + len(methods) )
        maxLenght -= 34

        print(maxLenght)
        self._lineName.setMaxLength(maxLenght)

    def add_to_attach(self):
        openFile = QtWidgets.QFileDialog.getOpenFileNames
        paths, _ = openFile(self, 'Добавить временный файл', '')

        self.attachs = paths
        self.__update_list()

    def __clean_deleted_apps(self):
        """ Отчистка удаленных заявок из списка выполненых. """
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
        MessageBeep()
        self.setDisabled(True)
        msg(0, text, 'Внимание!')
        self.setDisabled(False)
        if flag:
            while not path:
                path = QtWidgets.QFileDialog.getOpenFileName(self, text, '', r"Документы (*.xlsx; *.xls)")
            obj['paymentPath'] = path[0]
        else:
            while not path:
                path = QtWidgets.QFileDialog.getExistingDirectory(self, text)
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
        completer = QtWidgets.QCompleter( self )
        completer.setModel( self._comboCat.model() )
        completer.setCaseSensitivity( 0 )
        self._comboCat.setCompleter(completer)
        
        self._comboCat.clear()
        self._comboCat.addItems(catrgories)
        self._comboCat.setCurrentIndex(-1)

    def __open_documentstab(self):
        """ Открывает страницу настроек списка документов для текущей заявки. """

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
                self.pushButton.setEnabled(True)
            self._btnGenerate.setEnabled(True)
            self.__update_list()

    def __check_path(self, path):
        """ Проверяет наличие прикрепляемых файлов. """
        if os.path.exists(path):
            return(True)
        else:
            return(False)

    def __update_list(self):
        """ Обновляет список прикрепляемых документов. """
        _translate = QtCore.QCoreApplication.translate
        self.methodName = self._comboMethod.currentText()
        self._listDocuments.clear()
        self.checkboxes = []

        for doc in self.restoredData['documentList']:
            if self.__check_path(doc["dir"]): # проверка наличия файла
                try:
                    if doc['law'] == self.law and doc['method'] ==                                           self.methodName:

                        if not doc['checked']:
                            check = QtCore.Qt.Checked if doc['often'] >= 2                               else  QtCore.Qt.Unchecked

                            _item = QtWidgets.QListWidgetItem()
                            _item.setCheckState(check)
                            _item.setText(doc['name'])
                            self._listDocuments.addItem(_item)

                            self.checkboxes.append(_item)

                except AttributeError:
                    print("'MainUi' object has no attribute 'law'")
            else:
                self.__update_old_path(doc)
        
        for _path in self.attachs:
            name = os.path.basename(_path)
            self._listDocuments.addItem(name)

        if self._comboMethod.currentText():
            self._btnView.setEnabled(True)
            self.pushButton.setEnabled(True)
        else:
            self._btnView.setEnabled(False)
            self.pushButton.setEnabled(False)
        


    def __update_old_path(self, doc):
        """ Обновляет путь к файлу. """

        text = "Файл: {}\nперемещен или удален. Указать новый файл?"\
                                                .format(doc['name'])

        MessageBeep()
        self.setDisabled(True)
        chose = msg(0, text, "Файл ненайден", 4)
        self.setDisabled(False)
        if chose == 6:
            # edit Path
            old_path = doc['dir']
            text = r"Выберите новый файл вместо {}".format(doc['name'])

            openFile = QtWidgets.QFileDialog.getOpenFileName
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
                MessageBeep()
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
                    rowTop, ok = QtWidgets.QInputDialog.getText(self, title, text)
                    ok
                    if check_row(rowTop):
                        rowTop = ''
                general['cellTopLeft'] = rowTop

            if not general['cellBotDn']:
                text = "Укажите номер строки с последней позицией в расчете\n"
                rowBot = ''
                while not rowBot:
                    title = ''
                    rowBot, ok = QtWidgets.QInputDialog.getText(self, title, text)
                    if check_row(rowBot):
                        rowBot = ''
                    
                general['cellBotDn'] = rowBot

    def __generate_form(self):
        """ Создает объект с данными формы. """
        
        dataCategorys = self.restoredData['categories']
        dataMethods = self.restoredData['tenderMethodNames']

        check_new_item = self.__check_new_combo_item
        check_new_item( self._comboCat, dataCategorys )
        check_new_item( self._comboMethod, dataMethods )

        links = self.attachs
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
            _name = self.clear_filename( self._lineName.text().strip() )
            _regnum = self.clear_filename( self._lineRegNumber.text().strip() )
            _cat = self.clear_filename( self._comboCat.currentText().strip() )
            form = {
                'law': self.law,
                'name': _name,
                'regnumber': _regnum,
                'category': _cat,
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
                MessageBeep()
                self.setDisabled(True)
                msg(0, 'Пожалуйста заполните все данные формы!')
                self.setDisabled(False)
            else:
                self.form = form
                self.save = True
                self.hide()
                self.close()
                
        except AttributeError:
            MessageBeep()
            self.setDisabled(True)
            msg(0, 'Пожалуйста выберите федеральный закон!')
            self.setDisabled(False)

    def clear_filename(self, fileName):
        forbidden = '\\|/*<>?:"'
        for i in forbidden:
            if i in fileName:
                fileName = fileName.replace(i, '')
                
        return fileName


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
        self.settingsform = GeneralTab(self.restoredData, self.localGeneral)
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
            self.action0 = QtWidgets.QAction(self)
            self.action0.setText( name )
            self.chose_lasts.addAction(self.action0)
            self.action0.triggered.connect(lambda: __get_old_form(apps[-1]['path']))
        if len(apps) > 1:
            i = -2
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action1 = QtWidgets.QAction(self)
            self.action1.setText( name )
            self.chose_lasts.addAction(self.action1)
            self.action1.triggered.connect(lambda: __get_old_form(apps[-2]['path']))
        if len(apps) > 2:
            i = -3
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QtWidgets.QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: __get_old_form(apps[-3]['path']))
        if len(apps) > 3:
            i = -4
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QtWidgets.QAction(self)
            self.action2.setText( name )
            self.chose_lasts.addAction(self.action2)
            self.action2.triggered.connect(lambda: __get_old_form(apps[-4]['path']))
        if len(apps) > 4:
            i = -5
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            self.action2 = QtWidgets.QAction(self)
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
            form = dbase.read(path)
            setform(form)

    def __settings_callback(self, signal):
        """ Получает сигнал из настроек. """
        if signal:
            self.__update_list()
            self.__update_categories()
            self.__update_tend_method()
            self.setDisabled(False)


    def get_form(self):
        """ Возвращает заполненую форму. """
        if self.save:
            return self.form
        return False


def start(restored, localGeneral):
    """ Возвращает заполненую форму. """
    app = QtWidgets.QApplication(sys.argv) 
    window = MainUi(restored, localGeneral)
    # window = GeneralTab(restored)
    window.show()
    app.exec_()
    form = window.get_form()
    return form