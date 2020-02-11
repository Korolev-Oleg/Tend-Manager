from interface import UX_main
from processing import dbase

if __name__ == '__main__':
    # чтение локальной базы
    localRestored = dbase.read()

    localGeneral = localRestored['general']

    if localGeneral['shared']:
        
        # расшареная база
        sharedRestored = dbase.read(localGeneral['shared'])
        form = UX_main.show(sharedRestored, localRestored)
    else:
        form = UX_main.show(localRestored, localRestored)
