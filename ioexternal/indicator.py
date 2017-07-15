# -*- coding: utf-8 -*-
import logging
import RPi.GPIO as GPIO


class Indicator:
    LED_OK = 24
    LED_ALERT = 22

    def __init__(self):
        self.logger = logging.getLogger('app.ioexternal.Indicator')
        self.logger.debug('init')
        self.warning = None

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_OK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LED_ALERT, GPIO.OUT, initial=GPIO.LOW)

    def ok(self):
        if self.warning or self.warning is None:
            self.warning = False
            self._set_ok()

    def alert(self):
        if not self.warning or self.warning is None:
            self.warning = True
            self._set_alert()

    def __del__(self):
        self.logger.debug('del.')
        GPIO.cleanup(self.LED_OK)
        GPIO.cleanup(self.LED_ALERT)

    def _set_ok(self):
        self.logger.debug('Set indicator to OK')
        GPIO.output(self.LED_OK, GPIO.HIGH)
        GPIO.output(self.LED_ALERT, GPIO.LOW)

    def _set_alert(self):
        self.logger.debug('Set indicator to alert')
        GPIO.output(self.LED_OK, GPIO.LOW)
        GPIO.output(self.LED_ALERT, GPIO.HIGH)
