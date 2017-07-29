# -*- coding: utf-8 -*-
import logging
#import pyaudio
#import wave
import os
from pydub import AudioSegment


class TrackProcess:
    TRACK_FORMAT = 'mp3'

    def __init__(self):
        self.logger = logging.getLogger('app.ioexternal.TrackProcess')
        self.logger.debug('init')

    def convert(self, path):
        self.logger.debug('load track')
        song = AudioSegment.from_wav(path)
        self.logger.debug('fade (in/out) track')
        track = song.fade_in(3000).fade_out(3500)

        self.logger.debug('export song')
        p = os.path.splitext(path)[0] + '.' + self.TRACK_FORMAT
        track.export(p, format=self.TRACK_FORMAT)
        return p


if __name__ == '__main__':
    PATH_FILE = 'PATH_TO_MP3/file.mp3'

    tp = TrackProcess()

    print(tp.convert(PATH_FILE))
