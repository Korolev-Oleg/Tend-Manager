from pywin.mfc.dialog import GetSimpleInput as _input
i = None
while i == None:
    i = _input('номер строки:', '2','Номер строки с первой позицией в расчете')
    i = _input('номер строки:', '2','Номер строки с последней позицией в расчете')

print(i)