import sys


def clear_line():
    '''
    Очистить линию в консоли
    :return:
    '''
    sys.stdout.write('\033[2K\033[1G')
