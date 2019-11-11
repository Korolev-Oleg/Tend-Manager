import os, sys

from PyQt5                  import QtCore
from PyQt5                  import QtWidgets
from interface.progress     import Progress_Ui

from processing             import dbase, linking, excel, preVars, word


class Processing(QtCore.QThread):
    progress = QtCore.pyqtSignal(object)
    def __init__(self, form, restored, parent=None):
        super(Processing, self).__init__(parent)
        self.form = form
        self.restored = restored
        
    def run(self):
        form = self.form
        restored = self.restored

        self.progress.emit(('Подготовка переменных', 10))
        variables = preVars.init(restored['variables'], form)

        ### Set data
        self.progress.emit(('Подготовка путей', 20))
        general = restored['general']
        documents = restored['documentList']
        payment_path = general['paymentPath']
        ### make paths and pushing files
        dynamic_files = form['links']
        static_files = linking.make_static_srcs(documents, form)
        dist = linking.make_dist(restored, form) # files dist

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
        dbase.save(form, '%s/data' % project_path)
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

        restored['completedApps'].append(complete_app)
        self.progress.emit(('Готово!', 100))
        

def start(form, restored):
    app = QtWidgets.QApplication(sys.argv)
    window = Progress_Ui(form, restored, Processing)
    window.show()
    app.exec_()