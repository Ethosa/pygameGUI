# -*- coding: utf-8 -*-
# author: Ethosa

import re

import pygame
from .View import View


class TextView(View):
    def __init__(self, width=100, height=100,
                 background_color=(0, 0, 0, 0), text=""):
        """View constructor

        Keyword Arguments:
            width {number} -- view width (default: {100})
            height {number} -- view height (default: {100})
            background_color {tuple} -- backgrond color (default: {(0, 0, 0, 255)})
            text {str} -- standart text (default: {""})
        """
        View.__init__(self, width, height, background_color)
        self.text = []
        self.font = pygame.font.SysFont("Roboto", 12)
        self.font_info = ["Roboto", 12, "sys"]
        self.spacing = 0
        self.xalign = "left"
        self.yalign = "top"
        self.copied_back = self.background.copy()
        self.lines = None
        self.text_color = (0, 0, 0, 255)
        for char in text:
            self.add_char(char)

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
        if not color:
            color = self.text_color
        self.text.append([char, color,
                          is_underline, is_bold, is_italic])
        self.is_changed = 1

    def calc_lines(self):
        """Helper Method for Calculating the Length of Each Line"""
        x = y = 0
        self.w = self.h = 0
        self.lines = [[".", 0]]
        for char in self.text:
            bounds = self.font.size(char[0])
            if char[0] != "\n" and bounds[0]+x < self.width:
                x += bounds[0]
                self.lines[-1][1] += bounds[0]
                self.lines[-1][0] += char[0]
                if bounds[0] > self.w:
                    self.w += bounds[0]
            else:
                x = 0
                y += bounds[1] + self.spacing
                self.lines.append([".", 0])
                self.h += bounds[1]
        self.h += bounds[1]

    def calc_x_position(self, info):
        """Helper method for calculating x coordinate

        Returns:
            int -- x coordinate
        """
        length = self.font.size(info[0])[0]
        align = 0
        if self.xalign == "right":
            align = self.width - length
        elif self.xalign == "center":
            align = self.width//2 - length//2
        return align

    def calc_y_position(self):
        """Helper method for calculating x coordinate

        Returns:
            int -- x coordinate
        """
        align = 0
        if self.yalign == "bottom":
            align = self.height - self.h
        elif self.yalign == "center":
            align = self.height//2 - self.h//2
        return align

    def draw(self):
        """draws everything together"""
        super().draw()
        self.background = self.copied_back.copy()
        self.render_text()

    def get_char(self, position):
        """gets a character at a certain position

        Arguments:
            position {int} -- symbol position

        Returns:
            list -- symbol info
        """
        return self.text[position]

    def get_text(self):
        """returns text in normal form"""
        return "".join([i[0] for i in self.text])

    def render_text(self):
        """text rendering"""
        self.copied_back = self.background.copy()

        if not self.lines or self.is_changed:
            self.calc_lines()
            self.is_changed = 0

        y = self.calc_y_position()
        current_line = 0
        x = self.calc_x_position(self.lines[current_line])
        for char in self.text:
            bounds = self.font.size(char[0])
            if char[0] != "\n" and bounds[0]+x < self.width:
                if char[2]:
                    self.font.set_underline(True)
                if char[3]:
                    self.font.set_bold(True)
                if char[4]:
                    self.font.set_italic(True)
                rendered = self.font.render(char[0], True, char[1]).convert_alpha()
                self.background.blit(rendered, (x, y))

                self.font.set_underline(False)
                self.font.set_bold(False)
                self.font.set_italic(False)

                x += bounds[0]
            else:
                y += bounds[1] + self.spacing
                current_line += 1
                x = self.calc_x_position(self.lines[current_line])

    def set_align(self, xalign="left", yalign="top"):
        """setting gravity text

        Keyword Arguments:
            xalign {str} -- may be left, center or right (default: {"left"})
            yalign {str} -- may be top, center or bottom (default: {"top"})
        """
        self.xalign = xalign
        self.yalign = yalign

    def set_background_color(self, color):
        super().set_background_color(color)
        self.copied_back = self.background.copy()

    def set_char(self, position, char, color=None,
                 is_underline=0, is_bold=0, is_italic=0):
        """changes character information at a specific position

        Arguments:
            position {int} -- symbol position
            char {int} -- str

        Keyword Arguments:
            color {tuple} -- symbol color (default: {(0, 0, 0, 255)})
            is_underline {number} (default: {0})
            is_bold {number} (default: {0})
            is_italic {number} (default: {0})
        """
        if not color:
            color = self.text_color
        self.text[position] = [char, color,
                               is_underline, is_bold, is_italic]
        self.is_changed = 1

    def set_chars(self, start_position, end_position, chars,
                  color=None, is_underline=0,
                  is_bold=0, is_italic=0):
        """changes characters in a range

        Arguments:
            start_position {int} -- start range
            end_position {int} -- end range
            chars {str} -- list of chars

        Keyword Arguments:
            color {tuple} -- chars color (default: {(0, 0, 0, 255)})
            is_underline {number} (default: {0})
            is_bold {number} (default: {0})
            is_italic {number} (default: {0})
        """
        for i in range(start_position, end_position):
            self.set_char(i, chars[i], pygame.Color(color),
                          is_underline, is_bold, is_italic)

    def set_font(self, font):
        """sets a new font for rendering text

        Arguments:
            font {str} -- file path or font name
        """
        if isinstance(font, str):
            self.font_info[0] = font
            if re.search(r"[/]?\S+.(ttf|otf)", font):
                self.font = pygame.font.Font(font, self.font_info[1])
                self.font_info[2] = "file"
            else:
                self.font = pygame.font.SysFont(font, self.font_info[1])
                self.font_info[2] = "sys"
            self.is_changed = 0

    def set_text(self, text, color=None,
                 is_underline=0, is_bold=0, is_italic=0):
        """sets new text, removing old

        Arguments:
            text {str}

        Keyword Arguments:
            color {tuple} -- text color (default: {(0, 0, 0, 255)})
            is_underline {number} (default: {0})
            is_bold {number} (default: {0})
            is_italic {number} (default: {0})
        """
        self.text = []
        color = pygame.Color(color) if color else self.text_color
        for char in text:
            self.add_char(char, color, is_underline, is_bold, is_italic)

    def set_text_color(self, color=None):
        """set color at all text

        Keyword Arguments:
            color {tuple} -- text color (default: {(0, 0, 0, 255)})
        """
        color = pygame.Color(color)
        self.text_color = color
        for i, char in enumerate(self.text):
            self.text[i][1] = color

    def set_text_size(self, size):
        """sets font size

        Arguments:
            size {int} -- size in pixels
        """
        if self.font_info[2] == "sys":
            self.font = pygame.font.SysFont(self.font_info[0], size)
            self.font_info[1] = size
        else:
            self.font = pygame.font.Font(self.font_info[0], size)
            self.font_info[1] = size
        self.is_changed = 0

    def set_spacing(self, s):
        """sets white space between lines

        Arguments:
            s {int} -- space in pixels
        """
        self.spacing = s
        self.is_changed = 0
