# -*- coding: utf-8 -*-
import time
import os

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
        self._c = Clyp(username, password)

    def post(self, path):
        t = Track(path)
        self._process(t)

    def _process(self, track):
        print(track.name)
        print(track.path)
        print(track.description)

        print('size of file: ' + str(file_size_mb(track.path)) + ' Mb')

        self._c.post_track(track)


if __name__ == '__main__':
    MP3_PATH_1 = 'PATH/file1.mp3'
    MP3_PATH_2 = 'PATH/file2.mp3'

    pub = Publisher('USERNAME_CLYP', 'PASSWORD_CLYP')
    print('post N°1')
    pub.post(MP3_PATH_1)
    print('post N°2')
    pub.post(MP3_PATH_2)
