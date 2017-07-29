# -*- coding: utf-8 -*-
import time
import os
import logging

from internet.clyp import Clyp


class Track:
    def __init__(self, path):
        filename = os.path.basename(path)
        self.name = os.path.splitext(filename)[0].replace('-', ' ').title()
        self.path = path
        self.description = 'Record date : ' + time.strftime('%d/%m/%y %H:%M:%S')


def file_size_mb(path):
    f = float(os.path.getsize(path)) / (1024 * 1024)
    return int(f * 10) / 10


class Publisher:
    def __init__(self, username, password):
        self.logger = logging.getLogger('app.internet.Publisher')
        self._c = Clyp(username, password)

    def post(self, path):
        t = Track(path)

        # TODO call async method (to post tracks) / Add coroutine to list of task
        self.logger.debug(t.name)
        self.logger.debug(t.path)
        self.logger.debug(t.description)

        self.logger.debug('size of file: ' + str(file_size_mb(t.path)) + ' Mb')

        #time.sleep(file_size_mb(t.path))
        res = self._c.post_track(t)

        if res:
            self.logger.debug('Upload to Clyp OK, file is removed')
            os.remove(t.path)


if __name__ == '__main__':

    logger = logging.getLogger('app')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Console output
    consolelog = logging.StreamHandler()
    consolelog.setFormatter(formatter)
    logger.addHandler(consolelog)
    logger.setLevel(logging.DEBUG)

    MP3_PATH_1 = 'PATH/file1.mp3'
    MP3_PATH_2 = 'PATH/file2.mp3'
    MP3_PATH_3 = 'PATH/file3.mp3'

    pub = Publisher('USERNAME_CLYP', 'PASSWORD_CLYP')

    logger.info('Post N°1')
    pub.post(MP3_PATH_1)

    logger.info('Post N°2')
    pub.post(MP3_PATH_2)

    logger.info('Post N°3')
    pub.post(MP3_PATH_3)
