import pickle, os
from processing import dataTemplate

def data_init():
    new = dataTemplate.get()
    return new

def set_storage():
    storage_path = os.path.expanduser('~\Documents\TendManager')
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    return storage_path


def read():
    print( "Восстановление данных...." )
    storage_path = set_storage()
    path = '%s\storage' % storage_path
    if os.path.exists(path):
        with open(path, "rb") as file:
            restored = pickle.load(file)
    else:
        restored = data_init()
    
    return restored

def save(data, path=False):
    """ Сохраняет бинарный файл.

        Keyword arguments:
            path -> Default - ~\Documents\TendManager\storage
                 or
            path -> str

    """
    print('save')
    if not path:
        storage = set_storage()
        path = '%s\storage' % storage

    with open(path, "wb") as file:
        pickle.dump(data, file)


if __name__ == "__main__":
    # m = read()
    # print(m['general']['mainPath'])
    # # m.append(variables)
    # # m.remove({})
    # print(m)
    # save(new)
    print(os.listdir())