# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.error import URLError


URL_TO_CHECK = 'http://216.58.192.142'


def check_internet_on():
    try:
        urlopen(URL_TO_CHECK, timeout=1)
        return True
    except URLError as err:
        return False
