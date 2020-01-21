import re, pythoncom
import win32com.client
from win32api import MessageBox
import openpyxl


def rangeDelete(file, count, top_cell, end_cell, sheet=False):
    """ Deletes cells from xlsx with OLE COM.
    :param file: str url
    :param count: int
    :param top_cell: str - example 'A2'
    :param end_cell: str - example 'P301'
    :param sheet: str
    """
    pythoncom.CoInitialize()

    Excel = win32com.client.Dispatch("Excel.Application")

    xl_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
        pythoncom.IID_IDispatch, Excel)

    Excel = win32com.client.Dispatch(
        pythoncom.CoGetInterfaceAndReleaseStream(xl_id,
                                                 pythoncom.IID_IDispatch)
    )

    print(top_cell)
    top_index = int(re.search(r'[0-9]+', top_cell)[0])
    end_index = int(re.search(r'[0-9]+', end_cell)[0])
    top_char = re.search(r'[A-z]+', top_cell)[0]

    calc_rows = end_index - (end_index - count) + top_index
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
    except Exception as error:
        MessageBox(0, str(error))


# TODO Организовать сохранение ихображений
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

        top_cell = 'A%s' % general['cellTopLeft']  # добавляется буква А
        end_cell = 'A%s' % general['cellBotDn']  # добавляется буква А
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
        if link.endswith('xlsx'):
            find_replace(link, ex_variables)


def input_payment_settings():
    pass
