import unittest, re, requests, urllib
import time
import requests, urllib3

from win32api import MessageBox

from processing.num2t4ru import num2text, decimal2text


# from num2t4ru import num2text, decimal2text

def getStrCash(cash):
    """ cash - (str) """
    cash = cash.replace(' ', '')
    try:
        if isinstance(cash, str):
            declensions = [' рубль', ' рубля', ' рублей']
            if ',' in cash:
                prime_cash = int(cash.split(',')[0])
                denim_cash = int(cash.split(',')[1])

                text_prime = num2text(
                    prime_cash,
                    main_units=((u'рубль', u'рубля', u'рублей'), 'm'))

                for declen in declensions:
                    if declen in text_prime:
                        text_prime = text_prime.replace(declen, '')
                        ending = declen

                text_decim = num2text(
                    denim_cash,
                    main_units=((u'копейка', u'копейки', u'копеек'), 'm'))

                formatted_prime = '{0:,}'.format(prime_cash).replace(',', ' ')

                result = '%s (%s)%s %s %s' % (
                    formatted_prime, text_prime, ending, denim_cash, text_decim)
            else:
                text_cash = num2text(
                    int(cash),
                    main_units=((u'рубль', u'рубля', u'рублей'), 'm'))
                for declen in declensions:
                    if declen in text_cash:
                        text_cash = text_cash.replace(declen, '')
                        ending = declen

                formatted_cash = '{0:,}'.format(int(cash)).replace(',', ' ')
                result = '%s (%s)%s' % (formatted_cash, text_cash, ending)
            return result
        else:
            return cash
    except ValueError:
        return cash


def getDate(full=0, day=0, mounth=0, year=0, monstr=0):
    date = time.gmtime()

    if full:
        result = '%s.%s.%s' % (date[2], date[1], date[0])
    if day:
        result = date[2]
    if mounth:
        result = date[1]
    if year:
        result = date[0]
    if monstr:
        months = ['',
                  'января', 'февраля', 'марта',
                  'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября',
                  'октября', 'ноября', 'декабря',
                  ]
        result = months[date[1]]
    return result


def getPublishDate(reg_num):
    """
    Определяет дату регистрации закупки
    :param reg_num: str - реестровый номер
    :return: str - date[0] дата регистрации
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.1.238 '
            'Yowser/2.5 Safari/537.36'
        )
    }

    rgx_container = r'\"cardMainInfo__content\">\s+'
    rgx_date = r'\d\d\.\d\d.\d{4}'

    # set url
    if len(reg_num) > 18:
        url = (
                'http://zakupki.gov.ru/epz/order/notice/ea44/view/'
                'common-info.html?regNumber=%s' % reg_num
        )
    else:
        url = (
                'http://zakupki.gov.ru/223/purchase/public/purchase/'
                'info/common-info.html?regNumber=%s' % reg_num
        )

    html = requests.get(url, headers=headers, allow_redirects=True)
    regular = '%s%s' % (rgx_container, rgx_date)
    date_from_html = re.search(regular, html.text)[0]
    date = re.sub(rgx_container, '', date_from_html)

    if not date:
        MessageBox(0, (
                'Не удалось получить дату размещения закупки '
                '\n№%s в ЕИС \nвнесите изменения вручную!' % reg_num
        )
                   )

    else:
        # return date[0]
        return date


print(getPublishDate("0348200078219000059"))
