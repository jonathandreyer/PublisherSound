# -*- coding: utf-8 -*-
import sys
import argparse
import logging

from tools.periodic import TaskThread
from internet.internet import check_internet_on
from ioexternal.indicator import Indicator


ind = Indicator()


def check_connectivity():
    res = check_internet_on()
    logging.debug('Result check : ' + str(res))

    if res:
        ind.ok()
    else:
        ind.alert()


class PollingInternet(TaskThread):
    def task(self, **kwargs):
        logging.debug('Task wake up!')
        check_connectivity()


def print_and_log(msg=''):
    print(msg)
    logging.info(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument not valid!')
    parser.add_argument('-d', '--delay', type=int, help='time between polling', default=15)
    parser.add_argument('-l', '--log', help='Enable debug log', action='store_true')
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s')

    print_and_log()
    print_and_log('-------------------------------')
    print_and_log('-  Start polling service      -')
    print_and_log('-------------------------------')
    print_and_log()
    print_and_log('Parameters:')
    print_and_log(' # DELAY: ' + str(args.delay))
    if args.log:
        print_and_log(' # LOG:   enable')
    print_and_log()

    periodic_polling = PollingInternet()
    periodic_polling.set_interval(args.delay)
    periodic_polling.run()

    sys.exit()
