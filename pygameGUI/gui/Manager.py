# -*- coding: utf-8 -*-
# author: Ethosa


class Manager:
    """This class makes working with views a little easier.
    """
    def __init__(self, window):
        self.screen = window.screen
        self.views = []

    def draw(self):
        for view in self.views:
            view.draw()

    def event(self):
        for view in self.views:
            view.handle_event()

    def add(self, *views):
        """Adds one or more views to the manager.

        Arguments:
            *views {View}
        """
        for view in views:
            if view.parent is None:
                view.parent = self
            self.views.append(view)
