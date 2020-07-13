import docx
from win32api import MessageBox

from interface.UI.UI_progress  import Ui_Progress_Form
from PyQt5                  import QtWidgets
from PyQt5                  import QtGui
from PyQt5                  import QtCore

from validator.processing import preparing
from validator.processing import declination
from validator.processing import forbidden


class Validator(QtCore.QThread):
    progress = QtCore.pyqtSignal(object)
    def __init__(self, file, output=False, parent=None):
        super(Validator, self).__init__(parent)
        self.file = file
        self.output = output

    def run(self):
        if not self.output:
            self.output = self.file
            
        doc = docx.Document(self.file)

        self.progress.emit(('Подготовка документа', 10))
        preparing.init(doc)

        self.progress.emit(('Замена словосочетаний', 30))
        forbidden.search(doc)

        self.progress.emit(('Определение склонений', 50))
        declination.handling(doc)

        self.progress.emit(('Сохранение', 99))
        try:
            doc.save(self.output)
        except PermissionError:
            text = "Ошибка доступа", "Закройте %s и повторите попытку" % self.file
            get = MessageBox(0, text)
            print(get)
            
        self.progress.emit(('Готово', 'd'))