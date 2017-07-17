# -*- coding: utf-8 -*-
import logging
import RPi.GPIO as GPIO


class Recorder:
    GPIO_BTN = 27
    BOUNCETIME_MS = 250

    def __init__(self, func):
        self.logger = logging.getLogger('app.ioexternal.Recorder')
        self.logger.debug('init')

        self._fcs = list()

        if not isinstance(func, list):
            if callable(func):
                self._fcs.append(func)
            else:
                raise Exception('Not a callable function!')
        else:
            for f in func:
                if callable(f):
                    self._fcs.append(f)
                else:
                    raise Exception('Not a callable function!')

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.GPIO_BTN, GPIO.IN)
        GPIO.add_event_detect(self.GPIO_BTN, GPIO.FALLING, callback=self._event, bouncetime=self.BOUNCETIME_MS)

    def _event(self, channel):
        self.logger.debug('event on channel %s' % channel)
        for fc in self._fcs:
            fc()

    def __del__(self):
        self.logger.debug('del.')
        GPIO.remove_event_detect(self.GPIO_BTN)
        GPIO.cleanup(self.GPIO_BTN)


if __name__ == "__main__":
    import time

    logger = logging.getLogger('app')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console output
    consolelog = logging.StreamHandler()
    consolelog.setFormatter(formatter)
    logger.addHandler(consolelog)
    logger.setLevel(logging.DEBUG)

    def event():
        logger.info('hello from event')

    rec = Recorder(event)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print('interrupted!')
