""" Восстанавливает данные.
    
    Keyword arguments:
        restoredData -> []
        [0] -> список документов - {}
        [1] -> название способов закупок - []
        [2] -> {
            "excel":[{...}], -> var, cell, sheet, default, value
            "word": [{...}], -> var, default, value
            "default": [{...}] -> name, var, val
            }
"""

import pickle

def read():
    print( "Восстановление данных...." )
    with open("storage", "rb") as file:
        recoveryData = pickle.load(file)
    
    return recoveryData

def save(recoveryData):
    print( "Сохранение данных...." )
    with open("storage", "wb") as file:
        pickle.dump(recoveryData, file)

new = {
    "documentList": [
        {'checked': False, 'name': '26935327.gif', 'dir': 'C:/Users/Huston/Pictures/26935327.gif', 'method': 'Аукцион', 'law': '44'}, {'checked': False, 'name': 'minus_PNG64.png', 'dir': 'C:/Users/Huston/Pictures/minus_PNG64.png', 'method': 'Аукцион', 'law': '44'}
    ],
    "tenderMethodNames": [
        'Аукцион', 'Закрытый аукцион', 'Запрос котировок', 'Запрос предложений', 'Конкурс'
    ],
    "variables": {
        "excel": [{
            "var": None,
            "cell": "A1",
            "sheet": "active",
            "default": None,
            "value": "",
        }],
        "word": [{
            "var": "%ПЕРЕМЕННАЯ%",
            "default": None,
            "value": "Значение переменной"
        },{
            "var": "%ВТОРАЯ ПЕРЕМЕННАЯ%",
            "default": "%DATE%",
            "value": "Значение переменной"
        }],
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
    }
}

if __name__ == "__main__":
    m = read()
    # m.append(variables)
    # m.remove({})
    print(m)
    save(m)