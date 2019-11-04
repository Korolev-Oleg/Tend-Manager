import sys

from PyQt5 import QtWidgets
from interface.mainUi import MainUi
# from interface.variablesTab import Variables as MainUi  

from processing import dbase, linking, excel, preVars

restored = dbase.read()

## start interface
app = QtWidgets.QApplication(sys.argv) 
window = MainUi(restored)
window.show()
app.exec_()
dbase.save(restored)
form = window.getLinks()

### Testing
# print(form, end='\n\n\n')
# form = {'law': '44', 'name': 'НПЦ Спец.Мед.Помощи Детям ДЗМ, ГБУЗ', 'regnumber': '0373200099719001010', 'category': 'Бакалея', 'method': 'Аукцион', 'object': 'продуктов питания (бакалея)', 'calculation': True, 'appSecurity': '4544,57', 'contractSecurity': '22722,85', 'currentPrice': '454457,05', 'place': 'город Москва, улица Авиаторов, дом 38', 'peiod': '31.12.2019', 'positionCount': '21', 'links': ['C:/Users/Huston/Pictures/26935327.gif', 'C:/Users/Huston/Pictures/minus_PNG64.png', 'C:/Users/Huston/Pictures/26935327.gif', 'C:/Users/Huston/Pictures/minus_PNG64.png']}


if form:
    # preparing variables
    variables = preVars.init(restored['variables'], form)

    ### Set data
    general = restored['general']
    documents = restored['documentList']
    payment_path = general['paymentPath']
    ### make paths and pushing files
    dynamic_files = form['links']
    static_files = linking.make_static_srcs(documents, form)
    dist = linking.make_dist(restored, form) # files dist
    links = linking.push_files(dist, static_files, dynamic_files, payment_path)

    payment = dist[-1]
    excel.init(links, payment, variables, general, form)

dbase.save(restored)