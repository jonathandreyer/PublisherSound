# -*- coding: utf-8 -*-
import logging
import RPi.GPIO as GPIO


class Indicator:
    LED_OK = 24
    LED_ALERT = 22
    LED_PUBLISH = 10
    LED_RECORD = 23

    def __init__(self):
        self.logger = logging.getLogger('app.ioexternal.Indicator')
        self.logger.debug('init')
        self.warning = None
        self.publish = None
        self.record = None

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_OK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LED_ALERT, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LED_PUBLISH, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LED_RECORD, GPIO.OUT, initial=GPIO.LOW)

    def cloud_ok(self):
        if self.warning or self.warning is None:
            self.warning = False
            self._set_ok()

    def cloud_alert(self):
        if not self.warning or self.warning is None:
            self.warning = True
            self._set_alert()

    def publish_blink(self):
        if not self.publish or self.publish is None:
            self.publish = True
            self._publish_enable()

    def publish_end(self):
        if self.publish or self.publish is None:
            self.publish = False
            self._publish_end()

    def record_start(self):
        if not self.record or self.record is None:
            self.record = True
            self._set_record()

    def record_end(self):
        if self.record or self.record is None:
            self.record = False
            self._clear_record()

    def __del__(self):
        self.logger.debug('del.')
        GPIO.cleanup(self.LED_OK)
        GPIO.cleanup(self.LED_ALERT)
        GPIO.cleanup(self.LED_PUBLISH)
        GPIO.cleanup(self.LED_RECORD)

    def _set_ok(self):
        self.logger.debug('Set indicator to OK')
        GPIO.output(self.LED_OK, GPIO.HIGH)
        GPIO.output(self.LED_ALERT, GPIO.LOW)

    def _set_alert(self):
        self.logger.debug('Set indicator to Alert')
        GPIO.output(self.LED_OK, GPIO.LOW)
        GPIO.output(self.LED_ALERT, GPIO.HIGH)

    # TODO create task to blink
    def _publish_enable(self):
        self.logger.debug('Set indicator to publish Blink')
        GPIO.output(self.LED_PUBLISH, GPIO.HIGH)

    def _publish_end(self):
        self.logger.debug('Set indicator to publish Off')
        GPIO.output(self.LED_PUBLISH, GPIO.LOW)

    def _set_record(self):
        self.logger.debug('Set indicator to record ON')
        GPIO.output(self.LED_RECORD, GPIO.HIGH)

    def _clear_record(self):
        self.logger.debug('Set indicator to record OFF')
        GPIO.output(self.LED_RECORD, GPIO.LOW)
