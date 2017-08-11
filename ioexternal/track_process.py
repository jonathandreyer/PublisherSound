# -*- coding: utf-8 -*-
import logging
import os
from pydub import AudioSegment


class TrackProcess:
    TRACK_FORMAT = 'mp3'

    def __init__(self):
        self.logger = logging.getLogger('app.ioexternal.TrackProcess')
        self.logger.debug('init')

    def convert(self, path, remove_base=False):
        self.logger.debug('load track')
        song = AudioSegment.from_wav(path)
        self.logger.debug('fade (in/out) track')
        track = song.fade_in(700).fade_out(1000)

        self.logger.debug('export song')
        p = os.path.splitext(path)[0] + '.' + self.TRACK_FORMAT
        track.export(p, format=self.TRACK_FORMAT)

        if remove_base:
            os.remove(path)
            self.logger.debug('Base track file is removed')

        return p


if __name__ == '__main__':
    PATH_FILE = 'PATH_TO_MP3/file.mp3'

    tp = TrackProcess()

    print(tp.convert(PATH_FILE))
