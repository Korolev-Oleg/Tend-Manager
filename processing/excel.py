import re, pythoncom
import win32com.client
import openpyxl

def rangeDelete(file, count, top_cell, end_cell, sheet=False):
    """ Deletes cells from xlsx with OLE COM.
            file -> str url; count -> int; top_cell -> str 'A2'; end_cell -> str 'P301'; sheet -> str
    """
    pythoncom.CoInitialize()

    Excel = win32com.client.Dispatch("Excel.Application")

    xl_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, Excel)
    
    Excel = win32com.client.Dispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(xl_id, pythoncom.IID_IDispatch)
    )
 
    print(top_cell)
    top_indx = int(re.search(r'[0-9]+', top_cell)[0])
    end_indx = int(re.search(r'[0-9]+', end_cell)[0])
    top_char = re.search(r'[A-z]+', top_cell)[0]

    calc_rows = end_indx - (end_indx - count) + top_indx
    vrange = '%s%s:%s' % (top_char, calc_rows, end_cell)
    try:
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
    except AttributeError:
        print(
            '\n',
            'AttributeError: <unknown>.Workbooks in [excel.py line 26]',
            '\n')

def find_replace(link, variables):

    if link.count('xlsx'):
        doc = openpyxl.open(link)
        try:
            for sheet in doc:
                for rows in sheet:
                    for cell in rows:
                        for var in variables:
                            if isinstance(cell.value, str):
                                if cell.value.count(var['var']):
                                    replace = cell.value.replace(var['var'], 
                                                                var['value'])

                                    cell.value = replace
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

        top_cell = 'A%s' % general['cellTopLeft'] # добавляется буква А
        end_cell = 'A%s' % general['cellBotDn'] # добавляется буква А
        sheet = general['sheetName']
        print("\n", payment_path, "\n")
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