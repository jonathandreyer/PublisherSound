# -*- coding: utf-8 -*-
import logging
import RPi.GPIO as GPIO


class Recorder:
    GPIO_BTN = 27

    def __init__(self, func):
        self.logger = logging.getLogger('app.ioexternal.Recorder')
        self.logger.debug('init')
        self._func = func

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.GPIO_BTN, GPIO.IN)
        GPIO.add_event_detect(self.GPIO_BTN, GPIO.FALLING, callback=self._func, bouncetime=25)

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

    def event(channel):
        logger.info('hello from event %s' % channel)

    rec = Recorder(event)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print('interrupted!')
