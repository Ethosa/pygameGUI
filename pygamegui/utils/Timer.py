# -*- coding: utf-8 -*-
# author: Ethosa

from time import sleep

from .ThreadCreator import ThreadCreator


class Timer:
    def __init__(self):
        self.is_working = True
        self.is_seconds = True

    def after(self, seconds):
        """waits for the specified time and calls the function

        Arguments:
            seconds {number} -- time to wait
        """
        def decorator(callable_object):
            def thread():
                sleep(seconds / 1000 if not self.is_seconds else seconds)
                if self.is_working:
                    callable_object()
            ThreadCreator(thread).start()
        return decorator

    def after_every(self, start_seconds, every_seconds):
        """waits for the specified time and constantly calls the function

        Arguments:
            start_seconds {number} -- start time to wait
            every_seconds {number} -- time to wait
        """
        self.is_working = True

        def decorator(callable_object):
            def thread():
                sleep(start_seconds)
                while self.is_working:
                    callable_object()
                    sleep(every_seconds / 1000 if not self.is_seconds else every_seconds)
            ThreadCreator(thread).start()
        return decorator

    def cancel(self):
        self.is_working = False
