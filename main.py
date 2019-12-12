from interface              import mainUi
from processing             import dbase, process

if __name__ == '__main__':

    # чтение локальной базы
    localRestored = dbase.read()
    localGeneral = localRestored['general']

    if localGeneral['shared']:
        
        # расшареная база
        sharedRestored = dbase.read(localGeneral['shared'])
        form = mainUi.show(sharedRestored, localRestored)
    else:
        form = mainUi.show(localRestored, localRestored)
