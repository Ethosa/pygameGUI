# -*- coding: utf-8 -*-
# author: Ethosa

import re

import pygame
from .View import View


class TextView(View):
    def __init__(self, parent=None, width=100, height=100,
                 background_color=(0, 0, 0, 0), text=""):
        """View constructor

        Keyword Arguments:
            parent {Game} -- (default: {None})
            width {number} -- view width (default: {100})
            height {number} -- view height (default: {100})
            background_color {tuple} -- backgrond color (default: {(0, 0, 0, 255)})
            text {str} -- standart text (default: {""})
        """
        View.__init__(self, parent, width, height, background_color)
        self.text = []
        self.font = pygame.font.SysFont("Roboto", 12)
        self.font_info = ["Roboto", 12, "sys"]
        self.spacing = 0
        for char in text:
            self.add_char(char)
        self.copied_back = self.background.copy()

    def add_char(self, char, color=(0, 0, 0, 255),
                 is_underline=0, is_bold=0, is_italic=0):
        self.text.append([char, pygame.Color(color),
                          is_underline, is_bold, is_italic])

    def draw(self):
        super().draw()
        self.background = self.copied_back.copy()
        self.render_text()

    def get_char(self, position):
        return self.text[position]

    def get_text(self):
        return "".join([i[0] for i in self.text])

    def render_text(self):
        self.copied_back = self.background.copy()
        x = y = 0

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
                x = 0
                y += bounds[1] + self.spacing

    def set_char(self, position, char, color=(0, 0, 0, 255),
                 is_underline=0, is_bold=0, is_italic=0):
        self.text[position] = [char, pygame.Color(color),
                               is_underline, is_bold, is_italic]

    def set_chars(self, start_position, end_position, chars,
                  color=(0, 0, 0, 255), is_underline=0,
                  is_bold=0, is_italic=0):
        for i in range(start_position, end_position):
            self.set_char(i, chars[i], color,
                          is_underline, is_bold, is_italic)

    def set_font(self, font):
        if isinstance(font, str):
            self.font_info[0] = font
            if re.search(r"[/]?\S+.ttf", font):
                self.font = pygame.font.Font(font, self.font_info[1])
                self.font_info[2] = "file"
            else:
                self.font = pygame.font.SysFont(font, self.font_info[1])
                self.font_info[2] = "sys"

    def set_text(self, text, color=(0, 0, 0, 255),
                 is_underline=0, is_bold=0, is_italic=0):
        self.text = []
        for char in text:
            self.add_char(char, color, is_underline, is_bold, is_italic)

    def set_text_size(self, size):
        if self.font_info[2] == "sys":
            self.font = pygame.font.SysFont(self.font_info[0], size)
            self.font_info[1] = size
        else:
            self.font = pygame.font.Font(self.font_info[0], size)
            self.font_info[1] = size

    def set_spacing(self, s):
        self.spacing = s
