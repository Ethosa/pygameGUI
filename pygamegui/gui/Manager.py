# -*- coding: utf-8 -*-
# author: Ethosa

from pygame import image


class Manager:
    """This class makes working with views a little easier.
    """
    def __init__(self, window, autofill=True, autofill_color=(255, 255, 255, 255)):
        self.screen = window.screen
        self.views = []
        self.autofill = autofill
        self.autofill_color = autofill_color

    def add(self, *views):
        """Adds one or more views to the manager.

        Arguments:
            *views {View}
        """
        for view in views:
            if view.parent is None:
                view.set_parent(self)
            self.views.append(view)

    def draw(self):
        if self.autofill:
            self.screen.fill(self.autofill_color)
        for view in self.views:
            view.draw()

    def event(self):
        for view in self.views:
            view.handle_event()

    def take_screenshot(self, filename):
        """takes screenshot and save it in file

        Arguments:
            filename {str} -- file path
        """
        image.save(self.screen, filename)
