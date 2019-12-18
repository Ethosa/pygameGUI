# -*- coding: utf-8 -*-
# author: Ethosa

from threading import Thread


class ThreadCreator(Thread):
    """A small helper class for creating threads quickly

    Extends:
        Thread
    """
    def __init__(self, f, *args, **kwargs):
        Thread.__init__(self)
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.f(*self.args, **self.kwargs)
