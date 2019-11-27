import os, sys, pyperclip, win32api, win32con

from PyQt5                  import QtCore
from PyQt5                  import QtWidgets
from interface.progress     import Progress_Ui

from processing             import dbase, linking, excel, preVars, word


class Processing(QtCore.QThread):
    progress = QtCore.pyqtSignal(object)
    def __init__(self, data, parent=None):
        super(Processing, self).__init__(parent)
        form, restored, localRestored = data
        self.form = form
        self.localGeneral = localRestored['general']
        self.localRestored = localRestored
        self.restored = restored

    def save(self):
        if self.localRestored['general']['shared']:
            shared = self.localGeneral['shared']
            dbase.save(self.restored, shared)

        mainPath = self.localGeneral['mainPath']
        self.restored['general']['mainPath'] = mainPath
        dbase.save(self.restored)
        
        
    def run(self):
        form = self.form
        restored = self.restored

        self.progress.emit(('Подготовка переменных', 10))
        variables = preVars.init(restored['variables'], form)

        ### Set data
        self.progress.emit(('Подготовка путей', 20))
        general = self.localGeneral
        documents = restored['documentList']
        payment_path = general['paymentPath']
        ### make paths and pushing files
        dynamic_files = form['links']
        static_files = linking.make_static_srcs(documents, form)
        dist = linking.make_dist(self.localRestored, form) # files dist

        self.progress.emit(('Копирование документов', 30))
        links = linking.push_files(dist, static_files, dynamic_files, payment_path)

        self.progress.emit(('Подготовка расчета', 40))
        payment = dist[-1]
        excel.init(links, payment, variables, general, form)

        self.progress.emit(('Заполнение переменных', 90))

        print("Заполнение переменных")
        word.init(links, variables)
        
        print('пути')
        project_path = dist[-2]
        data_path = os.path.join(project_path, 'data')
        dbase.save(form, data_path)
        win32api.SetFileAttributes(data_path, win32con.FILE_ATTRIBUTE_HIDDEN)
        
        project_path = project_path.replace('/', '\\')
        if general['openfolder']:
            os.system('explorer "%s"' % project_path)

        if general['openpayment']:
            if payment:
                payment = payment.replace('/', '\\')
                os.system('explorer "%s"' % payment)

        complete_app = {
            'name': form['name'],
            'category': form['category'],
            'path': project_path,
        }

        print('add new completed')
        self.localRestored['completedApps'].append(complete_app)
        self.restored['completedApps'].append(complete_app)

        # путь к заявке в буфер обмена
        if self.localGeneral['windowsOnTop']:
            path = os.path.join(project_path, 'Заказчик')
            pyperclip.copy(path)
            pyperclip.paste()

        self.progress.emit(('Готово!', self.restored['completedApps']))
        self.save()

def start(self, form, restored, localGeneral):
    print('start progress')
    app_process = QtWidgets.QApplication(sys.argv)
    window = Progress_Ui(form, restored, Processing, localGeneral)
    window.show()
    app_process.exec_()