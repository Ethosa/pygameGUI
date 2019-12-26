# -*- coding: utf-8 -*-
# author: Ethosa

from .View import View


class LinearLayout(View):
    def __init__(self, width=100, height=100,
                 background_color=(255, 255, 255, 255)):
        """View constructor

        Keyword Arguments:
            width {number} -- view width (default: {100})
            height {number} -- view height (default: {100})
            background_color {tuple} -- backgrond color (default: {(255, 255, 255, 255)})
        """
        View.__init__(self, width=width, height=height, background_color=background_color)
        self.views = []
        self.view_offset = [0, 0]
        self.orientation = "vertical"
        self.gravity = ["left", "top"]

    def add_view(self, view):
        """Adds a new view to the container.

        Arguments:
            view {View} -- new view
        """
        view.x, view.y = self.view_offset[0] + self.x, self.view_offset[1] + self.y
        view.parent_layout = self

        if self.orientation == "vertical":
            self.view_offset[1] += view.height
        else:
            self.view_offset[0] += view.width
        self.parent.add(view)
        self.views.append(view)

        # calc positions of all views
        if self.orientation == "vertical":
            self._calc_vertical_positions()
        else:
            self._calc_horizontal_positions()
        self._calc_visible()

    def _calc_vertical_positions(self):
        if self.gravity[0] == "left":
            for view in self.views:
                view.x = self.x
        elif self.gravity[0] == "center":
            for view in self.views:
                view.x = (self.width//2 - view.width//2) + self.x
        elif self.gravity[0] == "right":
            for view in self.views:
                view.x = (self.width - view.width) + self.x

        if self.gravity[1] == "top":
            y = 0
            for view in self.views:
                view.y = self.y + y
                y += view.height
        elif self.gravity[1] == "center":
            h = sum([view.height for view in self.views])
            y = self.height//2 - h//2
            for view in self.views:
                view.y = self.y + y
                y += view.height
        elif self.gravity[1] == "bottom":
            h = sum([view.height for view in self.views])
            y = self.height - h
            for view in self.views:
                view.y = self.y + y
                y += view.height

    def _calc_horizontal_positions(self):
        if self.gravity[0] == "left":
            x = 0
            for view in self.views:
                view.x = self.x + x
                x += view.width
        elif self.gravity[0] == "center":
            w = sum([view.width for view in self.views])
            x = self.width//2 - w//2
            for view in self.views:
                view.x = x + self.x
                x += view.width
        elif self.gravity[0] == "right":
            w = sum([view.width for view in self.views])
            x = self.width - w
            for view in self.views:
                view.x = x + self.x
                x += view.width

        if self.gravity[1] == "top":
            for view in self.views:
                view.y = self.y
        elif self.gravity[1] == "center":
            for view in self.views:
                view.y = self.y + (self.height//2 - view.height//2)
        elif self.gravity[1] == "bottom":
            for view in self.views:
                view.y = self.y + (self.height - view.height)

    def _calc_visible(self):
        for view in self.views:
            if not (view.x < self.width and view.y < self.height and
                    view.x+view.width > self.x and view.y+view.height > self.y):
                view.is_visible = False
            else:
                view.is_visible = True

    def move(self, dx, dy):
        super().move(dx, dy)

        # calc positions of all views
        if self.orientation == "vertical":
            self._calc_vertical_positions()
        else:
            self._calc_horizontal_positions()
        self._calc_visible()

    def set_gravity_x(self, gravity="left"):
        self.gravity[0] = gravity

    def set_gravity_y(self, gravity="top"):
        self.gravity[1] = gravity

    def set_orientation(self, orientation="vertical"):
        self.orientation = orientation
        if orientation == "vertical":
            self._calc_vertical_positions()
        else:
            self._calc_horizontal_positions()
        self._calc_visible()
