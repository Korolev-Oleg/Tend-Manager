import pickle
import os

from processing import dataTemplate
# import dataTemplate
lock_path = os.path.expanduser(r'~\Documents\TendManager\.lock')

def lock():
    isexist = os.path.exists(lock_path)
    if not isexist:
        with open(lock_path, 'w') as file:
            file.write('manger-locked')
            return True
    else:
        print(False)
        return False

def unlock():
    isexist = os.path.exists(lock_path)
    if isexist:
        os.remove(lock_path)

def data_init():
    new = dataTemplate.get()
    return new

def set_storage():
    storage_path = os.path.expanduser(r'~\Documents\TendManager')
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    return storage_path

def read(path=False):
    if path:
        with open(path, "rb") as file:
            restored = pickle.load(file)
    else:
        print( "Восстановление данных...." )
        storage_path = set_storage()
        path = r'%s\storage' % storage_path
        if os.path.exists(path):
            with open(path, "rb") as file:
                restored = pickle.load(file)
        else:
            restored = data_init()
    
    return restored

def save(data, path=False):
    r""" Сохраняет бинарный файл.

        Keyword arguments:
            path -> Default - ~\Documents\TendManager\storage
                 or
            path -> str

    """
    print('save')
    if not path:
        storage = set_storage()
        path = r'%s\storage' % storage

    with open(path, "wb") as file:
        pickle.dump(data, file)


if __name__ == "__main__":
    data = read(r'\\192.168.200.1\Shared\ Тендерная_документация\storage.old')
    # data = read()
    data['general']['other']  = {
        'wndPosition': 2,
        'wndOnTop': False
    }
    # print(data['general'])
    # # m.append(variables)
    # # m.remove({})
    # print(m)
    save(data)