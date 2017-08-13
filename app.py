# -*- coding: utf-8 -*-
import sys
import argparse
import configparser
import logging

from tools.periodic import TaskThread
from tools.static_var import static_vars
from internet.check import check_internet_on
from ioexternal.indicator import Indicator
from ioexternal.recorder import Recorder
from ioexternal.audio import Audio
from internet.publisher import Publisher
from ioexternal.track_process import TrackProcess


# --- Check connectivity to internet ---
@static_vars(state_cloud=False)
def check_connectivity():
    check_connectivity.state_cloud = check_internet_on()
    logger.debug('Internet is reachable : ' + str(check_connectivity.state_cloud))

    if check_connectivity.state_cloud:
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

    if check_connectivity.state_cloud:
        if not event_btn.state_rec:
            ind.record_start()

            audio.start()
        else:
            audio.stop()

            ind.record_end()
            ind.publish_blink()

            p = audio.get_path()
            tp = TrackProcess().convert(path=p, remove_base=True)

            pub.post(tp)

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
    parser.add_argument('-c', type=str, help='config file', default='config.ini')
    parser.add_argument('-t', '--time', type=int, help='time between polling')
    parser.add_argument('-d', '--debug', help='Enable debug log console', action='store_true')
    args = parser.parse_args()

    # Read config from file
    config = configparser.ConfigParser()
    config.read(args.c)

    times = int(config['default']['TimePolling'])
    debug = True if str(config['default']['Debug']).lower() == 'yes' else False
    username = config['clyp.it']['User']
    password = config['clyp.it']['Password']

    # Read config from command line (override config file)
    if args.time:
        times = int(args.time)
    if args.debug:
        debug = args.debug

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info('###############################')
    logger.info('#  Service to publish track   #')
    logger.info('###############################')
    logger.info('')
    logger.info('Parameters:')
    logger.info(' # DELAY: ' + str(times))
    if debug:
        logger.info(' # LOG:   enable')
    logger.info('')

    try:
        ind = Indicator()
        audio = Audio()
        pub = Publisher(username=username, password=password)
        rec = Recorder(event_btn)

        logger.info('Ready to record')

        periodic_polling = PollingInternet()
        periodic_polling.set_interval(times)
        periodic_polling.run()
    except KeyboardInterrupt:
        logger.warning('Quit app by KeyboardInterrupt')
        sys.exit()
