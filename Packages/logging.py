import time


def log(*values : object):
    print(*values)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(time.ctime(time.time()), *values, file=f)