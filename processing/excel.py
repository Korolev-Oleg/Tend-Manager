import re
import win32com.client
import openpyxl

def rangeDelete(file, count, top_cell, end_cell, sheet=False):
    """ Deletes cells from xlsx with OLE COM.
            file -> str url; count -> int; top_cell -> str 'A2'; end_cell -> str 'P301'; sheet -> str
    """
    Excel = win32com.client.Dispatch("Excel.Application")

    top_indx = int(re.search(r'[0-9]+', top_cell)[0])
    end_indx = int(re.search(r'[0-9]+', end_cell)[0])
    top_char = re.search(r'[A-z]+', top_cell)[0]

    calc_rows = end_indx - (end_indx - count) + top_indx
    vrange = '%s%s:%s' % (top_char, calc_rows, end_cell)
    print(vrange)
    print(file)
    wbook = Excel.Workbooks.Open(file)
    if sheet:
        ws = wbook.Sheets(sheet)
    else:
        ws = wbook.ActiveSheet

    vrange = ws.Range(vrange)
    vrange.EntireRow.Delete()

    wbook.Save()
    wbook.Close()
    Excel.Quit()

def find_replace(link, variables):

    print(variables)

    if link.count('xlsx'):
        doc = openpyxl.open(link)
        try:
            for sheet in doc:
                for rows in sheet:
                    for cell in rows:
                        for var in variables:
                            if var['var'] == cell.value:
                                cell.value = var['val']
        except TypeError:
            pass
        doc.save(link)
    else:
        pass

def init(links, payment_path, variables, general, form):
    
    # range delete from payment 
    if payment_path:
        payment_path = payment_path.replace('/', '\\')
        count = int(form['positionCount'])

        if not general['cellTopLeft']:
            input_payment_settings()

        top_cell = general['cellTopLeft']
        end_cell = general['cellBotDn']
        sheet = general['sheetName']
        rangeDelete(payment_path, count, top_cell, end_cell, sheet)

    ex_variables = []
    for var in variables['excel']:
        ex_variables.append(var)

    for var in variables['default']:
        ex_variables.append(var)

    # replace variables
    for link in links:
        if link.count('xls'):
            find_replace(link, ex_variables)

def input_payment_settings():
    pass