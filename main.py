import sys

from PyQt5 import QtWidgets
from interface.mainUi import MainUi

from data import dbase

restored = dbase.read()

app = QtWidgets.QApplication(sys.argv) # start interface
window = MainUi(restored)
window.show()
app.exec_()

links = window.getLinks() # get data form
print(links)

dbase.save(restored)