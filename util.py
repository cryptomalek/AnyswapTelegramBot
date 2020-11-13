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


def build_href(path, page, name):
    full_url = '/'.join([site_url, path, page]).replace(r'//', '/')
    return f"<a href='{full_url}'>{name}</a>"
