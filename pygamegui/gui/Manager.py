# -*- coding: utf-8 -*-
# author: Ethosa

from pygame import image


class Manager:
    """This class makes working with views a little easier.
    """
    def __init__(self, window, autofill=True, autofill_color=(255, 255, 255, 255)):
        """constructor for Manager

        Arguments:
            window {Window} -- This class should include a self.screen variable

        Keyword Arguments:
            autofill {bool} -- automatically fill with color when redrawing (default: {True})
            autofill_color {tuple} -- fill color (default: {(255, 255, 255, 255)})
        """
        self.screen = window.screen
        self.window = window
        self.screens = {
            "Main": []
        }
        self.views = self.screens["Main"]
        self.autofill = autofill
        self.autofill_color = autofill_color
        self.last_id = 0

    def add(self, *views):
        """Adds one or more views to the manager.

        Arguments:
            *views {View}
        """
        for view in views:
            if view.parent is None:
                view.set_parent(self)
                view.view_id = self.last_id
                self.last_id += 1
            self.views.append(view)

    def add_screen(self, name):
        if name not in self.screens:
            self.screens[name] = []

    def draw(self):
        if self.autofill:
            self.screen.fill(self.autofill_color)
        for view in self.views:
            if (view.x < self.window.width and view.y < self.window.height and
                    view.x+view.width > 0 and view.y+view.height > 0):
                view.draw()
        for view in self.views:
            if (view.x < self.window.width and view.y < self.window.height and
                    view.x+view.width > 0 and view.y+view.height > 0):
                view.draw_tool_tip()

    def event(self):
        for view in self.views:
            if (view.x < self.window.width and view.y < self.window.height and
                    view.x+view.width > 0 and view.y+view.height > 0):
                view.handle_event()

    def get_view_by_id(self, view_id):
        """this method find view by it's id

        Arguments:
            view_id {int} -- view's ID (must be int!)

        Returns:
            View -- found view
        """
        if isinstance(view_id, int) and view_id > 0 and view_id < self.last_id:
            for index, view in enumerate(self.views):
                if view.view_id == view_id:
                    return self.views[index]

    def set_screen(self, name):
        self.views = self.screens[name]

    def take_screenshot(self, filename):
        """takes screenshot and save it in file

        Arguments:
            filename {str} -- file path
        """
        image.save(self.screen, filename)
