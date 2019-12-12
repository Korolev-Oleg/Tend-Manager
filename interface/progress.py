from interface.ui.progress  import Ui_Progress_Form
from PyQt5                  import QtWidgets
from PyQt5                  import QtGui
from PyQt5                  import QtCore
from interface.ui.RESOURSE  import resource_path

import time

class Progress_Ui(QtWidgets.QMainWindow, Ui_Progress_Form):
    signal = QtCore.pyqtSignal(object)
    def __init__(self, data, validator=False, parent=None):
        super().__init__()
        self.setupUi(self)
        self.status = 0
        self.setWindowFlags(QtCore.Qt.Sheet)

        # linking
        if not validator:
            form, restored, localRestored, Processing = data
            self.processing = Processing((form, restored, localRestored))
            self.processing.progress.connect(self.change_status)
            self.processing.start()

        # validator
        else:
            file, Validator = data
            self.validator_ex = Validator(file)
            self.validator_ex.progress.connect(self.change_status)
            self.validator_ex.start()

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
        label, value, = signal
        if isinstance(value, int):
            for i in range(self.status, value):
                self.progressBar.setValue(i)
                self.label.setText(str(label))
                time.sleep(0.01)
            self.status = value
        else:
            self.signal.emit(value)
            self.close()