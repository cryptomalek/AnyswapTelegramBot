import os


def log(msg: str):
    with open(os.getcwd() + r'\log.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + msg)
    return
