# from processing import preFuncs
from processing import preFuncs
from processing import dataTemplate

def init(variables, form):
    f = preFuncs
    ready_vars = dataTemplate.get(variables=1)
    ready_vars['excel'] = variables['excel']
    ready_vars['word'] = variables['word']

    df = ready_vars['default']
    df[0]['val'] = form['name']                             # заказчик
    df[1]['val'] = form['regnumber']                        # Реестровый
    df[2]['val'] = form['category']                         # Категория
    df[3]['val'] = form['method']                           # Способ
    df[4]['val'] = form['object']                           # Предмет
    df[5]['val'] = form['appSecurity']                      # Обесп заявки
    df[6]['val'] = f.getStrCash(form['appSecurity'])        # ^прописью
    df[7]['val'] = form['contractSecurity']                 # Обесп контр
    df[8]['val'] = f.getStrCash(form['contractSecurity'])   # ^прописью
    df[9]['val'] = form['currentPrice']                     # НМЦК
    df[10]['val'] = f.getStrCash(form['currentPrice'])      # ^прописью
    df[11]['val'] = form['place']                           # Место
    df[12]['val'] = form['peiod']                           # Срок
    df[13]['val'] = form['positionCount']                   # Кол поз
    df[14]['val'] = f.getDate(full=1)                       # дата
    df[15]['val'] = f.getDate(day=1)                        # День
    df[16]['val'] = f.getDate(mounth=1)                     # Месяц
    df[17]['val'] = f.getDate(year=1)                       # Год
    df[18]['val'] = f.getDate(monstr=1)                     # Месяц пропись
    df[19]['val'] = f.getPublishDate(form['regnumber'])                      # Дата ЕИС

    return ready_vars