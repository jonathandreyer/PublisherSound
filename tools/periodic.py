# -*- coding: utf-8 -*-
import threading


class TaskThread(threading.Thread):
    """Thread that executes a task every N seconds"""

    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 15.0
        self._kwargs = kwargs

    def set_interval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        while 1:
            if self._finished.isSet():
                return
            self.task(**self._kwargs)

            # sleep for interval or until shutdown
            self._finished.wait(self._interval)

    def task(self, **kwargs):
        """The task done by this thread - override in subclasses"""
        raise Exception  # ( or a more specific exception )


if __name__ == '__main__':
    from datetime import datetime

    class PeriodicPrint(TaskThread):
        def task(self, **kwargs):
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            if kwargs is not None:
                for key, value in kwargs.items():
                    print("%s == %s" % (key, value))

    kwargs = {"arg1": 22, "arg2": 'str'}
    pp = PeriodicPrint(**kwargs)
    pp.set_interval(5)
    pp.run()
