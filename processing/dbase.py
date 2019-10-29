""" Восстанавливает данные.
    
    Keyword arguments:
        restoredData -> {}
        documentList - {} checked, name, dir, method, law
        tenderMethodNames - []
        categories - []
        pathModel -> {} staticPath, dynamicPath, payment, otherPaths - []
        variables {
           "excel": -> var, cell, sheet, default, value
           "word": -> var, default, value
           "default": -> name, var, val
           'general'-> mainPath, paymentPath, sheetName, cellTopLeft, cellBotDn
           }
"""

import pickle, os

def data_init():
    new = {
        "documentList": [
            # {'checked': False, 'name': '26935327.gif', 'dir': 'C:/Users/Huston/Pictures/26935327.gif', 'method': 'Аукцион', 'law': '44'}, {'checked': False, 'name': 'minus_PNG64.png', 'dir': 'C:/Users/Huston/Pictures/minus_PNG64.png', 'method': 'Аукцион', 'law': '44'}
        ],
        "tenderMethodNames": [
            # 'Аукцион', 'Закрытый аукцион', 'Запрос котировок', 'Запрос предложений', 'Конкурс'
        ],
        'categories': [
            
        ],
        "variables": {
            "excel": [],
            "word": [],
            "default": [{
                    "name": "Наименование заказчика",
                    "var": "%ЗАКАЗЧИК%",
                    "val": None
                },{
                    "name": "Реестровый номер закупки",
                    "var": "%РЕЕСТРОВЫЙ НОМЕР%",
                    "val": None
                },{
                    "name": "Категория",
                    "var": "%КАТЕГОРИЯ%",
                    "val": None
                },{
                    "name": "Способ закупки",
                    "var": "%СПОСОБ ЗАКУПКИ%",
                    "val": None
                },{
                    "name": "Предмет закупки",
                    "var": "%ПРЕДМЕТ%",
                    "val": None
                },{
                    "name": "Обеспечение заявки",
                    "var": "%ОБЕСПЕЧЕНИЕ ЗАЯВКИ%",
                    "val": None
                },{
                    "name": "Обеспечение заявки прописью",
                    "var": "%ОБЕСПЕЧЕНИЕ ЗАЯВКИ% СТРОКА",
                    "val": None
                },{
                    "name": "Обеспечение контракта",
                    "var": "%ОБЕСПЕЧЕНИЕ КОНТРАКТА%",
                    "val": None
                },{
                    "name": "Обеспечение контракта прописью",
                    "var": "%ОБЕСПЕЧЕНИЕ КОНТРАКТА СТРОКА%",
                    "val": None
                },{
                    "name": "Начальная цена",
                    "var": "%НМЦК%",
                    "val": None
                },{
                    "name": "Начальная цена прописью",
                    "var": "%НМЦК СТРОКА%",
                    "val": None
                },{
                    "name": "Количество позиций",
                    "var": "%ПОЗИЦИИ%",
                    "val": None
                },{
                    "name": "Текущая дата",
                    "var": "%ДАТА%",
                    "val": None
                },{
                    "name": "День",
                    "var": "%ДЕНЬ%",
                    "val": None
                },{
                    "name": "Месяц",
                    "var": "%МЕСЯЦ%",
                    "val": None
                },{
                    "name": "Год",
                    "var": "%ГОД%",
                    "val": None
                },{
                    "name": "месяц прописью",
                    "var": "%МЕСЯЦ СТРОКА%",
                    "val": None
                }
            ]
        },
        'pathModel': {
            'staticPath': 'Состав заявки',
            'dynamicPath': 'Состав заявки/WORD',
            'payment': '',
            'otherPaths': [
                'Заказчик'
            ]
        },
        'general': {
            'mainPath': '', # Дирректория с заявками
            'paymentPath': '', # Расчет
            'sheetName': '', # имя основного листа в расчете
            'cellTopLeft': '',
            'cellBotDn': ''
        }
    }
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
    
    if not os.path.exists(path):
        pass

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