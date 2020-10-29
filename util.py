import os
from datetime import datetime


def log(msg: str):
    with open(os.getcwd() + r'/log ' + datetime.now().strftime('%y%m%d') + '.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + msg)
    return
