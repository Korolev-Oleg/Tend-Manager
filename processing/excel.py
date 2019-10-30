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

def find_replace():
    pass
