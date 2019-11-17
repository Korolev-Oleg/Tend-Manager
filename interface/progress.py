from interface.ui.progress  import Ui_Progress_Form
from PyQt5                  import QtWidgets
from PyQt5                  import QtGui
from interface.ui.RESOURSE  import resource_path

import time

class Progress_Ui(QtWidgets.QMainWindow, Ui_Progress_Form):
    def __init__(self, form, restored, Processing, localGeneral, parent=None):
        super().__init__()
        self.setupUi(self)
        self.status = 0
        self.processing = Processing(form, restored, localGeneral)
        self.processing.progress.connect(self.change_status)
        self.processing.start()
        self._set_icons()

    def _set_icons(self):
        def setup(icon, item, window=False):
            path = resource_path(icon)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(path),                  QtGui.QIcon.Normal, QtGui.QIcon.Off)
            if window:
                item.setWindowIcon(icon)
            else:
                item.setIcon(icon)

        setup('logo.ico', self, window=1)

    def change_status(self, signal):
        label, value,  = signal
        for i in range(self.status, value):
            self.progressBar.setValue(i)
            self.label.setText(str(label))
            time.sleep(0.01)
        self.status = value
        
        if value == 100:
            self.close()