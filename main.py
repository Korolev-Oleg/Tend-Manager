from interface              import mainUi
from processing             import dbase, process

restored = dbase.read()

shared = restored['general']['shared']
if shared:
    print('SHARED')
    restored = dbase.read(shared)

form = mainUi.start(restored)
        
if form:
    process.start(form, restored)

shared = restored['general']['shared']
if shared:
    dbase.save(restored, shared)

dbase.save(restored)