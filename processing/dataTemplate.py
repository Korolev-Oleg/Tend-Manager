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
                    "var": "_ЗАКАЗЧИК_",
                    'value': None
                },{
                    "name": "Реестровый номер закупки",         # 1
                    "var": "_РЕЕСТРОВЫЙ-НОМЕР_",
                    'value': None
                },{
                    "name": "Категория",                        # 2
                    "var": "_КАТЕГОРИЯ_",
                    'value': None
                },{
                    "name": "Способ закупки",                   # 3
                    "var": "_СПОСОБ-ЗАКУПКИ_",
                    'value': None
                },{
                    "name": "Предмет закупки",                  # 4
                    "var": "_ПРЕДМЕТ_",
                    'value': None
                },{
                    "name": "Обеспечение заявки",               # 5
                    "var": "_ОБЕСПЕЧЕНИЕ-ЗАЯВКИ_",
                    'value': None
                },{
                    "name": "Обеспечение заявки прописью",      # 6
                    "var": "_ОБЕСПЕЧЕНИЕ-ЗАЯВКИ-СТРОКА_",
                    'value': None
                },{
                    "name": "Обеспечение контракта",            # 7
                    "var": "_ОБЕСПЕЧЕНИЕ-КОНТРАКТА_",
                    'value': None
                },{
                    "name": "Обеспечение контракта прописью",   # 8
                    "var": "_ОБЕСПЕЧЕНИЕ-КОНТРАКТА-СТРОКА_",    
                    'value': None
                },{
                    "name": "Начальная цена",                   # 9
                    "var": "_НМЦК_",
                    'value': None
                },{
                    "name": "Начальная цена прописью",          # 10
                    "var": "_НМЦК-СТРОКА_",
                    'value': None
                },{
                    "name": "Место поставки",                   # 11
                    "var": "_МЕСТО-ПОСТАВКИ_",
                    'value': None
                },{
                    "name": "Срок поставки",                    # 12
                    "var": "_СРОК-ПОСТАВКИ_",
                    'value': None
                },{
                    "name": "Количество позиций",               # 13
                    "var": "_ПОЗИЦИИ_",
                    'value': None
                },{
                    "name": "Текущая дата",                     # 14
                    "var": "_ДАТА_",
                    'value': None
                },{
                    "name": "День",                             # 15
                    "var": "_ДЕНЬ_",
                    'value': None
                },{
                    "name": "Месяц",                            # 16
                    "var": "_МЕСЯЦ_",
                    'value': None
                },{
                    "name": "Год",                              # 17
                    "var": "_ГОД_",
                    'value': None
                },{
                    "name": "Месяц прописью",                   # 18
                    "var": "_МЕСЯЦ-ТЕКСТ_",
                    'value': None
                },{
                    "name": "Дата размещения в ЕИС",            # 19
                    "var": "_ЕИС-ДАТА_",
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
            'openpayment': True,
            'shared': False
        },
        'completedApps': []
    }
    if variables:
        return template['variables']
    if full:
        return template