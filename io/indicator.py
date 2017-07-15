# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO


class Indicator:
    LED_OK = 24
    LED_ALERT = 22

    def __init__(self):
        print('init. Indicator object!')
        self.warning = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_OK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LED_ALERT, GPIO.OUT, initial=GPIO.LOW)

    def ok(self):
        if self.warning:
            print("Internet is OK")
            self.warning = False

            GPIO.output(self.LED_OK, GPIO.HIGH)
            GPIO.output(self.LED_ALERT, GPIO.LOW)

    def alert(self):
        if not self.warning:
            print("Internet have something wrong!")
            self.warning = True

            GPIO.output(self.LED_OK, GPIO.LOW)
            GPIO.output(self.LED_ALERT, GPIO.HIGH)
