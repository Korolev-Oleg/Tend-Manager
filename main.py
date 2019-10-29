import sys

from PyQt5 import QtWidgets
from interface.mainUi import MainUi
# from interface.variablesTab import Variables as MainUi  

from processing import dbase, linking

restored = dbase.read()

app = QtWidgets.QApplication(sys.argv) # start interface
window = MainUi(restored)
window.show()
app.exec_()
dbase.save(restored)
form = window.getLinks() # get data form
print(form)
print()
print()
print()
print()
print()
# form = {'law': '44', 'name': 'НПЦ Спец.Мед.Помощи Детям ДЗМ, ГБУЗ', 'regnumber': '0373200034819000117', 'category': 'Бакалея', 'method': 'Аукцион', 'object': 'продуктов питания (бакалея)', 'calculation': True, 'appSecurity': '4 544.57', 'contractSecurity': '22 722.85', 'currentPrice': '454 457.05', 'place': 'город Москва, улица Авиаторов, дом 38', 'peiod': '31.12.2019', 'positionCount': '21', 'links': ['C:/Users/Huston/Pictures/26935327.gif', 'C:/Users/Huston/Pictures/minus_PNG64.png', 'C:/Users/Huston/Pictures/26935327.gif', 'C:/Users/Huston/Pictures/minus_PNG64.png']}

documents = restored['documentList']
static_files = linking.make_static_srcs(documents, form)
dynamic_files = form['links']
dist = linking.make_dist(restored, form)
payment = restored['general']['paymentPath']
linking.push_files(dist, static_files, dynamic_files, payment)

dbase.save(restored)