# -*- coding: utf-8 -*-
import sys
import argparse
import logging

from tools.periodic import TaskThread
from internet.check import check_internet_on
from ioexternal.indicator import Indicator
from ioexternal.recorder import Recorder
from ioexternal.audio import Audio


# --- Check connectivity to internet
def check_connectivity():
    res = check_internet_on()
    logger.debug('Internet is reachable : ' + str(res))

    if res:
        ind.ok()
    else:
        ind.alert()


class PollingInternet(TaskThread):
    def task(self, **kwargs):
        logger.debug('Task polling on internt : wake up!')
        check_connectivity()


# --- Recorder track
def event_btn():
    global state
    state = False

    logger.info('Event on channel')

    if not state:
        audio.start()
    else:
        audio.stop()

    state = not state


if __name__ == "__main__":
    logger = logging.getLogger('app')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console output
    consolelog = logging.StreamHandler()
    consolelog.setFormatter(formatter)
    logger.addHandler(consolelog)

    parser = argparse.ArgumentParser(description='Argument not valid!')
    parser.add_argument('-t', '--time', type=int, help='time between polling', default=15)
    parser.add_argument('-d', '--debug', help='Enable debug log console', action='store_true')
    args = parser.parse_args()

    debug = bool(args.debug)
    time = int(args.time)
    if debug:
        logger.setLevel(logging.DEBUG)

    logger.info('')
    logger.info('-------------------------------')
    logger.info('-  Start polling service      -')
    logger.info('-------------------------------')
    logger.info('')
    logger.info('Parameters:')
    logger.info(' - DELAY: ' + str(time))
    if args.debug:
        logger.info(' - LOG:   enable')
    logger.info('')

    ind = Indicator()
    audio = Audio()
    rec = Recorder(event_btn)

    periodic_polling = PollingInternet()
    periodic_polling.set_interval(time)
    periodic_polling.run()

    sys.exit()
