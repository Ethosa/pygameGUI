# -*- coding: utf-8 -*-
# author: Ethosa

from time import sleep

from .ThreadCreator import ThreadCreator


class Timer:
    def __init__(self):
        self.is_working = 1

    def after(self, seconds):
        def decorator(callable_object):
            def thread():
                sleep(seconds)
                callable_object()
            ThreadCreator(thread).start()
        return decorator

    def after_every(self, start_seconds, every_seconds):
        self.is_working = 1

        def decorator(callable_object):
            def thread():
                sleep(start_seconds)
                while self.is_working:
                    callable_object()
                    sleep(every_seconds)
            ThreadCreator(thread).start()

    def cancel(self):
        self.is_working = 0
