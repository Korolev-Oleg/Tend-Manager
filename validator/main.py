import docx
from win32api import MessageBox

from processing import preparing
from processing import declination
from processing import forbidden

file = 'test.docx'
output = 'output.docx'

doc = docx.Document(file)

preparing.init(doc)

forbidden.search(doc)

declination.handling(doc)


try:
    doc.save(output)
except PermissionError:
    get = MessageBox(0, "", "")
    print(get)