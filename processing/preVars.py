from processing import preFuncs
from processing import dataTemplate

def init(variables, form):
    f = preFuncs
    ready_vars = dataTemplate.get(variables=1)
    ready_vars['excel'] = variables['excel']
    ready_vars['word'] = variables['word']

    df = ready_vars['default']
    df[0]['value'] = form['name']                             # заказчик
    df[1]['value'] = form['regnumber']                        # Реестровый
    df[2]['value'] = form['category']                         # Категория
    df[3]['value'] = form['method']                           # Способ
    df[4]['value'] = form['object']                           # Предмет
    df[5]['value'] = form['appSecurity']                      # Обесп заявки
    df[6]['value'] = f.getStrCash(form['appSecurity'])        # ^прописью
    df[7]['value'] = form['contractSecurity']                 # Обесп контр
    df[8]['value'] = f.getStrCash(form['contractSecurity'])   # ^прописью
    df[9]['value'] = form['currentPrice']                     # НМЦК
    df[10]['value'] = f.getStrCash(form['currentPrice'])      # ^прописью
    df[11]['value'] = form['place']                           # Место
    df[12]['value'] = form['peiod']                           # Срок
    df[13]['value'] = form['positionCount']                   # Кол поз
    df[14]['value'] = f.getDate(full=1)                       # дата
    df[15]['value'] = f.getDate(day=1)                        # День
    df[16]['value'] = f.getDate(mounth=1)                     # Месяц
    df[17]['value'] = f.getDate(year=1)                       # Год
    df[18]['value'] = f.getDate(monstr=1)                     # Месяц пропись
    df[19]['value'] = f.getPublishDate(form['regnumber'])                      # Дата ЕИС

    return ready_vars