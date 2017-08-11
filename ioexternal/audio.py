# -*- coding: utf-8 -*-
import logging
import pyaudio
import wave
import os
from ctypes import *
from sys import platform as _platform

from tools.namesgenerator import get_random_name


# From https://gist.github.com/sloria/5693955
class Recorder(object):
    """A recorder class for recording audio to a WAV file.
    Records in mono by default.
    """

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                             self.frames_per_buffer)


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


# From https://gist.github.com/sloria/5693955
class RecordingFile(object):
    def __init__(self, fname, mode, channels,
                 rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

        # Suppres console message of Alsa when run on linux
        if _platform == "linux" or _platform == "linux2":
            asound = cdll.LoadLibrary('libasound.so')
            asound.snd_lib_error_set_handler(c_error_handler)

        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer,
                                     stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue

        return callback

    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile


class Audio:
    def __init__(self, base_path=''):
        self.logger = logging.getLogger('app.ioexternal.Audio')
        self.logger.debug('init')
        self._rec = Recorder(channels=1, rate=44100, frames_per_buffer=512)
        self._record_file = None
        self._path = ''

        if base_path == '':
            self._base_path = os.getcwd()
        else:
            self._base_path = base_path

    #def __del__(self):
    #    self.logger.debug('del.')

    def start(self):
        self.logger.info('start audio')

        if self._record_file is None:
            self._path = os.path.join(self._base_path, get_random_name('-')) + '.wav'
            self._record_file = self._rec.open(self._path)

            self._record_file.start_recording()
        else:
            raise Exception('Track already open')

    def stop(self):
        self.logger.info('stop audio')

        if self._record_file is not None:
            self._record_file.stop_recording()

            self._record_file = None
        else:
            raise Exception('Not recorded track')

    def get_path(self):
        return self._path


if __name__ == '__main__':
    import time

    a = Audio()

    a.start()
    time.sleep(7.5)
    a.stop()

    print(a.get_path())

    time.sleep(1)

    a.start()
    time.sleep(5)
    a.stop()

    print(a.get_path())

