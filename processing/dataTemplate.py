""" .
    return:
        restoredData {} -> 
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


def get(full=1, variables=False):
    template = {
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
                    "name": "Наименование заказчика",           # 0
                    "var": "%ЗАКАЗЧИК%",
                    'value': None
                },{
                    "name": "Реестровый номер закупки",         # 1
                    "var": "%РЕЕСТРОВЫЙ НОМЕР%",
                    'value': None
                },{
                    "name": "Категория",                        # 2
                    "var": "%КАТЕГОРИЯ%",
                    'value': None
                },{
                    "name": "Способ закупки",                   # 3
                    "var": "%СПОСОБ ЗАКУПКИ%",
                    'value': None
                },{
                    "name": "Предмет закупки",                  # 4
                    "var": "%ПРЕДМЕТ%",
                    'value': None
                },{
                    "name": "Обеспечение заявки",               # 5
                    "var": "%ОБЕСПЕЧЕНИЕ ЗАЯВКИ%",
                    'value': None
                },{
                    "name": "Обеспечение заявки прописью",      # 6
                    "var": "%ОБЕСПЕЧЕНИЕ ЗАЯВКИ% СТРОКА",
                    'value': None
                },{
                    "name": "Обеспечение контракта",            # 7
                    "var": "%ОБЕСПЕЧЕНИЕ КОНТРАКТА%",
                    'value': None
                },{
                    "name": "Обеспечение контракта прописью",   # 8
                    "var": "%ОБЕСПЕЧЕНИЕ КОНТРАКТА СТРОКА%",    
                    'value': None
                },{
                    "name": "Начальная цена",                   # 9
                    "var": "%НМЦК%",
                    'value': None
                },{
                    "name": "Начальная цена прописью",          # 10
                    "var": "%НМЦК СТРОКА%",
                    'value': None
                },{
                    "name": "Место поставки",                   # 11
                    "var": "%МЕСТО ПОСТАВКИ%",
                    'value': None
                },{
                    "name": "Срок поставки",                    # 12
                    "var": "%СРОК ПОСТАВКИ%",
                    'value': None
                },{
                    "name": "Количество позиций",               # 13
                    "var": "%ПОЗИЦИИ%",
                    'value': None
                },{
                    "name": "Текущая дата",                     # 14
                    "var": "%ДАТА%",
                    'value': None
                },{
                    "name": "День",                             # 15
                    "var": "%ДЕНЬ%",
                    'value': None
                },{
                    "name": "Месяц",                            # 16
                    "var": "%МЕСЯЦ%",
                    'value': None
                },{
                    "name": "Год",                              # 17
                    "var": "%ГОД%",
                    'value': None
                },{
                    "name": "Месяц прописью",                   # 118
                    "var": "%МЕСЯЦ ТЕКСТ%",
                    'value': None
                },{
                    "name": "Дата размещения в ЕИС",            # 19
                    "var": "%ЕИС ДАТА%",
                    'value': None
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
            'cellBotDn': '',
            'openfolder': True,
            'openpayment': True
        },
        'completedApps': []
    }
    if variables:
        return template['variables']
    if full:
        return template