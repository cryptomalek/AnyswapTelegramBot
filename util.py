import math
import os
from datetime import datetime
from config import site_url
import traceback


def get_logfile_path(filename):
    try:
        os.mkdir(os.getcwd() + r'/logs/')
    except:
        pass
    return os.getcwd() + r'/logs/' + filename + ' ' + datetime.now().strftime('%y%m%d') + '.txt'


def log(msg: str):
    with open(get_logfile_path('log'), 'a', encoding='utf-8') as f:
        f.write('\n' + str(msg))
    return


def error():
    with open(get_logfile_path('error'), 'a', encoding='utf-8') as f:
        f.write('\n[' + datetime.now().strftime('%H:%M:%S') + '] ' + str(traceback.format_exc()))
    return


def build_href(path, page, name, length=0):
    full_url = '/'.join([site_url, path, page])
    return f"<a href='{full_url}'>{name.ljust(length)}</a>"


def get_precision(amount):
    if amount == 0:
        return 0
    return max(0, 3 - math.floor(math.log(amount, 10)))


def formatcurrency(price):
    if price is None:
        return '-'
    return '$' + "{:,.{}f}".format(price, get_precision(price))


def formatnumber(amount):
    if amount is None:
        return '-'
    return "{:,.{}f}".format(amount, get_precision(amount))


def pad(s: str, dirc='^') -> str:
    return f'{s:{dirc}8}'


def formatPercent(percentage: int, precision=1) -> str:
    if percentage is None:
        return '-'
    return "{:.{}f}%".format(percentage * 100, precision)