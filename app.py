# -*- coding: utf-8 -*-
import sys
import argparse
import logging

from tools.periodic import TaskThread
from tools.static_var import static_vars
from internet.check import check_internet_on
from ioexternal.indicator import Indicator
from ioexternal.recorder import Recorder
from ioexternal.audio import Audio
from internet.publisher import Publisher


# --- Check connectivity to internet ---
def check_connectivity():
    res = check_internet_on()
    logger.debug('Internet is reachable : ' + str(res))

    if res:
        ind.cloud_ok()
    else:
        ind.cloud_alert()


class PollingInternet(TaskThread):
    def task(self, **kwargs):
        logger.debug('Task polling on internet : wake up!')
        check_connectivity()


# --- Recorder track ---
@static_vars(state_rec=False)
def event_btn():
    logger.info('Event on channel')

    if not event_btn.state_rec:
        ind.record_start()
        audio.start()
    else:
        audio.stop()
        ind.record_end()
        ind.publish_blink()
        p = audio.get_path()
        pub.post(p)
        ind.publish_end()

    event_btn.state_rec = not event_btn.state_rec


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
    times = int(args.time)
    if debug:
        logger.setLevel(logging.DEBUG)

    logger.info('')
    logger.info('-------------------------------')
    logger.info('-  Start polling service      -')
    logger.info('-------------------------------')
    logger.info('')
    logger.info('Parameters:')
    logger.info(' - DELAY: ' + str(times))
    if args.debug:
        logger.info(' - LOG:   enable')
    logger.info('')

    ind = Indicator()
    audio = Audio()
    rec = Recorder(event_btn)
    pub = Publisher(username='USERNAME_CLYP', password='PASSWORD_CLYP')

    periodic_polling = PollingInternet()
    periodic_polling.set_interval(times)
    periodic_polling.run()

    sys.exit()
