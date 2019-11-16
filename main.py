from interface              import mainUi
from processing             import dbase, process

restored = dbase.read()
localGeneral = restored['general']

shared = localGeneral['shared']
if shared:
    print(restored['general']['cellTopLeft'])
    print(localGeneral['cellTopLeft'])
    sharedRestored = dbase.read(localGeneral['shared'])
    form = mainUi.start(sharedRestored, localGeneral)
else:
    form = mainUi.start(restored, localGeneral)
        
if form:
    process.start(form, restored)

shared = localGeneral['shared']
if shared:
    dbase.save(sharedRestored, shared)

restored['general']['mainPath'] = localGeneral['mainPath']
dbase.save(restored)