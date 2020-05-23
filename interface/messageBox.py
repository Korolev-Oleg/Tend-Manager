from PyQt5.QtWidgets import QMessageBox


def msg(flag=0, text='', title='', self=0, warning=0, information=0):
    if warning:
        print(1)
        flags = QMessageBox.Ok
        QMessageBox.warning(self, title, text, flags)

    if information:
        flags = QMessageBox.Ok
        QMessageBox.warning(self, title, text, flags)
