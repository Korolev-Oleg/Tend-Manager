import os
import sys
import re
import pickle
import string
import time
import math
import shutil

from PyQt5 import (QtWidgets, QtCore, QtGui, Qt)
from PyQt5.QtWidgets import QMessageBox
from win32con import MB_OKCANCEL
from win32api import MessageBeep

from interface.ui.RESOURSE import resource_path
from interface.progress import Progress_Ui
from interface.generalTab import GeneralTab
from interface import animation
from interface.ui import mainUi as UiRight
from interface.ui import mainUiLeft as UiLeft
from processing.process import Processing
from processing import dbase
from validator.validator import Validator


class MainUi(QtWidgets.QMainWindow, UiRight.Ui_Ui, UiLeft.Ui_Ui):
    """ Главное окно.
        
        Возвращает заполненую форму с выбранными ссылками на документы
        return:
            form -> {} law, name, regnumber, category, method, object,calculation, appSecurity, contractSecurity, currentPrice, place, peiod, positionCount, links -> []
    """

    def __init__(self, restoredData, localRestored):
        super().__init__()

        # self.setlock()
        # restored
        self.restoredData = restoredData
        self.localRestored = localRestored
        self.localGeneral = localRestored['general']
        self.WND_MODE = localRestored['general']['other']['wndPosition']

        # window opts
        self.set_self_flags()

        # wtf
        self.set_attributes()
        self.__update_tend_method()
        self.__update_categories()
        self.__clean_deleted_apps()  # отчистка удаленных заявок
        self.__set_lastform_triggers()
        self.__set_max_field_lenght()
        self._set_icons()
        self.init_tray()

        # connects
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
        self.btn_open_documents.clicked.connect(
            self.win_animate.popup_show_full
        )

        self.actionAbout_2.triggered.connect(self.about)
        self.actionLicense_2.triggered.connect(self.license)
        self.actionValidator.triggered.connect(self.start_validator)
        self.actionClose.triggered.connect(self.close)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.installEventFilter(self)

    def about(self):
        text = '<b>Tend Manager</b><br><br>'
        text += 'Версия: 1.0.9<br>'
        text += '2019 - 2020©'
        QMessageBox.about(self, 'О программе', text)

    def setlock(self):
        if not dbase.lock():
            QtWidgets.QMessageBox.warning(
                self,
                'Ошибка',
                'Программа уже запущена!'
            )
            sys.exit(0)

    def set_self_flags(self):

        if self.WND_MODE == 0:
            self.setupUi(self)

        if self.WND_MODE == 1:
            UiLeft.Ui_Ui.setupUi(self, self)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
            self.menu.setTitle('Опции   ')

        if self.WND_MODE == 2:
            UiRight.Ui_Ui.setupUi(self, self)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)

        self._comboMethod.setEnabled(True)

    def set_attributes(self):
        self.save = False
        self.law = False
        self.attachs = []
        self.beep = MessageBeep
        self.coords = 0, 0
        self.screen = QtWidgets.QDesktopWidget().screenGeometry(-1)

        self.win_animate = animation.Window(self, self.WND_MODE)

    def start_validator(self):
        apps = self.localRestored['completedApps']
        if apps:
            last_app_path = apps[-1]['path']
        else:
            last_app_path = os.path.abspath('.')

        file_open = QtWidgets.QFileDialog.getOpenFileName

        file, _ = file_open(self, "Проверить заявку", last_app_path, "Документ Word (*.docx)")

        if file:
            self.win_animate.popup_hide()

            data = file, Validator
            self.progress = Progress_Ui(data, validator=True)

            self.progress.show()

    def license(self):
        QMessageBox.aboutQt(self, 'Лицензия')

    def eventFilter(self, obj, event):
        self.menubar.setGeometry(QtCore.QRect(630, 0, 755, 21))
        if not event.type() == 13:
            if not event.type() == 129:
                if not event.type() == 12:
                    if not event.type() == 77:
                        # print(event.type())
                        pass

        if event.type() == 99:
            self.win_animate.popup_hide()
            return True

        elif event.type() == 3:
            if not self.win_animate.popup_status:
                self.win_animate.popup_show()
                return True
            if self.win_animate.popup_status == -1:
                self.win_animate.popup_status = 1

        elif event.type() == 10:
            if not self.win_animate.popup_status:
                if not self.win_animate.corn_status:
                    self.win_animate.popup_corner_show()
                return True
        elif event.type() == 11:
            if not self.win_animate.popup_status:
                if self.win_animate.corn_status:
                    self.win_animate.popup_corner_hide()
                return True

        return False

    def init_tray(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        path = resource_path('logo.ico')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tray_icon.setIcon(icon)
        show_action = QtWidgets.QAction("Показать", self)
        quit_action = QtWidgets.QAction("Выход", self)
        hide_action = QtWidgets.QAction("Скрыть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def _set_icons(self):
        def setup(icon, item, window=False):
            path = resource_path(icon)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)

            if window:
                item.setWindowIcon(icon)
            else:
                item.setIcon(icon)

        setup('add.ico', self.pushButton)
        setup('arrow-right.ico', self.btn_open_documents)
        setup('logo.ico', self, window=1)

    def __update_max_lenght(self):
        cur_cat = self._comboCat.currentText()
        cur_meth = self._comboMethod.currentText()
        self.__set_max_field_lenght(cur_cat=cur_cat, cur_meth=cur_meth)

    def __set_max_field_lenght(self, cur_cat=False, cur_meth=False):
        """Устанавливает максимальную длину имени заявки"""

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

        pathToApps = self.localGeneral['mainPath']
        maxLenght = 218 - (len(pathToApps) + len(categories) + len(methods))
        maxLenght -= 35
        maxLenght = maxLenght / 2

        self._lineName.setMaxLength(maxLenght)

    def add_to_attach(self):
        openFile = QtWidgets.QFileDialog.getOpenFileNames
        paths, _ = openFile(self, 'Добавить временный файл', '')

        self.attachs = paths
        self.__update_list()

    def __clean_deleted_apps(self):
        """ Отчистка удаленных заявок из списка выполненых. """
        items = self.localRestored['completedApps']
        for item in items:
            if not os.path.exists(item['path']):
                items.remove(item)

    def __check_init_paths(self):
        """ Проверяет наличие путей к файлу расчета и к папке с заявками. """

        general = self.localGeneral
        path = os.path.exists(general['mainPath'])
        if not path:
            text = 'Выберите директорию в которой будут хранится'
            text += ' и создаваться новые заявки'
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
        QMessageBox.warning(self, 'Внимание!', text, QMessageBox.Ok)
        self.setDisabled(False)

        fileOpen = QtWidgets.QFileDialog.getOpenFileName
        getExistDir = QtWidgets.QFileDialog.getExistingDirectory
        if flag:
            while not path:
                path = fileOpen(self, text, '', r"Документы (*.xlsx; *.xls)")

            obj['paymentPath'] = path[0]
        else:
            while not path:
                path = getExistDir(self, text)
            obj['mainPath'] = path

    def __touggle_payment(self):
        """ Переключает активность полей расчета. """

        if self._checkBoxPayment.isChecked():
            enabled = True
        else:
            enabled = False

        self._linePlace.setEnabled(enabled)
        self._linePeriod.setEnabled(enabled)
        self.label_place.setEnabled(enabled)
        self.label_period.setEnabled(enabled)
        self._lineAppSecurity.setEnabled(enabled)
        self._lineCurrentPrice.setEnabled(enabled)
        self.label_appSecurity.setEnabled(enabled)
        self._linePositionCount.setEnabled(enabled)
        self.label_currentPrice.setEnabled(enabled)
        self.label_positionCount.setEnabled(enabled)
        self._lineContractSecurity.setEnabled(enabled)
        self.label_contractSecurity.setEnabled(enabled)

    def __update_categories(self):
        catrgories = self.restoredData['categories']
        catrgories.sort()

        # авто комплит
        completer = QtWidgets.QCompleter(self)
        completer.setModel(self._comboCat.model())
        completer.setCaseSensitivity(0)
        self._comboCat.setCompleter(completer)

        self._comboCat.clear()
        self._comboCat.addItems(catrgories)
        self._comboCat.setCurrentIndex(-1)

    def __open_documentstab(self):
        """ Открывает страницу настроек списка документов для текущей заявки. """

        self.__open_settings([self.law, self._comboMethod.currentText()])

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
            if self._comboMethod.currentText():
                self._btnView.setEnabled(True)
                self.pushButton.setEnabled(True)
            self._btnGenerate.setEnabled(True)
            self.__update_list()

    def __check_path(self, path):
        """ Проверяет наличие прикрепляемых файлов. """

        if os.path.exists(path):
            return (True)
        else:
            return (False)

    def __update_list(self):
        """ Обновляет список прикрепляемых документов. """

        _translate = QtCore.QCoreApplication.translate
        self.methodName = self._comboMethod.currentText()
        self._listDocuments.clear()
        self.checkboxes = []

        for doc in self.restoredData['documentList']:
            if self.__check_path(doc["dir"]):  # Check file exist

                if doc['law'] == self.law and doc['method'] == self.methodName:

                    if not doc['checked']:
                        check = QtCore.Qt.Checked if doc['often'] >= 2 else QtCore.Qt.Unchecked

                        _item = QtWidgets.QListWidgetItem()
                        _item.setCheckState(check)
                        _item.setText(doc['name'])

                        self._listDocuments.addItem(_item)
                        self.checkboxes.append(_item)

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

        text = "Файл: {}\nперемещен или удален. Указать новый файл?" \
            .format(doc['name'])

        MessageBeep()
        self.setDisabled(True)
        buttons = QMessageBox.Ok | QMessageBox.No
        chose = QMessageBox.warning(self, "Файл ненайден", text, buttons)
        self.setDisabled(False)
        if chose == QMessageBox.Ok:
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

                text = 'Укажите числовой номер!'
                QMessageBox.warning(self, 'Внимание!', text, QMessageBox.Ok)
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

    def check_clone_app(self, form):
        collected_path = os.path.join(
            self.restoredData['general']['mainPath'],
            form['method'],
            form['name'],
            form['category'],
            'Торг № %s' % form['regnumber']
        )

        isExist = os.path.exists(collected_path)
        if isExist:
            replace = QtWidgets.QMessageBox.question(
                self,
                'Внимание',
                'Заявка\n%s\nУже существует\nЗаменить?' % form['name']
            )
            if replace == QtWidgets.QMessageBox.Yes:
                try:
                    shutil.rmtree(collected_path)
                    self.__clean_deleted_apps()
                    isExist = False
                except OSError:
                    QtWidgets.QMessageBox.warning(
                        self,
                        'Ошибка',
                        'Закройте папку и повторите попытку!'
                    )

        return isExist

    def __generate_form(self):
        """ Создает объект с данными формы. """

        dataCategorys = self.restoredData['categories']
        dataMethods = self.restoredData['tenderMethodNames']

        check_new_item = self.__check_new_combo_item
        check_new_item(self._comboCat, dataCategorys)
        check_new_item(self._comboMethod, dataMethods)

        links = self.attachs
        _list = self._listDocuments
        for i in range(_list.count()):
            filename = _list.item(i)
            if filename.checkState():
                for doc in self.restoredData['documentList']:
                    if doc['name'] == filename.text():
                        links.append(doc['dir'])  # ссылка на файл
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
            _name = self.clear_filename(self._lineName.text().strip())
            _regnum = self.clear_filename(self._lineRegNumber.text().strip())
            _cat = self.clear_filename(self._comboCat.currentText().strip())
            form = {
                'law': self.law,
                'name': _name,
                'regnumber': _regnum,
                'category': _cat,
                'method': self._comboMethod.currentText().strip(),
                'object': self._lineObject.text().strip(),
                'calculation': self._checkBoxPayment.isChecked(),
                'appSecurity': get_cash(self._lineAppSecurity),
                'contractSecurity': get_cash(self._lineContractSecurity),
                'currentPrice': get_cash(self._lineCurrentPrice),
                'positionCount': self._linePositionCount.text().strip(),
                'place': self._linePlace.text().strip(),
                'peiod': self._linePeriod.text().strip(),
                'links': links
            }

            self.__check_init_paths()  # проверка основных путей
            self.__chech_excel_fields()  # проверка полей для расчета

            if self.__check_form_data(form):
                MessageBeep()
                self.setDisabled(True)
                text = 'Пожалуйста заполните все данные формы!'
                QMessageBox.warning(self, 'Внимание!', text, QMessageBox.Ok)
                self.setDisabled(False)
            else:
                # Все проверки пройдены
                self.form = form
                if not self.check_clone_app(form):
                    self.start_processing()

        except AttributeError:
            MessageBeep()
            self.setDisabled(True)
            text = 'Пожалуйста выберите федеральный закон!'
            QMessageBox.warning(self, 'Внимание!', text, QMessageBox.Ok)

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
        self.win_animate.popup_hide()
        self.setDisabled(True)

        self.settingsform = GeneralTab(self.restoredData, self.localGeneral)
        self.settingsform.params.connect(self.__settings_callback)
        self.settingsform.show()
        if data:
            self.settingsform.displayDesired(data)

    def __set_lastform_triggers(self):
        """ Последние заполненные заявки. """
        apps = self.localRestored['completedApps']
        if len(apps) > 0:
            i = -1
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            try:
                self.action1.setText(name)
                self.action1.triggered.connect(lambda: __get_old_form(apps[-1]['path']))
            except AttributeError:
                self.action1 = QtWidgets.QAction(self)
                self.action1.setText(name)
                self.chose_lasts.addAction(self.action1)
                self.action1.triggered.connect(lambda: __get_old_form(apps[-1]['path']))
        if len(apps) > 1:
            i = -2
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            try:
                self.action2.setText(name)
                self.action2.triggered.connect(lambda: __get_old_form(apps[-2]['path']))
            except AttributeError:
                self.action2 = QtWidgets.QAction(self)
                self.action2.setText(name)
                self.chose_lasts.addAction(self.action2)
                self.action2.triggered.connect(lambda: __get_old_form(apps[-2]['path']))
        if len(apps) > 2:
            i = -3
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            try:
                self.action3.setText(name)
                self.action3.triggered.connect(lambda: __get_old_form(apps[-3]['path']))
            except AttributeError:
                self.action3 = QtWidgets.QAction(self)
                self.action3.setText(name)
                self.chose_lasts.addAction(self.action3)
                self.action3.triggered.connect(lambda: __get_old_form(apps[-3]['path']))
        if len(apps) > 3:
            i = -4
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            try:
                self.action4.setText(name)
                self.action4.triggered.connect(lambda: __get_old_form(apps[-4]['path']))
            except AttributeError:
                self.action4 = QtWidgets.QAction(self)
                self.action4.setText(name)
                self.chose_lasts.addAction(self.action4)
                self.action4.triggered.connect(lambda: __get_old_form(apps[-4]['path']))
        if len(apps) > 4:
            i = -5
            name = '%s (%s)' % (apps[i]['name'], apps[i]['category'])
            try:
                self.action5.setText(name)
                self.action5.triggered.connect(lambda: __get_old_form(apps[-5]['path']))
            except AttributeError:
                self.action5 = QtWidgets.QAction(self)
                self.action5.setText(name)
                self.chose_lasts.addAction(self.action5)
                self.action5.triggered.connect(lambda: __get_old_form(apps[-5]['path']))

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
            try:
                data_path = r'%s\data' % path
                form = dbase.read(data_path)
                setform(form)
                os.system('explorer "%s"' % path)

            except FileNotFoundError:
                QtWidgets.QMessageBox.warning(
                    self, 'Внимание', 'Заявка не существует'
                )
                self.__clean_deleted_apps()
                self.__set_lastform_triggers()

    def clear_form(self):
        self._radio223.setChecked(False)
        self._radio44.setChecked(False)
        self._lineName.setText('')
        self._lineRegNumber.setText('')
        self.__update_categories()
        self.__update_tend_method()
        self._lineObject.setText('')
        self._checkBoxPayment.setChecked(False)
        self._lineAppSecurity.setText('')
        self._lineContractSecurity.setText('')
        self._lineCurrentPrice.setText('')
        self._linePlace.setText('')
        self._linePeriod.setText('')
        self._linePositionCount.setText('')
        self.__touggle_payment()

    def __settings_callback(self, data):
        """ Получает сигнал из настроек. """
        restored, localGeneral = data
        if data:
            self.localGeneral = localGeneral
            self.restoredData = restored
            self.__update_list()
            self.__update_categories()
            self.__update_tend_method()
            self.setDisabled(False)
            dbase.save(self.localRestored)

    def closeEvent(self, event):
        print('close event')

        if self.localRestored['general']['shared']:
            shared = self.localGeneral['shared']
            dbase.save(self.restoredData, shared)

        mainPath = self.localGeneral['mainPath']
        self.restoredData['general']['mainPath'] = mainPath
        dbase.save(self.localRestored)

        self.tray_icon.hide()
        dbase.unlock()
        sys.exit()

    def get_form(self):
        """ Возвращает заполненую форму. """
        if self.save:
            return self.form
        return False

    def set_completted_apps(self, apps):
        self.localRestored['completedApps'] = apps
        self.__set_lastform_triggers()

    def start_processing(self):
        self.win_animate.popup_hide()

        data = self.form, self.restoredData, self.localRestored, Processing
        self.progress = Progress_Ui(data)
        self.progress.signal.connect(self.set_completted_apps)
        self.progress.show()
        self.clear_form()
        self._listDocuments.clear()
        self.attachs = []


def show(restored, localRestored):
    """ Возвращает заполненую форму. """
    app = QtWidgets.QApplication(sys.argv)
    window = MainUi(restored, localRestored)
    window.show()
    sys.exit(app.exec_())
    form = window.get_form()
    return form
