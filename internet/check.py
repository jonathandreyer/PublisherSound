# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.error import URLError


URL_TO_CHECK = 'http://www.google.com'


def check_internet_on():
    try:
        urlopen(URL_TO_CHECK, timeout=1)
        return True
    except URLError as err:
        return False


if __name__ == '__main__':
    status = check_internet_on()
    print('Internet reachable : {}'.format(status))
