from interface              import mainUi
from processing             import dbase, process

if __name__ == '__main__':
    restored = dbase.read()
    localGeneral = restored['general']
    localRestored = restored

    shared = localGeneral['shared']
    if shared:
        print('shared')
        sharedRestored = dbase.read(localGeneral['shared'])
        form = mainUi.show(sharedRestored, localRestored)
    else:
        form = mainUi.show(restored, localRestored)

def form_init(form, restored, localGeneral):
  
    # process.start(form, restored, localGeneral)

    shared = localGeneral['shared']
    if shared:
        try:
            sharedRestored = restored
            dbase.save(sharedRestored, shared)
        except NameError:
            print('Name error', shared)
            pass

    restored['general']['mainPath'] = localGeneral['mainPath']
    dbase.save(restored)