# -*- coding: utf-8 -*-
# author: Ethosa

from math import sqrt

import pygame


class LinearGradient:
    def __init__(self, image_size=(100, 100), position1=(0, 0),
                 position2=(99, 99), color1=(255, 255, 255, 255),
                 color2=(0, 0, 0, 255), position3=None):
        self.surface = pygame.Surface(image_size).convert_alpha()
        self.size = image_size
        if position3 is None:
            x1, y1 = position1
            x2, y2 = position2
            position1 = y2 - y1
            position2 = x1 - x2
            position3 = x2*y1 - y2*x1
        self.position1 = position1
        self.position2 = position2
        self.position3 = position3
        self.distance_multiplier = 1.0 / sqrt(position1*position1 + position2*position2)

        self.color_in = (color1[0]/255, color1[1]/255, color1[2]/255, color1[3]/255)
        self.color_out = (color2[0]/255, color2[1]/255, color2[2]/255, color2[3]/255)

    def distance(self, x, y):
        return (self.position1 * x + self.position2 * y + self.position3) * self.distance_multiplier

    def color(self, distance):
        r = self.color_in[0] * distance + self.color_out[0] * (1 - distance)
        g = self.color_in[1] * distance + self.color_out[1] * (1 - distance)
        b = self.color_in[2] * distance + self.color_out[2] * (1 - distance)
        a = self.color_in[3] * distance + self.color_out[3] * (1 - distance)
        return (int(r*255), int(g*255), int(b*255), int(a*255))

    def fill_gradient(self, max_distance=None):
        w, h = self.size
        ul = self.distance(0, 0)
        ur = self.distance(w-1, 0)
        for y in range(h):
            for x in range(w):
                dist = self.distance(x, y)
                ratio = 0.5 + 0.5 * dist / w
                ratio = max(0.0, min(1.0, ratio))
                self.surface.set_at((x, y), self.color(1.0 - ratio if ul > ur else ratio))
        self.surface = pygame.transform.flip(self.surface, True, False)
