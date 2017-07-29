# -*- coding: utf-8 -*-
import logging


class Audio:
    def __init__(self):
        self.logger = logging.getLogger('app.ioexternal.Audio')
        self.logger.debug('init')
        pass

    def __del__(self):
        self.logger.debug('del.')
        pass

    def start(self):
        self.logger.info('start audio')

    def stop(self):
        self.logger.info('stop audio')

    def get_path(self):
        pass
