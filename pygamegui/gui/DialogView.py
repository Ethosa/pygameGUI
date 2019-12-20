# -*- coding: utf-8 -*-
# author: Ethosa

from .LinearLayout import LinearLayout


class DialogView(LinearLayout):
    def __init__(self, width=100, height=100,
                 background_color=(0, 0, 0, 0), text=""):
        """View constructor

        Keyword Arguments:
            width {number} -- view width (default: {100})
            height {number} -- view height (default: {100})
            background_color {tuple} -- backgrond color (default: {(0, 0, 0, 255)})
            text {str} -- standart text (default: {""})
        """
        LinearLayout.__init__(self, width, height, background_color)
        self.set_background_color("#00000050")
        self.set_orientation("vertical")
        self.is_visible = False

        self.closed = lambda: None
        self.showed = lambda: None

    def add_view(self, view):
        super().add_view(view)
        view.is_visible = self.is_visible

    def close(self):
        self.is_visible = False
        for view in self.views:
            view.is_visible = False
        self.closed()

    def on_close(self, f):
        self.closed = f

    def on_show(self, f):
        self.showed = f

    def set_parent(self, parent):
        super().set_parent(parent)
        self.parent_layout = parent.window
        self.resize("fill_parent", "fill_parent")
        self.x = 0
        self.y = 0
        self.set_gravity_x("center")
        self.set_gravity_y("center")

    def show(self):
        self.is_visible = True
        for view in self.views:
            view.is_visible = True
        self._calc_visible()
        self.showed()
