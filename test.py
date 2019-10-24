# lets = [
#     {"var": "%var1%", "default": None, "value": "text"},
#     {"var": "%var2%", "default": None, "value": "text"},
#     {"var": "%var3%", "default": None, "value": "text"},
#     {"var": "%var4%", "default": None, "value": "text"},
#     {"var": "%var5%", "default": None, "value": "text"},
#     {"var": "%var6%", "default": None, "value": "text"},
#     {"var": "%var73%", "default": None, "value": "text"},
#     {"var": "%var30%", "default": None, "value": "text"},
# ]
# print(len(lets))

# var = "%var73%"
# item = {"var": var, "default": None, "value": "text"}

# find = False
# for let in lets:
#     if let["var"] == var:
#         find = True
#     else:
#         continue
      

# if not find:
#     lets.append(item)

# print(len(lets))

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

for document in new['documentList']:
    print(document.keys())


    try:
        pass
    except expression as identifier:
        pass
