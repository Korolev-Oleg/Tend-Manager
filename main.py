from interface              import mainUi
from processing             import dbase
import process

restored = dbase.read()

print(restored)
form = mainUi.start(restored)
        
if form:
    process.start(form, restored)

dbase.save(restored)