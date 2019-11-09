from interface.ui.progress  import Ui_Progress_Form
from PyQt5                  import QtWidgets

import time

class Progress_Ui(QtWidgets.QMainWindow, Ui_Progress_Form):
    def __init__(self, form, restored, Processing, parent=None):
        super().__init__()
        self.setupUi(self)
        self.status = 0
        self.processing = Processing(form, restored)
        self.processing.progress.connect(self.change_status)
        self.processing.start()

    def change_status(self, signal):
        label, value,  = signal
        for i in range(self.status, value):
            self.progressBar.setValue(i)
            self.label.setText(str(label))
            time.sleep(0.01)
        self.status = value
        if value == 100:
            self.close()