import sys, os

from PyQt5 import QtWidgets
from interface.mainUi import MainUi
# from interface.variablesTab import Variables as MainUi  

from processing import dbase, linking, excel, preVars, word

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
# form = {'law': '44', 'name': 'Маи, ФГБУ', 'regnumber': '0373100065619000154', 'category': 'Фрукты', 'method': 'Аукцион', 'object': 'продуктов питания', 'calculation': True, 'appSecurity': '10 949,65', 'contractSecurity': '10 949,65', 'currentPrice': '10 949,65', 'place': 'место', 'peiod': 'срок', 'positionCount': '50', 'links': ['C:/Users/Huston/Documents/Тендерная_Документация/WORD/Декларация СМП.doc', 'C:/Users/Huston/Documents/Тендерная_Документация/WORD/Декларация соответствия требованиям.doc', 'C:/Users/Huston/Documents/Тендерная_Документация/WORD/Заявка на участие.docx', 'C:/Users/Huston/Documents/Тендерная_Документация/WORD/Сведения об ИНН.doc', 'C:/Users/Huston/Documents/Тендерная_Документация/Декларации/Декларация 832.docx']}


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

    word.init(links, variables)

    project_path = dist[-2]
    dbase.save(form, '%s/data' % project_path)

    project_path = project_path.replace('/', '\\')
    if general['openfolder']:
        os.system('explorer %s' % project_path)

    if general['openpayment']:
        payment = payment.replace('/', '\\')
        os.system('explorer %s' % payment)

    complete_app = {
        'name': form['name'],
        'category': form['category'],
        'path': project_path,
    }

    restored['completedApps'].append(complete_app)

dbase.save(restored)