from interface.UX import UX_main
from processing import dbase
from processing import license

if __name__ == '__main__':
    license.check()
    # чтение локальной базы
    localRestored = dbase.read()
    localGeneral = localRestored['general']
    if localGeneral['shared']:
        # чтение расшареной базы
        sharedRestored = dbase.read(localGeneral['shared'])
        form = UX_main.show(sharedRestored, localRestored)
    else:
        form = UX_main.show(localRestored, localRestored)
