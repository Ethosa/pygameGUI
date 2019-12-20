# -*- coding: utf-8 -*-
# author: Ethosa

from .TextView import TextView


class Button(TextView):
    def __init__(self, width=100, height=100,
                 background_color=(0, 0, 0, 0), text=""):
        """View constructor

        Keyword Arguments:
            width {number} -- view width (default: {100})
            height {number} -- view height (default: {100})
            background_color {tuple} -- backgrond color (default: {(0, 0, 0, 255)})
            text {str} -- standart text (default: {""})
        """
        TextView.__init__(self, width, height, background_color, text)
        self.set_align("center", "center")
        self.set_background_color("#e0e0e0")

    def add_char(self, char, color=None,
                 is_underline=0, is_bold=0, is_italic=0):
        """Adds one new formatted character to a string

        Arguments:
            char {str} -- symbol for formatting

        Keyword Arguments:
            color {tuple} -- symbol color (default: {(0, 0, 0, 255)})
            is_underline {number} (default: {0})
            is_bold {number} (default: {0})
            is_italic {number} (default: {0})
        """
        super().add_char(char, color, is_underline, 1, is_italic)
